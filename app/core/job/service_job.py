from sqlalchemy.orm import Session

from app.schema import (
    job as job_schema,
    page as page_schema,
    campaign as campaign_schema,
    working_time as working_time_schema,
)
from app.crud import (
    job as jobCRUD,
    campaign as campaignCRUD,
    experience as experienceCRUD,
    job_position as job_positionCRUD,
    working_time as working_timeCRUD,
    work_location as work_locationCRUD,
    job_category as job_categoryCRUD,
    skill as skillCRUD,
    job_skill as job_skillCRUD,
    category as categoryCRUD,
    company as companyCRUD,
)
from app.core.auth import service_business_auth
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role, JobStatus, JobType, CampaignStatus, JobApprovalStatus
from app.core.location import service_location
from app.core.working_times import service_working_times
from app.core.work_locations import service_work_locations
from app.core.company import service_company
from app.core.category import service_category
from app.core.auth import service_business_auth
from app.core.skill import service_skill
from app.core.campaign import service_campaign
from app.core.job_approval_requests import service_job_approval_request


def get_list_job_by_business(db: Session, data: dict, current_user):
    try:
        page = job_schema.JobFilterByBusiness(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if current_user.role == Role.BUSINESS:
        page.business_id = current_user.business.id

    return get_list_job(db, page.dict())


def get_list_job_by_user(db: Session, data: dict):
    try:
        page = job_schema.JobFilterByUser(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    page.job_status = JobStatus.PUBLISHED
    page.job_approve_status = JobApprovalStatus.APPROVED
    return get_list_job(db, page.dict())


def get_list_job(db: Session, data: dict):
    jobs = jobCRUD.get_multi(db, **data)
    jobs_response = [get_job_info(db, job) for job in jobs]
    return constant.SUCCESS, 200, jobs_response


def get_job_by_id_for_business(db: Session, job_id: int, current_user):
    job = jobCRUD.get(db, job_id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if job.business_id != current_user.business.id and current_user.role not in [
        Role.SUPER_USER,
        Role.ADMIN,
    ]:
        return constant.ERROR, 403, "Permission denied"
    job_response = get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def get_job_by_id_for_user(db: Session, job_id: int):
    job = jobCRUD.get(db, job_id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if (
        job.job_status != JobStatus.PUBLISHED
        or job.job_approve_status != JobApprovalStatus.APPROVED
    ):
        return constant.ERROR, 404, "Job not found"
    job_response = get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def get_job_by_campaign_id(db: Session, campaign_id: int, current_user):
    campaign = campaignCRUD.get(db, campaign_id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if campaign.business_id != current_user.business.id and current_user.role not in [
        Role.SUPER_USER,
        Role.ADMIN,
    ]:
        return constant.ERROR, 403, "Permission denied"

    job = jobCRUD.get_by_campaign_id(db, campaign_id)
    job_response = get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def create_job(db: Session, data: dict, current_user):
    service_business_auth.verified_level(current_user.business, 2)
    try:
        job_data = job_schema.JobCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    service_skill.check_skills_exist(db, job_data.must_have_skills)
    service_skill.check_skills_exist(db, job_data.should_have_skills)
    service_location.check_match_list_province_district(db, job_data.locations)
    service_category.check_categories_exist(db, job_data.categories)
    service_working_times.check_working_times(db, job_data.working_times)

    if not experienceCRUD.get(db, id=job_data.job_experience_id):
        return constant.ERROR, 404, "Experience not found"
    if not job_positionCRUD.get(db, job_data.job_position_id):
        return constant.ERROR, 404, "Job position not found"
    campaign = service_campaign.check_campaign_exist(
        db,
        business_id=current_user.business.id,
        campaign_id=job_data.campaign_id,
        title=job_data.title,
    )
    job_data.campaign_id = campaign.id
    company = companyCRUD.get_company_by_business_id(db, current_user.business.id)
    if not company:
        return constant.ERROR, 404, "Require join company"
    if jobCRUD.get_by_campaign_id(db, campaign.id):
        return constant.ERROR, 400, "Campaign already has job"

    is_verified_company = company.is_verified
    job_skills = job_data.must_have_skills + job_data.should_have_skills
    job_categories = job_data.categories
    job_data_in = job_schema.JobCreate(
        **job_data.dict(),
        business_id=current_user.business.id,
        status=JobStatus.PENDING,
        employer_verified=is_verified_company,
    )

    job = jobCRUD.create(db=db, obj_in=job_data_in)
    service_working_times.create_working_time_job(
        db, job_id=job.id, data=job_data.working_times
    )
    service_work_locations.create_work_location_job(
        db, job_id=job.id, data=job_data.locations
    )
    service_skill.create_skill_job(db, job.id, job_skills)
    service_category.create_category_job(db, job.id, job_categories)
    service_job_approval_request.create_job_approval_request_job(db, job.id)

    job_response = get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def update_job(db: Session, data: dict, current_user):
    try:
        job_data = job_schema.JobUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    job = jobCRUD.get(db, job_data.job_id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if job.business_id != current_user.business.id:
        return constant.ERROR, 403, "Permission denied"

    must_have_skills_data = job_data.must_have_skills
    should_have_skills_data = job_data.should_have_skills
    locations_data = job_data.locations
    categories_data = job_data.categories
    working_times_data = job_data.working_times

    service_skill.check_skills_exist(db, must_have_skills_data)
    service_skill.check_skills_exist(db, should_have_skills_data)
    service_location.check_match_list_province_district(db, locations_data)
    service_category.check_categories_exist(db, categories_data)
    service_working_times.check_working_times(db, working_times_data)

    if not experienceCRUD.get(db, id=job_data.job_experience_id):
        return constant.ERROR, 404, "Experience not found"
    if not job_positionCRUD.get(db, job_data.job_position_id):
        return constant.ERROR, 404, "Job position not found"

    job_data_in = job_schema.JobUpdate(**job_data.dict())
    job = jobCRUD.update(db=db, db_obj=job, obj_in=job_data_in)

    working_times = job.working_times
    work_locations = job.work_locations
    job_categories = job.job_category_secondary
    job_skills = job.job_skill_secondary

    service_working_times.update_working_time_job(
        db, job.id, working_times_data, working_times
    )
    service_work_locations.update_work_location_job(
        db, job.id, locations_data, work_locations
    )
    service_skill.update_skill_job(
        db, must_have_skills_data + should_have_skills_data, job_skills
    )
    service_category.update_category_job(db, categories_data, job_categories)

    job_response = get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def delete_job(db: Session, job_id: int, current_user):
    job = jobCRUD.get(db, job_id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if job.business_id != current_user.business.id:
        return constant.ERROR, 403, "Permission denied"
    job = jobCRUD.remove(db, id=job_id)
    return constant.SUCCESS, 200, "Job has been deleted"


def get_job_info(db: Session, job):
    working_times_response = service_working_times.get_working_times_by_job_id(
        db, job.id
    )
    work_locations_response = service_work_locations.get_work_locations_by_job_id(
        db, job.id
    )
    company = companyCRUD.get(db, job.business_id)
    company_response = service_company.get_company_info(db, company)
    categories_response = service_category.get_list_category_by_model(
        db, job.job_categories
    )
    must_have_skills_response = service_skill.get_list_skill_by_model(
        db, job.must_have_skills
    )
    should_have_skills_response = service_skill.get_list_skill_by_model(
        db, job.should_have_skills
    )
    job_response = job_schema.JobItemResponse(
        **{
            k: v
            for k, v in job.__dict__.items()
            if k
            not in [
                "working_times",
                "must_have_skills",
                "should_have_skills",
                "locations",
                "job_categories",
            ]
        },
        working_times=working_times_response,
        locations=work_locations_response,
        company=company_response,
        categories=categories_response,
        must_have_skills=must_have_skills_response,
        should_have_skills=should_have_skills_response,
    )
    return job_response

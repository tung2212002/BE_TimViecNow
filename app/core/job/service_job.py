from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from redis import Redis

from app.schema import (
    job as job_schema,
    job_approval_request as job_approval_request_schema,
)
from app.crud import (
    job as jobCRUD,
    campaign as campaignCRUD,
    experience as experienceCRUD,
    job_position as job_positionCRUD,
    company as companyCRUD,
    job_approval_request as job_approval_requestCRUD,
)
from app.core.auth import service_business_auth
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import (
    Role,
    JobStatus,
    SalaryType,
    JobApprovalStatus,
    CampaignStatus,
    RequestApproval,
)
from app.core.location import service_location
from app.core.working_times import service_working_times
from app.core.work_locations import service_work_locations
from app.core.company import service_company
from app.core.category import service_category
from app.core.auth import service_business_auth
from app.core.skill import service_skill
from app.core.campaign import service_campaign, helper_campaign
from app.core.job import helper_job
from app.core.job_approval_requests import helper_job_approval_request
from app.storage.redis import redis_dependency
from app.storage.cache.job_cache_service import job_cache_service


def get_by_business(db: Session, data: dict, current_user):
    try:
        page = job_schema.JobFilterByBusiness(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if current_user.role == Role.BUSINESS:
        if page.business_id and page.business_id != current_user.id:
            return constant.ERROR, 403, "Permission denied"
        page.business_id = current_user.id
        company = companyCRUD.get_company_by_business_id(db, current_user.id)
        if not company:
            return constant.ERROR, 404, "Business not join company"
        if page.company_id and page.company_id != company.id:
            return constant.ERROR, 403, "Permission denied"
        page.company_id = company.id
    response = get_list_job(db, page.model_dump())
    return constant.SUCCESS, 200, response


def get_by_user(db: Session, data: dict):
    try:
        page = job_schema.JobFilterByUser(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    page.job_status = JobStatus.PUBLISHED
    page.job_approve_status = JobApprovalStatus.APPROVED
    jobs = get_list_job(db, page.model_dump())

    params = job_schema.JobCount(**data)
    number_of_all_jobs = jobCRUD.count(db, **params.model_dump())

    response = {
        "count": number_of_all_jobs,
        "jobs": jobs,
    }
    return constant.SUCCESS, 200, response


async def search_by_user(db: Session, redis, data: dict):
    try:
        page = job_schema.JobSearchByUser(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    page.job_status = JobStatus.PUBLISHED
    page.job_approve_status = JobApprovalStatus.APPROVED
    jobs = jobCRUD.search(db, **page.model_dump())
    count = 0
    jobs_of_district_response = []
    if (page.province_id or page.district_id) and page.suggest:
        try:
            cache_key = f"province_district:{page.model_dump()}"
            jobs_of_district_response = await job_cache_service.get_list(cache_key)
        except Exception as e:
            # log
            print(e)
            jobs_of_district_response = None

        if not jobs_of_district_response:
            jobs_of_district = jobCRUD.get_number_job_of_district(
                db, **page.model_dump()
            )
            jobs_of_district_response = []
            for key, value in jobs_of_district:
                count += value
                if value > 0 and key is not None:
                    district = service_location.get_district_info(db, key)
                    jobs_of_district_response.append(
                        {
                            "district": district,
                            "count": value,
                        }
                    )
            try:
                expire_time = 60 * 10
                await job_cache_service.set_list(
                    cache_key,
                    [
                        {
                            "district": jobs_of_district_data["district"].__dict__,
                            "count": jobs_of_district_data["count"],
                        }
                        for jobs_of_district_data in jobs_of_district_response
                    ],
                    expire_time,
                )
            except Exception as e:
                # log
                print(e)
                pass

    else:
        cache_key = f"count_search_by_user:{page.model_dump()}"
        count = None
        try:
            count = await job_cache_service.get(cache_key)
        except Exception as e:
            # log
            print(e)
            pass

        if not count:
            params = job_schema.JobCount(**data)
            count = jobCRUD.count(db, **params.model_dump())
            try:
                expire_time = 60 * 60 * 24
                await job_cache_service.set(cache_key, count, expire_time)
            except Exception as e:
                # log
                print(e)
                pass

    jobs_response = [
        helper_job.get_job_info(db, job)
        for job in jobs
        if helper_job.get_job_info(db, job).company
    ]

    response = {
        "count": count,
        "option": page,
        "jobs": jobs_response,
        "jobs_of_district": jobs_of_district_response,
    }

    return constant.SUCCESS, 200, response


async def search_by_business(db: Session, current_user, data: dict):
    try:
        page = job_schema.JobSearchByUser(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if current_user.role == Role.BUSINESS:
        if page.business_id and page.business_id != current_user.id:
            return constant.ERROR, 403, "Permission denied"
        page.business_id = current_user.id
        company = companyCRUD.get_company_by_business_id(db, current_user.id)
        if not company:
            return constant.ERROR, 404, "Business not join company"
        if page.company_id and page.company_id != company.id:
            return constant.ERROR, 403, "Permission denied"
        page.company_id = company.id

    jobs = jobCRUD.search(db, **page.model_dump())
    params = job_schema.JobCount(**page.model_dump())
    count = jobCRUD.count(db, **params.model_dump())

    jobs_response = []
    for job in jobs:
        job_res = helper_job.get_job_info(db, job)
        jobs_response.append(job_res) if job_res.company else None

    response = {
        "count": count,
        "option": page,
        "jobs": jobs_response,
    }
    return constant.SUCCESS, 200, response


def get_list_job(db: Session, data: dict):
    jobs = jobCRUD.get_multi(db, **data)
    jobs_response = []
    for job in jobs:
        job_res = helper_job.get_job_info(db, job)
        jobs_response.append(job_res) if job_res.company else None

    return jobs_response


def get_by_id_for_business(db: Session, job_id: int, current_user):
    job = jobCRUD.get(db, job_id)
    company = companyCRUD.get_company_by_business_id(db, current_user.id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if (
        (job.business_id != current_user.id or job.campaign.company_id != company.id)
        and current_user.role
        not in [
            Role.SUPER_USER,
            Role.ADMIN,
        ]
        or not company
    ):
        return constant.ERROR, 403, "Permission denied"
    job_response = helper_job.get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def get_by_id_for_user(db: Session, job_id: int):
    job = jobCRUD.get(db, job_id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if (
        job.status != JobStatus.PUBLISHED
        or job.job_approval_request.status != JobApprovalStatus.APPROVED
    ):
        return constant.ERROR, 404, "Job not found"
    job_response = helper_job.get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


def get_by_campaign_id(db: Session, campaign_id: int, current_user):
    campaign = campaignCRUD.get(db, campaign_id)
    company = companyCRUD.get_company_by_business_id(db, current_user.id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if (
        (campaign.business_id != current_user.id or campaign.company_id != company.id)
        and current_user.role
        not in [
            Role.SUPER_USER,
            Role.ADMIN,
        ]
        or not company
    ):
        return constant.ERROR, 403, "Permission denied"

    job = jobCRUD.get_by_campaign_id(db, campaign_id)
    job_response = helper_job.get_job_info(db, job)
    return constant.SUCCESS, 200, job_response


async def count_job_by_category(redis: Redis, db: Session):
    time_scan = db.query(func.now()).first()[0]
    response = None
    try:
        response = await redis.get_list("count_job_by_category")
    except Exception as e:
        # log
        response = None
    if not response:
        data = jobCRUD.count_job_by_category(db)
        response = []

        for id, count in data:
            category = service_category.get_category_info_by_id(db, id)
            response.append(
                {**category.model_dump(), "count": count, "time_scan": str(time_scan)}
            )
        try:
            expire_time = 60 * 60 * 24
            await redis.set_list("count_job_by_category", response, expire_time)
        except Exception as e:
            print(e)
            # log
            pass
    return constant.SUCCESS, 200, response


async def count_job_by_salary(redis: Redis, db: Session):
    response = None
    try:
        response = await redis.get_list("count_job_by_salary")
    except Exception as e:
        # log
        response = None
    if not response:
        salary_ranges = [
            (0, 3, SalaryType.VND),
            (3, 10, SalaryType.VND),
            (10, 20, SalaryType.VND),
            (20, 30, SalaryType.VND),
            (30, 0, SalaryType.VND),
            (0, 0, SalaryType.DEAL),
        ]
        time_scan = db.query(func.now()).first()[0]
        data = jobCRUD.count_job_by_salary(db, salary_ranges)
        data = zip(salary_ranges, data)
        response = []
        for (min, max, salary_type), count in data:
            response.append(
                {
                    "min_salary": min,
                    "max_salary": max,
                    "salary_type": salary_type,
                    "count": count,
                    "time_scan": str(time_scan),
                }
            )
        try:
            expire_time = 60 * 60 * 24
            await redis.set_list("count_job_by_salary", response, expire_time)
        except Exception as e:
            pass
    return constant.SUCCESS, 200, response


def count_job_by_district(db: Session):
    response = jobCRUD.count_job_by_district(db)
    return constant.SUCCESS, 200, response


async def get_cruitment_demand(redis: Redis, db: Session):
    time_scan = db.query(func.now()).first()[0]
    approved_time = time_scan.date() - timedelta(days=1)
    params = job_schema.JobCount(
        job_status=JobStatus.PUBLISHED,
        job_approve_status=JobApprovalStatus.APPROVED,
    )

    cache_key = f"cruitment_demand:{params.deadline}"
    try:
        response = await redis.get_dict(cache_key)
    except Exception as e:
        # log
        response = None
    if not response:
        number_of_job_24h = jobCRUD.count(
            db, **params.model_dump(), approved_time=approved_time
        )
        number_of_job_active = jobCRUD.count(
            db,
            **params.model_dump(),
        )
        number_of_company_active = jobCRUD.count_company_active_job(db)
        response = {
            "number_of_job_24h": number_of_job_24h,
            "number_of_job_active": number_of_job_active,
            "number_of_company_active": number_of_company_active,
            "time_scan": str(time_scan),
        }
        try:
            expire_time = 60 * 60 * 24
            await redis.set_dict(cache_key, response, expire_time)
        except Exception as e:
            # log
            pass

    return constant.SUCCESS, 200, response


def create(db: Session, data: dict, current_user):
    business = current_user.business
    service_business_auth.verified_level(business, 2)
    try:
        job_data = job_schema.JobCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    company = business.company
    if not company:
        return constant.ERROR, 404, "Require join company"

    service_skill.check_skills_exist(db, job_data.must_have_skills)
    service_skill.check_skills_exist(db, job_data.should_have_skills)
    service_location.check_match_list_province_district(db, job_data.locations)
    service_category.check_categories_exist(db, job_data.categories)
    service_working_times.check_working_times(db, job_data.working_times)

    if not experienceCRUD.get(db, id=job_data.job_experience_id):
        return constant.ERROR, 404, "Experience not found"
    if not job_positionCRUD.get(db, job_data.job_position_id):
        return constant.ERROR, 404, "Job position not found"
    campaign = helper_campaign.check_campaign_exist(
        db,
        business_id=current_user.id,
        campaign_id=job_data.campaign_id,
        status=CampaignStatus.OPEN,
        title=job_data.title,
    )
    if jobCRUD.get_by_campaign_id(db, campaign.id):
        return constant.ERROR, 400, "Campaign already has job"
    job_data.campaign_id = campaign.id

    is_verified_company = company.is_verified
    job_skills = job_data.must_have_skills + job_data.should_have_skills
    job_categories = job_data.categories
    job_data_in = job_schema.JobCreate(
        **job_data.model_dump(),
        business_id=current_user.id,
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

    job_response = helper_job.get_job_info(db, job)
    return constant.SUCCESS, 201, job_response


def update(db: Session, data: dict, current_user):
    try:
        job_data = job_schema.JobUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    job = jobCRUD.get(db, job_data.job_id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    company = current_user.business.company
    if (
        job.business_id != current_user.id
        or not company
        or job.campaign.business_id != current_user.id
        or job.campaign.company_id != company.id
    ):
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

    job_approval_request_data = {
        "work_locations": job_data.locations,
        **job_data.model_dump(),
    }
    job_approval_request = job_approval_request_schema.JobApprovalRequestCreate(
        **job_approval_request_data
    )
    job_approval_requests_pending_before = (
        job_approval_requestCRUD.get_pending_by_job_id(db, job.id)
    )
    if job_approval_requests_pending_before:
        for job_approval_request_pending_before in job_approval_requests_pending_before:
            job_approval_requestCRUD.remove(
                db, id=job_approval_request_pending_before.id
            )
    job_approval_request = (
        helper_job_approval_request.create_job_update_approval_request(
            db,
            {
                **job_approval_request_data,
                "request": RequestApproval.UPDATE,
            },
        )
    )
    job_approval_request_response = (
        job_approval_request_schema.JobApprovalRequestResponse(
            **job_approval_request.__dict__
        )
    )
    return constant.SUCCESS, 201, job_approval_request_response


def delete(db: Session, job_id: int, current_user):
    job = jobCRUD.get(db, job_id)
    company = companyCRUD.get_company_by_business_id(db, current_user.id)
    if not job:
        return constant.ERROR, 404, "Job not found"
    if (
        not company
        or job.business_id != current_user.id
        or job.campaign.company_id != company.id
    ):
        return constant.ERROR, 403, "Permission denied"
    job = jobCRUD.remove(db, id=job_id)
    return constant.SUCCESS, 200, "Job has been deleted"

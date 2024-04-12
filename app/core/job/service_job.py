from sqlalchemy.orm import Session

from app.model.job import Job
from app.model.campaign import Campaign
from app.schema import (
    job as job_schema,
    page as page_schema,
    campaign as campaign_schema,
)
from app.crud import job as jobCRUD, campaign as campaignCRUD
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role, JobStatus, JobType


def get_list_job_business(db: Session, data: dict, current_user):
    try:
        page = page_schema.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    jobs = []
    business_id = data.get("business_id")
    if not business_id and current_user.role == Role.BUSINESS:
        business_id = current_user.business.id
        jobs = jobCRUD.get_multi(db=db, business_id=business_id, **page.dict())
    elif (
        business_id
        and current_user.business.id != business_id
        and current_user.role not in [Role.SUPER_USER, Role.ADMIN]
    ):
        return constant.ERROR, 403, "Permission denied"
    elif business_id:
        jobs = jobCRUD.get_multi(db, business_id, **page.dict())
    else:
        jobs = jobCRUD.get_multi(db, **page.dict())

    jobs_response = [get_job_info_business(job) for job in jobs]
    return constant.SUCCESS, 200, jobs_response


def get_job_info_business(job: Job):
    business = job.business
    company = job.company
    campaign = job.campaign
    job_experience = job.job_experience
    cv_applications = job.cv_applications
    job_approval_requests = job.job_approval_requests
    must_have_skills = job.must_have_skills
    should_have_skills = job.should_have_skills
    job_categories = job.job_categories
    working_times = job.working_times
    work_locations = job.work_locations
    job_response = job_schema.JobItemResponse(
        **job.dict(),
    )

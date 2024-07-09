from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from redis import Redis

from app.schema import (
    job as job_schema,
)
from app.crud import (
    job as jobCRUD,
    campaign as campaignCRUD,
    experience as experienceCRUD,
    job_position as job_positionCRUD,
    company as companyCRUD,
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
)
from app.core.location import service_location
from app.core.working_times import service_working_times
from app.core.work_locations import service_work_locations
from app.core.company import service_company
from app.core.category import service_category
from app.core.auth import service_business_auth
from app.core.skill import service_skill
from app.core.campaign import service_campaign, helper_campaign
from app.storage.redis import redis_client


def get_list_job(db: Session, data: dict):
    jobs = jobCRUD.get_multi(db, **data)
    jobs_response = []
    for job in jobs:
        job_res = get_job_info(db, job)
        jobs_response.append(job_res) if job_res.company else None

    return jobs_response


def get_jobs_active_by_company(db: Session, company_id: int):
    obj_in = {
        "company_id": company_id,
        "job_status": JobStatus.PUBLISHED,
        "job_approve_status": JobApprovalStatus.APPROVED,
        "deadline": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }
    return jobCRUD.count(db, **obj_in)


def get_job_info(db: Session, job, Schema=job_schema.JobItemResponse):
    working_times_response = service_working_times.get_working_times_by_job_id(
        db, job.id
    )
    work_locations_response = service_work_locations.get_work_locations_by_job_id(
        db, job.id
    )
    company = companyCRUD.get_company_by_business_id(db, job.business_id)
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
    job_response = Schema(
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


def get_job_info_general(db: Session, job):
    job_response = job_schema.JobItemResponseGeneral(
        **job.__dict__,
    )
    return job_response


def search_job_info(db: Session, job, Schema=job_schema.JobItemResponse):
    work_locations_response = service_work_locations.get_work_locations_by_job_id(
        db, job.id
    )
    company = companyCRUD.get_company_by_business_id(db, job.business_id)
    company_response = service_company.get_company_info(db, company)

    job_response = Schema(
        **{
            k: v
            for k, v in job.__dict__.items()
            if k
            not in [
                "locations",
            ]
        },
        locations=work_locations_response,
        company=company_response,
    )
    return job_response

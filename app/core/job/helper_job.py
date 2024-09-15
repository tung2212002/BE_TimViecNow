from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from redis.asyncio import Redis

from app.schema import (
    job as job_schema,
)
from app.crud import (
    job as jobCRUD,
    company as companyCRUD,
)
from app.hepler.enum import (
    JobStatus,
    JobApprovalStatus,
)
from app.core.working_times import service_working_times
from app.core.work_locations import service_work_locations
from app.core.company import service_company
from app.core.category import service_category
from app.core.skill import service_skill
from app.storage.cache.job_cache_service import job_cache_service


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


async def get_job_info(
    db: Session, redis: Redis, job, Schema=job_schema.JobItemResponse
):
    job_id = job.id
    try:
        job_response = await job_cache_service.get_cache_job_info(redis, job_id)
        if job_response:
            return job_response
    except Exception as e:
        print(e)

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

    try:
        await job_cache_service.cache_job_info(redis, job_id, job_response.__dict__)
    except Exception as e:
        print(e)
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


def get_count_job_user_search_key(data: job_schema.JobSearchByUser) -> str:
    return f"{data.province_id}_{data.district_id}_{data.province_id}_{data.category_id}_{data.field_id}_{data.employment_type}_{data.job_experience_id}_{data.job_position_id}_{data.min_salary}_{data.max_salary}_{data.salary_type}_{data.deadline}_{data.keyword}_{data.suggest}_{data.updated_at}_{data.sort_by}_{data.order_by}_{data.skip}_{data.limit}"

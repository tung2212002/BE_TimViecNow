from sqlalchemy.orm import Session
from datetime import timedelta
from redis.asyncio import Redis

from app.schema import (
    job as job_schema,
    job_approval_request as job_approval_request_schema,
    job_statistics as job_statistics_schema,
)
from app import crud
from app.core import constant
from app.hepler.enum import (
    Role,
    JobStatus,
    SalaryType,
    JobApprovalStatus,
    CampaignStatus,
    RequestApproval,
)
from app.core.location import location_service
from app.core.job_approval_requests import job_approval_request_helper
from app.storage.cache.job_cache_service import job_cache_service
from app.hepler.common import CommonHelper
from app.model import ManagerBase
from app.core.job.job_helper import job_helper
from app.core.category.category_helper import category_helper
from app.core.auth.business_auth_helper import business_auth_helper
from app.core.campaign.campaign_helper import campaign_helper


class JobService:
    async def get_by_business(
        self, db: Session, redis: Redis, data: dict, current_user
    ):
        page = job_helper.validate_page_business(data)

        if current_user.role == Role.BUSINESS:
            if page.business_id and page.business_id != current_user.id:
                return constant.ERROR, 403, "Permission denied"
            page.business_id = current_user.id
            company = crud.company.get_by_business_id(db, current_user.id)
            if not company:
                return constant.ERROR, 404, "Business not join company"
            if page.company_id and page.company_id != company.id:
                return constant.ERROR, 403, "Permission denied"
            page.company_id = company.id
        response = await job_helper.get_list_job(db, redis, page.model_dump())
        return constant.SUCCESS, 200, response

    async def get_by_user(self, db: Session, redis: Redis, data: dict):
        page = job_helper.validate_page_user(data)

        page.job_status = JobStatus.PUBLISHED
        page.job_approve_status = JobApprovalStatus.APPROVED
        jobs = await job_helper.get_list_job(db, redis, page.model_dump())

        params = job_schema.JobCount(**data)
        number_of_all_jobs = crud.job.count(db, **params.model_dump())

        response = {
            "count": number_of_all_jobs,
            "jobs": jobs,
        }
        return constant.SUCCESS, 200, response

    async def search_by_user(self, db: Session, redis: Redis, data: dict):
        page = job_helper.validate_page_user_search(data)

        page.job_status = JobStatus.PUBLISHED
        page.job_approve_status = JobApprovalStatus.APPROVED
        try:
            jobs_response = await job_cache_service.get_cache_user_search(
                redis, job_helper.get_count_job_user_search_key(page)
            )
            if jobs_response:
                return constant.SUCCESS, 200, jobs_response
        except Exception as e:
            print(e)

        jobs = crud.job.user_search(db, **page.model_dump())
        count = 0
        jobs_of_district_response = []

        if (page.province_id or page.district_id) and page.suggest:
            try:
                cache_key = page.model_dump().__str__()
                jobs_of_district_response = await job_cache_service.get_list(
                    redis, cache_key
                )
            except Exception as e:
                print(e)

            if not jobs_of_district_response:
                jobs_of_district = crud.job.get_number_job_of_district(
                    db, **page.model_dump()
                )
                jobs_of_district_response = []
                for key, value in jobs_of_district:
                    count += value
                    if value > 0 and key is not None:
                        district = location_service.get_district_info(db, key)
                        jobs_of_district_response.append(
                            {
                                "district": district,
                                "count": value,
                            }
                        )
                try:
                    await job_cache_service.cache_province_district_search_by_user(
                        redis,
                        cache_key,
                        [
                            {
                                "district": jobs_of_district_data["district"].__dict__,
                                "count": jobs_of_district_data["count"],
                            }
                            for jobs_of_district_data in jobs_of_district_response
                        ],
                    )
                except Exception as e:
                    print(e)

        else:
            cache_key = job_helper.get_count_job_user_search_key(page)
            count = None
            try:
                count = await job_cache_service.get_cache_count_search_by_user(
                    redis, cache_key
                )
            except Exception as e:
                print(e)

            if not count:
                params = job_schema.JobCount(**data)
                count = crud.job.user_count(db, **params.model_dump())
                try:
                    await job_cache_service.cache_count_search_by_user(
                        redis, cache_key, count
                    )
                except Exception as e:
                    print(e)

        jobs_response = []
        for job in jobs:
            job_res = await job_helper.get_info(db, redis, job)
            (
                jobs_response.append(job_res)
                if (
                    isinstance(job_res, dict)
                    and job_res.get("company")
                    or job_res.company
                )
                else None
            )

        response = {
            "count": count,
            "option": page,
            "jobs": jobs_response,
            "jobs_of_district": jobs_of_district_response,
        }

        try:
            await job_cache_service.cache_user_search(redis, cache_key, response)
        except Exception as e:
            print(e)

        return constant.SUCCESS, 200, response

    async def search_by_business(
        self, db: Session, redis: Redis, current_user, data: dict
    ):
        page = job_helper.validate_page_business_search(data)

        if current_user.role == Role.BUSINESS:
            if page.business_id and page.business_id != current_user.id:
                return constant.ERROR, 403, "Permission denied"
            page.business_id = current_user.id
            company = crud.company.get_by_business_id(db, current_user.id)
            if not company:
                return constant.ERROR, 404, "Business not join company"
            if page.company_id and page.company_id != company.id:
                return constant.ERROR, 403, "Permission denied"
            page.company_id = company.id

        jobs = crud.job.search(db, **page.model_dump())
        params = job_schema.JobCount(**page.model_dump())
        count = crud.job.count(db, **params.model_dump())

        jobs_response = []
        for job in jobs:
            job_res = await job_helper.get_info(db, redis, job)
            jobs_response.append(job_res) if job_res.company else None

        response = {
            "count": count,
            "option": page,
            "jobs": jobs_response,
        }
        return constant.SUCCESS, 200, response

    async def get_by_id_for_business(
        self, db: Session, redis: Redis, job_id: int, current_user: ManagerBase
    ):
        job = crud.job.get(db, job_id)
        company = crud.company.get_by_business_id(db, current_user.id)
        if not job:
            return constant.ERROR, 404, "Job not found"
        if (
            (
                job.business_id != current_user.id
                or job.campaign.company_id != company.id
            )
            and current_user.role
            not in [
                Role.SUPER_USER,
                Role.ADMIN,
            ]
            or not company
        ):
            return constant.ERROR, 403, "Permission denied"
        job_response = await job_helper.get_info(db, redis, job)
        return constant.SUCCESS, 200, job_response

    async def get_by_id_for_user(self, db: Session, redis: Redis, job_id: int):
        job = crud.job.get(db, job_id)
        if not job:
            return constant.ERROR, 404, "Job not found"
        if (
            job.status != JobStatus.PUBLISHED
            or job.job_approval_request.status != JobApprovalStatus.APPROVED
        ):
            return constant.ERROR, 404, "Job not found"
        job_response = await job_helper.get_info(db, redis, job)
        return constant.SUCCESS, 200, job_response

    async def get_by_campaign_id(
        self, db: Session, redis: Redis, campaign_id: int, current_user: ManagerBase
    ):
        campaign = crud.campaign.get(db, campaign_id)
        company = crud.company.get_by_business_id(db, current_user.id)
        if not campaign:
            return constant.ERROR, 404, "Campaign not found"
        if (
            (
                campaign.business_id != current_user.id
                or campaign.company_id != company.id
            )
            and current_user.role
            not in [
                Role.SUPER_USER,
                Role.ADMIN,
            ]
            or not company
        ):
            return constant.ERROR, 403, "Permission denied"

        job = crud.job.get_by_campaign_id(db, campaign_id)
        job_response = await job_helper.get_info(db, redis, job)
        return constant.SUCCESS, 200, job_response

    async def count_job_by_category(self, db: Session, redis: Redis):
        time_scan = CommonHelper.get_current_time(db)
        response = None
        try:
            response = await job_cache_service.get_cache_count_job_by_category(redis)
        except Exception as e:
            print(e)

        if not response:
            data = crud.job.count_job_by_category(db)
            response = []

            for id, count in data:
                category = category_helper.get_info_by_id(db, id)
                response.append(
                    {
                        **category.model_dump(),
                        "count": count,
                        "time_scan": str(time_scan),
                    }
                )
            try:
                await job_cache_service.cache_count_job_by_category(redis, response)
            except Exception as e:
                print(e)

        return constant.SUCCESS, 200, response

    async def count_job_by_salary(self, db: Session, redis: Redis):
        data = None
        salary_ranges = [
            (0, 3, SalaryType.VND),
            (3, 10, SalaryType.VND),
            (10, 20, SalaryType.VND),
            (20, 30, SalaryType.VND),
            (30, 999, SalaryType.VND),
        ]
        other_salary = [
            SalaryType.DEAL,
            SalaryType.USD,
            "other",
        ]
        try:
            data = await job_cache_service.get_cache_count_job_by_salary(redis)
        except Exception as e:
            print(e)

        time_scan = CommonHelper.get_current_time(db)
        if not data:
            data = crud.job.count_job_by_salary(db, salary_ranges)
            try:
                await job_cache_service.cache_count_job_by_salary(redis, data)
            except Exception as e:
                print(e)

        response = []
        for index, (idx, count) in enumerate(data[:-3]):
            min, max, salary_type = salary_ranges[idx]
            response.append(
                job_statistics_schema.JobCountBySalary(
                    min_salary=min,
                    max_salary=max if max != 999 else 0,
                    salary_type=salary_type,
                    count=count,
                    time_scan=time_scan,
                )
            )

        for index, (idx, count) in enumerate(data[-3:]):
            salary_type = other_salary[index]
            response.append(
                job_statistics_schema.JobCountBySalary(
                    min_salary=0,
                    max_salary=0,
                    salary_type=salary_type,
                    count=count,
                    time_scan=time_scan,
                )
            )

        return constant.SUCCESS, 200, response

    async def count_job_by_district(self, db: Session):
        response = crud.job.count_job_by_district(db)
        return constant.SUCCESS, 200, response

    async def get_cruitment_demand(self, db: Session, redis: Redis):
        time_scan = CommonHelper.get_current_time(db)
        approved_time = time_scan - timedelta(days=1)

        response = None
        params = job_schema.JobCount(
            job_status=JobStatus.PUBLISHED,
            job_approve_status=JobApprovalStatus.APPROVED,
        )

        try:
            response = await job_cache_service.get_cache_job_cruiment_demand(redis)
        except Exception as e:
            print(e)

        if not response:
            number_of_job_24h = await job_cache_service.get_cache_count_job_24h(redis)
            if not number_of_job_24h:
                number_of_job_24h = crud.job.user_count(
                    db, **params.model_dump(), approved_time=approved_time
                )
                try:
                    await job_cache_service.cache_count_job_24h(
                        redis, number_of_job_24h
                    )
                except Exception as e:
                    print(e)

            number_of_job_active = await job_cache_service.get_cache_count_job_active(
                redis
            )
            if not number_of_job_active:
                number_of_job_active = crud.job.user_count(
                    db,
                    **params.model_dump(),
                )
                try:
                    await job_cache_service.cache_count_job_active(
                        redis, number_of_job_active
                    )
                except Exception as e:
                    print(e)
            number_of_company_active = (
                await job_cache_service.get_cache_count_job_active(redis)
            )
            if not number_of_company_active:
                number_of_company_active = crud.job.count_company_active_job(db)
                try:
                    await job_cache_service.cache_count_job_active(
                        redis, number_of_company_active
                    )
                except Exception as e:
                    print(e)
            response = {
                "number_of_job_24h": number_of_job_24h,
                "number_of_job_active": number_of_job_active,
                "number_of_company_active": number_of_company_active,
                "time_scan": str(time_scan),
            }
            try:
                await job_cache_service.cache_job_cruiment_demand(redis, response)
            except Exception as e:
                print(e)

        return constant.SUCCESS, 200, response

    async def create(
        self, db: Session, redis: Redis, data: dict, current_user: ManagerBase
    ):
        business = current_user.business
        business_auth_helper.verified_level(business, 2)
        job_data = job_helper.validate_create(data)

        company = business.company
        if not company:
            return constant.ERROR, 404, "Require join company"

        job_helper.check_fields(
            db,
            must_have_skills=job_data.must_have_skills,
            should_have_skills=job_data.should_have_skills,
            locations=job_data.locations,
            categories=job_data.categories,
            working_times=job_data.working_times,
            job_experience_id=job_data.job_experience_id,
            job_position_id=job_data.job_position_id,
        )

        campaign = campaign_helper.check_exist(
            db,
            business_id=current_user.id,
            campaign_id=job_data.campaign_id,
            status=CampaignStatus.OPEN,
            title=job_data.title,
        )
        if crud.job.get_by_campaign_id(db, campaign.id):
            return constant.ERROR, 400, "Campaign already has job"
        job_data.campaign_id = campaign.id

        is_verified_company = company.is_verified
        job_data_in = job_schema.JobCreate(
            **job_data.model_dump(),
            business_id=current_user.id,
            status=JobStatus.PENDING,
            employer_verified=is_verified_company,
        )

        job = crud.job.create(db=db, obj_in=job_data_in)
        job_helper.create_fields(
            db,
            job_id=job.id,
            must_have_skills=job_data.must_have_skills,
            should_have_skills=job_data.should_have_skills,
            locations=job_data.locations,
            categories=job_data.categories,
            working_times=job_data.working_times,
        )
        job_response = await job_helper.get_info(db, redis, job)
        return constant.SUCCESS, 201, job_response

    async def update(self, db: Session, data: dict, current_user):
        pass
        job_data = job_helper.validate_update(data)

        job = crud.job.get(db, job_data.job_id)
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

        job_helper.check_fields(
            db,
            must_have_skills=must_have_skills_data,
            should_have_skills=should_have_skills_data,
            locations=locations_data,
            categories=categories_data,
            working_times=working_times_data,
            experience_id=job_data.job_experience_id,
            position_id=job_data.job_position_id,
        )

        job_approval_request_data = {
            "work_locations": job_data.locations,
            **job_data.model_dump(),
        }
        job_approval_request = job_approval_request_schema.JobApprovalRequestCreate(
            **job_approval_request_data
        )
        job_approval_requests_pending_before = (
            crud.job_approval_request.get_pending_by_job_id(db, job.id)
        )
        if job_approval_requests_pending_before:
            for (
                job_approval_request_pending_before
            ) in job_approval_requests_pending_before:
                crud.job_approval_request.remove(
                    db, id=job_approval_request_pending_before.id
                )
        job_approval_request = (
            job_approval_request_helper.create_job_update_approval_request(
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

    async def delete(self, db: Session, job_id: int, current_user):
        job = crud.job.get(db, job_id)
        company = crud.company.get_by_business_id(db, current_user.id)
        if not job:
            return constant.ERROR, 404, "Job not found"
        if (
            not company
            or job.business_id != current_user.id
            or job.campaign.company_id != company.id
        ):
            return constant.ERROR, 403, "Permission denied"
        job = crud.job.remove(db, id=job_id)
        return constant.SUCCESS, 200, "Job has been deleted"


job_service = JobService()

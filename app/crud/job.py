from typing import Type
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import distinct

from .base import CRUDBase
from app.model.job import Job
from app.model.job_approval_request import JobApprovalRequest
from app.model.business import Business
from app.model.work_location import WorkLocation
from app.model.province import Province
from app.model.district import District
from app.model.campaign import Campaign
from app.model.field import Field
from app.model.job_category import JobCategory
from app.model.company import Company
from app.model.company_field import CompanyField
from app.schema.job import JobCreate, JobUpdate
from app.hepler.enum import JobStatus, SalaryType


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    def __init__(self, model: Type[Job]):
        super().__init__(model)
        self.job_approval_request = JobApprovalRequest
        self.business = Business
        self.work_location = WorkLocation
        self.province = Province
        self.district = District
        self.job_category = JobCategory
        self.field = Field
        self.company = Company
        self.company_field = CompanyField
        self.campaign = Campaign

    def get_multi(
        self,
        db: Session,
        **kwargs,
    ):
        query = db.query(self.model)
        if kwargs.get("province_id") or kwargs.get("district_id"):
            query = query.join(
                self.work_location, self.model.id == self.work_location.job_id
            )

        query = self.apply_filters(
            query,
            **kwargs,
        )
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 10)
        sort_by = kwargs.get("sort_by", "id")
        order_by = kwargs.get("order_by", "desc")
        return (
            query.order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .distinct()
            .all()
        )

    def get_by_campaign_id(self, db: Session, campaign_id: int):
        return (
            db.query(self.model).filter(self.model.campaign_id == campaign_id).first()
        )

    def count(
        self,
        db: Session,
        **kwargs,
    ):
        query = db.query(self.model)
        if kwargs.get("province_id") or kwargs.get("district_id"):
            query = query.join(
                self.work_location, self.model.id == self.work_location.job_id
            )
        query = self.apply_filters(
            query,
            **kwargs,
        )
        return query.distinct().count()

    def search(
        self,
        db: Session,
        **kwargs,
    ):
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 10)
        sort_by = kwargs.get("sort_by", "id")
        order_by = kwargs.get("order_by", "desc")
        province_id = kwargs.get("province_id")
        district_id = kwargs.get("district_id")

        number_job_of_district = []
        jobs_query = db.query(self.model)
        if province_id or district_id:
            jobs_query = jobs_query.join(
                self.work_location, self.model.id == self.work_location.job_id
            )
        jobs = (
            self.apply_filters(jobs_query, **kwargs)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .distinct()
            .all()
        )

        if province_id:
            number_job_of_district = self.get_number_job_of_district(db, **kwargs)

        return jobs, number_job_of_district

    def get_number_job_of_district(self, db: Session, **filters):

        query = db.query(
            self.work_location.district_id,
            func.count(distinct(self.model.id)),
        )
        query = query.join(self.model, self.work_location.job_id == self.model.id)
        query = self.apply_filters(query, **filters)
        query = query.group_by(
            self.work_location.district_id,
        )
        return query.all()

    def apply_filters(self, query, **filters):
        company_id = filters.get("company_id")
        field_id = filters.get("field_id")
        campaign_id = filters.get("campaign_id")
        business_id = filters.get("business_id")
        job_status = filters.get("job_status")
        job_approve_status = filters.get("job_approve_status")
        province_id = filters.get("province_id")
        district_id = filters.get("district_id")
        category_id = filters.get("category_id")
        employment_type = filters.get("employment_type")
        job_experience_id = filters.get("job_experience_id")
        job_position_id = filters.get("job_position_id")
        min_salary = filters.get("min_salary")
        max_salary = filters.get("max_salary")
        salary_type = filters.get("salary_type")
        deadline = filters.get("deadline")
        keyword = filters.get("keyword")

        if company_id or field_id:
            query = query.join(
                self.campaign, self.model.campaign_id == self.campaign.id
            )
            if company_id:
                query = query.filter(self.campaign.company_id == company_id)
            if field_id:
                query = query.join(
                    self.company, self.campaign.company_id == self.company.id
                )
                query = query.join(
                    self.company_field, self.company.id == self.company_field.company_id
                ).filter(self.company_field.field_id == field_id)
        if campaign_id:
            query = query.filter(self.model.campaign_id == campaign_id)
        if business_id:
            query = query.filter(self.model.business_id == business_id)
        if job_status:
            query = query.filter(self.model.status == job_status)
        if job_approve_status:
            query = query.join(
                self.job_approval_request,
                self.model.id == self.job_approval_request.job_id,
            ).filter(self.job_approval_request.status == job_approve_status)

        if province_id or district_id:

            if province_id:
                query = query.filter(self.work_location.province_id == province_id)
            if district_id:
                query = query.filter(self.work_location.district_id == district_id)
        if category_id:
            query = query.join(
                self.job_category, self.model.id == self.job_category.job_id
            ).filter(self.job_category.category_id == category_id)
        if employment_type:

            query = query.filter(self.model.employment_type == employment_type)
        if job_experience_id:

            query = query.filter(self.model.job_experience_id == job_experience_id)
        if job_position_id:

            query = query.filter(self.model.job_position_id == job_position_id)
        if salary_type:
            query = query.filter(self.model.salary_type == salary_type)
        if min_salary:
            query = query.filter(self.model.min_salary >= min_salary)
        if max_salary:
            query = query.filter(self.model.max_salary <= max_salary)
        if salary_type:
            query = query.filter(self.model.salary_type == salary_type)
        if min_salary or max_salary and not salary_type:
            query = query.filter(self.model.salary_type != SalaryType.DEAL)

        if deadline:
            query = query.filter(self.model.deadline >= deadline)
        if keyword:
            query = query.filter(self.model.title.ilike(f"%{keyword}%"))
        return query


job = CRUDJob(Job)

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app import crud
from app.schema import (
    company as schema_company,
    field as schema_field,
    page as schema_page,
)
from app.core.helper_base import HelperBase
from app.model import Company
from app.hepler.enum import JobStatus, JobApprovalStatus


class CompanyHelper(HelperBase):
    def get_info(self, db: Session, company: Company, detail=False) -> Optional[dict]:
        if not company:
            return None
        fields = company.fields

        company_response = schema_company.CompanyItemResponse(
            **company.__dict__,
        )
        if detail:
            company_response.total_active_jobs = self.get_jobs_active_by_company(
                db, company.id
            )
        return {
            **company_response.__dict__,
            "fields": [
                schema_field.FieldItemResponse(**field.__dict__) for field in fields
            ],
        }

    def get_jobs_active_by_company(self, db: Session, company_id: int):
        obj_in = {
            "company_id": company_id,
            "job_status": JobStatus.PUBLISHED,
            "job_approve_status": JobApprovalStatus.APPROVED,
            "deadline": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        }
        return crud.job.count(db, **obj_in)

    def get_list_info(
        self, db: Session, companies: list[Company], detail=False
    ) -> list:
        return [self.get_info(db, company, detail) for company in companies]

    def get_private_info(self, db: Session, company: Company) -> Optional[dict]:
        if not company:
            return None
        fields = company.fields
        company_response = schema_company.CompanyPrivateResponse(
            **company.__dict__,
        )

        return {
            **company_response.__dict__,
            "fields": [
                schema_field.FieldItemResponse(**field.__dict__) for field in fields
            ],
        }


company_helper = CompanyHelper(
    schema_page.Pagination,
    schema_company.CompanyCreateRequest,
    schema_company.CompanyUpdateRequest,
)

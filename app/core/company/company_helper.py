from sqlalchemy.orm import Session
from typing import Optional, Union, List
from datetime import datetime, timezone

from app import crud
from app.schema.company import (
    CompanyItemResponse,
    CompanyPrivateResponse,
    CompanyItemDetailSearchResponse,
    CompanyItemGeneralResponse,
)
from app.schema.field import FieldItemResponse
from app.model import Company
from app.hepler.enum import JobStatus, JobApprovalStatus
from app.core.field.field_helper import field_helper


class CompanyHelper:
    def get_info(
        self, db: Session, company: Company, detail=False
    ) -> Union[CompanyItemResponse, CompanyItemDetailSearchResponse]:
        if not company:
            return None
        fields = company.fields

        if detail:
            return CompanyItemDetailSearchResponse(
                **{k: v for k, v in company.__dict__.items() if k not in ["fields"]},
                fields=field_helper.get_list_info(fields),
                total_active_jobs=self.get_jobs_active_by_company(db, company.id),
            )
        print("1")
        return CompanyItemResponse(
            **{k: v for k, v in company.__dict__.items() if k not in ["fields"]},
            fields=field_helper.get_list_info(fields),
        )

    def get_info_general(
        self, company: Company
    ) -> Optional[CompanyItemGeneralResponse]:
        print(company.__dict__)
        if not company:
            return None
        return CompanyItemGeneralResponse(
            **company.__dict__,
        )

    def get_jobs_active_by_company(self, db: Session, company_id: int) -> int:
        obj_in = {
            "company_id": company_id,
            "job_status": JobStatus.PUBLISHED,
            "job_approve_status": JobApprovalStatus.APPROVED,
            "deadline": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        }

        return crud.job.user_count(db, **obj_in)

    def get_list_info(
        self, db: Session, companies: list[Company], detail=False
    ) -> List[Union[CompanyItemResponse, CompanyItemDetailSearchResponse]]:
        return [self.get_info(db, company, detail) for company in companies]

    def get_private_info(
        self, db: Session, company: Company
    ) -> Optional[CompanyPrivateResponse]:
        if not company:
            return None

        fields = company.fields
        return {
            **{k: v for k, v in company.__dict__.items() if k not in ["fields"]},
            "fields": field_helper.get_list_info(fields),
        }


company_helper = CompanyHelper()

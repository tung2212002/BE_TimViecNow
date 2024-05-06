from typing import List
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Company
from app.model.company_field import CompanyField
from app.schema.company import CompanyCreateRequest, CompanyUpdateRequest


class CRUDCompany(CRUDBase[Company, CompanyCreateRequest, CompanyUpdateRequest]):
    def get_company_by_business_id(self, db: Session, business_id: int):
        return (
            db.query(self.model).filter(self.model.business_id == business_id).first()
        )

    def get_company_by_tax_code(self, db: Session, tax_code: str):
        return db.query(self.model).filter(self.model.tax_code == tax_code).first()

    def get_company_by_email(self, db: Session, email: str):
        return db.query(self.model).filter(self.model.email == email).first()

    def get_multi(self, db: Session, **kwargs):
        skip = kwargs.get("skip")
        limit = kwargs.get("limit")
        sort_by = kwargs.get("sort_by")
        order_by = kwargs.get("order_by")
        query = db.query(self.model)
        if kwargs.get("fields"):
            query = query.join(CompanyField, CompanyField.company_id == self.model.id)
            for field_id in kwargs.get("fields"):
                query = query.filter(CompanyField.field_id == field_id)
        return (
            query.order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


company = CRUDCompany(Company)

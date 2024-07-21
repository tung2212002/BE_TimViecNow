from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

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
        key_word = kwargs.get("keyword")
        fields = kwargs.get("fields")
        query = db.query(self.model)
        if fields:
            query = query.join(CompanyField, CompanyField.company_id == self.model.id)
            for field_id in kwargs.get("fields"):
                query = query.filter(CompanyField.field_id == field_id)
        if key_word:
            query = query.filter(self.model.name.ilike(f"%{key_word}%"))
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

    def search_multi(self, db: Session, **kwargs):
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 10)
        sort_by = kwargs.get("sort_by", "id")
        order_by = kwargs.get("order_by", "asc")

        query = db.query(self.model)
        query = self.apply_search_multi(query, **kwargs)
        total_query = db.query(func.count(distinct(self.model.id)))
        total_query = self.apply_search_multi(total_query, **kwargs)
        query = query.order_by(
            getattr(self.model, sort_by).desc()
            if order_by == "desc"
            else getattr(self.model, sort_by)
        )
        query = query.offset(skip).limit(limit)
        total = total_query.scalar()
        return total, query.all()

    def apply_search_multi(self, query, **kwargs):
        key_word = kwargs.get("keyword")
        fields = kwargs.get("fields")

        if fields:
            query = query.join(CompanyField, CompanyField.company_id == Company.id)
            query = query.filter(CompanyField.field_id.in_(fields))

        if key_word:
            query = query.filter(Company.name.ilike(f"%{key_word}%"))

        return query


company = CRUDCompany(Company)

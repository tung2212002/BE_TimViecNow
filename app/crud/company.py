from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Company
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


company = CRUDCompany(Company)

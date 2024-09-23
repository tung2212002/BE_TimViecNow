from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import CompanyField
from app.schema.company_field import CompanyFieldCreate, CompanyFieldUpdate


class CRUDCompanyField(CRUDBase[CompanyField, CompanyFieldCreate, CompanyFieldUpdate]):
    def get_by_company_id_and_field_id(
        self, db: Session, company_id: int, field_id: int
    ) -> CompanyField:
        return (
            db.query(self.model)
            .filter(self.model.company_id == company_id)
            .filter(self.model.field_id == field_id)
            .first()
        )

    def remove_by_company_id_and_field_id(
        self, db: Session, company_id: int, field_id: int
    ) -> None:
        db.query(self.model).filter(self.model.company_id == company_id).filter(
            self.model.field_id == field_id
        ).delete()
        db.commit()

    def get_field_ids_by_company_id(self, db: Session, company_id: int):
        return (
            field_id
            for (field_id,) in db.query(self.model.field_id)
            .filter(self.model.company_id == company_id)
            .all()
        )


company_field = CRUDCompanyField(CompanyField)

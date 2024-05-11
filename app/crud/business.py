from typing import List
from sqlalchemy.orm import Session

from app.schema import business as schema_business
from app.core.security import verify_password
from .base import CRUDBase
from app.model.business import Business
from app.hepler.enum import Role
from app.crud.manager_base import manager_base


class CRUDBusiness(
    CRUDBase[
        Business,
        schema_business.BusinessCreateRequest,
        schema_business.BusinessUpdateRequest,
    ]
):

    def get_by_email(self, db: Session, email: str) -> Business:
        user = manager_base.get_by_email(db, email)
        return (
            db.query(Business).filter(Business.id == user.id).first() if user else None
        )

    def create(
        self, db: Session, *, obj_in: schema_business.BusinessCreateRequest
    ) -> Business:
        db_obj = Business(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order_by: str = "desc"
    ) -> List[Business]:
        return super().get_multi(
            db, skip=skip, limit=limit, sort_by=sort_by, order_by=order_by
        )

    def authenticate(self, db: Session, *, email: str, password: str) -> Business:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: Business) -> bool:
        return user.is_active

    def is_admin(self, user: Business) -> bool:
        return user.role == Role.ADMIN

    def is_superuser(self, user: Business) -> bool:
        return user.role == Role.SUPER_USER

    def set_active(self, db: Session, *, db_obj: Business, is_active: bool) -> Business:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_business_by_company_id(self, db: Session, company_id: int):
        return db.query(self.model).filter(self.model.company_id == company_id).first()

    def set_company(
        self, db: Session, *, db_obj: Business, company_id: int
    ) -> Business:
        db_obj.company_id = company_id
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_is_verified_email(
        self, db: Session, *, db_obj: Business, is_verified_email: bool
    ) -> Business:
        db_obj.is_verified_email = is_verified_email
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_is_verified_phone(
        self, db: Session, *, db_obj: Business, is_verified_phone: bool
    ) -> Business:
        db_obj.is_verified_phone = is_verified_phone
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_is_verified_identity(
        self, db: Session, *, db_obj: Business, is_verified_identity: bool
    ) -> Business:
        db_obj.is_verified_identity = is_verified_identity
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_is_verified_company(
        self, db: Session, *, db_obj: Business, is_verified_company: bool
    ) -> Business:
        db_obj.is_verified_company = is_verified_company
        db.commit()
        db.refresh(db_obj)
        return db_obj


business = CRUDBusiness(Business)

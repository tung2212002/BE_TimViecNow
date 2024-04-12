from typing import List
from sqlalchemy.orm import Session

from app.schema import business as schema_business
from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.model.business import Business
from app.model.manager_base import ManagerBase
from app.schema import manager_base as schema_manager_base
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
            db.query(Business).filter(Business.manager_base_id == user.id).first()
            if user
            else None
        )

    def get_by_manager_base_id(self, db: Session, manager_base_id: int) -> Business:
        return (
            db.query(Business)
            .filter(Business.manager_base_id == manager_base_id)
            .first()
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

    def get_businesses_by_company_id(
        self,
        db: Session,
        company_id: int,
        *,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order_by: str = "desc"
    ):
        return (
            db.query(self.model)
            .filter(self.model.company_id == company_id)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_business_by_company_id(self, db: Session, company_id: int):
        return db.query(self.model).filter(self.model.company_id == company_id).first()


business = CRUDBusiness(Business)

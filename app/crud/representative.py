from sqlalchemy.orm import Session

from app.schema import representative as schema_representative
from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.model.representative import Representative
from app.model.manager_base import ManagerBase
from app.schema import manager_base as schema_manager_base
from app.hepler.enum import Role
from app.crud.manager_base import manager_base


class CRUDRepresentative(
    CRUDBase[
        Representative,
        schema_representative.RepresentativeCreateRequest,
        schema_representative.RepresentativeUpdateRequest,
    ]
):

    def get_by_email(self, db: Session, email: str) -> Representative:
        user = manager_base.get_by_email(db, email)
        return (
            db.query(Representative)
            .filter(Representative.manager_base_id == user.id)
            .first()
            if user
            else None
        )

    def create(
        self, db: Session, *, obj_in: schema_representative.RepresentativeCreateRequest
    ) -> Representative:
        db_obj = Representative(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Representative,
        obj_in: schema_representative.RepresentativeUpdateRequest
    ) -> Representative:
        if obj_in.password:
            obj_in.hashed_password = get_password_hash(obj_in.password)
        manager_base.update(db, db_obj=db_obj.manager_base, obj_in=obj_in)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> Representative:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: Representative) -> bool:
        return user.is_active

    def is_admin(self, user: Representative) -> bool:
        return user.role == Role.ADMIN

    def is_superuser(self, user: Representative) -> bool:
        return user.role == Role.SUPER_USER

    def set_active(
        self, db: Session, *, db_obj: Representative, is_active: bool
    ) -> Representative:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj


representative = CRUDRepresentative(Representative)

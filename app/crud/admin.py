from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.model.admin import Admin
from app.model.manager_base import ManagerBase
from app.schema import admin as schema_admin, manager_base as schema_manager_base
from app.hepler.enum import Role
from app.crud.manager_base import manager_base


class CRUDAdmin(
    CRUDBase[Admin, schema_admin.AdminCreateRequest, schema_admin.AdminUpdateRequest]
):

    def get_by_email(self, db: Session, email: str) -> Admin:
        manager = manager_base.get_by_email(db, email)
        return (
            db.query(Admin).filter(Admin.id == manager.id).first() if manager else None
        )

    def create(self, db: Session, *, obj_in: schema_admin.AdminCreateRequest) -> Admin:
        manager_base_obj = manager_base.create(
            db,
            obj_in=schema_manager_base.ManagerBaseCreateRequest(
                **obj_in.dict(exclude_unset=True),
            ),
        )
        db_obj = Admin(
            manager_base_id=manager_base_obj.id,
            phone_number=obj_in.phone_number,
            gender=obj_in.gender,
            role=obj_in.role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def update(
        self, db: Session, *, db_obj: Admin, obj_in: schema_admin.AdminUpdateRequest
    ) -> Admin:
        if obj_in.password:
            obj_in.hashed_password = get_password_hash(obj_in.password)
        manager_base.update(db, db_obj=db_obj.manager_base, obj_in=obj_in)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> Admin:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: Admin) -> bool:
        return user.is_active

    def is_superuser(self, user: Admin) -> bool:
        return user.role == Role.SUPER_USER

    def set_active(self, db: Session, *, db_obj: Admin, is_active: bool) -> Admin:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj


admin = CRUDAdmin(Admin)

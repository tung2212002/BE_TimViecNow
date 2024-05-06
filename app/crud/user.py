from typing import List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.model.user import User
from app.schema import user as schema_user
from app.hepler.enum import Role


class CRUDUser(
    CRUDBase[User, schema_user.UserCreateRequest, schema_user.UserUpdateRequest]
):

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: schema_user.UserCreateRequest) -> User:
        db_obj = User(
            **obj_in.dict(exclude_unset=True, exclude={"password", "confirm_password"}),
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: schema_user.UserUpdateRequest
    ) -> User:
        if hasattr(obj_in, "password") and obj_in.password:
            obj_in.hashed_password = get_password_hash(obj_in.password)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> User:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.role == Role.SUPER_USER

    def set_active(self, db: Session, *, db_obj: User, is_active: bool) -> User:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)

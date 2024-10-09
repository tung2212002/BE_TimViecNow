from typing import List
from sqlalchemy.orm import Session

from app.core.security import PasswordManager
from .base import CRUDBase
from app.model import User, Account
from app.schema import user as schema_user
from app.hepler.enum import Role


class CRUDUser(CRUDBase[User, schema_user.UserCreate, schema_user.UserUpdate]):

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: schema_user.UserCreate) -> User:
        db_obj = User(
            **obj_in.dict(exclude_unset=True, exclude={"password", "confirm_password"}),
            hashed_password=(
                PasswordManager.get_password_hash(obj_in.password)
                if obj_in.password
                else None
            ),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: schema_user.UserUpdate
    ) -> User:
        if isinstance(obj_in, dict) and obj_in.get("password"):
            obj_in["hashed_password"] = PasswordManager.get_password_hash(
                obj_in["new_password"]
            )
        elif hasattr(obj_in, "new_password"):
            obj_in = obj_in.model_dump(exclude_unset=True)
            obj_in.update(
                {
                    "hashed_password": PasswordManager.get_password_hash(
                        obj_in["new_password"]
                    )
                }
            )
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> User:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not PasswordManager.verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        account: Account = user.account
        return account.role == Role.SUPER_USER

    def set_verify(self, db: Session, db_obj: User, is_verify: bool) -> User:
        db_obj.is_verified = is_verify
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_active(self, db: Session, *, db_obj: User, is_active: bool) -> User:
        account: Account = db_obj.account
        account.is_active = is_active
        db.commit()
        db.refresh(account)
        return db_obj

    def increase_count_job_apply(self, db: Session, db_obj: User) -> User:
        db_obj.count_job_apply += 1
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
        order_by: str = "desc",
    ) -> List[User]:

        return (
            db.query(self.model)
            .join(Account, Account.id == self.model.id)
            .order_by(
                getattr(Account, sort_by).desc()
                if order_by == "desc"
                else getattr(Account, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


user = CRUDUser(User)

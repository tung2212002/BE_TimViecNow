from sqlalchemy.orm import Session
from typing import List

from app.core.security import PasswordManager
from .base import CRUDBase
from app.model import Manager, Account
from app.schema.manager import ManagerCreate, ManagerUpdate
from app.hepler.enum import Role, TypeAccount


class CRUDManager(
    CRUDBase[
        Manager,
        ManagerCreate,
        ManagerUpdate,
    ]
):

    def get(self, db: Session, id: int) -> Manager:
        return (
            db.query(self.model)
            .join(Account, Account.id == self.model.id)
            .filter(Account.type_account == TypeAccount.BUSINESS, self.model.id == id)
            .first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[Manager]:
        return (
            db.query(self.model)
            .join(Account, Account.id == self.model.id)
            .filter(Account.type_account == TypeAccount.BUSINESS)
            .order_by(
                getattr(Account, sort_by).desc()
                if order_by == "desc"
                else getattr(Account, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_admin(self, db: Session, id: int) -> Manager:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi_by_admin(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[Manager]:
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

    def get_list_admin(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[Manager]:
        return (
            db.query(self.model)
            .join(Account, Account.id == self.model.id)
            .filter(Account.role == Role.ADMIN)
            .order_by(
                getattr(Account, sort_by).desc()
                if order_by == "desc"
                else getattr(Account, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_list_business(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[Manager]:

        return (
            db.query(self.model)
            .join(Account, Account.id == self.model.id)
            .filter(Account.type_account == TypeAccount.BUSINESS)
            .order_by(
                getattr(Account, sort_by).desc()
                if order_by == "desc"
                else getattr(Account, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_email(self, db: Session, email: str) -> Manager:
        return db.query(Manager).filter(Manager.email == email).first()

    def create(self, db: Session, *, obj_in: ManagerCreate) -> Manager:
        db_obj = Manager(
            **obj_in.model_dump(
                exclude_unset=True, exclude={"password", "confirm_password"}
            ),
            hashed_password=PasswordManager.get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Manager,
        obj_in: ManagerUpdate,
    ) -> Manager:

        if isinstance(obj_in, dict):
            if obj_in.get("password"):
                obj_in["hashed_password"] = PasswordManager.get_password_hash(
                    obj_in["password"]
                )
                obj_in.pop("password")
        elif hasattr(obj_in, "password") and obj_in.password:
            obj_in = obj_in.copy(
                update={
                    "hashed_password": PasswordManager.get_password_hash(
                        obj_in.password
                    )
                }
            )
            obj_in.pop("password")
            obj_in.pop("confirm_password")
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> Manager:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not PasswordManager.verify_password(password, user.hashed_password):
            return None
        return user


manager = CRUDManager(Manager)

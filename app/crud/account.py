from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import exists, select

from .base import CRUDBase
from app.model import Account, CVApplication, Campaign
from app.schema import account as schema_account
from app.hepler.enum import Role


class CRUDAccount(
    CRUDBase[Account, schema_account.AccountCreate, schema_account.AccountUpdate]
):
    def is_active(self, account: Account) -> bool:
        return account.is_active

    def is_superuser(self, account: Account) -> bool:
        return account.role == Role.SUPER_USER

    def is_normal_user(self, account: Account) -> bool:
        return account.role == Role.USER

    def is_social_network(self, account: Account) -> bool:
        return account.role == Role.SOCIAL_NETWORK

    def is_business(self, account: Account) -> bool:
        return account.role == Role.BUSINESS

    def is_admin(self, account: Account) -> bool:
        return account.role == Role.ADMIN

    def set_active(self, db: Session, *, db_obj: Account, is_active: bool) -> Account:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj


account = CRUDAccount(Account)

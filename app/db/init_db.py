from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    admin as schema_admin,
    manager as schema_manager,
    account as schema_account,
)
from app.core.config import settings
from app.hepler.enum import Role, Gender, TypeAccount
from app.model import Account


def init_db(db: Session) -> None:
    user = crud.manager.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        account_in: schema_account.AccountCreate = schema_account.AccountCreate(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            role=Role.SUPER_USER,
            type_account=TypeAccount.BUSINESS,
        )
        account: Account = crud.account.create(db, obj_in=account_in)
        manager_in: schema_manager.ManagerCreate = schema_manager.ManagerCreate(
            id=account.id,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            phone_number=settings.FIRST_SUPERUSER_PHONE_NUMBER,
        )
        crud.manager.create(db, obj_in=manager_in)
        admin_in: schema_admin.AdminCreate = schema_admin.AdminCreate(
            id=account.id, gender=Gender.OTHER
        )
        crud.admin.create(db, obj_in=admin_in)

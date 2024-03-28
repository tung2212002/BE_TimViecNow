from sqlalchemy.orm import Session

from app import crud
from app.schema import admin as schema_admin, manager_base as schema_manager_base
from app.core.config import settings
from app.hepler.enum import Role, Gender


def init_db(db: Session) -> None:
    user = crud.manager_base.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        manager_base_in = schema_manager_base.ManagerBaseCreateRequest(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            confirm_password=settings.FIRST_SUPERUSER_PASSWORD,
            role=Role.SUPER_USER,
        )

        manager_base = crud.manager_base.create(db, obj_in=manager_base_in)

        user_in = schema_admin.AdminCreateRequest(
            gender=Gender.OTHER,
            phone_number=settings.FIRST_SUPERUSER_PHONE_NUMBER,
        )
        user_in = dict(user_in)
        user_in["manager_base_id"] = manager_base.id
        user = crud.admin.create(db, obj_in=user_in)

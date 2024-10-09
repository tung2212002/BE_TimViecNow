from sqlalchemy.orm import Session

from app import crud
from app.schema import admin as schema_admin, manager as schema_manager
from app.core.config import settings
from app.hepler.enum import Role, Gender


def init_db(db: Session) -> None:
    user = crud.manager.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        manager_in = schema_manager.ManagerCreateRequest(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            confirm_password=settings.FIRST_SUPERUSER_PASSWORD,
            role=Role.SUPER_USER,
        )

        manager = crud.manager.create(db, obj_in=manager_in)

        user_in = schema_admin.AdminCreateRequest(
            gender=Gender.OTHER,
            phone_number=settings.FIRST_SUPERUSER_PHONE_NUMBER,
        )
        user_in = dict(user_in)
        user_in["id"] = manager.id
        user = crud.admin.create(db, obj_in=user_in)

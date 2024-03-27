from sqlalchemy.orm import Session

from app import crud
from app.schema import admin as schema_admin
from app.core.config import settings
from app.hepler.enum import Role, Gender


def init_db(db: Session) -> None:
    user = crud.manager_base.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schema_admin.SuperUserCreateRequest(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            confirm_password=settings.FIRST_SUPERUSER_PASSWORD,
            role=Role.SUPER_USER,
            gender=Gender.OTHER,
            phone_number=settings.FIRST_SUPERUSER_PHONE_NUMBER,
        )
        user = crud.admin.create(db, obj_in=user_in)

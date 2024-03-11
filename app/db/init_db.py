from sqlalchemy.orm import Session

from app import crud
from app.schema import user as schema_user
from app.core.config import settings
from app.hepler.enum import Role


def init_db(db: Session) -> None:

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schema_user.UserCreateRequest(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=Role.SUPER_USER,
        )
        user = crud.user.create(db, obj_in=user_in)

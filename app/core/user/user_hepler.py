from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    user as schema_user,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.model import User
from app.core.helper_base import HelperBase


class UserHelper(HelperBase):
    def validate_get_by_email(self, db: Session, data: dict) -> User:
        try:
            user_data = schema_user.UserGetRequest(**data)
        except Exception as e:
            return custom_response_error(
                status=400, response=get_message_validation_error(e)
            )
        return user_data


user_helper = UserHelper(
    schema_page.Pagination,
    schema_user.UserCreateRequest,
    schema_user.UserUpdateRequest,
)

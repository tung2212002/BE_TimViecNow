from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Union
from datetime import datetime, timezone

from app import crud
from app.core import constant
from app.core.auth.jwt.auth_handler import token_manager
from app.core.auth.jwt.auth_bearer import JWTBearer
from app.hepler.enum import Role, TypeAccount, VerifyType
from app.core.security import PasswordManager
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.model import ManagerBase, User, Business, Admin, SuperUser


class UserAuthHelper:
    pass


user_ath_helper = UserAuthHelper()

from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional

from app.hepler.enum import Role
from app.core import constant


class AuthChangePassword(BaseModel):
    old_password: str
    new_password: str

    @validator("old_password")
    def validate_old_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        elif len(v) > 50:
            raise ValueError("Password must be at most 50 characters")
        return v

    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        elif len(v) > 50:
            raise ValueError("Password must be at most 50 characters")
        elif not re.match(constant.REGEX_PASSWORD, v):
            raise ValueError(
                "Password must contain at least one number, one uppercase, and one lowercase letter"
            )
        return v

    model_config = ConfigDict(from_attribute=True)


class AuthLogin(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        if not re.match(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif len(v) > 50:
            raise ValueError("Password must be at most 50 characters")
        elif not re.match(constant.REGEX_PASSWORD, v):
            raise ValueError(
                "Password must contain at least one special character, one digit, one alphabet, one uppercase letter"
            )
        return v

    model_config = ConfigDict(from_attribute=True)

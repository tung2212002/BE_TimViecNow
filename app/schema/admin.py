from pydantic import BaseModel, validator, ConfigDict
import re
from typing import Optional
from datetime import datetime

from app.hepler.enum import Role, Gender, TypeAccount
from app.core import constant


class AdminBase(BaseModel):
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("gender")
    def validate_gender(cls, v):
        if v is not None:
            if v not in Gender.__members__.values():
                raise ValueError("Invalid gender")
            return v
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v


class AdminItemResponse(AdminBase):
    id: int
    is_active: bool
    role: Role
    email: str
    avatar: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    type_account: Optional[TypeAccount]

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v


class AdminCreateRequest(AdminBase):
    pass


class AdminCreate(AdminBase):
    pass


class AdminGetByEmailRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        if not re.match(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v


class AdminUpdateRequest(BaseModel):
    phone_number: Optional[str] = None
    gender: Optional[Gender] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")

    @validator("gender")
    def validate_gender(cls, v):
        if v is not None:
            if v not in Gender.__members__.values():
                raise ValueError("Invalid gender")
            return v


class AdminUpdate(AdminUpdateRequest):
    pass

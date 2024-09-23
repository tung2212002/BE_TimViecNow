from pydantic import BaseModel, validator, ConfigDict
import re
from typing import Optional
from datetime import datetime

from app.hepler.enum import Role, Gender, TypeAccount
from app.core import constant
from app.hepler.schema_validator import SchemaValidator


class AdminBase(BaseModel):
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)


# request
class AdminCreateRequest(AdminBase):
    pass


class AdminGetByEmailRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)


class AdminUpdateRequest(BaseModel):
    phone_number: Optional[str] = None
    gender: Optional[Gender] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)


# schema
class AdminCreate(AdminBase):
    pass


class AdminUpdate(AdminUpdateRequest):
    pass


# response
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
        return SchemaValidator.validate_avatar_url(v)

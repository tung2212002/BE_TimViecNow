from pydantic import BaseModel, validator, ConfigDict
from typing import Optional
from datetime import datetime
from fastapi import UploadFile

from app.hepler.enum import Role, Gender, TypeAccount
from app.hepler.schema_validator import SchemaValidator


class AdminBase(BaseModel):
    gender: Optional[Gender] = None
    phone_number: str
    email: str
    full_name: str
    avatar: Optional[UploadFile] = None
    type_account: TypeAccount.BUSINESS
    role: Role = Role.ADMIN

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)

    @validator("full_name")
    def validate_full_name(cls, v):
        return SchemaValidator.validate_full_name(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_upload_file(v)

    @validator("type_account")
    def validate_type_account(cls, v):
        return TypeAccount.BUSINESS

    @validator("role")
    def validate_role(cls, v):
        return Role.ADMIN


# request
class AdminCreateRequest(AdminBase):
    password: str
    confirm_password: str
    role: Optional[Role] = Role.ADMIN

    @validator("password")
    def validate_password(cls, v):
        return SchemaValidator.validate_password(v)

    @validator("confirm_password")
    def validate_confirm_password(cls, v, values):
        return SchemaValidator.validate_confirm_password(v, values)


class AdminGetByEmailRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)


class AdminUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[Gender] = None
    avatar: Optional[UploadFile] = None
    role: Optional[Role] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)

    @validator("full_name")
    def validate_full_name(cls, v):
        return SchemaValidator.validate_full_name(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_upload_file(v)

    @validator("role")
    def validate_role(cls, v):
        return SchemaValidator.validate_role(v)

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# schema
class AdminCreate(BaseModel):
    id: int
    gender: Gender


class AdminUpdate(BaseModel):
    gender: Gender


# response
class AdminItemResponse(BaseModel):
    id: int
    is_active: bool
    role: Role
    email: str
    phone_number: str
    full_name: str
    avatar: Optional[str] = None
    is_verified: Optional[bool] = False
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    type_account: Optional[TypeAccount]
    gender: Optional[Gender] = None

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_url(v)

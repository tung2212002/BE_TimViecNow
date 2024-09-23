from pydantic import BaseModel, validator, ConfigDict
from fastapi import UploadFile
from typing import Optional

from app.hepler.enum import Role, TypeAccount
from app.hepler.schema_validator import SchemaValidator


class UserBase(BaseModel):
    full_name: str
    email: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("full_name")
    def validate_full_name(cls, v):
        return SchemaValidator.validate_full_name(v)

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)


# request
class UserGetRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)


class UserCreateRequest(UserBase):
    avatar: Optional[UploadFile] = None
    password: str
    confirm_password: str
    role: Role = Role.USER

    @validator("confirm_password")
    def validate_password(cls, v, values):
        return SchemaValidator.validate_confirm_password(v, values)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validator_avatar_upload_file(v)

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[UploadFile] = None

    @validator("full_name")
    def validate_full_name(cls, v):
        return SchemaValidator.validate_full_name(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validator_avatar_upload_file(v)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)


# schema
class UserCreate(UserBase):
    avatar: Optional[str] = None
    role: Role = Role.USER
    password: str
    confirm_password: str

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER


class UserUpdate(BaseModel):
    full_name: str
    phone_number: str
    avatar: Optional[str] = None
    role: Role = Role.USER


# response
class UserItemResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool = True
    role: Role = Role.USER
    phone_number: Optional[str] = None
    type_account: Optional[TypeAccount] = TypeAccount.NORMAL

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_url(v)

    @validator("is_active")
    def validate_is_active(cls, v):
        return v or True

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER

    @validator("type_account")
    def validate_type_account(cls, v):
        return v or TypeAccount.NORMAL

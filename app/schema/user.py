from pydantic import BaseModel, validator, ConfigDict
from fastapi import UploadFile
from typing import Optional
from datetime import datetime

from app.hepler.enum import Role, TypeAccount, Gender
from app.hepler.schema_validator import SchemaValidator


class UserBase(BaseModel):
    full_name: str
    email: str
    phone_number: Optional[str] = None
    gender: Optional[Gender] = None
    avatar: Optional[UploadFile] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("full_name")
    def validate_full_name(cls, v):
        return SchemaValidator.validate_full_name(v)

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_upload_file(v)


# request
class UserGetRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)


class UserCreateRequest(UserBase):
    password: str
    confirm_password: str

    @validator("password")
    def validate_password(cls, v):
        return SchemaValidator.validate_password(v)

    @validator("confirm_password")
    def validate_confirm_password(cls, v, values):
        return SchemaValidator.validate_confirm_password(v, values)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_upload_file(v)


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[UploadFile] = None
    gender: Optional[Gender] = None

    @validator("full_name")
    def validate_full_name(cls, v):
        return SchemaValidator.validate_full_name(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_upload_file(v)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)


# schema
class UserCreate(BaseModel):
    id: int
    phone_number: Optional[str] = None
    email: str
    gender: Optional[Gender] = None
    password: Optional[str] = None
    role: Role = Role.USER
    type_account: TypeAccount = TypeAccount.NORMAL

    @validator("type_account")
    def validate_type_account(cls, v):
        return TypeAccount.NORMAL

    @validator("role")
    def validate_role(cls, v):
        return Role.USER


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[Gender] = None


# response
class UserItemResponse(BaseModel):
    id: int
    full_name: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[Gender] = None
    avatar: Optional[str] = None
    is_active: bool = True
    role: Role = Role.USER
    phone_number: Optional[str] = None
    type_account: Optional[TypeAccount] = TypeAccount.NORMAL
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

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


class UserBasicResponse(BaseModel):
    id: int
    full_name: str
    email: str
    avatar: Optional[str] = None
    nickname: Optional[str] = None
    role: Role = Role.USER
    type_account: TypeAccount = TypeAccount.NORMAL
    last_login: Optional[datetime] = None

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER

    @validator("type_account")
    def validate_type_account(cls, v):
        return v or TypeAccount.NORMAL

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_url(v)

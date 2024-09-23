from pydantic import BaseModel, Field, validator, ConfigDict
from fastapi import UploadFile
from typing import Optional
from datetime import datetime

from app.hepler.enum import Role, TypeAccount
from app.hepler.schema_validator import SchemaValidator


class ManagerBaseBase(BaseModel):
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
class ManagerBaseGetRequest(BaseModel):
    email: str = Field(..., example="1@email.com")

    @validator("email")
    def validate_email(cls, v):
        SchemaValidator.validate_email(v)


class ManagerBaseCreateRequest(ManagerBaseBase):
    avatar: Optional[UploadFile] = None
    password: str
    confirm_password: str
    role: Optional[Role] = Role.BUSINESS

    @validator("confirm_password")
    def validate_password(cls, v, values):
        return SchemaValidator.validate_confirm_password(v, values)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validator_avatar_upload_file(v)

    @validator("role")
    def validate_role(cls, v):
        return v or Role.BUSINESS


class ManagerBaseUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    avatar: Optional[UploadFile] = None
    password: Optional[str] = None

    @validator("full_name")
    def validate_full_name(cls, v):
        if v:
            return SchemaValidator.validate_full_name(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        if v:
            return SchemaValidator.validator_avatar_upload_file(v)

    @validator("password")
    def validate_password(cls, v):
        if v:
            return SchemaValidator.validate_password(v)


# schema
class ManagerBaseCreate(ManagerBaseCreateRequest):
    pass


class ManagerBaseUpdate(ManagerBaseUpdateRequest):
    pass


# response
class ManagerBaseItemResponse(ManagerBaseBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime]
    role: Role
    type_account: Optional[TypeAccount]

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_url(v)

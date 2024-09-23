from pydantic import BaseModel, validator, ConfigDict
from fastapi import UploadFile
from typing import Optional, Any
from datetime import datetime

from app.hepler.enum import Role, Gender
from app.hepler.schema_validator import SchemaValidator


class BusinessBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attribute=True)

    phone_number: str
    gender: str
    company_name: str
    work_position: str
    work_location: Optional[str] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)


# request
class BusinessUpdateRequest(BaseModel):
    phone_number: Optional[str] = None
    gender: Optional[Gender] = None
    company_name: Optional[str] = None
    work_position: Optional[str] = None
    work_location: Optional[str] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None
    avatar: Optional[UploadFile] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return SchemaValidator.validate_phone_number(v)

    @validator("gender")
    def validate_gender(cls, v):
        return SchemaValidator.validate_gender(v)

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validator_avatar_upload_file(v)


class BusinessGetByEmailRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)


class BusinessCreateRequest(BusinessBase):
    province_id: int
    district_id: Optional[int] = None


# schema
class BusinessCreate(BusinessCreateRequest):
    pass


class BusinessUpdate(BusinessUpdateRequest):
    pass


# response
class BusinessItemResponse(BusinessBase):
    id: int
    full_name: str
    email: str
    avatar: Optional[str] = None
    is_active: bool
    role: Role
    work_location: Optional[str] = None
    work_position: str
    updated_at: str
    created_at: str
    province: Optional[dict] = None
    district: Optional[dict] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_verified_email: bool
    is_verified_phone: bool
    is_verified_company: bool
    is_verified_identity: bool

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_url(v)

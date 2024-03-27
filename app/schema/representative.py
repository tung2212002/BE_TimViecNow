from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional, Any
from datetime import datetime

from app.hepler.enum import Role, Gender
from app.core import constant


class RepresentativeBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attribute=True)

    phone_number: str
    gender: str
    company: str
    work_position: str
    work_location: str

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v

    @validator("gender")
    def validate_gender(cls, v):
        if not v in Gender.__members__.values():
            raise ValueError("Invalid gender")
        return v


class RepresentativeItemResponse(RepresentativeBase):

    id: int
    email: str
    avatar: Optional[str] = None
    is_active: bool
    role: Role
    work_location: str
    work_position: str
    updated_at: str
    created_at: str
    province: Optional[dict] = None
    district: Optional[dict] = None
    last_login: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


class RepresentativeGetRequest(BaseModel):
    id: int


class RepresentativeCreateRequest(RepresentativeBase):
    province_id: Optional[int] = None
    district_id: Optional[int] = None


class RepresentativeUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[UploadFile] = None
    gender: Optional[Gender] = None
    company: Optional[str] = None
    work_position: Optional[str] = None
    work_location: Optional[str] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None

    @validator("full_name")
    def validate_full_name(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError("Full name must be at least 3 characters")
            elif len(v) > 50:
                raise ValueError("Full name must be at most 50 characters")
            elif not v.replace(" ", "").isalpha():
                raise ValueError("Full name must be alphabet")
            return v

    @validator("email")
    def validate_email(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_EMAIL, v):
                raise ValueError("Invalid email")
            return v

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")
            return v

    @validator("gender")
    def validate_gender(cls, v):
        if v is not None:
            if v not in Gender.__members__.values():
                raise ValueError("Invalid gender")
            return v

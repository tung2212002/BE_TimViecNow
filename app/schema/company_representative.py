from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional

from app.hepler.enum import Role, Gender
from app.core import constant


class CompanyRepresentativeBase(BaseModel):
    full_name: str
    email: str
    phone_number: str
    gender: str
    company = str
    work_position = str
    work_location = str
    district = str

    model_config = ConfigDict(from_attribute=True)

    @validator("full_name")
    def validate_full_name(cls, v):
        if len(v) < 3:
            raise ValueError("Full name must be at least 3 characters")
        elif len(v) > 50:
            raise ValueError("Full name must be at most 50 characters")
        elif not v.replace(" ", "").isalpha():
            raise ValueError("Full name must be alphabet")
        return v

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v

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


class CompanyRepresentativeItemResponse(CompanyRepresentativeBase):
    id: int
    picture_path: Optional[str] = None
    is_active: bool
    role: Role
    updated_at: str
    created_at: str
    last_login: Optional[str] = None


class CompanyRepresentativeGetRequest(BaseModel):
    id = int


class CompanyRepresentativeCreateRequest(CompanyRepresentativeBase):
    picture: Optional[UploadFile] = None
    password: str
    confirm_password: str
    role: Role = Role.REPRESENTATIVE

    @validator("password")
    def validate_password(cls, v, values):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif len(v) > 50:
            raise ValueError("Password must be at most 50 characters")
        elif not re.match(constant.REGEX_PASSWORD, v):
            raise ValueError(
                "Password must contain at least one special character, one digit, one alphabet, one uppercase letter"
            )
        elif "confirm_password" in values and v != values["confirm_password"]:
            raise ValueError("Password and confirm password must match")
        return v

    @validator("picture")
    def validate_picture(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
        return v


class CompanyRepresentativeUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    picture: Optional[UploadFile] = None
    gender: Optional[str] = None
    company: Optional[str] = None
    work_position: Optional[str] = None
    work_location: Optional[str] = None
    district: Optional[str] = None

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

    @validator("picture")
    def validate_picture(cls, v):
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

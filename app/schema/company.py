from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional, List


from app.hepler.enum import CompanyType
from app.core import constant


class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: str
    total_active_jobs: int
    is_premium: bool = False
    label: Optional[str] = None
    logo: Optional[UploadFile] = None
    website: Optional[str] = None
    address: str
    company_short_description: Optional[str] = None
    scale: str
    tax_code: str
    field: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("name")
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Name must be at least 3 characters")
        elif len(v) > 255:
            raise ValueError("Name must be at most 255 characters")
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

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
        return v


class CompanyItemResponse(BaseModel):
    id: int
    name: str
    email: str
    type: CompanyType
    phone_number: str
    is_premium: bool
    label: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    address: str
    company_short_description: Optional[str] = None
    scale: str
    fields: List[object]
    is_verified: bool


class CompanyPrivateResponse(BaseModel):
    id: int
    name: str
    email: str
    type: CompanyType
    phone_number: str
    is_premium: bool
    label: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    address: str
    company_short_description: Optional[str] = None
    scale: str
    fields: List[object]
    tax_code: str
    is_verified: bool


class CompanyJobResponse(CompanyBase):
    id: int
    name: str
    logo: Optional[str] = None


class CompanyGetRequest(BaseModel):
    id: int


class CompanyCreateRequest(CompanyBase):
    fields: List[int]


class CompanyCreate(CompanyBase):
    fields: List[int]


class CompanyUpdateRequest(BaseModel):
    id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    total_active_jobs: Optional[int] = None
    is_premium: Optional[bool] = None
    label: Optional[str] = None
    logo: Optional[UploadFile] = None
    website: Optional[str] = None
    address: Optional[str] = None
    company_short_description: Optional[str] = None
    scale: Optional[str] = None
    tax_code: Optional[str] = None
    fields: Optional[List] = None

    @validator("email")
    def validate_email(cls, v):
        if v is not None:
            if not re.fullmatch(constant.REGEX_EMAIL, v):
                raise ValueError("Invalid email")
            return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")
            return v

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
        return v


class CompanyUpdate(BaseModel):
    id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    total_active_jobs: Optional[int] = None
    is_premium: Optional[bool] = None
    label: Optional[str] = None
    logo: Optional[UploadFile] = None
    website: Optional[str] = None
    address: Optional[str] = None
    company_short_description: Optional[str] = None
    scale: Optional[str] = None
    tax_code: Optional[str] = None
    fields: Optional[List] = None

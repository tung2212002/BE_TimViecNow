from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import UploadFile
from typing import Optional

from app.hepler.enum import Role, TypeAccount, Provider
from app.core import constant


class SocialNetworkBase(BaseModel):
    full_name: Optional[str] = None
    email: str
    social_id: Optional[str] = None
    phone_number: Optional[str] = None
    type: Provider

    model_config = ConfigDict(from_attribute=True, extra="ignore")

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
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")
            return v
        return v


# request
class SocialNetworkGetRequest(BaseModel):
    email: str = Field(..., example="1@email.com")

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v


class SocialNetworkCreateRequest(SocialNetworkBase):
    role: Role = Role.SOCIAL_NETWORK
    access_token: str
    user_id: Optional[int] = None


class SocialNetworkUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[UploadFile] = None
    access_token: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

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
        return v


# schema
class SocialNetworkCreate(BaseModel):
    type: Provider
    social_id: str
    email: str
    access_token: str
    id: int


class SocialNetworkUpdate(BaseModel):
    access_token: Optional[str] = None


# response
class SocialNetworkItemResponse(SocialNetworkBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool = True
    role: Role = Role.SOCIAL_NETWORK
    type_account: Optional[TypeAccount] = TypeAccount.NORMAL
    user_id: Optional[int] = None

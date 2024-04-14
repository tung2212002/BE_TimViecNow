from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional
from datetime import datetime

from app.core import constant
from app.hepler.enum import Role, TypeAccount, FolderBucket
from app.hepler.generate_file_name import generate_file_name


class ManagerBaseBase(BaseModel):
    full_name: str
    email: str
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


class ManagerBaseItemResponse(ManagerBaseBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime]
    role: Role
    type_account: Optional[TypeAccount]

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v


class ManagerBaseGetRequest(BaseModel):
    email: str = Field(..., example="1@email.com")

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v


class ManagerBaseCreateRequest(ManagerBaseBase):
    avatar: Optional[UploadFile] = None
    password: str
    confirm_password: str
    role: Optional[Role] = Role.BUSINESS

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

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
            v.filename = generate_file_name(v.filename, FolderBucket.AVATAR)
        return v


class ManagerBaseCreate(ManagerBaseCreateRequest):
    pass


class ManagerBaseUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[UploadFile] = None
    password: Optional[str] = None

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
            v.filename = generate_file_name(v.filename, FolderBucket.AVATAR)
        return v

    @validator("password")
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters")
            elif len(v) > 50:
                raise ValueError("Password must be at most 50 characters")
            elif not re.match(constant.REGEX_PASSWORD, v):
                raise ValueError(
                    "Password must contain at least one special character, one digit, one alphabet, one uppercase letter"
                )
            return v


class ManagerBaseUpdate(ManagerBaseUpdateRequest):
    pass

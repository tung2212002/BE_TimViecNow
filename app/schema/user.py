from pydantic import BaseModel, validator, ConfigDict
import re
from fastapi import UploadFile
from typing import Optional

from app.hepler.enum import Role, TypeAccount, FolderBucket
from app.core import constant
from app.hepler.generate_file_name import generate_file_name


class UserBase(BaseModel):
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


class UserItemResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool = True
    role: Role = Role.USER
    phone_number: Optional[str] = None
    type_account: Optional[TypeAccount] = TypeAccount.NORMAL

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v

    @validator("is_active")
    def validate_is_active(cls, v):
        return v or True

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER

    @validator("type_account")
    def validate_type_account(cls, v):
        return v or TypeAccount.NORMAL


class UserGetRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v


class UserCreateRequest(UserBase):
    avatar: Optional[UploadFile] = None
    password: str
    confirm_password: str
    role: Role = Role.USER

    @validator("confirm_password")
    def validate_password(cls, v, values):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif len(v) > 50:
            raise ValueError("Password must be at most 50 characters")
        elif not re.match(constant.REGEX_PASSWORD, v):
            raise ValueError(
                "Password must contain at least one special character, one digit, one alphabet, one uppercase letter"
            )
        elif "password" in values and v != values["password"]:
            raise ValueError("Password and confirm password must match")
        return v

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
            v.filename = generate_file_name(FolderBucket.AVATAR, v.filename)
        return v

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER


class UserCreate(UserBase):
    avatar: Optional[str] = None
    role: Role = Role.USER
    password: str
    confirm_password: str

    @validator("role")
    def validate_role(cls, v):
        return v or Role.USER


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[UploadFile] = None

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


class UserUpdate(UserUpdateRequest):
    pass

from pydantic import BaseModel, ConfigDict, validator
from typing import Optional
import re
from datetime import datetime, timezone

from app.core import constant
from app.hepler.enum import VerifyCodeStatus


class VerifyCodeBase(BaseModel):
    code: str
    email: str
    status: Optional[VerifyCodeStatus] = VerifyCodeStatus.ACTIVE

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class VerifyCodeRequest(BaseModel):
    code: str
    session_id: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("code")
    def validate_code(cls, code):
        if code.isdigit() and len(code) == 6:
            return code
        raise ValueError("Code must be 6 digits")


class VerifyCodeCreate(VerifyCodeBase):
    manager_base_id: int
    failed_attempts: Optional[int] = 0
    session_id: Optional[str] = None


class VerifyCodeCreateRequest(VerifyCodeCreate):
    pass


class VerifyCodeItemResponse(VerifyCodeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    expired_at: datetime
    failed_attempts: int


class VerifyCodeUpdate(BaseModel):
    status: Optional[VerifyCodeStatus] = None
    failed_attempts: Optional[int] = None


class VerifyCodeUpdateRequest(VerifyCodeUpdate):
    pass

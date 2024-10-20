from pydantic import BaseModel, ConfigDict, validator
from typing import Optional
from datetime import datetime

from app.hepler.enum import VerifyCodeStatus
from app.hepler.schema_validator import SchemaValidator


class VerifyCodeBase(BaseModel):
    code: str
    email: str
    status: Optional[VerifyCodeStatus] = VerifyCodeStatus.ACTIVE

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("status")
    def validate_status(cls, v):
        return v or VerifyCodeStatus.ACTIVE


# request
class VerifyCodeRequest(BaseModel):
    code: str
    session_id: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("code")
    def validate_code(cls, v):
        return SchemaValidator.validate_code(v)


class VerifyCodeCreateRequest(VerifyCodeBase):
    manager_id: int
    failed_attempts: Optional[int] = 0
    session_id: Optional[str] = None


class VerifyCodeUpdateRequest(VerifyCodeBase):
    status: Optional[VerifyCodeStatus] = None
    failed_attempts: Optional[int] = None


# schema
class VerifyCodeCreate(VerifyCodeCreateRequest):
    pass


class VerifyCodeUpdate(VerifyCodeUpdateRequest):
    pass


# response
class VerifyCodeItemResponse(VerifyCodeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    expired_at: datetime
    failed_attempts: int

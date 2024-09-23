from pydantic import BaseModel, ConfigDict, validator
from typing import Optional
import re
from datetime import datetime

from app.hepler.enum import Role, TypeAccount, TokenType
from app.hepler.schema_validator import SchemaValidator


class TokenPayload(BaseModel):
    email: str
    id: int
    is_active: bool
    role: Role
    type_account: TypeAccount
    is_verified: Optional[bool] = None
    type: TokenType
    exp: datetime
    iat: datetime

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")

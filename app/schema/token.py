from pydantic import BaseModel, ConfigDict, validator
from typing import Optional
import re
from datetime import datetime

from app.hepler.enum import Role, TypeAccount, TokenType
from app.core.constant import REGEX_EMAIL


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
        if not re.fullmatch(REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v

    model_config = ConfigDict(from_attribute=True, extra="ignore")

from pydantic import BaseModel, ConfigDict, validator
from typing import Optional
import re
from datetime import datetime

from app.hepler.enum import Role, TypeAccount, TokenType
from app.hepler.schema_validator import SchemaValidator


class TokenPayload(BaseModel):
    id: int
    role: Role
    type_account: TypeAccount
    type: TokenType
    exp: datetime
    iat: datetime

    model_config = ConfigDict(from_attribute=True, extra="ignore")

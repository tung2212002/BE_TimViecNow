from pydantic import BaseModel, ConfigDict, validator
from typing import Optional

from app.core import constant


class VerifyCodeBlockCreate(BaseModel):
    email: str

from pydantic import BaseModel, validator


class VerifyCodeBlockCreate(BaseModel):
    email: str

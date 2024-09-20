from pydantic import BaseModel, validator, ConfigDict

from app.core import constant
from app.hepler.schema_validator import SchemaValidator


class AuthChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @validator("old_password")
    def validate_old_password(cls, v):
        return SchemaValidator.validate_old_password(v)

    @validator("new_password")
    def validate_new_password(cls, v):
        return SchemaValidator.validate_password(v)

    @validator("confirm_password")
    def validate_confirm_password(cls, v, values):
        return SchemaValidator.validate_confirm_password(v, values)

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class AuthLogin(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)

    @validator("password")
    def validate_password(cls, v):
        return SchemaValidator.validate_password(v)

    model_config = ConfigDict(from_attribute=True)


class AuthForgotPassword(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        return SchemaValidator.validate_email(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")

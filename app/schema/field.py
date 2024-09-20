from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional


class FieldBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class FieldCreateRequest(FieldBase):
    pass


class FieldUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


# schema
class FieldCreate(FieldBase):
    pass


class FieldUpdate(FieldBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


# response
class FieldItemResponse(FieldBase):
    id: int

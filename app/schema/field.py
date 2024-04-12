from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional


class FieldBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class FieldCreateRequest(FieldBase):
    pass


class FieldCreate(FieldBase):
    pass


class FieldUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class FieldUpdate(FieldBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class FieldItemResponse(FieldBase):
    id: int


class FieldListResponse(FieldBase):
    pass


class FieldGetRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v


class FieldDeleteRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v

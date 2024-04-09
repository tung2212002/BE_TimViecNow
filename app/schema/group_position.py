from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional


class GroupPositionBase(BaseModel):
    name: str
    slug: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class GroupPositionCreateRequest(GroupPositionBase):
    pass


class GroupPositionUpdateRequest(GroupPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None


class GroupPositionItemResponse(GroupPositionBase):
    id: int
    tags: Optional[list] = None


class GroupPositionListResponse(GroupPositionBase):
    pass


class GroupPositionGetRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v


class GroupPositionDeleteRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v

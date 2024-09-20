from pydantic import BaseModel, validator, ConfigDict
from typing import Optional


class GroupPositionBase(BaseModel):
    name: str
    slug: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class GroupPositionCreateRequest(GroupPositionBase):
    pass


class GroupPositionUpdateRequest(GroupPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None


# schema
class GroupPositionCreate(GroupPositionBase):
    pass


class GroupPositionUpdate(GroupPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None


# response
class GroupPositionItemResponse(GroupPositionBase):
    id: int
    tags: Optional[list] = None

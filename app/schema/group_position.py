from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from app.schema.job_position import JobPositionItemResponse


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
    tags: Optional[List[JobPositionItemResponse]] = None

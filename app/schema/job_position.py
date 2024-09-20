from pydantic import BaseModel, validator, ConfigDict
from typing import Optional


class JobPositionBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class JobPositionCreateRequest(JobPositionBase):
    group_postion_id: int


class JobPositionUpdateRequest(JobPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    group_postion_id: Optional[int] = None


# schema
class JobPositionCreate(JobPositionBase):
    pass


class JobPositionUpdate(JobPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    group_postion_id: Optional[int] = None


# response
class JobPositionItemResponse(JobPositionBase):
    id: int

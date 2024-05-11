from pydantic import BaseModel, validator, ConfigDict
from typing import Optional


class JobPositionBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class JobPositionCreateRequest(JobPositionBase):
    group_postion_id: int


class JobPositionCreate(JobPositionBase):
    pass


class JobPositionUpdateRequest(JobPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    group_postion_id: Optional[int] = None


class JobPositionUpdate(JobPositionBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    group_postion_id: Optional[int] = None


class JobPositionItemResponse(JobPositionBase):
    id: int


class JobPositionListResponse(JobPositionBase):
    pass


class JobPositionGetRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v


class JobPositionDeleteRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v

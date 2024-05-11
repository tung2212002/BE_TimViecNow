from pydantic import BaseModel, validator, ConfigDict
from typing import Optional


class SkillBase(BaseModel):
    name: str
    slug: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class SkillCreateRequest(SkillBase):
    pass


class SkillCreate(SkillBase):
    pass


class SkillUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


class SkillUpdate(SkillBase):
    name: Optional[str] = None
    slug: Optional[str] = None


class SkillItemResponse(SkillBase):
    id: int


class SkillListResponse(SkillBase):
    pass


class SkillGetRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v


class SkillDeleteRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v

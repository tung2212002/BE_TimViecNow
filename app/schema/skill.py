from pydantic import BaseModel, validator, ConfigDict
from typing import Optional

from app.hepler.enum import JobSkillType


class SkillBase(BaseModel):
    name: str
    slug: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class SkillCreateRequest(SkillBase):
    pass


class SkillUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


# schema
class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    pass


# response
class SkillItemResponse(SkillBase):
    id: int

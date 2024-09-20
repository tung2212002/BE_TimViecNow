from pydantic import BaseModel, validator, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class CategoryCreateRequest(CategoryBase):
    pass


class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


# schema
class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


# response
class CategoryItemResponse(CategoryBase):
    id: int
    count: int
    pass

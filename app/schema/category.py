from pydantic import BaseModel, validator, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class CategoryCreateRequest(CategoryBase):
    pass


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class CategoryItemResponse(CategoryBase):
    id: int
    count: int


class CategoryListResponse(CategoryBase):
    pass


class CategoryGetRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v


class CategoryDeleteRequest(BaseModel):
    id: int

    @validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("Invalid id")
        return v

from pydantic import BaseModel, validator, Field, conint
from typing import Optional

from app.hepler.enum import OrderBy, SortType


class Pagination(BaseModel):
    skip: Optional[conint(ge=0)] = 0
    limit: Optional[conint(ge=1, le=100)] = 10
    sort_by: Optional[str] = "id"
    order_by: Optional[str] = "asc"

    @validator("sort_by")
    def validate_sort_by(cls, v):
        if v not in OrderBy.__members__.values():
            raise ValueError("Invalid sort_by")
        return v

    @validator("order_by")
    def validate_order_by(cls, v):
        if v not in SortType.__members__.values():
            raise ValueError("Invalid order_by")
        return v

from pydantic import BaseModel, validator, Field, conint, ConfigDict
from typing import Optional

from app.hepler.enum import OrderBy, SortType


class Pagination(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 100
    sort_by: Optional[OrderBy] = OrderBy.ID
    order_by: Optional[SortType] = SortType.ASC

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("limit")
    def validate_limit(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Invalid limit")
        return v

    @validator("skip")
    def validate_skip(cls, v):
        if v < 0:
            raise ValueError("Invalid skip")
        return v

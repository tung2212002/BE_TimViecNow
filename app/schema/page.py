from pydantic import BaseModel, validator, Field, conint, ConfigDict
from typing import Optional

from app.hepler.enum import SortBy, OrderType


class Pagination(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 100
    sort_by: Optional[SortBy] = SortBy.ID
    order_by: Optional[OrderType] = OrderType.ASC

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("limit")
    def validate_limit(cls, v):
        if v < 0 or v > 1000:
            raise ValueError("Invalid limit")
        return v

    @validator("skip")
    def validate_skip(cls, v):
        if v < 0:
            raise ValueError("Invalid skip")
        return v

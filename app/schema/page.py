from pydantic import BaseModel, validator, ConfigDict, field_validator, Field
from typing import Optional

from app.hepler.enum import SortBy, OrderType


class Pagination(BaseModel):
    skip: Optional[int] = Field(0, ge=0, le=100000)
    limit: Optional[int] = Field(10, ge=1, le=1000)
    sort_by: Optional[SortBy] = SortBy.ID
    order_by: Optional[OrderType] = OrderType.ASC

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("skip")
    def validate_skip(cls, v):
        return v or 0

    @validator("limit")
    def validate_limit(cls, v):
        return v or 1000

    @validator("sort_by")
    def validate_sort_by(cls, v):
        return v or SortBy.ID

    @validator("order_by")
    def validate_order_by(cls, v):
        return v or OrderType.ASC

    def get_key(self) -> str:
        return f"{self.skip}_{self.limit}_{self.sort_by}_{self.order_by}"

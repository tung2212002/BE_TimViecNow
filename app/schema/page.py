from pydantic import BaseModel, validator, ConfigDict
from typing import Optional

from app.hepler.enum import SortBy, OrderType
from app.hepler.schema_validator import SchemaValidator


class Pagination(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 100
    sort_by: Optional[SortBy] = SortBy.ID
    order_by: Optional[OrderType] = OrderType.ASC

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("limit")
    def validate_limit(cls, v):
        return SchemaValidator.validate_limit(v)

    @validator("skip")
    def validate_skip(cls, v):
        return SchemaValidator.validate_skip(v)

    @validator("sort_by")
    def validate_sort_by(cls, v):
        return v or SortBy.ID

    @validator("order_by")
    def validate_order_by(cls, v):
        return v or OrderType.ASC

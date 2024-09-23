from pydantic import BaseModel, validator, ConfigDict
from datetime import time

from app.hepler.schema_validator import SchemaValidator


class WorkingTimeBase(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    job_id: int
    start_time: time
    end_time: time
    date_from: int
    date_to: int

    @validator("date_from")
    def validate_date_from(cls, v):
        return SchemaValidator.validate_date_of_week(v)

    @validator("date_to")
    def validate_date_to(cls, v):
        return SchemaValidator.validate_date_of_week(v)


# request
class WorkingTimeCreateRequest(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    start_time: time
    end_time: time
    date_from: int
    date_to: int

    @validator("date_from")
    def validate_date_from(cls, v):
        return SchemaValidator.validate_date_of_week(v)

    @validator("date_to")
    def validate_date_to(cls, v):
        return SchemaValidator.validate_date_of_week(v)


# schema
class WorkingTimeCreate(WorkingTimeBase):
    pass


class WorkingTimeUpdate(WorkingTimeBase):
    pass


# response
class WorkingTimeResponse(BaseModel):
    start_time: time
    end_time: time
    date_from: int
    date_to: int
    id: int

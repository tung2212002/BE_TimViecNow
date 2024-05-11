from pydantic import BaseModel, validator, ConfigDict
from datetime import time


class WorkingTimeBase(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    job_id: int
    start_time: time
    end_time: time
    date_from: int
    date_to: int

    @validator("date_from")
    def validate_date_from(cls, v):
        if v < 1 or v > 7:
            raise ValueError("Invalid date from")
        return v

    @validator("date_to")
    def validate_date_to(cls, v):
        if v < 1 or v > 7:
            raise ValueError("Invalid date to")
        return v


class WorkingTimeResponse(BaseModel):
    start_time: time
    end_time: time
    date_from: int
    date_to: int
    id: int


class WorkingTimeCreateRequest(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    start_time: time
    end_time: time
    date_from: int
    date_to: int

    @validator("date_from")
    def validate_date_from(cls, v):
        if v < 1 or v > 7:
            raise ValueError("Invalid date from")
        return v

    @validator("date_to")
    def validate_date_to(cls, v):
        if v < 1 or v > 7:
            raise ValueError("Invalid date to")
        return v


class WorkingTimeCreate(WorkingTimeBase):
    pass


class WorkingTimeUpdate(WorkingTimeBase):
    pass

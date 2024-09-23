from pydantic import BaseModel, ConfigDict
from typing import Optional


class WorkLocationBase(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    job_id: int
    province_id: int
    district_id: Optional[int] = None
    description: Optional[str] = None


# request
class WorkLocatioCreateRequest(WorkLocationBase):
    pass


class WorkLocatioUpdateRequest(WorkLocationBase):
    pass


# schema
class WorkLocatioCreate(WorkLocationBase):
    pass


class WorkLocatioUpdate(WorkLocationBase):
    pass


# response
class WorkLocatioResponse(BaseModel):
    province: dict
    district: Optional[dict] = None
    description: Optional[str] = None

from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional


class DistrictBase(BaseModel):
    name: str
    code: str
    name_with_type: str
    slug: str
    type: str

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class DistrictCreate(DistrictBase):
    pass


class DistrictUpdate(DistrictBase):
    name: Optional[str] = None
    code: Optional[str] = None
    name_with_type: Optional[str] = None
    slug: Optional[str] = None
    type: Optional[str] = None


class DistrictItemResponse(DistrictBase):
    id: int


class DistrictListResponse(DistrictBase):
    pass


class DistrictGetRequest(BaseModel):
    id: int


class DistrictDeleteRequest(BaseModel):
    id: int

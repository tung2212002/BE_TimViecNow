from pydantic import BaseModel, validator, ConfigDict
from typing import Optional, Any
from datetime import datetime
import re

from app.hepler.enum import CampaignStatus
from app.core import constant


class CampaignBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attribute=True)

    title: str
    is_flash: Optional[bool] = False
    business_id: int

    @validator("title")
    def validate_title(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError("Invalid title")
        return v


class CampaignItemResponse(CampaignBase):
    id: int
    created_at: str
    updated_at: str
    status: Optional[str] = CampaignStatus.OPEN
    optimal_score: Optional[int] = 0
    job: Optional[dict] = None


class CampaignGetRequest(BaseModel):
    id: int


class CampaignGetByBusinessIdRequest(BaseModel):
    business_id: int


class CampaignCreateRequest(CampaignBase):
    pass


class CampaignUpdateRequest(CampaignBase):
    status: Optional[str] = CampaignStatus.OPEN
    optimal_score: Optional[int] = 0

    @validator("status")
    def validate_status(cls, v):
        if not v in CampaignStatus.__members__.values():
            raise ValueError("Invalid status")
        return v


class CampaignDeleteRequest(BaseModel):
    id: int

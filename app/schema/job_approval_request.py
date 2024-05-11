from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.schema.page import Pagination
from app.hepler.enum import JobApprovalStatus


class JobApprovalRequestBase(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    job_id: int
    status: Optional[JobApprovalStatus] = None


class JobApprovalRequestCreate(JobApprovalRequestBase):
    pass


class JobApprovalRequestUpdate(JobApprovalRequestBase):
    pass


class JobApprovalRequestResponse(JobApprovalRequestBase):
    id: int
    status: JobApprovalStatus
    created_at: datetime
    updated_at: datetime


class JobApprovalFilter(Pagination):
    status: Optional[JobApprovalStatus] = None
    job_id: Optional[int] = None

from pydantic import BaseModel, validator, ConfigDict
from typing import Optional
from datetime import datetime, time

from app.schema.page import Pagination
from app.hepler.enum import JobApprovalStatus


class JobApprovalRequestBase(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    job_id: int
    status: Optional[JobApprovalStatus] = JobApprovalStatus.PENDING


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
    status: Optional[JobApprovalStatus] = JobApprovalStatus.ALL
    job_id: Optional[int] = None

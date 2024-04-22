from app.crud.base import CRUDBase

from app.model.job_approval_request import JobApprovalRequest
from app.schema.job_approval_request import (
    JobApprovalRequestCreate,
    JobApprovalRequestUpdate,
)


class CRUDJobApprovalRequest(
    CRUDBase[JobApprovalRequest, JobApprovalRequestCreate, JobApprovalRequestUpdate]
):
    pass


job_approval_request = CRUDJobApprovalRequest(JobApprovalRequest)

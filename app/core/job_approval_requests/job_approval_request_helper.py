from app.schema import (
    job_approval_request as schema_job_approval_request,
    job as job_schema,
)
from app.core.helper_base import HelperBase


# def create_job_approval_request(db: Session, job_id: int):
#     job_approval_request_in = schema_job_approval_request.JobApprovalRequestCreate(
#         job_id=job_id
#     )
#     job_approval_request = crud.job_approval_request.create(
#         db, obj_in=job_approval_request_in
#     )
#     return job_approval_request


# def create_job_update_approval_request(db: Session, data: dict):
#     job_approval_request = crud.job_approval_request.create(db, obj_in=data)
#     return job_approval_request


class JobApprovalRequestHelper(HelperBase):
    pass


job_approval_request_helper = JobApprovalRequestHelper(
    schema_job_approval_request.JobApprovalRequestList,
    job_schema.JobApproveRequest,
    job_schema.JobApproveUpdateJobRequest,
)

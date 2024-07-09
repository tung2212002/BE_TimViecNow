from sqlalchemy.orm import Session

from app.crud.job_approval_request import (
    job_approval_request as job_approval_requestCRUD,
)
from app.schema import (
    job_approval_request as schema_job_approval_request,
)


def create_job_approval_request(db: Session, job_id: int):
    job_approval_request_in = schema_job_approval_request.JobApprovalRequestCreate(
        job_id=job_id
    )
    job_approval_request = job_approval_requestCRUD.create(
        db, obj_in=job_approval_request_in
    )
    return job_approval_request


def create_job_update_approval_request(db: Session, data: dict):
    job_approval_request = job_approval_requestCRUD.create(db, obj_in=data)
    return job_approval_request

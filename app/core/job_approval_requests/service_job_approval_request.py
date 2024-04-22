from sqlalchemy.orm import Session
from typing import Optional

from app.crud.campaign import campaign as campaignCRUD
from app.crud.job_approval_request import (
    job_approval_request as job_approval_requestCRUD,
)
from app.schema import (
    job_approval_request as schema_job_approval_request,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def create_job_approval_request_job(db: Session, job_id: int):
    job_approval_request_in = schema_job_approval_request.JobApprovalRequestCreate(
        job_id=job_id
    )
    job_approval_request = job_approval_requestCRUD.create(
        db, obj_in=job_approval_request_in
    )
    return job_approval_request

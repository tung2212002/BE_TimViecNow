from sqlalchemy.orm import Session

from app.crud.job_approval_request import (
    job_approval_request as job_approval_requestCRUD,
)
from app.schema import (
    job_approval_request as schema_job_approval_request,
    job as job_schema,
    job_approval_log as schema_job_approval_log,
)
from app.core import constant
from app.hepler.response_custom import custom_response_error
from app.core.job import helper_job
from app.core.job_approval_log import helper_job_approval_log
from app.crud.job import job as jobCRUD
from app.hepler.enum import JobStatus, JobApprovalStatus
from app.hepler.exception_handler import get_message_validation_error


def get(db: Session, data: dict):
    try:
        job_approval_request_data = schema_job_approval_request.JobApprovalRequestList(
            **data
        )
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    job_approval_requests = job_approval_requestCRUD.get_multi(
        db,
        **job_approval_request_data.model_dump(),
    )
    return constant.SUCCESS, 200, job_approval_requests


def get_by_id(db: Session, job_approval_request_id: int, current_user):
    job_approval_request = job_approval_requestCRUD.get(db, job_approval_request_id)
    if not job_approval_request:
        return constant.ERROR, 404, "Job approval request not found"
    return constant.SUCCESS, 200, job_approval_request


def approve(db: Session, current_user, data: dict):
    try:
        job_approval_request_data = job_schema.JobApproveRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    job_approval_request = job_approval_requestCRUD.get(
        db, job_approval_request_data.job_approval_request_id
    )
    if not job_approval_request:
        return constant.ERROR, 404, "Job approval request not found"
    job = job_approval_request.job
    if job_approval_request.status == job_approval_request_data.status:
        return constant.ERROR, 400, "Job already approved"
    if job_approval_request_data.status == JobApprovalStatus.APPROVED:
        if job.status != JobStatus.PUBLISHED:
            jobCRUD.update(db, db_obj=job, obj_in={"status": JobStatus.PUBLISHED})
    job_approval_request.id
    job_approval_requestCRUD.update(
        db,
        db_obj=job_approval_request,
        obj_in={"status": job_approval_request_data.status},
    )
    job_approval_log = schema_job_approval_log.JobApprovalLogCreate(
        **{
            "job_approval_request_id": job_approval_request.id,
            "previous_status": job_approval_request.status,
            "new_status": job_approval_request_data.status,
            "admin_id": current_user.id,
            "reason": job_approval_request_data.reason,
        }
    )
    helper_job_approval_log.create_job_approval_log(
        db,
        job_approval_log,
    )
    return constant.SUCCESS, 200, job_approval_request


def approve_update(db: Session, current_user, data: dict):
    try:
        job_approval_update_data = job_schema.JobApproveUpdateJobRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    job_approval_request = job_approval_requestCRUD.get(
        db, job_approval_update_data.job_approval_request_id
    )
    if not job_approval_request:
        return constant.ERROR, 404, "Job approval request not found"

    job = job_approval_request.job
    if job_approval_request.status == job_approval_update_data.status:
        return constant.ERROR, 400, "Job already approved"

    if (
        job_approval_update_data.status == job_approval_request.status
        or job_approval_request.status != JobApprovalStatus.PENDING
    ):
        return constant.ERROR, 400, "Invalid status"

    job_approval_request.id
    if job_approval_request.status == JobApprovalStatus.APPROVED:
        job_update_in = schema_job_approval_request.JobApprovalRequestResponse(
            **job_approval_request.__dict__
        )
        jobCRUD.update(db, db_obj=job, obj_in=job_update_in)
    job_approval_requestCRUD.update(
        db,
        db_obj=job_approval_request,
        obj_in={"status": job_approval_update_data.status},
    )
    job_approval_log = schema_job_approval_log.JobApprovalLogCreate(
        **{
            "job_approval_request_id": job_approval_request.id,
            "previous_status": job_approval_request.status,
            "new_status": job_approval_update_data.status,
            "admin_id": current_user.id,
            "reason": job_approval_update_data.reason,
        }
    )
    helper_job_approval_log.create_job_approval_log(
        db,
        job_approval_log,
    )
    return constant.SUCCESS, 200, job_approval_request

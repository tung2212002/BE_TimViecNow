from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    job_approval_request as schema_job_approval_request,
    job_approval_log as schema_job_approval_log,
)
from app.core import constant
from app.core.job_approval_log.ob_approval_log_helper import job_approval_log_helper
from app.crud.job import job as jobCRUD
from app.hepler.enum import JobStatus, JobApprovalStatus
from app.core.job_approval_requests.job_approval_request_helper import (
    job_approval_request_helper,
)
from app.model import ManagerBase


class JobApprovalRequestService:
    async def get(self, db: Session, data: dict):
        job_approval_request_data = job_approval_request_helper.validate_pagination(
            data
        )

        job_approval_requests = crud.job_approval_request.get_multi(
            db,
            **job_approval_request_data.model_dump(),
        )
        return constant.SUCCESS, 200, job_approval_requests

    async def get_by_id(self, db: Session, id: int):
        job_approval_request = crud.job_approval_request.get(db, id)
        if not job_approval_request:
            return constant.ERROR, 404, "Job approval request not found"
        return constant.SUCCESS, 200, job_approval_request

    async def approve(self, db: Session, current_user: ManagerBase, data: dict):
        job_approval_request_data = job_approval_request_helper.validate_create(data)

        job_approval_request = crud.job_approval_request.get(
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
        crud.job_approval_request.update(
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
        job_approval_log_helper.create_job_approval_log(
            db,
            job_approval_log,
        )
        return constant.SUCCESS, 200, job_approval_request

    async def approve_update(self, db: Session, current_user: ManagerBase, data: dict):
        job_approval_update_data = job_approval_request_helper.validate_update(data)

        job_approval_request = crud.job_approval_request.get(
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
            job_update_in = schema_job_approval_request.JobApprovalRequestUpdate(
                **job_approval_request.__dict__
            )
            jobCRUD.update(db, db_obj=job, obj_in=job_update_in)
        crud.job_approval_request.update(
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
        job_approval_log_helper.create_job_approval_log(
            db,
            job_approval_log,
        )
        return constant.SUCCESS, 200, job_approval_request


job_approval_request_service = JobApprovalRequestService()

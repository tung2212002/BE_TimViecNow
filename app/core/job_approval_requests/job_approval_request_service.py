from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    job_approval_request as schema_job_approval_request,
    job_approval_log as schema_job_approval_log,
)
from app.core.job_approval_log.job_approval_log_helper import job_approval_log_helper
from app.crud.job import job as jobCRUD
from app.hepler.enum import JobStatus, JobApprovalStatus
from app.model import ManagerBase
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse


class JobApprovalRequestService:
    async def get(self, db: Session, data: dict):
        job_approval_request_data = schema_job_approval_request.JobApprovalRequestList(
            **data
        )

        response = crud.job_approval_request.get_multi(
            db,
            **job_approval_request_data.model_dump(),
        )

        return CustomResponse(data=response)

    async def get_by_id(self, db: Session, id: int):
        response = crud.job_approval_request.get(db, id)
        if not response:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Job approval request not found",
            )

        return CustomResponse(data=response)

    async def approve(self, db: Session, current_user: ManagerBase, data: dict):
        job_approval_request_data = (
            schema_job_approval_request.JobApprovalRequestCreate(**data)
        )

        job_approval_request = crud.job_approval_request.get(
            db, job_approval_request_data.job_approval_request_id
        )
        if not job_approval_request:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Job approval request not found",
            )

        job = job_approval_request.job
        if job_approval_request.status == job_approval_request_data.status:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Job already approved"
            )

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

        return CustomResponse(data=job_approval_request)

    async def approve_update(self, db: Session, current_user: ManagerBase, data: dict):
        job_approval_update_data = schema_job_approval_request.JobApprovalRequestUpdate(
            **data
        )

        job_approval_request = crud.job_approval_request.get(
            db, job_approval_update_data.job_approval_request_id
        )
        if not job_approval_request:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Job approval request not found",
            )

        job = job_approval_request.job
        if job_approval_request.status == job_approval_update_data.status:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Job already approved"
            )

        if (
            job_approval_update_data.status == job_approval_request.status
            or job_approval_request.status != JobApprovalStatus.PENDING
        ):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Invalid status"
            )

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

        return CustomResponse(data=job_approval_request)


job_approval_request_service = JobApprovalRequestService()

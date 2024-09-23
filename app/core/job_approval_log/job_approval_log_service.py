# from sqlalchemy.orm import Session

# from app.crud.job_approval_request import (
#     job_approval_request as job_approval_requestCRUD,
# )
# from app.schema import (
#     job_approval_request as schema_job_approval_request,
#     job as job_schema,
# )
# from app.core import constant
# from app.hepler.response_custom import custom_response_error
# from app.core.job import job_helper
# from app.crud.job import job as jobCRUD
# from app.hepler.enum import JobStatus, JobApprovalStatus
# from app.hepler.exception_handler import get_message_validation_error


# def get(db: Session, data: dict):
#     try:
#         job_approval_request_data = schema_job_approval_request.JobApprovalRequestList(
#             **data
#         )
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     job_approval_requests = job_approval_requestCRUD.get_multi(
#         db,
#         **job_approval_request_data.model_dump(),
#     )
#     return constant.SUCCESS, 200, job_approval_requests


# def get_by_id(db: Session, job_approval_request_id: int):
#     job_approval_request = job_approval_requestCRUD.get(db, job_approval_request_id)
#     if not job_approval_request:
#         return constant.ERROR, 404, "Job approval request not found"
#     return constant.SUCCESS, 200, job_approval_request


# def approve(db: Session, data: dict, current_user):
#     try:
#         job_approval_request_data = job_schema.JobApproveRequest(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     job_approval_request = job_approval_requestCRUD.get(
#         db, job_approval_request_data.job_approval_request_id
#     )
#     if not job_approval_request:
#         return constant.ERROR, 404, "Job approval request not found"
#     job = job_approval_request.job
#     if job_approval_request.status == job_approval_request_data.status:
#         return constant.ERROR, 400, "Job already approved"
#     if job_approval_request_data.status == JobApprovalStatus.APPROVED:
#         jobCRUD.update(db, db_obj=job, obj_in={"status": JobStatus.PUBLISHED})
#     job_approval_request = job_approval_requestCRUD.update(
#         db, db_obj=job_approval_request, obj_in=job_approval_request_data.model_dump()
#     )
#     return constant.SUCCESS, 200, job_approval_request

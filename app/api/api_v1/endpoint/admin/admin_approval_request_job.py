from fastapi import APIRouter, Depends, Body, Query, Path

from app.db.base import CurrentSession
from app.core.auth.user_manager_service import user_manager_service
from app.core import constant
from app.core.job_approval_requests.job_approval_request_service import (
    job_approval_request_service,
)
from app.hepler.response_custom import custom_response, custom_response_error
from app.hepler.enum import (
    SortBy,
    OrderType,
    JobApprovalStatus,
    AdminJobApprovalStatus,
)

router = APIRouter()


@router.get("/", summary="Get list of approve request job.")
async def get_list_approve_request_job(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_admin),
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=100),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    status: JobApprovalStatus = Query(
        None,
        description="The status of job approval request.",
        example=JobApprovalStatus.PENDING,
    ),
    company_id: int = Query(None, description="The company id.", example=1),
    business_id: int = Query(None, description="The business id.", example=1),
):
    """
    Get list of approve request job.

    This endpoint allows getting a list of approve request job.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - status (str): The status of job approval request.
    - company_id (int): The company id.
    - business_id (int): The business id.

    Returns:
    - status_code (200): The list of approve request job.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = locals()

    status, status_code, response = await job_approval_request_service.get(db, {**args})

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{job_approval_request_id}", summary="Get approve request job by id.")
async def get_approve_request_job_by_id(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_admin),
    job_approval_request_id: int = Path(..., description="The job id.", example=1),
):
    """
    Get approve request job by id.

    This endpoint allows getting approve request job by id.

    Parameters:
    - job_approval_request_id (int): The job id.

    Returns:
    - status_code (200): The approve request job.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = await job_approval_request_service.get_by_id(
        db, job_approval_request_id, current_user=current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{job_approval_request_id}/approve", summary="Approve job.")
async def approve_job_request_by_id(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_admin),
    job_approval_request_id: int = Path(..., description="The job id.", example=1),
    data: dict = Body(
        ...,
        description="The data to approve job.",
        example={"status": AdminJobApprovalStatus.APPROVED, "reason": ""},
    ),
):
    """
    Approve job.

    This endpoint allows approve job.

    Parameters:
    - job_approval_request_id (int): The job id.
    - data (dict): The data to approve job.

    Returns:
    - status_code (200): The job is approved.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = await job_approval_request_service.approve(
        db,
        current_user=current_user,
        data={"job_approval_request_id": job_approval_request_id, **data},
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{job_approval_request_id}/job", summary="Approve update job.")
async def approve_job_request_by_id(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_admin),
    job_approval_request_id: int = Path(..., description="The job id.", example=1),
    data: dict = Body(
        ...,
        description="The data to approve update job.",
        example={"status": AdminJobApprovalStatus.APPROVED, "reason": ""},
    ),
):
    """
    Approve job.

    This endpoint allows approve update job.

    Parameters:
    - job_approval_request_id (int): The job id.
    - data (dict): The data to approve update job.

    Returns:
    - status_code (200): The job is approved.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = await job_approval_request_service.approve_update(
        db,
        current_user=current_user,
        data={"job_approval_request_id": job_approval_request_id, **data},
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

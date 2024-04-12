from fastapi import APIRouter, Depends, Query, Request, Path, Body
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.hepler.response_custom import custom_response, custom_response_error
from app.core import constant
from app.core.position import service_position
from app.core.auth.service_business_auth import get_current_user, get_current_admin


router = APIRouter()


@router.get("/group_position", summary="Get list of group positions.")
def get_list_group_position(
    request: Request,
    skip: int = Query(
        0, description="The number of group positions to skip.", example=0
    ),
    limit: int = Query(
        100, description="The number of group positions to return.", example=100
    ),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
):
    """
    Get list of group positions.

    This endpoint allows getting a list of group positions.

    Parameters:
    - skip (int): The number of group positions to skip.
    - limit (int): The number of group positions to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of group positions has been found successfully.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_position.get_list_group_position(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/group_position/{group_position_id}", summary="Get group position by id.")
def get_group_position_by_id(
    group_position_id: int = Path(..., description="The group position id."),
    db: Session = Depends(get_db),
):
    """
    Get group position by id.

    This endpoint allows getting a group position by id.

    Parameters:
    - group_position_id (int): The group position id.

    Returns:
    - status_code (200): The group position has been found successfully.
    - status_code (404): The group position is not found.

    """
    status, status_code, response = service_position.get_group_position_by_id(
        db, group_position_id
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/group_position", summary="Create a new group position.")
def create_group_position(
    data: dict = Body(
        ...,
        description="The group position data.",
        example={"name": "Group Position 1", "slug": "group-position-1"},
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Create a new group position by admin.

    This endpoint allows create a new group position by admin.

    Parameters:
    - name (str): The name of the group position.
    - slug (str): The slug of the group position.

    Returns:
    - status_code (201): The group position has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The group position is already created.

    """

    status, status_code, response = service_position.create_group_position(db, data)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/job_position", summary="Get list of job positions.")
def get_list_job_position(
    request: Request,
    skip: int = Query(0, description="The number of job positions to skip.", example=0),
    limit: int = Query(
        100, description="The number of job positions to return.", example=100
    ),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
):
    """
    Get list of job positions.

    This endpoint allows getting a list of job positions.

    Parameters:
    - skip (int): The number of job positions to skip.
    - limit (int): The number of job positions to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of job positions has been found successfully.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_position.get_list_job_position(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/job_position/{job_position_id}", summary="Get job position by id.")
def get_job_position_by_id(
    job_position_id: int = Path(..., description="The job position id."),
    db: Session = Depends(get_db),
):
    """
    Get job position by id.

    This endpoint allows getting a job position by id.

    Parameters:
    - job_position_id (int): The job position id.

    Returns:
    - status_code (200): The job position has been found successfully.
    - status_code (404): The job position is not found.

    """
    status, status_code, response = service_position.get_job_position_by_id(
        db, job_position_id
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/job_position", summary="Create a new job position.")
def create_job_position(
    data: dict = Body(
        ...,
        description="The job position data.",
        example={
            "name": "Job Position 1",
            "slug": "job-position-1",
            "group_position_id": 1,
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Create a new job position.

    This endpoint allows create a new job position.

    Parameters:
    - name (str): The name of the job position.
    - slug (str): The slug of the job position.
    - group_position_id (int): The group position id of the job position.

    Returns:
    - status_code (201): The job position has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The job position is already created.

    """

    status, status_code, response = service_position.create_job_position(db, data)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

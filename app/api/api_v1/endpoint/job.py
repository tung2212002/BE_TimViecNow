from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    File,
    UploadFile,
    Form,
    Body,
    Query,
    Path,
)
from sqlalchemy.orm import Session
from typing import Annotated, Any, List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime, date

from app.db.base import get_db
from app.core.auth.service_user_auth import get_current_user
from app.core import constant
from app.core.job import service_job
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("/search", summary="Search list of job.")
def search_job(
    request: Request,
    skip: int = Query(0, description="The number of users to skip.", example=0),
    limit: int = Query(100, description="The number of users to return.", example=100),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("desc", description="The order to sort by.", example="desc"),
    company_id: int = Query(None, description="The company id.", example=1),
    province_id: int = Query(None, description="The province id.", example=1),
    district_id: int = Query(None, description="The district id.", example=1),
    category_id: int = Query(None, description="The category id.", example=1),
    field_id: int = Query(None, description="The field id.", example=1),
    employment_type: str = Query(
        None, description="The employment type.", example="full_time"
    ),
    job_experience_id: int = Query(None, description="The experience id.", example=1),
    min_salary: int = Query(None, description="The min salary.", example=1000000),
    max_salary: int = Query(None, description="The max salary.", example=10000000),
    salary_type: str = Query(None, description="The type salary.", example="vnd"),
    job_position_id: int = Query(None, description="The position id.", example=1),
    keyword: str = Query(None, description="The keyword.", example="developer"),
    db: Session = Depends(get_db),
):
    """
    Get list of job by user.

    This endpoint allows getting a list of job by user.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - company_id (int): The company id.
    - province_id (int): The province id.
    - district_id (int): The district id.
    - category_id (int): The category id.
    - field_id (int): The field id.
    - employment_type (str): The employment type.
    - job_experience_id (int): The experience id.
    - job_position_id (int): The position id.
    - min_salary (int): The min salary.
    - max_salary (int): The max salary.
    - salary_type (str): The type salary.
    - keyword (str): The keyword.

    Returns:
    - status_code (200): The list of job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_job.search_job_by_user(db, {**args})

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("", summary="Get list of job.")
def get_job(
    request: Request,
    skip: int = Query(0, description="The number of users to skip.", example=0),
    limit: int = Query(100, description="The number of users to return.", example=100),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("desc", description="The order to sort by.", example="desc"),
    company_id: int = Query(None, description="The company id.", example=1),
    province_id: int = Query(None, description="The province id.", example=1),
    db: Session = Depends(get_db),
):
    """
    Get list of job by user.

    This endpoint allows getting a list of job by user.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - company_id (int): The company id.
    - province_id (int): The province id.

    Returns:
    - status_code (200): The list of job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_job.get_list_job_by_user(db, {**args})

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{job_id}", summary="Get job by id.")
def get_job_by_id(
    job_id: int = Path(
        ...,
        description="The job id.",
        example=1,
    ),
    db: Session = Depends(get_db),
):
    """
    Get job by id.

    This endpoint allows getting a job by id.

    Parameters:
    - job_id (int): The job id.

    Returns:
    - status_code (200): The job has been found successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.get_job_by_id_for_user(db, job_id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
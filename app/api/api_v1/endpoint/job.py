from fastapi import APIRouter, Depends, Query, Path

from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core import constant
from app.core.job import service_job
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType, SortJobBy, JobType, SalaryType

router = APIRouter()


@router.get("/search", summary="Search list of job.")
def search_job(
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=100),
    sort_by: SortJobBy = Query(
        None, description="The field to sort by.", example=SortJobBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    company_id: int = Query(None, description="The company id.", example=1),
    province_id: int = Query(None, description="The province id.", example=1),
    district_id: int = Query(None, description="The district id.", example=1),
    category_id: int = Query(None, description="The category id.", example=1),
    field_id: int = Query(None, description="The field id.", example=1),
    employment_type: JobType = Query(
        None, description="The employment type.", example=JobType.FULL_TIME
    ),
    job_experience_id: int = Query(None, description="The experience id.", example=1),
    min_salary: int = Query(None, description="The min salary.", example=1000000),
    max_salary: int = Query(None, description="The max salary.", example=10000000),
    salary_type: SalaryType = Query(
        None, description="The type salary.", example=SalaryType.VND
    ),
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
    args = locals()

    status, status_code, response = service_job.search_by_user(db, {**args})

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("", summary="Get list of job.")
def get_job(
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=100),
    sort_by: SortJobBy = Query(
        None, description="The field to sort by.", example=SortJobBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
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
    args = locals()

    status, status_code, response = service_job.get_by_user(db, {**args})

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/count_job_by_category", summary="Count job by category.")
def count_job_by_category(
    db: Session = Depends(get_db),
):
    """
    Count job by category.

    This endpoint allows counting job by category.

    Returns:
    - status_code (200): The job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.count_job_by_category(db)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/count_job_by_salary", summary="Count job by salary.")
def count_job_by_salary(
    db: Session = Depends(get_db),
):
    """
    Count job by salary.

    This endpoint allows counting job by salary.

    Returns:
    - status_code (200): The job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.count_job_by_salary(db)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/cruitment_demand", summary="Get information of recruitment demand.")
def get_cruitment_demand(
    db: Session = Depends(get_db),
):
    """
    Get information of recruitment demand.

    This endpoint allows getting information of recruitment demand.

    Returns:
    - status_code (200): The recruitment demand has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The recruitment demand is not found.

    """
    status, status_code, response = service_job.get_cruitment_demand(db)

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
    status, status_code, response = service_job.get_by_id_for_user(db, job_id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

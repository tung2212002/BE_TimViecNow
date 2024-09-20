from fastapi import APIRouter, Depends, Query, Path
from redis.asyncio import Redis
from datetime import date

from app.db.base import CurrentSession
from app.storage.redis import get_redis
from app.core import constant
from app.core.job.job_service import job_service
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType, SortJobBy, JobType, SalaryType

router = APIRouter()


@router.get("/search", summary="Search list of job.")
async def search_job(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
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
    updated_at: date = Query(None, description="The updated at.", example=date.today()),
    suggest: bool = Query(False, description="The suggest job.", example=False),
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
    - updated_at (date): The updated at.

    Returns:
    - status_code (200): The list of job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = locals()

    status, status_code, response = await job_service.search_by_user(
        db, redis, {**args}
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("", summary="Get list of job.")
async def get_job(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
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

    status, status_code, response = await job_service.get_by_user(db, redis, {**args})

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/count_job_by_category", summary="Count job by category.")
async def count_job_by_category(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
):
    """
    Count job by category.

    This endpoint allows counting job by category.

    Returns:
    - status_code (200): The job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The job is not found.

    """
    status, status_code, response = await job_service.count_job_by_category(db, redis)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/count_job_by_salary", summary="Count job by salary.")
async def count_job_by_salary(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
):
    """
    Count job by salary.

    This endpoint allows counting job by salary.

    Returns:
    - status_code (200): The job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The job is not found.

    """
    status, status_code, response = await job_service.count_job_by_salary(db, redis)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/cruitment_demand", summary="Get information of recruitment demand.")
async def get_cruitment_demand(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
):
    """
    Get information of recruitment demand.

    This endpoint allows getting information of recruitment demand.

    Returns:
    - status_code (200): The recruitment demand has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The recruitment demand is not found.

    """
    status, status_code, response = await job_service.get_cruitment_demand(db, redis)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{job_id}", summary="Get job by id.")
async def get_job_by_id(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
    job_id: int = Path(
        ...,
        description="The job id.",
        example=1,
    ),
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
    status, status_code, response = await job_service.get_by_id_for_user(
        db, redis, job_id
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

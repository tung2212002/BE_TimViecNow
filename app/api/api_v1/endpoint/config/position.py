from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.storage.redis import get_redis
from app.db.base import get_db
from app.core.auth.user_manager_service import user_manager_service
from app.core.job_position.position_service import job_position_service
from app.hepler.enum import OrderType

router = APIRouter()


@router.get("/job_position", summary="Get list of job positions.")
async def get_list_job_position(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    skip: int = Query(
        None, description="The number of job positions to skip.", example=0
    ),
    limit: int = Query(
        None, description="The number of job positions to return.", example=100
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
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
    args = locals()

    return await job_position_service.get_position(db, redis, args)


@router.get("/job_position/{id}", summary="Get job position by id.")
async def get_job_position_by_id(
    db: Session = Depends(get_db),
    id: int = Path(..., description="The job position id.", example=1),
):
    """
    Get job position by id.

    This endpoint allows getting a job position by id.

    Parameters:
    - id (int): The job position id.

    Returns:
    - status_code (200): The job position has been found successfully.
    - status_code (404): The job position is not found.

    """
    return await job_position_service.get_position_by_id(db, id)


@router.post("/job_position", summary="Create a new job position.")
async def create_job_position(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    data: dict = Body(
        ...,
        description="The job position data.",
        example={
            "name": "Vị trí nghề nghiệp",
            "slug": "vi-tri-nghe-nghiep",
            "id": 0,
        },
    ),
):
    """
    Create a new job position.

    This endpoint allows create a new job position.

    Parameters:
    - name (str): The name of the job position.
    - slug (str): The slug of the job position.
    - id (int): The group position id of the job position.

    Returns:
    - status_code (201): The job position has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The job position is already created.

    """
    return await job_position_service.create_position(db, data)


@router.put("/job_position/{id}", summary="Update job position by id.")
async def update_job_position_by_id(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    id: int = Path(..., description="The job position id.", example=1),
    data: dict = Body(
        ...,
        description="The job position data.",
        example={
            "name": "Vị trí nghề nghiệp",
            "slug": "vi-tri-nghe-nghiep",
            "id": 0,
        },
    ),
):
    """
    Update job position by id.

    This endpoint allows updating job position by id.

    Parameters:
    - id (int): The job position id.
    - name (str): The name of the job position.
    - slug (str): The slug of the job position.
    - id (int): The group position id of the job position.

    Returns:
    - status_code (200): The job position has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The job position is not found.

    """
    return await job_position_service.update_position(db, id, data)


@router.delete("/job_position/{id}", summary="Delete job position by id.")
async def delete_job_position_by_id(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    id: int = Path(..., description="The job position id.", example=1),
):
    """
    Delete job position by id.

    This endpoint allows deleting job position by id.

    Parameters:
    - id (int): The job position id.

    Returns:
    - status_code (200): The job position has been deleted successfully.
    - status_code (404): The job position is not found.

    """
    return await job_position_service.delete_position(db, id)

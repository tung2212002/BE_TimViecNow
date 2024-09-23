from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.storage.redis import get_redis
from app.db.base import get_db
from app.core.job_position.position_service import job_position_service
from app.core.auth.user_manager_service import user_manager_service
from app.hepler.enum import OrderType

router = APIRouter()


@router.get("/group_position", summary="Get list of group positions.")
async def get_list_group_position(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    skip: int = Query(
        None, description="The number of group positions to skip.", example=0
    ),
    limit: int = Query(
        None, description="The number of group positions to return.", example=100
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
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
    args = locals()

    return await job_position_service.get_group(db, redis, args)


@router.get("/group_position/{id}", summary="Get group position by id.")
async def get_group_position_by_id(
    db: Session = Depends(get_db),
    id: int = Path(..., description="The group position id.", example=1),
):
    """
    Get group position by id.

    This endpoint allows getting a group position by id.

    Parameters:
    - id (int): The group position id.

    Returns:
    - status_code (200): The group position has been found successfully.
    - status_code (404): The group position is not found.

    """
    return await job_position_service.get_group_by_id(db, id)


@router.post("/group_position", summary="Create a new group position.")
async def create_group_position(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    data: dict = Body(
        ...,
        description="The group position data.",
        example={"name": "Group Position 1", "slug": "group-position-1"},
    ),
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
    return await job_position_service.create_group(db, data)


@router.put("/group_position/{id}", summary="Update group position by id.")
async def update_group_position_by_id(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    id: int = Path(..., description="The group position id.", example=1),
    data: dict = Body(
        ...,
        description="The group position data.",
        example={"name": "Group Position 1", "slug": "group-position-1"},
    ),
):
    """
    Update group position by id.

    This endpoint allows updating group position by id.

    Parameters:
    - id (int): The group position id.
    - name (str): The name of the group position.
    - slug (str): The slug of the group position.

    Returns:
    - status_code (200): The group position has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The group position is not found.

    """
    return await job_position_service.update_group(db, id, data)


@router.delete("/group_position/{id}", summary="Delete group position by id.")
async def delete_group_position_by_id(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    id: int = Path(..., description="The group position id.", example=1),
):
    """
    Delete group position by id.

    This endpoint allows deleting group position by id.

    Parameters:
    - id (int): The group position id.

    Returns:
    - status_code (200): The group position has been deleted successfully.
    - status_code (404): The group position is not found.

    """
    return await job_position_service.delete_group(db, id)

from fastapi import APIRouter, Depends, Query, Path
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.location.location_service import location_service
from app.hepler.enum import OrderType
from app.storage.redis import get_redis

router = APIRouter()


@router.get("/province", summary="Get list of provinces.")
async def get_list_province(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    skip: int = Query(None, description="The number of province to skip.", example=0),
    limit: int = Query(
        None, description="The number of province to return.", example=100
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
):
    """
    Get list of provinces.

    This endpoint allows getting a list of provinces.

    Parameters:
    - skip (int): The number of provinces to skip.
    - limit (int): The number of provinces to return.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of provinces has been found successfully.

    """
    args = locals()

    return await location_service.get_province(db, redis, args)


@router.get("/province/{id}", summary="Get province by id.")
async def get_province_by_id(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    id: int = Path(..., description="The province id.", example=1),
):
    """
    Get province by id.

    This endpoint allows getting a province by id.

    Parameters:
    - id (int): The province id.

    Returns:
    - status_code (200): The province has been found successfully.
    - status_code (404): The province is not found.

    """
    return await location_service.get_province_by_id(db, redis, id)


@router.get("/district", summary="Get list of districts.")
async def get_list_district(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    province_id: int = Query(..., description="The province id.", example=1),
    skip: int = Query(None, description="The number of districts to skip.", example=0),
    limit: int = Query(
        None, description="The number of districts to return.", example=10
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
):
    """
    Get list of districts.

    This endpoint allows getting a list of districts.

    Parameters:
    - province_id (int): The province id.
    - skip (int): The number of districts to skip.
    - limit (int): The number of districts to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of districts has been found successfully.

    """
    args = locals()

    return await location_service.get_district(db, redis, args)


@router.get("/district/{id}", summary="Get district by id.")
async def get_district_by_id(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    id: int = Path(..., description="The district id.", example=1),
):
    """
    Get district by id.

    This endpoint allows getting a district by id.

    Parameters:
    - id (int): The district id.

    Returns:
    - status_code (200): The district has been found successfully.
    - status_code (404): The district is not found.

    """
    return await location_service.get_district_by_id(db, redis, id)

from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core import constant
from app.core.location import service_location
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType

router = APIRouter()


@router.get("/province", summary="Get list of provinces.")
def get_list_province(
    skip: int = Query(None, description="The number of province to skip.", example=0),
    limit: int = Query(
        None, description="The number of province to return.", example=100
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
    db: Session = Depends(get_db),
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

    status, status_code, response = service_location.get_province(db, args)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/province/{id}", summary="Get province by id.")
def get_province_by_id(
    id: int = Path(..., description="The province id.", example=1),
    db: Session = Depends(get_db),
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
    status, status_code, response = service_location.get_province_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/district", summary="Get list of districts.")
def get_list_district(
    province_id: int = Query(..., description="The province id.", example=1),
    skip: int = Query(None, description="The number of districts to skip.", example=0),
    limit: int = Query(
        None, description="The number of districts to return.", example=10
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
    db: Session = Depends(get_db),
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

    status, status_code, response = service_location.get_district(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/district/{id}", summary="Get district by id.")
def get_district_by_id(
    id: int = Path(..., description="The district id.", example=1),
    db: Session = Depends(get_db),
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
    status, status_code, response = service_location.get_district_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

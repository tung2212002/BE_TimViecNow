from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.hepler.response_custom import custom_response_error, custom_response
from app.core import constant
from app.core.location import service_location

router = APIRouter()


@router.get("/province", summary="Get list of provinces.")
def get_list_province(
    request: Request,
    skip: int = Query(0, description="The number of province to skip.", example=0),
    limit: int = Query(
        100, description="The number of province to return.", example=100
    ),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
):
    """
    Get list of provinces.

    This endpoint allows getting a list of provinces.

    Parameters:
    - skip (int): The number of provinces to skip.
    - limit (int): The number of provinces to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of provinces has been found successfully.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_location.get_list_province(db, args)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/province/{province_id}", summary="Get province by id.")
def get_province_by_id(
    province_id: int = Path(..., description="The province id."),
    db: Session = Depends(get_db),
):
    """
    Get province by id.

    This endpoint allows getting a province by id.

    Parameters:
    - province_id (int): The province id.

    Returns:
    - status_code (200): The province has been found successfully.
    - status_code (404): The province is not found.

    """
    status, status_code, response = service_location.get_province_by_id(db, province_id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/district", summary="Get list of districts.")
def get_list_district(
    request: Request,
    province_id: int = Query(..., description="The province id."),
    skip: int = Query(0, description="The number of districts to skip.", example=0),
    limit: int = Query(
        100, description="The number of districts to return.", example=10
    ),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
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
    params = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_location.get_list_district(db, params)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/district/{district_id}", summary="Get district by id.")
def get_district_by_id(
    district_id: int = Path(..., description="The district id."),
    db: Session = Depends(get_db),
):
    """
    Get district by id.

    This endpoint allows getting a district by id.

    Parameters:
    - district_id (int): The district id.

    Returns:
    - status_code (200): The district has been found successfully.
    - status_code (404): The district is not found.

    """
    status, status_code, response = service_location.get_district_by_id(db, district_id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

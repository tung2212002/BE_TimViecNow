from fastapi import (
    APIRouter,
    Query,
    Path,
)
from typing import List


from app.db.base import CurrentSession
from app.core import constant
from app.core.company.company_service import company_service
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType, SortBy

router = APIRouter()


@router.get("", summary="Get list of companies.")
async def get_companies(
    db: CurrentSession,
    skip: int = Query(None, description="The number of companies to skip.", example=0),
    limit: int = Query(
        None, description="The number of companies to return.", example=10
    ),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    fields: List[int] = Query(
        None, description="The fields of the company.", example=list([1])
    ),
):
    """
    Get list of companies.

    This endpoint allows getting a list of companies.

    Parameters:
    - skip (int): The number of companies to skip.
    - limit (int): The number of companies to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of companies has been found successfully.
    - status_code (404): The list of companies is not found.
    - status_code (400): The request is invalid.

    """
    args = locals()

    status, status_code, response = await company_service.get(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/search", summary="Search list of company.")
async def get_company(
    db: CurrentSession,
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: str = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    keyword: str = Query(None, description="The keyword.", example="cong ty"),
    fields: list[int] = Query(
        None, description="The list of field id.", example=list([int(2)])
    ),
):
    """
    Get list of company.

    This endpoint allows getting a list of company.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - keyword (str): The keyword.
    - fields (list[int]): The list of field id.

    Returns:
    - status_code (200): The list of company has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The list of company is not found.

    """
    args = locals()
    status_message, status_code, response = company_service.search(db, args)

    if status_message == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status_message == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get a company by id.")
async def get_company_by_id(
    db: CurrentSession,
    id: int = Path(..., description="The id of the company.", example=1),
):
    """
    Get a company by id.

    This endpoint allows getting a company by id.

    Parameters:
    - id (int): The id of the company.

    Returns:
    - status_code (200): The company has been found successfully.
    - status_code (404): The company is not found.
    - status_code (400): The request is invalid.

    """
    status, status_code, response = await company_service.get_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

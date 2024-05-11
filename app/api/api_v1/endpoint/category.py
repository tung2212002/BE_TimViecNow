from fastapi import APIRouter, Depends, Request, Query, Path, Body
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType
from app.core import constant
from app.core.category import service_category
from app.core.auth.service_business_auth import get_current_superuser

router = APIRouter()


@router.get("", summary="Get list of categories.")
def get_list_category(
    request: Request,
    skip: int = Query(None, description="The number of category to skip.", example=0),
    limit: int = Query(
        None, description="The number of category to return.", example=100
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of categories.

    This endpoint allows getting a list of categories.

    Parameters:
    - skip (int): The number of categories to skip.
    - limit (int): The number of categories to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Return:
    - status_code (200): The list of categories has been found successfully.

    """
    args = locals()

    status, status_code, response = service_category.get(db, args)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get category by id.")
def get_category_by_id(
    id: int = Path(..., description="The category id."),
    db: Session = Depends(get_db),
):
    """
    Get category by id.

    This endpoint allows getting a category by id.

    Parameters:
    - id (int): The category id.

    Return:
    - status_code (200): The category has been found successfully.
    - status_code (404): The category is not found.

    """
    status, status_code, response = service_category.get_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a category.")
def create_category(
    data: dict = Body(
        ...,
        example={
            "name": "",
            "slug": "",
            "description": "",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Create a category.

    This endpoint allows creating a new category.

    Parameters:
    - name (str): The name of the category.
    - slug (str): The slug of the category.
    - description (str): The description of the category.

    Return:
    - status_code (201): The category has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The category is already created.

    """
    data = locals()

    status, status_code, response = service_category.create(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a category by id.")
def update_category_by_id(
    id: int = Path(..., description="The category id."),
    data: dict = Body(
        ...,
        example={
            "name": "",
            "slug": "",
            "description": "",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Update a category by id.

    This endpoint allows updating a category by id.

    Parameters:
    - id (int): The category id.
    - name (str): The name of the category.
    - slug (str): The slug of the category.
    - description (str): The description of the category.

    Return:
    - status_code (200): The category has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The category is not found.

    """
    data = locals()

    status, status_code, response = service_category.update(db, id, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a category by id.")
def delete_category_by_id(
    id: int = Path(..., description="The category id."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Delete a category by id.

    This endpoint allows deleting a category by id.

    Parameters:
    - id (int): The category id.

    Return:
    - status_code (200): The category has been deleted successfully.
    - status_code (404): The category is not found.

    """
    status, status_code, response = service_category.delete(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

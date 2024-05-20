from fastapi import (
    APIRouter,
    Depends,
    Request,
    File,
    UploadFile,
    Form,
    Query,
    Path,
)
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.auth.service_user_auth import get_current_user
from app.core.auth.service_business_auth import get_current_admin
from app.core import constant
from app.core.user import service_user
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType, SortBy

router = APIRouter()


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Get the current user.

    This endpoint allows getting the current user.

    Returns:
    - status_code (200): The current user has been found successfully.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_user.get_me(current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("", summary="Get list of users.")
def get_user(
    request: Request,
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Get list of users by admin.

    This endpoint allows getting a list of users by admin.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of users has been found successfully.
    - status_code (404): The list of users is not found.
    - status_code (401): The user is not authorized.
    - status_code (400): The request is invalid.

    """
    args = locals()

    status, status_code, response = service_user.get(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get a user by id.")
def get_user_by_id(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Get a user by id by admin.

    This endpoint allows getting a user by id by admin.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been found successfully.
    - status_code (404): The user is not found.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_user.get_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Register a new user by admin.")
def create_user(
    full_name: str = Form(
        ...,
        description="The full name of the user.",
        json_schema_extra={"example": "Tung Ong"},
    ),
    email: str = Form(
        ...,
        description="The email of the user.",
        json_schema_extra={"example": "ongtung@gmail.com"},
    ),
    password: str = Form(
        ...,
        description="The password of the user.",
        json_schema_extra={"example": "@Password1234"},
    ),
    confirm_password: str = Form(
        ...,
        description="The confirm password of the user.",
        json_schema_extra={"example": "@Password1234"},
    ),
    avatar: UploadFile = File(None, description="The profile avatar of the user."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Create a new user by admin.

    This endpoint allows creating a new user by admin with the provided information.

    Parameters:
    - full_name (str): The full name of the user.
    - email (str): The email address of the user.
    - password (str): The password of the user.
    - confirm_password (str): The confirm password of the user.
    - avatar (UploadFile): The profile avatar of the user.
    - role (str): The role of the user.

    Returns:
    - status_code (201): The user has been created successfully.
    - status_code (401): The user is not authorized.
    - status_code (400): The request is invalid.
    - status_code (409): The user is already registered.

    """
    data = locals()

    status, status_code, response = service_user.create(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a user.")
def update_user(
    id: int = Path(..., description="The id of the user."),
    full_name: str = Form(
        None,
        description="The full name of the user.",
        json_schema_extra={"example": "Tung Ong"},
    ),
    phone_number: str = Form(
        None,
        description="The phone number of the user.",
        json_schema_extra={"example": "0323456789"},
    ),
    avatar: UploadFile = File(
        None,
        description="The profile avatar of the user.",
        json_schema_extra={"example": "avatar.jpg"},
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update a user.

    This endpoint allows updating a user with the provided information,

    Parameters:
    - id (int): The id of the user.
    - full_name (str): The full name of the user.
    - email (str): The email address of the user.
    - phone_number (str): The phone number of the user.
    - avatar (UploadFile): The profile avatar of the user.

    Returns:
    - status_code (200): The user has been updated successfully.
    - status_code (401): User is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The user is not found.

    """
    data = locals()

    status, status_code, response = service_user.update(db, id, data, current_user)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a user.")
def delete_user(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a user.

    This endpoint allows deleting a user by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been deleted successfully.
    - status_code (401): User is not authorized.
    - status_code (404): The user is not found.

    """
    status, status_code, response = service_user.delete(db, id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

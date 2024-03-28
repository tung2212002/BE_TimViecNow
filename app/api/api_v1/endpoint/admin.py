from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    File,
    UploadFile,
    Form,
    Body,
    Query,
    Path,
)
from sqlalchemy.orm import Session
from typing import Annotated, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.core.auth.service_business_auth import (
    get_current_superuser,
    get_current_admin,
)
from app.core import constant
from app.core.admin import service_admin
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("", summary="Get list of admin by superuser.")
def get(
    request: Request,
    skip: int = Query(description="The number of users to skip.", example=0),
    limit: int = Query(description="The number of users to return.", example=10),
    sort_by: str = Query(description="The field to sort by.", example="id"),
    order_by: str = Query(description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Get list of admin by superuser.

    This endpoint allows getting a list of admin by superuser.

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
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_admin.get_list_admin(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get a admin by id.")
def get_by_id(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Get a admin by id.

    This endpoint allows getting a admin by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been found successfully.
    - status_code (404): The user is not found.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_admin.get_admin_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Register a new admin by superuser.")
def create_admin(
    full_name: Annotated[str, Form(..., description="The full name of the admin.")],
    email: Annotated[str, Form(..., description="The email of the admin.")],
    password: Annotated[str, Form(..., description="The password of the admin.")],
    confirm_password: Annotated[
        str, Form(..., description="The confirm password of the admin.")
    ],
    phone_number: Annotated[
        str, Form(..., description="The phone number of the admin.")
    ],
    gender: str = Form(None, description="Gender of the admin."),
    avatar: UploadFile = File(None, description="The profile avatar of the admin."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Register a new user by admin.

    This endpoint allows create a new user by admin.

    Parameters:
    - full_name (str): The full name of the user.
    - email (str): The email of the user.
    - password (str): The password of the user.
    - confirm_password (str): The confirm password of the user.
    - avatar (UploadFile): The profile avatar of the user.
    - province_id (int): The province id of the user.
    - phone_number (str): The phone number of the user.
    - gender (str): The gender of the user.

    Returns:
    - status_code (201): The admin has been registered successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The admin is already registered.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}
    status, status_code, response = service_admin.create_admin(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a admin.")
def update_admin(
    id: int = Path(..., description="The id of the user.", example=1),
    full_name: str = Form(None, description="The full name of the user."),
    phone_number: str = Form(None, description="The phone number of the user."),
    avatar: UploadFile = File(None, description="The profile avatar of the user."),
    gender: str = Form(None, description="Gender of the user."),
    password: str = Form(None, description="The password of the user."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Update a admin.

    This endpoint allows updating a admin with the provided information,

    Parameters:
    - id (int): The id of the user.
    - full_name (str): The full name of the user.
    - email (str): The email address of the user.
    - phone_number (str): The phone number of the user.
    - avatar (UploadFile): The profile avatar of the user.
    - password (str): The password of the user.

    Returns:
    - status_code (200): The user has been updated successfully.
    - status_code (401): User is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The user is not found.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_admin.update_admin(db, data, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a admin.")
def delete_admin(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Delete a admin.

    This endpoint allows deleting a admin by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been deleted successfully.
    - status_code (401): User is not authorized.
    - status_code (404): The user is not found.

    """

    status, status_code, response = service_admin.delete_admin(db, id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

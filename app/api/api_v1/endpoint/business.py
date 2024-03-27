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
from app.core.auth.service_business_auth import get_current_user, get_current_superuser
from app.core import constant
from app.core.representative import service_representative
from app.schema import user as schema_user, page as schema_page
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Get the current representative.

    This endpoint allows getting the current representative.

    Returns:
    - status_code (200): The current user has been found successfully.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_representative.get_me(current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("")
def get_user(
    request: Request,
    skip: int = Query(description="The number of users to skip.", example=0),
    limit: int = Query(description="The number of users to return.", example=10),
    sort_by: str = Query(description="The field to sort by.", example="id"),
    order_by: str = Query(description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of users.

    This endpoint allows getting a list of representative.

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

    status, status_code, response = service_representative.get_list_user(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}")
def get_user_by_id(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get a representative by id.

    This endpoint allows getting a representative by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been found successfully.
    - status_code (404): The user is not found.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_representative.get_user_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("")
def create_user(
    full_name: str = Form(
        ..., description="The full name of the user.", example="John Doe"
    ),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Create a new user by superuser.

    This endpoint allows creating a new user by superuser with the provided information.

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
    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_representative.create_user(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}")
def update_user(
    id: int = Path(..., description="The id of the user.", example=1),
    full_name: str = Form(
        None, description="The full name of the user.", example="John Doe"
    ),
    email: str = Form(None, description="The email address of the user."),
    phone_number: str = Form(None, description="The phone number of the user."),
    avatar: UploadFile = File(None, description="The profile avatar of the user."),
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

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_representative.update_user(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}")
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

    status, status_code, response = service_representative.delete_user(
        db, id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

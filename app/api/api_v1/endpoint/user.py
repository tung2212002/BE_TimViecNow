from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    File,
    UploadFile,
    Form,
    Body,
)
from sqlalchemy.orm import Session
from typing import Annotated, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.core.auth.service_auth import get_current_user, get_current_superuser
from app.core import constant
from app.core.user import service_user
from app.schema import user as schema_user, page as schema_page
from app.hepler.response_custom import custom_response_error, custom_response

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


@router.post("/get")
def get_user(
    data: dict = Body(
        ..., example={"skip": 0, "limit": 10, "sort_by": "id", "order_by": "desc"}
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of users.

    This endpoint allows getting a list of users.

    Parameters:
    - skip (int): The number of items to skip.
    - limit (int): The number of items to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of users has been found successfully.
    - status_code (404): The list of users is not found.
    - status_code (401): The user is not authorized.
    - status_code (400): The request is invalid.

    """
    status, status_code, response = service_user.get_list_user(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/create")
def create_user(
    full_name: str = Form(
        ...,
    ),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    picture: UploadFile = File(None),
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
    - picture (UploadFile): The profile avatar of the user.
    - role (str): The role of the user.

    Returns:
    - status_code (201): The user has been created successfully.
    - status_code (401): The user is not authorized.
    - status_code (400): The request is invalid.
    - status_code (409): The user is already registered.

    """
    data = {
        "full_name": full_name,
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "picture": picture,
    }
    status, status_code, response = service_user.create_user(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

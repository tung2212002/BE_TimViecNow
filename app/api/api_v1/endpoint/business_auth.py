from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    File,
    UploadFile,
    Form,
    Body,
    Request,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import Field

from app.db.base import get_db
from app.core.auth import service_business_auth
from app.core import constant
from app.core.business import service_business
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.post("/register", summary="Register a new business.")
def register_business(
    full_name: Annotated[str, Form(..., description="The full name of the business.")],
    email: Annotated[str, Form(..., description="The email of the business.")],
    password: Annotated[str, Form(..., description="The password of the business.")],
    confirm_password: Annotated[
        str, Form(..., description="The confirm password of the business.")
    ],
    province_id: Annotated[
        int, Form(..., description="The province id of the business.")
    ],
    phone_number: Annotated[
        str, Form(..., description="The phone number of the business.")
    ],
    gender: Annotated[str, Form(..., description="Gender of the business.")],
    company_name: Annotated[str, Form(..., description="The company of the business.")],
    work_position: Annotated[
        str, Form(..., description="The work position of the business.")
    ],
    work_location: str = Form(None, description="The work location of the business."),
    avatar: UploadFile = File(None, description="The profile avatar of the business."),
    district_id: int = Form(None, description="The district id of the business."),
    db: Session = Depends(get_db),
):
    """
    Register a new business.

    This endpoint allows create a new business.

    Parameters:
    - full_name (str): The full name of the business.
    - email (str): The email of the business.
    - password (str): The password of the business.
    - confirm_password (str): The confirm password of the business.
    - avatar (UploadFile): The profile avatar of the business.
    - province_id (int): The province id of the business.
    - district_id (int): The district id of the business.
    - phone_number (str): The phone number of the business.
    - gender (str): The gender of the business.
    - company (str): The company of the business.
    - work_position (str): The work position of the business.
    - work_location (str): The work location of the business.

    Returns:
    - status_code (201): The business has been registered successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The business is already registered.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}
    status, status_code, response = service_business.create_business(db, data)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/login", summary="Login business.")
def login_auth(
    data: dict = Body(
        ..., example={"email": "1@email.com", "password": "@Password1234"}
    ),
    db: Session = Depends(get_db),
):
    """
    Login business.

    This endpoint allows logging in a business.

    Parameters:
    - email (str): The email of the business.
    - password (str): The password of the business.

    Returns:
    - status_code (200): The business has been logged in successfully.
    - status_code (400): The request is invalid.
    - status_code (401): The password is incorrect.
    - status_code (404): The business is not found.

    """
    status, status_code, response = service_business_auth.authenticate(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/refresh_token", summary="Refresh token.")
def refresh_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_business_auth.get_current_user),
):
    """
    Refresh token.

    This endpoint allows refreshing the token.

    Returns:
    - status_code (200): The token has been refreshed successfully.
    - status_code (401): Token revoked or expired.
    - status_code (404): The business is not found.

    """
    status, status_code, response = service_business_auth.refresh_token(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/logout", summary="Logout business.")
def logout_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_business_auth.get_current_user),
):
    """
    Logout business.

    This endpoint allows logging out a business.

    Returns:
    - status_code (200): The business has been logged out successfully.
    - status_code (401): The business is not authorized.
    - status_code (404): The business is not found.

    """

    status, status_code, response = service_business_auth.logout(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/verify_token", summary="Verify token.")
def verify_token_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_business_auth.get_current_user),
):
    """
    Verify token.

    This endpoint allows verifying the token.

    Returns:
    - status_code (200): The token is valid.
    - status_code (401): Token revoked or expired.
    - status_code (404): The business is not found.

    """
    token = request.headers.get("Authorization").split(" ")[1]
    status, status_code, response = service_business_auth.check_verify_token(db, token)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/change_password", summary="Change password.")
def change_password(
    request: Request,
    data: dict = Body(
        ...,
        example={
            "old_password": "@Password1234",
            "new_password": "@Password12345",
            "confirm_password": "@Password12345",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(service_business_auth.get_current_user),
):
    """
    Change password.

    This endpoint allows changing the password.

    Parameters:
    - old_password (str): The old password of the business.
    - new_password (str): The new password of the business.
    - confirm_password (str): The confirm password of the business.

    Returns:
    - status_code (200): The password has been changed successfully.
    - status_code (400): The request is invalid.
    - status_code (401): The password is incorrect.
    - status_code (404): The business is not found.
    - status_code (409): The new password is the same as the old password.

    """
    status, status_code, response = service_business_auth.change_password(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/send_forgot_password", summary="Forgot password.")
def forgot_password(
    request: Request,
    data: dict = Body(
        ...,
        example={
            "email": "clone46191@gmail.com",
        },
    ),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    """
    Send code forgot password to email.

    This endpoint allows sending code forgot password to email.

    Parameters:
    - email (str): The email of the business.

    Returns:
    - status_code (200): The password has been sent successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The business is not found.

    """
    status, status_code, response = service_business_auth.send_forgot_password(
        db, background_tasks, data
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

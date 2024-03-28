from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    File,
    UploadFile,
    Form,
    Body,
    Request,
)
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.core.auth import service_user_auth
from app.core import constant
from app.core.user import service_user
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.post("/register", summary="Register a new user.")
def register_auth(
    full_name: str = Form(..., description="The full name of the user."),
    email: str = Form(..., description="The email of the user."),
    password: str = Form(..., description="The password of the user."),
    confirm_password: str = Form(..., description="The confirm password of the user."),
    avatar: UploadFile = File(None, description="The profile avatar of the user."),
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    This endpoint allows registering a new user.

    Parameters:
    - full_name (str): The full name of the user.
    - email (str): The email of the user.
    - password (str): The password of the user.
    - confirm_password (str): The confirm password of the user.
    - avatar (UploadFile): The profile avatar of the user.

    Returns:
    - status_code (201): The user has been registered successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The user is already registered.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_user.create_user(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/login", summary="Login user.")
def login_auth(
    data: dict = Body(
        ..., example={"email": "1@email.com", "password": "@Password1234"}
    ),
    db: Session = Depends(get_db),
):
    """
    Login user.

    This endpoint allows logging in a user.

    Parameters:
    - email (str): The email of the user.
    - password (str): The password of the user.

    Returns:
    - status_code (200): The user has been logged in successfully.
    - status_code (400): The request is invalid.
    - status_code (401): The password is incorrect.
    - status_code (404): The user is not found.

    """
    status, status_code, response = service_user_auth.authenticate(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/refresh_token", summary="Refresh token.")
def refresh_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_user_auth.get_current_user),
):
    """
    Refresh token.

    This endpoint allows refreshing the token.

    Returns:
    - status_code (200): The token has been refreshed successfully.
    - status_code (401): Token revoked or expired.
    - status_code (404): The user is not found.

    """
    status, status_code, response = service_user_auth.refresh_token(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/logout", summary="Logout user.")
def logout_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_user_auth.get_current_user),
):
    """
    Logout user.

    This endpoint allows logging out a user.

    Returns:
    - status_code (200): The user has been logged out successfully.
    - status_code (401): The user is not authorized.
    - status_code (404): The user is not found.

    """

    status, status_code, response = service_user_auth.logout(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/verify_token", summary="Verify token.")
def verify_token_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_user_auth.get_current_user),
):
    """
    Verify token.

    This endpoint allows verifying the token.

    Returns:
    - status_code (200): The token is valid.
    - status_code (401): Token revoked or expired.
    - status_code (404): The user is not found.

    """
    token = request.headers.get("Authorization").split(" ")[1]
    status, status_code, response = service_user_auth.check_verify_token(db, token)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

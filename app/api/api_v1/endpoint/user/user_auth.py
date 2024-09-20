from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    Body,
    Request,
)

from app.db.base import CurrentSession
from app.core.auth.user_manager_service import user_manager_service
from app.core.auth.user_auth_service import user_auth_service
from app.core import constant
from app.core.user import user_service
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.post("/register", summary="Register a new user.")
async def register_auth(
    db: CurrentSession,
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
    data = locals()

    status, status_code, response = await user_service.create(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/login", summary="Login user.")
async def login_auth(
    db: CurrentSession,
    data: dict = Body(
        ...,
        description="The data to login a user.",
        example={"email": "ongtung@gmail.com", "password": "@Password1234"},
    ),
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
    status, status_code, response = await user_auth_service.authenticate(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/login_google", summary="Login user by google.")
async def login_google(
    db: CurrentSession,
    data: dict = Body(..., example={"access_token": "access_token"}),
):
    """
    Login user by google.

    This endpoint allows logging in a user by google.

    Parameters:
    - access_token (str): The access token from google.

    Returns:
    - status_code (200): The user has been logged in successfully.
    - status_code (400): The request is invalid.
    - status_code (401): The password is incorrect.
    - status_code (404): The user is not found.

    """

    status, status_code, response = await user_auth_service.authenticate_google(
        db, data
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/refresh_token", summary="Refresh token.")
async def refresh_auth(
    request: Request,
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_user),
):
    """
    Refresh token.

    This endpoint allows refreshing the token.

    Returns:
    - status_code (200): The token has been refreshed successfully.
    - status_code (401): Token revoked or expired.
    - status_code (404): The user is not found.

    """
    status, status_code, response = await user_auth_service.refresh_token(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/logout", summary="Logout user.")
async def logout_auth(
    request: Request,
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_user),
):
    """
    Logout user.

    This endpoint allows logging out a user.

    Returns:
    - status_code (200): The user has been logged out successfully.
    - status_code (401): The user is not authorized.
    - status_code (404): The user is not found.

    """

    status, status_code, response = await user_auth_service.logout(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/verify_token", summary="Verify token.")
async def verify_token_auth(
    request: Request,
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_user),
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
    status, status_code, response = await user_auth_service.check_verify_token(
        db, token
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/change_password", summary="Change password.")
async def change_password(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_user),
    data: dict = Body(
        ...,
        example={
            "old_password": "@Password1234",
            "new_password": "@Password12345",
            "confirm_password": "@Password12345",
        },
    ),
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
    status, status_code, response = await user_auth_service.change_password(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

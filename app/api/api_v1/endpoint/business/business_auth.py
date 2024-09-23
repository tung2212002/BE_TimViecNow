from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    Body,
    Request,
    BackgroundTasks,
)
from typing import Annotated
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.auth.user_manager_service import user_manager_service
from app.core.auth.business_auth_service import business_auth_service
from app.core.business.business_service import business_service
from app.hepler.enum import Gender

router = APIRouter()


@router.post("/register", summary="Register a new business.")
async def register_business(
    full_name: Annotated[
        str,
        Form(
            ...,
            description="The full name of the business.",
            json_schema_extra={"example": "Tung Ong"},
        ),
    ],
    email: Annotated[
        str,
        Form(
            ...,
            description="The email of the business.",
            json_schema_extra={"example": "tungong@email.com"},
        ),
    ],
    password: Annotated[
        str,
        Form(
            ...,
            description="The password of the business.",
            json_schema_extra={"example": "@Password1234"},
        ),
    ],
    confirm_password: Annotated[
        str,
        Form(
            ...,
            description="The confirm password of the business.",
            json_schema_extra={"example": "@Password1234"},
        ),
    ],
    province_id: Annotated[
        int,
        Form(
            ...,
            description="The province id of the business.",
            json_schema_extra={"example": 1},
        ),
    ],
    phone_number: Annotated[
        str,
        Form(
            ...,
            description="The phone number of the business.",
            json_schema_extra={"example": "0323456789"},
        ),
    ],
    gender: Annotated[
        Gender,
        Form(
            ...,
            description="Gender of the business.",
            json_schema_extra={"example": Gender.OTHER},
        ),
    ],
    company_name: Annotated[
        str,
        Form(
            ...,
            description="The company of the business.",
            json_schema_extra={"example": "Tung Ong Company"},
        ),
    ],
    work_position: Annotated[
        str,
        Form(
            ...,
            description="The work position of the business.",
            json_schema_extra={"example": "Nhân viên"},
        ),
    ],
    work_location: str = Form(
        None,
        description="The work location of the business.",
        json_schema_extra={"example": "Hà Nội"},
    ),
    avatar: UploadFile = File(None, description="The profile avatar of the business."),
    district_id: int = Form(
        None,
        description="The district id of the business.",
        json_schema_extra={"example": 1},
    ),
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
    data = locals()

    return await business_service.create(db, data)


@router.post("/login", summary="Login business.")
async def login_auth(
    db: Session = Depends(get_db),
    data: dict = Body(
        ..., example={"email": "ongtung2212002@gmail.com", "password": "@Amin1234"}
    ),
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
    return await business_auth_service.authenticate(db, data)


@router.post("/refresh_token", summary="Refresh token.")
async def refresh_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
):
    """
    Refresh token.

    This endpoint allows refreshing the token.

    Returns:
    - status_code (200): The token has been refreshed successfully.
    - status_code (401): Token revoked or expired.
    - status_code (404): The business is not found.

    """
    return await business_auth_service.refresh_token(db, request)


@router.post("/logout", summary="Logout business.")
async def logout_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
):
    """
    Logout business.

    This endpoint allows logging out a business.

    Returns:
    - status_code (200): The business has been logged out successfully.
    - status_code (401): The business is not authorized.
    - status_code (404): The business is not found.

    """
    return await business_auth_service.logout(db, request)


@router.post("/verify_token", summary="Verify token.")
async def verify_token_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
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
    return await business_auth_service.check_verify_token(db, token)


@router.post("/change_password", summary="Change password.")
async def change_password(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
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
    return await business_auth_service.change_password(db, data, current_user)


@router.post("/change_password_for_test", summary="Change password.")
async def change_password(
    db: Session = Depends(get_db),
    data: dict = Body(
        ...,
        example={
            "password": "@Password1234",
            "user_id": "2",
        },
    ),
):
    """
    Change password.

    This endpoint allows changing the password for test.

    Parameters:
    - password (str): The password of the business.
    - user_id (int): The user id of the business.

    Returns:

    """
    return await business_auth_service.change_password_for_test(db, data)


@router.post("/send_forgot_password", summary="Forgot password.")
async def forgot_password(
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    data: dict = Body(
        ...,
        example={
            "email": "clone46191@gmail.com",
        },
    ),
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
    return "Coming soon"
    return await business_auth_service.send_forgot_password(db, background_tasks, data)

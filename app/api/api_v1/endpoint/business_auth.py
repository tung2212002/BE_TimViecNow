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
from typing import Annotated
from pydantic import Field

from app.db.base import get_db
from app.core.auth import service_business_auth
from app.core import constant
from app.core.representative import service_representative
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.post("/register", summary="Register a new representative.")
def register_representative(
    full_name: Annotated[
        str, Form(..., description="The full name of the representative.")
    ],
    email: Annotated[str, Form(..., description="The email of the representative.")],
    password: Annotated[
        str, Form(..., description="The password of the representative.")
    ],
    confirm_password: Annotated[
        str, Form(..., description="The confirm password of the representative.")
    ],
    province_id: Annotated[
        int, Form(..., description="The province id of the representative.")
    ],
    phone_number: Annotated[
        str, Form(..., description="The phone number of the representative.")
    ],
    gender: Annotated[str, Form(..., description="Gender of the representative.")],
    company: Annotated[
        str, Form(..., description="The company of the representative.")
    ],
    work_position: Annotated[
        str, Form(..., description="The work position of the representative.")
    ],
    work_location: Annotated[
        str, Form(..., description="The work location of the representative.")
    ],
    avatar: UploadFile = File(
        None, description="The profile avatar of the representative."
    ),
    district_id: int = Form(None, description="The district id of the representative."),
    db: Session = Depends(get_db),
):
    """
    Register a new representative.

    This endpoint allows create a new representative.

    Parameters:
    - full_name (str): The full name of the representative.
    - email (str): The email of the representative.
    - password (str): The password of the representative.
    - confirm_password (str): The confirm password of the representative.
    - avatar (UploadFile): The profile avatar of the representative.
    - province_id (int): The province id of the representative.
    - district_id (int): The district id of the representative.
    - phone_number (str): The phone number of the representative.
    - gender (str): The gender of the representative.
    - company (str): The company of the representative.
    - work_position (str): The work position of the representative.
    - work_location (str): The work location of the representative.

    Returns:
    - status_code (201): The representative has been registered successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The representative is already registered.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}
    status, status_code, response = service_representative.create_representative(
        db, data
    )
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/login", summary="Login representative.")
def login_auth(
    data: dict = Body(
        ..., example={"email": "1@email.com", "password": "@Password1234"}
    ),
    db: Session = Depends(get_db),
):
    """
    Login representative.

    This endpoint allows logging in a representative.

    Parameters:
    - email (str): The email of the representative.
    - password (str): The password of the representative.

    Returns:
    - status_code (200): The representative has been logged in successfully.
    - status_code (400): The request is invalid.
    - status_code (401): The password is incorrect.
    - status_code (404): The representative is not found.

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
    - status_code (404): The representative is not found.

    """
    status, status_code, response = service_business_auth.refresh_token(db, request)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/logout", summary="Logout representative.")
def logout_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_business_auth.get_current_user),
):
    """
    Logout representative.

    This endpoint allows logging out a representative.

    Returns:
    - status_code (200): The representative has been logged out successfully.
    - status_code (401): The representative is not authorized.
    - status_code (404): The representative is not found.

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
    - status_code (404): The representative is not found.

    """
    token = request.headers.get("Authorization").split(" ")[1]
    status, status_code, response = service_business_auth.check_verify_token(db, token)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)

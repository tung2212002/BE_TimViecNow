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
from app.core.auth import service_auth
from app.core import constant
from app.core.user import service_user

router = APIRouter()


@router.post("/register")
def register_auth(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    This endpoint allows registering a new user.

    Parameters:
    - full_name (str): The full name of the user.
    - email (str): The email of the user.
    - password (str): The password of the user.
    - picture (UploadFile): The profile avatar of the user.

    Returns:
    - status_code (201): The user has been registered successfully.
    - status_code (400): The request is invalid.

    """

    data = {
        "full_name": full_name,
        "email": email,
        "password": password,
        "picture": picture,
    }
    status, status_code, response = service_user.create_user(db, data)
    if status == constant.ERROR:
        raise HTTPException(status_code=status_code, detail=response)
    elif status == constant.SUCCESS:
        return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.post("/login")
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
    status, status_code, response = service_auth.authenticate(db, data)
    if status == constant.ERROR:
        raise HTTPException(status_code=status_code, detail=response)
    elif status == constant.SUCCESS:
        return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.post("/refresh_token")
def refresh_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_auth.get_current_user),
):
    """
    Refresh token.

    This endpoint allows refreshing the token.

    Returns:
    - status_code (200): The token has been refreshed successfully.
    - status_code (401): Token revoked or expired.
    - status_code (404): The user is not found.

    """
    status, status_code, response = service_auth.refresh_token(db, request)
    if status == constant.ERROR:
        raise HTTPException(status_code=status_code, detail=response)
    elif status == constant.SUCCESS:
        return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.post("/logout")
def logout_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_auth.get_current_user),
):
    """
    Logout user.

    This endpoint allows logging out a user.

    Returns:
    - status_code (200): The user has been logged out successfully.
    - status_code (401): The user is not authorized.
    - status_code (404): The user is not found.

    """

    status, status_code, response = service_auth.logout(db, request)
    if status == constant.ERROR:
        raise HTTPException(status_code=status_code, detail=response)
    elif status == constant.SUCCESS:
        return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
    
@router.post("/verify_token")
def verify_token_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(service_auth.get_current_user),
):
    """
    Verify token.

    This endpoint allows verifying the token.

    Returns:
    - status_code (200): The token is valid.
    - status_code (401): Token revoked or expired.
    - status_code (404): The user is not found.

    """
    status, status_code, response = service_auth.verify_token(db, request)
    if status == constant.ERROR:
        raise HTTPException(status_code=status_code, detail=response)
    elif status == constant.SUCCESS:
        return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.post("/test_login")
def test_login_auth():
    response = {
        "user": {"id": 1, "full_name": "test", "email": ""},
        "access_token": "test",
        "refresh_token": "test",
    }

    return JSONResponse(status_code=200, content=jsonable_encoder(response))

@router.post("/test_logout")
def test_logout_auth():
    response = {"detail": "Successfully logged out."}

    return JSONResponse(status_code=200, content=jsonable_encoder(response))

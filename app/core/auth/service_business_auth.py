from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
import requests

from app.core import constant
from app.core.security import pwd_context
from app.core.config import settings
from app import crud
from app.schema import (
    auth as schema_auth,
    manager_base as schema_manager_base,
)
from app.db.base import get_db
from app.core.auth.auth_bearer import JWTBearer
from app.core.auth.auth_handler import signJWT, decodeJWT, signJWTRefreshToken
from app.hepler.enum import Role, TypeAccount
from app.hepler.exception_handler import get_message_validation_error
from app.core.business.service_business import get_info_user


def authenticate(db: Session, data: dict):
    try:
        user_data = schema_auth.AuthLogin(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    user = crud.manager_base.get_by_email(db, user_data.email)
    if not user:
        return constant.ERROR, 404, "User not found"
    if not verify_password(user_data.password, user.hashed_password):
        return constant.ERROR, 401, "Incorrect password"

    access_token = signJWT(user)
    refresh_token = signJWTRefreshToken(user)

    business = user.business
    if business is None:
        return (
            constant.SUCCESS,
            200,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": schema_manager_base.ManagerBaseItemResponse(**user.__dict__),
            },
        )

    user_response = get_info_user(user)
    response = (
        constant.SUCCESS,
        200,
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {**user_response},
        },
    )
    return response


def authenticate_google(db: Session, token: str):
    try:
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        response = requests.get(url)
        if response.status_code != 200:
            return constant.ERROR, 401, "Token invalid"
        data = response.json()
        email = data.get("email")
        if email is None:
            return constant.ERROR, 401, "Email not found"
        user = crud.manager_base.get_by_email(db, email)
        if user is None:
            return constant.ERROR, 404, "User not found"

        access_token = signJWT(user)
        refresh_token = signJWTRefreshToken(user)

        business = user.business
        if business is None:
            return (
                constant.SUCCESS,
                200,
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": schema_manager_base.ManagerBaseItemResponse(
                        **user.__dict__
                    ),
                },
            )

        user_response = get_info_user(user)
        response = (
            constant.SUCCESS,
            200,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {**user_response},
            },
        )
        return response
    except Exception as e:
        return constant.ERROR, 400, str(e)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_current_active_user(email: str):
    pass


def get_current_user(data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    token_decode = data["payload"]
    if token_decode["type_account"] != TypeAccount.BUSINESS:
        raise HTTPException(status_code=403, detail="Not permission")
    token = data["token"]
    if check_blacklist(db, token):
        raise HTTPException(status_code=401, detail="Token revoked")
    id = token_decode["id"]
    role = token_decode["role"]
    if role == Role.BUSINESS:
        user = crud.manager_base.get(db, id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    elif role == Role.ADMIN or role == Role.SUPER_USER:
        user = crud.manager_base.get_by_admin(db, id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


def get_current_admin(data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    token_decode = data["payload"]
    if token_decode["type_account"] != TypeAccount.BUSINESS:
        raise HTTPException(status_code=403, detail="Not permission")
    token = data["token"]
    if check_blacklist(db, token):
        raise HTTPException(status_code=401, detail="Token revoked")
    id = token_decode["id"]
    role = token_decode["role"]
    if role != Role.ADMIN and role != Role.SUPER_USER:
        raise HTTPException(status_code=403, detail="Not permission")
    user = crud.manager_base.get_by_admin(db, id)

    if user is None:
        raise HTTPException(status_code=403, detail="Not permission")
    return user


def get_current_superuser(
    data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    token_decode = data["payload"]
    if token_decode["type_account"] != TypeAccount.BUSINESS:
        raise HTTPException(status_code=403, detail="Not permission")
    token = data["token"]
    if check_blacklist(db, token):
        raise HTTPException(status_code=401, detail="Token revoked")
    id = token_decode["id"]
    role = token_decode["role"]
    if role != Role.SUPER_USER:
        raise HTTPException(status_code=403, detail="Not permission")
    user = crud.manager_base.get_by_admin(db, id)
    if user is None:
        return constant.ERROR, 403, "Not permission"
    return user


def get_token_user(data: dict = Depends(JWTBearer())):
    return data["token"]


def check_verify_token(db: Session, token: str):
    token_decode = decodeJWT(token)
    exp = token_decode["exp"]
    now = datetime.now(timezone.utc)
    if now > datetime.fromtimestamp(exp, timezone.utc):
        return constant.ERROR, 401, "Token expired"
    check_blacklist = crud.blacklist.get_by_token(db, token)
    if check_blacklist:
        return constant.ERROR, 401, "Token revoked"
    return constant.SUCCESS, 200, token_decode


def refresh_token(db: Session, request):
    refresh_token = request.headers.get("Authorization").split(" ")[1]
    token_decode = decodeJWT(refresh_token)
    if token_decode["type"] != "refresh_token":
        return constant.ERROR, 401, "Invalid token"
    id = token_decode["id"]
    user = crud.manager_base.get(db, id)
    business = user.business
    if user is None:
        return constant.ERROR, 404, "User not found"

    access_token = signJWT(user)
    user_response = get_info_user(user)

    response = (
        constant.SUCCESS,
        200,
        {
            "access_token": access_token,
            "user": user_response,
        },
    )
    return response


def logout(db: Session, request: dict):
    token = request.headers.get("Authorization").split(" ")[1]
    crud.blacklist.create(db=db, token=token)
    return constant.SUCCESS, 200, "Logout successfully"


def check_blacklist(db: Session, token: str):
    return crud.blacklist.get_by_token(db, token)

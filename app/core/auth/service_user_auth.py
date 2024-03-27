from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends

from app.core import constant
from app.core.security import pwd_context
from app.core.config import settings
from app import crud
from app.schema import user as schema_user, auth as schema_auth
from app.db.base import get_db
from app.core.auth.auth_bearer import JWTBearer
from app.core.auth.auth_handler import signJWT, decodeJWT
from app.hepler.enum import Role
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def authenticate(db: Session, data: dict):
    try:
        user_data = schema_auth.AuthLogin(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    user = crud.user.get_by_email(db, user_data.email)
    if not user:
        return constant.ERROR, 404, "User not found"
    if not verify_password(user_data.password, user.hashed_password):
        return constant.ERROR, 401, "Incorrect password"
    access_token = signJWT(
        {
            "email": user.email,
            "id": user.id,
            "is_active": user.is_active,
            "role": user.role,
            "type": "access_token",
        }
    )
    refresh_token = signJWT(
        {
            "email": user.email,
            "id": user.id,
            "is_active": user.is_active,
            "role": user.role,
            "type": "refresh_token",
        }
    )
    user = schema_user.UserItemResponse(**user.__dict__)
    response = (
        constant.SUCCESS,
        200,
        {"access_token": access_token, "refresh_token": refresh_token, "user": user},
    )
    return response


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_current_active_user(username: str):
    pass


def get_current_user(data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    token_decode = data["payload"]
    token = data["token"]
    if check_blacklist(db, token):
        custom_response_error(401, constant.ERROR, "Token revoked")
    email = token_decode["email"]
    user = crud.user.get_by_email(db, email)
    if user is None:
        custom_response_error(404, constant.ERROR, "User not found")
    return user


def get_current_admin(data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    token_decode = data["payload"]
    token = data["token"]
    if check_blacklist(db, token):
        custom_response_error(401, constant.ERROR, "Token revoked")
    email = token_decode["email"]
    user = crud.user.get_by_email(db, email)
    if user is None:
        custom_response_error(404, constant.ERROR, "User not found")
    if user.role != Role.ADMIN:
        custom_response_error(403, constant.ERROR, "Not permission")
    return user


def get_current_superuser(
    data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    token_decode = data["payload"]
    token = data["token"]
    if check_blacklist(db, token):
        # raise HTTPException(status_code=401, detail="Token revoked")
        custom_response_error(401, constant.ERROR, "Token revoked")
    email = token_decode["email"]
    user = crud.user.get_by_email(db, email)
    if user is None:
        # return constant.ERROR, 404, "User not found"
        custom_response_error(404, constant.ERROR, "User not found")
    if user.role != Role.SUPER_USER:
        # return constant.ERROR, 403, "Not permission"
        custom_response_error(403, constant.ERROR, "Not permission")
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
        raise HTTPException(status_code=401, detail="Token revoked")
    return constant.SUCCESS, 200, token_decode


def refresh_token(db: Session, request):
    refresh_token = request.headers.get("Authorization").split(" ")[1]
    token_decode = decodeJWT(refresh_token)
    if token_decode["type"] != "refresh_token":
        return constant.ERROR, 401, "Invalid token"
    email = token_decode["email"]
    user = crud.user.get_by_email(db, email)
    if user is None:
        return constant.ERROR, 404, "User not found"
    access_token = signJWT(
        {
            "email": user.email,
            "id": user.id,
            "is_active": user.is_active,
            "role": user.role,
            "type": "access_token",
        }
    )
    user = schema_user.UserItemResponse(**user.__dict__)
    response = (constant.SUCCESS, 200, {"access_token": access_token, "user": user})
    return response


def logout(db: Session, request: dict):
    token = request.headers.get("Authorization").split(" ")[1]
    crud.blacklist.create(db=db, token=token)
    return constant.SUCCESS, 200, "Logout successfully"


def check_blacklist(db: Session, token: str):
    return crud.blacklist.get_by_token(db, token)

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException, Depends
import requests
from fastapi import HTTPException, Request

from app.core import constant
from app.core.security import pwd_context
from app import crud
from app.schema import (
    user as schema_user,
    auth as schema_auth,
    social_network as schema_social_network,
)
from app.db.base import CurrentSession
from app.core.auth.jwt.auth_bearer import JWTBearer
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.enum import Role, TypeAccount
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role, TypeAccount, Provider
from app.core.security import PasswordManager
from app.model import User, SocialNetwork


# async def authenticate(self,db: Session, data: dict):
#     try:
#         user_data = schema_auth.AuthLogin(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     user = crud.user.get_by_email(db, user_data.email)
#     if not user:
#         return constant.ERROR, 404, "User not found"
#     if not verify_password(user_data.password, user.hashed_password):
#         return constant.ERROR, 401, "Incorrect password"

#     access_token = signJWT(user)
#     refresh_token = signJWTRefreshToken(user)
#     user = schema_user.UserItemResponse(**user.__dict__)

#     response = (
#         constant.SUCCESS,
#         200,
#         {"access_token": access_token, "refresh_token": refresh_token, "user": user},
#     )
#     return response


# async def authenticate_google(self,db: Session, data: dict):
#     token = data.get("access_token")
#     if token is None:
#         return constant.ERROR, 400, "Token is required"
#     url = f"{constant.GOOGLE_GET_USER_INFO_URL}{token}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return constant.ERROR, 400, "Invalid token"
#     data = response.json()
#     email = data.get("email")
#     if email is None:
#         return constant.ERROR, 400, "Invalid token"
#     social_network = crud.social_network.get_by_email(db, email)
#     if not social_network:
#         data = schema_social_network.SocialNetworkCreateRequest(
#             **data,
#             type=Provider.GOOGLE,
#             social_id=data.get("id"),
#             full_name=data.get("name"),
#             avatar=data.get("picture"),
#             access_token=token,
#         )
#         social_network = crud.social_network.create(db=db, obj_in=data)
#     if not social_network.is_verified:
#         social_network = schema_social_network.SocialNetworkItemResponse(
#             **social_network.__dict__
#         )
#     else:
#         social_network = schema_user.UserItemResponse(**social_network.user.__dict__)
#         access_token = signJWT(social_network)
#         response = (
#             constant.SUCCESS,
#             200,
#             {"access_token": access_token, "user": social_network},
#         )
#         return response
#     access_token = signJWT(social_network)
#     response = (
#         constant.SUCCESS,
#         200,
#         {"access_token": access_token, "user": social_network},
#     )
#     return response


# def verify_password(password: str, hashed_password: str):
#     return pwd_context.verify(password, hashed_password)


# async def get_current_active_user(username: str):
#     pass


# def get_current_user(self,db: CurrentSession, data: dict = Depends(JWTBearer())):
#     token_decode = data["payload"]
#     if token_decode["type_account"] != TypeAccount.NORMAL:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     token = data["token"]
#     if check_blacklist(db, token):
#         raise HTTPException(status_code=401, detail="Token revoked")
#     id = token_decode["id"]
#     if token_decode["role"] == Role.USER:
#         user = crud.user.get(db, id)
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
#     elif token_decode["role"] == Role.SOCIAL_NETWORK:
#         social_network = crud.social_network.get(db, id)
#         if social_network is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         if not social_network.is_verified:
#             return social_network
#         return social_network.user


# async def check_verify_token(self,db: Session, token: str):
#     token_decode = decodeJWT(token)
#     exp = token_decode["exp"]
#     now = datetime.now(timezone.utc)
#     if now > datetime.fromtimestamp(exp, timezone.utc):
#         return constant.ERROR, 401, "Token expired"
#     check_blacklist = crud.blacklist.get_by_token(db, token)
#     if check_blacklist:
#         raise HTTPException(status_code=401, detail="Token revoked")
#     return constant.SUCCESS, 200, token_decode


# async def refresh_token(self,db: Session, request):
#     refresh_token = request.headers.get("Authorization").split(" ")[1]
#     token_decode = decodeJWT(refresh_token)
#     if token_decode["type"] != "refresh_token":
#         return constant.ERROR, 401, "Invalid token"
#     email = token_decode["email"]
#     user = crud.user.get_by_email(db, email)
#     if user is None:
#         return constant.ERROR, 404, "User not found"

#     user.id
#     access_token = signJWT(user)
#     user = schema_user.UserItemResponse(**user.__dict__)

#     response = (constant.SUCCESS, 200, {"access_token": access_token, "user": user})
#     return response


# async def logout(self,db: Session, request: dict):
#     token = request.headers.get("Authorization").split(" ")[1]
#     crud.blacklist.create(db=db, token=token)
#     return constant.SUCCESS, 200, "Logout successfully"


# def check_blacklist(self,db: Session, token: str):
#     return crud.blacklist.get_by_token(db, token)


# async def change_password(self,db: Session, data: dict, current_user):
#     try:
#         user_data = schema_auth.AuthChangePassword(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     if user_data.old_password == user_data.new_password:
#         return constant.ERROR, 409, "Old password and new password are the same"
#     if not verify_password(user_data.old_password, current_user.hashed_password):
#         return constant.ERROR, 401, "Incorrect password"
#     crud.user.update(db=db, obj_in=user_data, db_obj=current_user)
#     return constant.SUCCESS, 200, "Change password successfully"


class UserAuthService:
    async def authenticate(self, db: Session, data: dict):
        try:
            user_data = schema_auth.AuthLogin(**data)
        except Exception as e:
            return constant.ERROR, 400, get_message_validation_error(e)
        user = crud.user.get_by_email(db, user_data.email)
        if not user:
            return constant.ERROR, 404, "User not found"
        if not PasswordManager.verify_password(
            user_data.password, user.hashed_password
        ):
            return constant.ERROR, 401, "Incorrect password"

        access_token = token_manager.signJWT(user)
        refresh_token = token_manager.signJWTRefreshToken(user)
        user = schema_user.UserItemResponse(**user.__dict__)

        response = (
            constant.SUCCESS,
            200,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user,
            },
        )
        return response

    async def authenticate_google(self, db: Session, data: dict):
        token = data.get("access_token")
        if token is None:
            return constant.ERROR, 400, "Token is required"
        url = f"{constant.GOOGLE_GET_USER_INFO_URL}{token}"
        response = requests.get(url)
        if response.status_code != 200:
            return constant.ERROR, 400, "Invalid token"
        data = response.json()
        email = data.get("email")
        if email is None:
            return constant.ERROR, 400, "Invalid token"
        social_network = crud.social_network.get_by_email(db, email)
        if not social_network:
            data = schema_social_network.SocialNetworkCreateRequest(
                **data,
                type=Provider.GOOGLE,
                social_id=data.get("id"),
                full_name=data.get("name"),
                avatar=data.get("picture"),
                access_token=token,
            )
            social_network = crud.social_network.create(db=db, obj_in=data)
        if not social_network.is_verified:
            social_network = schema_social_network.SocialNetworkItemResponse(
                **social_network.__dict__
            )
        else:
            social_network = schema_user.UserItemResponse(
                **social_network.user.__dict__
            )
            access_token = token_manager.signJWT(social_network)
            response = (
                constant.SUCCESS,
                200,
                {"access_token": access_token, "user": social_network},
            )
            return response
        access_token = token_manager.signJWT(social_network)
        response = (
            constant.SUCCESS,
            200,
            {"access_token": access_token, "user": social_network},
        )
        return response

    async def check_verify_token(self, db: Session, token: str):
        token_decode = token_manager.decodeJWT(token)
        exp = token_decode["exp"]
        now = datetime.now(timezone.utc)
        if now > datetime.fromtimestamp(exp, timezone.utc):
            return constant.ERROR, 401, "Token expired"
        check_blacklist = crud.blacklist.get_by_token(db, token)
        if check_blacklist:
            raise HTTPException(status_code=401, detail="Token revoked")
        return constant.SUCCESS, 200, token_decode

    async def refresh_token(self, db: Session, request: Request):
        refresh_token = request.headers.get("Authorization").split(" ")[1]
        token_decode = token_manager.decodeJWT(refresh_token)
        if token_decode["type"] != "refresh_token":
            return constant.ERROR, 401, "Invalid token"
        email = token_decode["email"]
        user = crud.user.get_by_email(db, email)
        if user is None:
            return constant.ERROR, 404, "User not found"

        user.id
        access_token = token_manager.signJWT(user)
        user = schema_user.UserItemResponse(**user.__dict__)

        response = (constant.SUCCESS, 200, {"access_token": access_token, "user": user})
        return response

    async def logout(self, db: Session, request: dict):
        token = request.headers.get("Authorization").split(" ")[1]
        crud.blacklist.create(db=db, token=token)
        return constant.SUCCESS, 200, "Logout successfully"

    async def change_password(self, db: Session, data: dict, current_user: User):
        try:
            user_data = schema_auth.AuthChangePassword(**data)
        except Exception as e:
            return constant.ERROR, 400, get_message_validation_error(e)
        if user_data.old_password == user_data.new_password:
            return constant.ERROR, 409, "Old password and new password are the same"
        if not PasswordManager.verify_password(
            user_data.old_password, current_user.hashed_password
        ):
            return constant.ERROR, 401, "Incorrect password"
        crud.user.update(db=db, obj_in=user_data, db_obj=current_user)
        return constant.SUCCESS, 200, "Change password successfully"


user_auth_service = UserAuthService()

from sqlalchemy.orm import Session
from datetime import datetime, timezone
import requests
from fastapi import Request

from app.core import constant
from app import crud
from app.schema import (
    user as schema_user,
    social_network as schema_social_network,
    auth as schema_auth,
)
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.enum import Provider
from app.core.security import PasswordManager
from app.model import User
from app.common.exception import CustomException
from app.common.response import CustomResponse
from fastapi import status


class UserAuthService:
    async def authenticate(self, db: Session, data: dict):
        user_data = schema_auth.AuthLogin(**data)

        user = crud.user.get_by_email(db, user_data.email)
        if not user:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        if not PasswordManager.verify_password(
            user_data.password, user.hashed_password
        ):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Incorrect password"
            )

        access_token = token_manager.signJWT(user)
        refresh_token = token_manager.signJWTRefreshToken(user)
        user = schema_user.UserItemResponse(**user.__dict__)

        return CustomResponse(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user,
            }
        )

    async def authenticate_google(self, db: Session, data: dict):
        token = data.get("access_token")
        if token is None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Token is required"
            )

        url = f"{constant.GOOGLE_GET_USER_INFO_URL}{token}"
        response = requests.get(url)
        if response.status_code != 200:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Invalid token"
            )

        data = response.json()
        email = data.get("email")
        if email is None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Invalid token"
            )

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
            return CustomResponse(
                data={"access_token": access_token, "user": social_network}
            )

        access_token = token_manager.signJWT(social_network)

        return CustomResponse(
            data={"access_token": access_token, "user": social_network}
        )

    async def check_verify_token(self, db: Session, token: str):
        token_decode = token_manager.decodeJWT(token)
        exp = token_decode["exp"]
        now = datetime.now(timezone.utc)
        if now > datetime.fromtimestamp(exp, timezone.utc):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Token expired"
            )

        check_blacklist = crud.blacklist.get_by_token(db, token)
        if check_blacklist:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Token revoked"
            )

        return CustomResponse(data=token_decode)

    async def refresh_token(self, db: Session, request: Request):
        refresh_token = request.headers.get("Authorization").split(" ")[1]
        token_decode = token_manager.decodeJWT(refresh_token)
        if token_decode["type"] != "refresh_token":
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Invalid token"
            )

        email = token_decode["email"]
        user = crud.user.get_by_email(db, email)
        if user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        user.id
        access_token = token_manager.signJWT(user)
        user = schema_user.UserItemResponse(**user.__dict__)

        return CustomResponse(data={"access_token": access_token, "user": user})

    async def logout(self, db: Session, request: Request):
        token = request.headers.get("Authorization").split(" ")[1]
        crud.blacklist.create(db=db, token=token)

        return CustomResponse(msg="Logout successfully")

    async def change_password(self, db: Session, data: dict, current_user: User):
        user_data = schema_auth.AuthChangePassword(**data)

        if user_data.old_password == user_data.new_password:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT,
                msg="Old password and new password are the same",
            )

        if not PasswordManager.verify_password(
            user_data.old_password, current_user.hashed_password
        ):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Incorrect password"
            )

        crud.user.update(db=db, obj_in=user_data, db_obj=current_user)

        return CustomResponse(msg="Change password successfully")


user_auth_service = UserAuthService()

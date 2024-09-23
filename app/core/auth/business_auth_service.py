from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import Request
from fastapi import BackgroundTasks

from app import crud
from app.schema import (
    manager_base as schema_manager_base,
    auth as schema_auth,
)
from app.core.auth.jwt.auth_handler import token_manager
from app.core.business.business_helper import business_hepler
from app.core.security import PasswordManager
from app.common.exception import CustomException
from app.common.response import CustomResponse
from fastapi import status
from app.model import ManagerBase


class BusinessService:
    async def authenticate(self, db: Session, data: dict):
        user_data = schema_auth.AuthLogin(**data)

        user = crud.manager_base.get_by_email(db, user_data.email)
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

        business = user.business
        if business is None:
            return CustomResponse(
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": schema_manager_base.ManagerBaseItemResponse(
                        **user.__dict__
                    ),
                }
            )

        user_response = business_hepler.get_info(db, user)

        return CustomResponse(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {**user_response},
            }
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

        id = token_decode["id"]
        user = crud.manager_base.get(db, id)
        business = user.business
        if user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        access_token = token_manager.signJWT(user)
        user_response = business_hepler.get_info(db, user)

        return CustomResponse(
            data={
                "access_token": access_token,
                "user": user_response,
            }
        )

    async def logout(self, db: Session, request: Request):
        token = request.headers.get("Authorization").split(" ")[1]
        crud.blacklist.create(db=db, token=token)

        return CustomResponse(msg="Logout successfully")

    async def change_password(self, db: Session, data: dict, current_user: ManagerBase):
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

        crud.manager_base.update(
            db=db, obj_in={"password": user_data.new_password}, db_obj=current_user
        )

        return CustomResponse(msg="Change password successfully")

    async def send_forgot_password(
        self, db: Session, background_tasks: BackgroundTasks, data: dict
    ):
        user_data = schema_auth.AuthForgotPassword(**data)

        user = crud.manager_base.get_by_email(db, user_data.email)
        if user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        token = token_manager.signJWT(user)

        return CustomResponse(msg="Send email successfully")

    async def change_password_for_test(self, db: Session, data: dict):
        pass_word = data.get("password")
        user_id = data.get("user_id")
        current_user = crud.manager_base.get(db, user_id)

        crud.manager_base.update(
            db=db, obj_in={"password": pass_word}, db_obj=current_user
        )

        return CustomResponse(msg="Change password test successfully")


business_auth_service = BusinessService()

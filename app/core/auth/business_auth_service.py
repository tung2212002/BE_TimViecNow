from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import Request
from fastapi import BackgroundTasks

from app.crud import manager as managerCRUD, blacklist as blacklistCRUD
from app.schema.auth import AuthLogin, AuthChangePassword, AuthForgotPassword
from app.core.auth.jwt.auth_handler import token_manager
from app.core.business.business_helper import business_helper
from app.core.admin.admin_helper import admin_helper
from app.common.exception import CustomException
from app.common.response import CustomResponse
from fastapi import status
from app.model import Manager, Account


class BusinessService:
    async def authenticate(self, db: Session, data: dict):
        manager_data = AuthLogin(**data)

        manager = managerCRUD.get_by_email(db, manager_data.email)
        if not manager:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        if not managerCRUD.authenticate(
            db, email=manager_data.email, password=manager_data.password
        ):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Incorrect password"
            )

        payload = token_manager.create_payload(manager.account)
        access_token = token_manager.signJWT(payload)
        refresh_token = token_manager.signJWTRefreshToken(payload)

        business = manager.business
        if business is None:
            return CustomResponse(
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": admin_helper.get_info_by_manager(db, manager),
                }
            )

        business_response = business_helper.get_info_by_manager(db, manager)

        return CustomResponse(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": business_response,
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

        check_blacklist = blacklistCRUD.get_by_token(db, token)
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
        manager = managerCRUD.get(db, id)
        if manager is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
            )
        business = manager.business
        if business is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
            )

        payload = token_manager.create_payload(manager.account)
        access_token = token_manager.signJWT(payload)
        manager_response = business_helper.get_info(db, manager)

        return CustomResponse(
            data={
                "access_token": access_token,
                "manager": manager_response,
            }
        )

    async def logout(self, db: Session, request: Request):
        token = request.headers.get("Authorization").split(" ")[1]
        blacklistCRUD.create(db=db, token=token)

        return CustomResponse(msg="Logout successfully")

    async def change_password(self, db: Session, data: dict, current_user: Account):
        business_data = AuthChangePassword(**data)

        if business_data.old_password == business_data.new_password:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT,
                msg="Old password and new password are the same",
            )

        manager: Manager = current_user.manager
        if not managerCRUD.authenticate(
            db, email=manager.email, password=business_data.old_password
        ):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Incorrect password"
            )

        managerCRUD.update(
            db=db, obj_in={"password": business_data.new_password}, db_obj=manager
        )

        return CustomResponse(msg="Change password successfully")

    async def send_forgot_password(
        self, db: Session, background_tasks: BackgroundTasks, data: dict
    ):
        business_data = AuthForgotPassword(**data)

        user = managerCRUD.get_by_email(db, business_data.email)
        if user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        token = token_manager.signJWT(user)

        return CustomResponse(msg="Send email successfully")

    async def change_password_for_test(self, db: Session, data: dict):
        pass_word = data.get("password")
        user_id = data.get("user_id")
        current_user = managerCRUD.get(db, user_id)

        managerCRUD.update(db=db, obj_in={"password": pass_word}, db_obj=current_user)

        return CustomResponse(msg="Change password test successfully")


business_auth_service = BusinessService()

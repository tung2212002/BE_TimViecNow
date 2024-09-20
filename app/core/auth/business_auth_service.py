from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException, Depends, Request
from typing import List
from fastapi import BackgroundTasks

from app.core import constant
from app.core.security import pwd_context
from app import crud
from app.schema import (
    auth as schema_auth,
    manager_base as schema_manager_base,
)
from app.db.base import CurrentSession
from app.core.auth.jwt.auth_bearer import JWTBearer
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.enum import Role, TypeAccount, VerifyType
from app.hepler.exception_handler import get_message_validation_error
from app.core.business.business_helper import business_hepler
from app.hepler.response_custom import custom_response_error
from app.core.security import PasswordManager

# async def authenticate(db: Session, data: dict):
#     try:
#         user_data = schema_auth.AuthLogin(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     user = crud.manager_base.get_by_email(db, user_data.email)
#     if not user:
#         return constant.ERROR, 404, "User not found"
#     if not verify_password(user_data.password, user.hashed_password):
#         return constant.ERROR, 401, "Incorrect password"

#     access_token = signJWT(user)
#     refresh_token = signJWTRefreshToken(user)

#     business = user.business
#     if business is None:
#         return (
#             constant.SUCCESS,
#             200,
#             {
#                 "access_token": access_token,
#                 "refresh_token": refresh_token,
#                 "user": schema_manager_base.ManagerBaseItemResponse(**user.__dict__),
#             },
#         )

#     user_response = business_hepler.get_info(db, user)
#     response = (
#         constant.SUCCESS,
#         200,
#         {
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "user": {**user_response},
#         },
#     )
#     return response


# def verify_password(password: str, hashed_password: str):
#     return pwd_context.verify(password, hashed_password)


# def get_current_active_user(email: str):
#     pass


# def get_current_user_by_role(db: Session, data: dict, allowed_roles: List[Role]):
#     token_decode = data["payload"]
#     if token_decode["type_account"] != TypeAccount.BUSINESS:
#         raise HTTPException(status_code=403, detail="Not permission")
#     token = data["token"]
#     if check_blacklist(db, token):
#         raise HTTPException(status_code=401, detail="Token revoked")
#     id = token_decode["id"]
#     role = token_decode["role"]
#     if role not in allowed_roles:
#         raise HTTPException(status_code=403, detail="Not permission")
#     user = crud.manager_base.get_by_admin(db, id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# def get_current_user(self, db: Session, data: dict = Depends(JWTBearer())):
#     return get_current_user_by_role(
#         db, data, [Role.BUSINESS, Role.ADMIN, Role.SUPER_USER]
#     )


# def get_current_business(self, db: Session, data: dict = Depends(JWTBearer())):
#     return get_current_user_by_role(db, data, [Role.BUSINESS])


# def get_current_admin(self, db: Session, data: dict = Depends(JWTBearer())):
#     return get_current_user_by_role(db, data, [Role.ADMIN, Role.SUPER_USER])


# def get_current_superuser(self, db: Session, data: dict = Depends(JWTBearer())):
#     return get_current_user_by_role(db, data, [Role.SUPER_USER])


# def check_permission_business(current_user, roles: List[Role], business_id: int = None):
#     if business_id:
#         if current_user.role not in [Role.SUPER_USER, Role.ADMIN]:
#             if current_user.id != business_id:
#                 custom_response_error(
#                     status_code=403, status=constant.ERROR, response="Permission denied"
#                 )
#             else:
#                 return Role.BUSINESS
#     else:
#         if current_user.role not in roles:
#             custom_response_error(
#                 status_code=403, status=constant.ERROR, response="Permission denied"
#             )
#         elif current_user.role == Role.BUSINESS:
#             return Role.BUSINESS
#     return Role.ADMIN


# async def check_verify_token(db: Session, token: str):
#     token_decode = decodeJWT(token)
#     exp = token_decode["exp"]
#     now = datetime.now(timezone.utc)
#     if now > datetime.fromtimestamp(exp, timezone.utc):
#         return constant.ERROR, 401, "Token expired"
#     check_blacklist = crud.blacklist.get_by_token(db, token)
#     if check_blacklist:
#         return constant.ERROR, 401, "Token revoked"
#     return constant.SUCCESS, 200, token_decode


# async def refresh_token(db: Session, request):
#     refresh_token = request.headers.get("Authorization").split(" ")[1]
#     token_decode = decodeJWT(refresh_token)
#     if token_decode["type"] != "refresh_token":
#         return constant.ERROR, 401, "Invalid token"
#     id = token_decode["id"]
#     user = crud.manager_base.get(db, id)
#     business = user.business
#     if user is None:
#         return constant.ERROR, 404, "User not found"

#     access_token = signJWT(user)
#     user_response = await business_hepler.get_info(db, user)

#     response = (
#         constant.SUCCESS,
#         200,
#         {
#             "access_token": access_token,
#             "user": user_response,
#         },
#     )
#     return response


# def verified_email(user) -> bool:
#     try:
#         if not user.is_verified_email:
#             raise HTTPException(status_code=401, detail="Email not verified")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Email not verified")


# def verified_phone(user) -> bool:
#     return True
#     if not user.is_verified_phone:
#         raise HTTPException(status_code=401, detail="Phone not verified")


# def verified_company(user) -> bool:
#     try:
#         if not user.is_verified_company:
#             raise HTTPException(status_code=401, detail="Company not verified")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Company not verified")


# def verified_identity(user) -> bool:
#     if not user.is_verified_identity:
#         raise HTTPException(status_code=401, detail="Indentity not verified")


# def verified(user, verify_types: List[VerifyType]) -> None:
#     for verify_type in verify_types:
#         if verify_type == VerifyType.EMAIL:
#             verified_email(user)
#         elif verify_type == VerifyType.PHONE:
#             verified_phone(user)
#         elif verify_type == VerifyType.COMPANY:
#             verified_company(user)
#         elif verify_type == VerifyType.IDENTIFY:
#             verified_identity(user)


# def verified_level(user, level: int) -> None:
#     if level == 1:
#         verified(user, [VerifyType.EMAIL])
#     elif level == 2:
#         verified(user, [VerifyType.EMAIL, VerifyType.PHONE])
#     elif level == 3:
#         verified(user, [VerifyType.EMAIL, VerifyType.PHONE, VerifyType.COMPANY])
#     elif level == 4:
#         verified(
#             user,
#             [
#                 VerifyType.EMAIL,
#                 VerifyType.PHONE,
#                 VerifyType.COMPANY,
#                 VerifyType.IDENTIFY,
#             ],
#         )


# async def logout(db: Session, request: dict):
#     token = request.headers.get("Authorization").split(" ")[1]
#     crud.blacklist.create(db=db, token=token)
#     return constant.SUCCESS, 200, "Logout successfully"


# def check_blacklist(db: Session, token: str):
#     return crud.blacklist.get_by_token(db, token)


# async def change_password(db: Session, data: dict, current_user):
#     try:
#         user_data = schema_auth.AuthChangePassword(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     if user_data.old_password == user_data.new_password:
#         return constant.ERROR, 409, "Old password and new password are the same"
#     if not verify_password(user_data.old_password, current_user.hashed_password):
#         return constant.ERROR, 401, "Incorrect password"
#     crud.manager_base.update(
#         db=db, obj_in={"password": user_data.new_password}, db_obj=current_user
#     )
#     return constant.SUCCESS, 200, "Change password successfully"


# async def send_forgot_password(db: Session, background_tasks, data: dict):
#     try:
#         user_data = schema_auth.AuthForgotPassword(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     user = crud.manager_base.get_by_email(db, user_data.email)
#     if user is None:
#         return constant.ERROR, 404, "User not found"
#     token = signJWT(user)
#     return constant.SUCCESS, 200, "Send email successfully"


class BusinessService:
    async def authenticate(self, db: Session, data: dict):
        try:
            user_data = schema_auth.AuthLogin(**data)
        except Exception as e:
            return constant.ERROR, 400, get_message_validation_error(e)
        user = crud.manager_base.get_by_email(db, user_data.email)
        if not user:
            return constant.ERROR, 404, "User not found"
        if not PasswordManager.verify_password(
            user_data.password, user.hashed_password
        ):
            return constant.ERROR, 401, "Incorrect password"

        access_token = token_manager.signJWT(user)
        refresh_token = token_manager.signJWTRefreshToken(user)

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

        user_response = business_hepler.get_info(db, user)
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

    async def check_verify_token(self, db: Session, token: str):
        token_decode = token_manager.decodeJWT(token)
        exp = token_decode["exp"]
        now = datetime.now(timezone.utc)
        if now > datetime.fromtimestamp(exp, timezone.utc):
            return constant.ERROR, 401, "Token expired"
        check_blacklist = crud.blacklist.get_by_token(db, token)
        if check_blacklist:
            return constant.ERROR, 401, "Token revoked"
        return constant.SUCCESS, 200, token_decode

    async def refresh_token(self, db: Session, request: Request):
        refresh_token = request.headers.get("Authorization").split(" ")[1]
        token_decode = token_manager.decodeJWT(refresh_token)
        if token_decode["type"] != "refresh_token":
            return constant.ERROR, 401, "Invalid token"
        id = token_decode["id"]
        user = crud.manager_base.get(db, id)
        business = user.business
        if user is None:
            return constant.ERROR, 404, "User not found"

        access_token = token_manager.signJWT(user)
        user_response = await business_hepler.get_info(db, user)

        response = (
            constant.SUCCESS,
            200,
            {
                "access_token": access_token,
                "user": user_response,
            },
        )
        return response

    async def logout(self, db: Session, request: Request):
        token = request.headers.get("Authorization").split(" ")[1]
        crud.blacklist.create(db=db, token=token)
        return constant.SUCCESS, 200, "Logout successfully"

    async def change_password(self, db: Session, data: dict, current_user):
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
        crud.manager_base.update(
            db=db, obj_in={"password": user_data.new_password}, db_obj=current_user
        )
        return constant.SUCCESS, 200, "Change password successfully"

    async def send_forgot_password(
        self, db: Session, background_tasks: BackgroundTasks, data: dict
    ):
        try:
            user_data = schema_auth.AuthForgotPassword(**data)
        except Exception as e:
            return constant.ERROR, 400, get_message_validation_error(e)
        user = crud.manager_base.get_by_email(db, user_data.email)
        if user is None:
            return constant.ERROR, 404, "User not found"
        token = token_manager.signJWT(user)
        return constant.SUCCESS, 200, "Send email successfully"


business_auth_service = BusinessService()

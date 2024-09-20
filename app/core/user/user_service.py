from sqlalchemy.orm import Session

from app import crud
from app.core import constant
from app.schema import (
    user as schema_user,
    social_network as schema_social_network,
)
from app.core.auth.jwt.auth_bearer import JWTBearer
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.enum import Role
from app.storage.s3 import s3_service
from app.core.user.user_hepler import user_helper
from app.model import User


# async def get_me(current_user: User):
#     if current_user is None:
#         return constant.ERROR, 401, "Unauthorized"
#     if current_user.role == Role.SOCIAL_NETWORK:
#         if not current_user.is_verified:
#             return (
#                 constant.SUCCESS,
#                 200,
#                 schema_social_network.SocialNetworkItemResponse(
#                     **current_user.__dict__
#                 ),
#             )
#     user = schema_user.UserItemResponse(**current_user.__dict__)
#     return constant.SUCCESS, 200, user


# async def get_by_email(db: Session, data: dict):
#     user_data = user_helper.validate_get_by_email(db, data)
#     user = crud.user.get_by_email(db, user_data.email)
#     if not user:
#         return constant.ERROR, 404, "User not found"
#     user = schema_user.UserItemResponse(**user.__dict__)
#     return constant.SUCCESS, 200, user


# async def get_by_id(db: Session, id: int):
#     user = crud.user.get(db, id)
#     if not user:
#         return constant.ERROR, 404, "User not found"
#     user = schema_user.UserItemResponse(**user.__dict__)
#     return constant.SUCCESS, 200, user


# async def get(db: Session, data: dict):
#     page = user_helper.validate_pagination(data)
#     users = crud.user.get_multi(db, **page.dict())
#     if not users:
#         return constant.ERROR, 404, "Users not found"
#     users = [schema_user.UserItemResponse(**user.__dict__) for user in users]
#     return constant.SUCCESS, 200, users


# async def create(db: Session, data: dict):
#     user_data = user_helper.validate_create(data)
#     user = crud.user.get_by_email(db, user_data.email)
#     if user:
#         return constant.ERROR, 409, "Email already registered"
#     avatar = user_data.avatar
#     if avatar:
#         key = avatar.filename
#         s3_service.upload_file(avatar, key)
#         user_data.avatar = key
#     obj_in = schema_user.UserCreate(**user_data.__dict__)
#     user = crud.user.create(db, obj_in=obj_in)
#     user_reponse = schema_user.UserItemResponse(**user.__dict__)

#     access_token = signJWT(user)
#     refresh_token = signJWTRefreshToken(user)

#     response = (
#         constant.SUCCESS,
#         201,
#         {
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "user": user_reponse,
#         },
#     )
#     return response


# async def update(db: Session, id: int, data: dict, current_user: User):
#     if current_user is None or current_user.id != id:
#         return constant.ERROR, 401, "Unauthorized"

#     user = user_helper.validate_update(data)

#     user_update = crud.user.update(db=db, db_obj=current_user, obj_in=user)
#     user_update = schema_user.UserItemResponse(**user_update.__dict__)
#     response = (constant.SUCCESS, 200, user_update)
#     return response


# async def delete(db: Session, id: int, current_user: User):
#     if current_user is None:
#         return constant.ERROR, 404, "User not found"
#     if current_user.id != id:
#         return constant.ERROR, 401, "Unauthorized"
#     if id is None:
#         return constant.ERROR, 400, "Id is required"
#     crud.user.remove(db=db, id=id)
#     response = constant.SUCCESS, 200, "User has been deleted successfully"
#     return response


# async def set_user_active(db: Session, id: int, active: bool):
#     if id is None:
#         return constant.ERROR, 400, "Id is required"
#     response = constant.SUCCESS, 200, crud.user.set_active(db, id, active)
#     return response


class UserService:
    async def get_me(self, current_user: User):
        if current_user is None:
            return constant.ERROR, 401, "Unauthorized"
        if current_user.role == Role.SOCIAL_NETWORK:
            if not current_user.is_verified:
                return (
                    constant.SUCCESS,
                    200,
                    schema_social_network.SocialNetworkItemResponse(
                        **current_user.__dict__
                    ),
                )
        user = schema_user.UserItemResponse(**current_user.__dict__)
        return constant.SUCCESS, 200, user

    async def get_by_email(self, db: Session, data: dict):
        user_data = user_helper.validate_get_by_email(db, data)
        user = crud.user.get_by_email(db, user_data.email)
        if not user:
            return constant.ERROR, 404, "User not found"
        user = schema_user.UserItemResponse(**user.__dict__)
        return constant.SUCCESS, 200, user

    async def get_by_id(self, db: Session, id: int):
        user = crud.user.get(db, id)
        if not user:
            return constant.ERROR, 404, "User not found"
        user = schema_user.UserItemResponse(**user.__dict__)
        return constant.SUCCESS, 200, user

    async def get(self, db: Session, data: dict):
        page = user_helper.validate_pagination(data)
        users = crud.user.get_multi(db, **page.dict())
        if not users:
            return constant.ERROR, 404, "Users not found"
        users = [schema_user.UserItemResponse(**user.__dict__) for user in users]
        return constant.SUCCESS, 200, users

    async def create(self, db: Session, data: dict):
        user_data = user_helper.validate_create(data)
        user = crud.user.get_by_email(db, user_data.email)
        if user:
            return constant.ERROR, 409, "Email already registered"
        avatar = user_data.avatar
        if avatar:
            key = avatar.filename
            s3_service.upload_file(avatar, key)
            user_data.avatar = key
        obj_in = schema_user.UserCreate(**user_data.__dict__)
        user = crud.user.create(db, obj_in=obj_in)
        user_reponse = schema_user.UserItemResponse(**user.__dict__)

        access_token = token_manager.signJWT(user)
        refresh_token = token_manager.signJWTRefreshToken(user)

        response = (
            constant.SUCCESS,
            201,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_reponse,
            },
        )
        return response

    async def delete(self, db: Session, id: int, current_user: User):
        if current_user is None:
            return constant.ERROR, 401, "Unauthorized"
        if id != current_user.id:
            return constant.ERROR, 401, "Unauthorized"
        if id is None:
            return constant.ERROR, 400, "Id is required"
        crud.user.remove(db, id=id)
        response = constant.SUCCESS, 200, "User has been deleted successfully"
        return response


user_service = UserService()

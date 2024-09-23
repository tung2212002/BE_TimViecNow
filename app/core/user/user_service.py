from sqlalchemy.orm import Session

from app import crud
from app.core import constant
from app.schema import (
    user as schema_user,
    social_network as schema_social_network,
    page as schema_page,
)
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.enum import Role
from app.storage.s3 import s3_service
from app.model import User
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse


class UserService:
    async def get_me(self, current_user: User):
        if current_user is None:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        if current_user.role == Role.SOCIAL_NETWORK:
            if not current_user.is_verified:
                return (
                    constant.SUCCESS,
                    200,
                    schema_social_network.SocialNetworkItemResponse(
                        **current_user.__dict__
                    ),
                )
        response = schema_user.UserItemResponse(**current_user.__dict__)

        return CustomResponse(data=response)

    async def get_by_email(self, db: Session, data: dict):
        user_data = schema_user.UserGetRequest(**data)

        user = crud.user.get_by_email(db, user_data.email)
        if not user:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )
        resposne = schema_user.UserItemResponse(**user.__dict__)

        return CustomResponse(data=resposne)

    async def get_by_id(self, db: Session, id: int):
        user = crud.user.get(db, id)
        if not user:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        response = schema_user.UserItemResponse(**user.__dict__)

        return CustomResponse(data=response)

    async def get(self, db: Session, data: dict):
        page = schema_page.Pagination(**data)

        users = crud.user.get_multi(db, **page.dict())
        if not users:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Users not found"
            )

        response = [schema_user.UserItemResponse(**user.__dict__) for user in users]

        return CustomResponse(data=response)

    async def create(self, db: Session, data: dict):
        user_data = schema_user.UserCreateRequest(**data)

        user = crud.user.get_by_email(db, user_data.email)
        if user:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT, msg="Email already registered"
            )
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

        return CustomResponse(
            status_code=status.HTTP_201_CREATED,
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_reponse,
            },
        )

    async def update(self, db: Session, data: dict, current_user: User):
        user_data = schema_user.UserUpdateRequest(**data)

        avatar = user_data.avatar
        if avatar:
            key = avatar.filename
            s3_service.upload_file(avatar, key)
            user_data.avatar = key
        user_data = schema_user.UserUpdate(**user_data.__dict__)
        user = crud.user.update(db, obj_in=user_data, db_obj=current_user)
        response = schema_user.UserItemResponse(**user.__dict__)

        return CustomResponse(data=response)

    async def delete(self, db: Session, id: int, current_user: User):
        if current_user is None:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        if id != current_user.id:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        if id is None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Id is required"
            )

        crud.user.remove(db, id=id)

        return CustomResponse(msg="User has been deleted successfully")


user_service = UserService()

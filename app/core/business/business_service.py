from sqlalchemy.orm import Session

from app import crud
from app.core.auth.jwt.auth_handler import token_manager
from app.storage.s3 import s3_service
from app.core.business.business_helper import business_hepler
from app.model import ManagerBase
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.schema import (
    business as schema_business,
    page as schema_page,
    manager_base as schema_manager_base,
)
from app.hepler.enum import Role


class BusinessService:
    async def get_me(self, db: Session, current_user: ManagerBase):
        if current_user is None:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        response = business_hepler.get_info(db, current_user)

        return CustomResponse(data=response)

    async def get_by_email(self, db: Session, data: dict):
        business_data = schema_business.BusinessGetByEmailRequest(**data)

        business = crud.manager_base.get_by_email(db, business_data.email)
        if not business:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
            )

        response = business_hepler.get_info(db, business)

        return CustomResponse(data=response)

    async def get_by_id(self, db: Session, id: int):
        business = crud.manager_base.get(db, id)
        if not business:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
            )

        response = business_hepler.get_info(db, business)

        return CustomResponse(data=response)

    async def get(self, db: Session, data: dict):
        page = schema_page.Pagination(**data)

        businesss = crud.manager_base.get_multi(db, **page.model_dump())
        if not businesss:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Businesss not found"
            )

        response = [business_hepler.get_info(db, business) for business in businesss]

        return CustomResponse(data=response)

    async def create(self, db: Session, data: dict):
        data["role"] = Role.BUSINESS
        manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
        business_data = schema_business.BusinessCreateRequest(**data)

        manager_base = crud.manager_base.get_by_email(db, manager_base_data.email)
        if manager_base:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT, msg="Email already registered"
            )

        avatar = manager_base_data.avatar
        if avatar:
            key = avatar.filename
            s3_service.upload_file(avatar, key)
            manager_base_data.avatar = key
        province = crud.province.get(db, business_data.province_id)
        if not province:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Province not found"
            )

        if business_data.district_id is not None:
            district = crud.district.get(db, business_data.district_id)
            districts = province.district
            if district not in districts:

                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="District not found"
                )

        manager_base = crud.manager_base.create(
            db,
            obj_in=manager_base_data,
        )

        business_input = dict(business_data)
        business_input["id"] = manager_base.id
        business = crud.business.create(
            db,
            obj_in=business_input,
        )

        business_response = business_hepler.get_info(db, manager_base)
        access_token = token_manager.signJWT(manager_base)
        refresh_token = token_manager.signJWTRefreshToken(manager_base)

        return CustomResponse(
            status_code=status.HTTP_201_CREATED,
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": business_response,
            },
        )

    async def update(self, db: Session, data: dict, current_user: ManagerBase):
        if data["id"] != current_user.id:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Permission denied"
            )

        business = schema_business.BusinessUpdateRequest(**data)
        manager_base = schema_manager_base.ManagerBaseUpdateRequest(**data)

        avatar = manager_base.avatar
        if avatar:
            key = avatar.filename
            s3_service.upload_file(avatar, key)
            manager_base.avatar = key
        if business.province_id:
            province = crud.province.get(db, business.province_id)
            if not province:

                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="Province not found"
                )

        if business.district_id:
            district = crud.district.get(db, business.district_id)
            districts = province.district
            if district not in districts:
                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="District not found"
                )

        manager_base = crud.manager_base.update(
            db=db, db_obj=current_user, obj_in=manager_base
        )
        business = crud.business.update(
            db=db, db_obj=current_user.business, obj_in=business
        )
        response = business_hepler.get_info(db, manager_base)

        return CustomResponse(data=response)

    async def delete(self, db: Session, id: int, current_user: ManagerBase):
        if current_user is None or id != current_user.id:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        crud.manager_base.remove(db, id=id)

        return CustomResponse(msg="Business has been deleted successfully")

    async def set_user_active(self, db: Session, id: int, active: bool):
        if id is None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Id is required"
            )

        manager_base = crud.manager_base.get(db, id)
        response = crud.manager_base.set_active(db, manager_base, active)

        return CustomResponse(data=response)


business_service = BusinessService()

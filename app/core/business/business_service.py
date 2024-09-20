from sqlalchemy.orm import Session

from app import crud
from app.core import constant
from app.core.auth.jwt.auth_handler import token_manager
from app.storage.s3 import s3_service
from .business_helper import business_hepler
from app.model import ManagerBase


class BusinessService:
    async def get_me(self, db: Session, current_user: ManagerBase):
        if current_user is None:
            return constant.ERROR, 401, "Unauthorized"

        business_reseponse = business_hepler.get_info(db, current_user)

        return constant.SUCCESS, 200, business_reseponse

    async def get_by_email(self, db: Session, data: dict):
        business_data = business_hepler.validate_get_by_email(data)

        business = crud.manager_base.get_by_email(db, business_data.email)
        if not business:
            return constant.ERROR, 404, "Businesss not found"

        business_response = business_hepler.get_info(db, business)

        return constant.SUCCESS, 200, business_response

    async def get_by_id(self, db: Session, id: int):
        business = crud.manager_base.get(db, id)
        if not business:
            return constant.ERROR, 404, "Business not found"

        business_response = business_hepler.get_info(db, business)

        return constant.SUCCESS, 200, business_response

    async def get(self, db: Session, data: dict):
        page = business_hepler.validate_pagination(data)

        businesss = crud.manager_base.get_multi(db, **page.model_dump())
        if not businesss:
            return constant.ERROR, 404, "businesss not found"
        businesss = [business_hepler.get_info(db, business) for business in businesss]
        return constant.SUCCESS, 200, businesss

    async def create(self, db: Session, data: dict):
        data, manager_base_data, business_data = business_hepler.validate_create(data)

        manager_base = crud.manager_base.get_by_email(db, manager_base_data.email)
        if manager_base:
            return constant.ERROR, 409, "Email already registered"
        avatar = manager_base_data.avatar
        if avatar:
            key = avatar.filename
            s3_service.upload_file(avatar, key)
            manager_base_data.avatar = key
        province = crud.province.get(db, business_data.province_id)
        if not province:
            return constant.ERROR, 404, "Province not found"
        if business_data.district_id is not None:
            district = crud.district.get(db, business_data.district_id)
            districts = province.district
            if district not in districts:
                return constant.ERROR, 404, "District not found"

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

        response = (
            constant.SUCCESS,
            201,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": business_response,
            },
        )
        return response

    async def update(self, db: Session, data: dict, current_user: ManagerBase):
        if data["id"] != current_user.id:
            return constant.ERROR, 401, "Permission denied"
        business, manager_base = business_hepler.validate_update(data)

        avatar = manager_base.avatar
        if avatar:
            key = avatar.filename
            s3_service.upload_file(avatar, key)
            manager_base.avatar = key
        if business.province_id:
            province = crud.province.get(db, business.province_id)
            if not province:
                return constant.ERROR, 404, "Province not found"

        if business.district_id:
            district = crud.district.get(db, business.district_id)
            districts = province.district
            if district not in districts:
                return constant.ERROR, 404, "District not found"

        manager_base = crud.manager_base.update(
            db=db, db_obj=current_user, obj_in=manager_base
        )
        business = crud.business.update(
            db=db, db_obj=current_user.business, obj_in=business
        )
        business_response = business_hepler.get_info(db, manager_base)

        return constant.SUCCESS, 200, business_response

    async def delete(self, db: Session, id: int, current_user: ManagerBase):
        if current_user is None:
            return constant.ERROR, 401, "Unauthorized"
        if id != current_user.id:
            return constant.ERROR, 401, "Unauthorized"
        if id is None:
            return constant.ERROR, 400, "Id is required"
        crud.manager_base.remove(db, id=id)
        response = constant.SUCCESS, 200, "Business has been deleted successfully"
        return response

    async def set_user_active(self, db: Session, id: int, active: bool):
        if id is None:
            return constant.ERROR, 400, "Id is required"
        manager_base = crud.manager_base.get(db, id)
        response = (
            constant.SUCCESS,
            200,
            crud.manager_base.set_active(db, manager_base, active),
        )
        return response


business_service = BusinessService()

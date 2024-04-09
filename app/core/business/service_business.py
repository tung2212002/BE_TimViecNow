from sqlalchemy.orm import Session

from app.core.security import pwd_context
from app.crud.manager_base import manager_base as manager_baseCRUD
from app.crud.business import business as businessCRUD
from app.crud.province import province as provinceCRUD
from app.crud.district import district as districtCRUD
from app.core import constant
from app.schema import (
    business as schema_business,
    page as schema_page,
    manager_base as schema_manager_base,
    province as schema_province,
    admin as schema_admin,
    district as schema_district,
)
from app.core.auth.service_business_auth import signJWT, signJWTRefreshToken
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role, TypeAccount
from app.model import ManagerBase, Business, Province, District


def get_me(current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"

    business_reseponse = get_info_user(current_user)

    return constant.SUCCESS, 200, business_reseponse


def get_business_by_email(db: Session, data: dict):
    try:
        business_data = schema_business.BusinessGetByEmailRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    business = manager_baseCRUD.get_by_email(db, business_data.email)
    if not business:
        return constant.ERROR, 404, "Businesss not found"

    business_response = get_info_user(business)

    return constant.SUCCESS, 200, business_response


def get_business_by_id(db: Session, id: int):
    business = manager_baseCRUD.get(db, id)
    if not business:
        return constant.ERROR, 404, "Business not found"

    business_response = get_info_user(business)

    return constant.SUCCESS, 200, business_response


def get_list_business(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    businesss = manager_baseCRUD.get_multi(db, **page.dict())
    if not businesss:
        return constant.ERROR, 404, "businesss not found"
    businesss = [get_info_user(business) for business in businesss]
    return constant.SUCCESS, 200, businesss


def create_business(db: Session, data: dict):
    try:
        data["role"] = Role.BUSINESS
        manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
        business_data = schema_business.BusinessCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    manager_base = manager_baseCRUD.get_by_email(db, manager_base_data.email)
    if manager_base:
        return constant.ERROR, 409, "Email already registered"
    province = provinceCRUD.get(db, business_data.province_id)
    if not province:
        return constant.ERROR, 404, "Province not found"
    if business_data.district_id is not None:
        district = districtCRUD.get(db, business_data.district_id)
        districts = province.district
        if district not in districts:
            return constant.ERROR, 404, "District not found"

    manager_base = manager_baseCRUD.create(
        db,
        obj_in=manager_base_data,
    )

    business_input = dict(business_data)
    business_input["manager_base_id"] = manager_base.id
    business = businessCRUD.create(
        db,
        obj_in=business_input,
    )

    business_response = get_info_user(manager_base)
    access_token = signJWT(manager_base)
    refresh_token = signJWTRefreshToken(manager_base)

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


def update_business(db: Session, data: dict, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if current_user.role != Role.BUSINESS:
        return constant.ERROR, 401, "Unauthorized"
    if data["id"] != current_user.id:
        return constant.ERROR, 401, "Unauthorized"
    try:
        business = schema_business.BusinessUpdateRequest(**data)
        manager_base = schema_manager_base.ManagerBaseUpdateRequest(**data)
    except Exception as e:
        error = [f'{error["loc"][0]}: {error["msg"]}' for error in e.errors()]
        return constant.ERROR, 400, error

    if business.province_id:
        province = provinceCRUD.get(db, business.province_id)
        if not province:
            return constant.ERROR, 404, "Province not found"

    if business.district_id:
        district = districtCRUD.get(db, business.district_id)
        districts = province.district
        if district not in districts:
            return constant.ERROR, 404, "District not found"

    manager_base = manager_baseCRUD.update(
        db=db, db_obj=current_user, obj_in=manager_base
    )
    business = businessCRUD.update(db=db, db_obj=current_user.business, obj_in=business)
    business_response = get_info_user(manager_base)

    return constant.SUCCESS, 200, business_response


def delete_business(db: Session, id: int, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if id != current_user.id:
        return constant.ERROR, 401, "Unauthorized"
    if id is None:
        return constant.ERROR, 400, "Id is required"
    response = constant.SUCCESS, 200, manager_baseCRUD.remove(db, id)
    return response


def set_user_active(db: Session, id: int, active: bool):
    if id is None:
        return constant.ERROR, 400, "Id is required"
    manager_base = manager_baseCRUD.get(db, id)
    response = (
        constant.SUCCESS,
        200,
        manager_baseCRUD.set_active(db, manager_base, active),
    )
    return response


def get_info_user(manager_base):
    role = manager_base.role
    if role == Role.ADMIN or role == Role.SUPER_USER:
        admin = manager_base.admin
        if not admin:
            return schema_manager_base.ManagerBaseItemResponse(**manager_base.__dict__)
        data_response = {**admin.__dict__, **manager_base.__dict__}
        user = schema_admin.AdminItemResponse(**data_response)
        return user

    business = manager_base.business
    data_response = {**business.__dict__, **manager_base.__dict__}
    user = schema_business.BusinessItemResponse(**data_response)

    province = schema_province.ProvinceItemResponse(**business.province.__dict__)
    district = (
        schema_district.DistrictItemResponse(**business.district.__dict__)
        if business.district
        else None
    )

    return {
        **user.__dict__,
        "province": province,
        "district": district,
    }

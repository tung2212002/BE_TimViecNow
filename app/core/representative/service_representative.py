from sqlalchemy.orm import Session

from app.core.security import pwd_context
from app.crud.manager_base import manager_base as manager_baseCRUD
from app.crud.representative import representative as representativeCRUD
from app.crud.province import province as provinceCRUD
from app.crud.district import district as districtCRUD
from app.core import constant
from app.schema import (
    representative as schema_representative,
    page as schema_page,
    manager_base as schema_manager_base,
    province as schema_province,
)
from app.core.auth.service_business_auth import signJWT
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role


def get_me(current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    user = schema_representative.RepresentativeItemResponse(**current_user.__dict__)
    return constant.SUCCESS, 200, user


def get_user_by_email(db: Session, data: dict):
    try:
        user_data = schema_representative.RepresentativeGetRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    user = representativeCRUD.get_by_email(db, user_data.email)
    if not user:
        return constant.ERROR, 404, "User not found"
    user = schema_representative.RepresentativeItemResponse(**user.__dict__)
    return constant.SUCCESS, 200, user


def get_user_by_id(db: Session, id: int):
    user = representativeCRUD.get(db, id)
    if not user:
        return constant.ERROR, 404, "User not found"
    user = schema_representative.RepresentativeItemResponse(**user.__dict__)
    return constant.SUCCESS, 200, user


def get_list_user(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    users = representativeCRUD.get_multi(db, **page.dict())
    if not users:
        return constant.ERROR, 404, "Users not found"
    users = [
        schema_representative.RepresentativeItemResponse(**user.__dict__)
        for user in users
    ]
    return constant.SUCCESS, 200, users


def create_user(db: Session, data: dict):
    try:
        data["role"] = Role.REPRESENTATIVE
        manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
        user_data = schema_representative.RepresentativeCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    manager_base = manager_baseCRUD.get_by_email(db, manager_base_data.email)
    if manager_base:
        return constant.ERROR, 409, "Email already registered"
    province = provinceCRUD.get(db, user_data.province_id)
    if not province:
        return constant.ERROR, 404, "Province not found"
    if user_data.district_id:
        district = districtCRUD.get(db, user_data.district_id)
        if not district:
            return constant.ERROR, 404, "District not found"

    manager_base = manager_baseCRUD.create(
        db,
        obj_in=manager_base_data,
    )

    user_input = dict(user_data)
    user_input["manager_base_id"] = manager_base.id
    user = representativeCRUD.create(
        db,
        obj_in=user_input,
    )

    manager_base.id
    data_response = {
        **manager_base.__dict__,
        **user.__dict__,
    }
    user_response = schema_representative.RepresentativeItemResponse(**data_response)
    province = schema_province.ProvinceItemResponse(**user.province.__dict__)
    district = (
        schema_province.DistrictItemResponse(**user.district.__dict__)
        if user.district
        else None
    )

    token = {
        "email": user_response.email,
        "id": user_response.id,
        "is_active": user_response.is_active,
        "role": user_response.role,
        "type": "access_token",
    }
    access_token = signJWT(token)
    token["type"] = "refresh_token"
    refresh_token = signJWT(token)

    response = (
        constant.SUCCESS,
        201,
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                **user_response.__dict__,
                "province": province,
                "district": district,
            },
        },
    )
    return response


def update_user(db: Session, data: dict, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if data["email"] != current_user.email:
        return constant.ERROR, 401, "Unauthorized"

    try:
        user = schema_representative.UserUpdate(**data)
    except Exception as e:
        error = [f'{error["loc"][0]}: {error["msg"]}' for error in e.errors()]
        return constant.ERROR, 400, error

    user_update = representativeCRUD.update(data["email"], data, db)
    user_update = schema_representative.RepresentativeItemResponse(
        **user_update.__dict__
    )
    response = (constant.SUCCESS, 200, user_update)
    return response


def delete_user(db: Session, email: str, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if email != current_user.email:
        return constant.ERROR, 401, "Unauthorized"
    if email is None:
        return constant.ERROR, 400, "Email is required"
    response = constant.SUCCESS, 200, representativeCRUD.delete(email, db)
    return response


def set_user_active(db: Session, id: int, active: bool):
    if id is None:
        return constant.ERROR, 400, "Id is required"
    response = constant.SUCCESS, 200, representativeCRUD.set_active(db, id, active)
    return response

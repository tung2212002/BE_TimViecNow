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
    admin as schema_admin,
    district as schema_district,
)
from app.core.auth.service_business_auth import signJWT, signJWTRefreshToken
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role, TypeAccount


def get_me(current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"

    representative_reseponse = get_info_user(current_user)

    return constant.SUCCESS, 200, representative_reseponse


def get_representative_by_email(db: Session, data: dict):
    try:
        representative_data = schema_representative.RepresentativeGetByEmailRequest(
            **data
        )
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    representative = manager_baseCRUD.get_by_email(db, representative_data.email)
    if not representative:
        return constant.ERROR, 404, "Representatives not found"

    representative_response = get_info_user(representative)

    return constant.SUCCESS, 200, representative_response


def get_representative_by_id(db: Session, id: int):
    representative = manager_baseCRUD.get(db, id)
    if not representative:
        return constant.ERROR, 404, "Representative not found"

    representative_response = get_info_user(representative)

    return constant.SUCCESS, 200, representative_response


def get_list_representative(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    representatives = manager_baseCRUD.get_multi(db, **page.dict())
    if not representatives:
        return constant.ERROR, 404, "Representatives not found"
    representatives = [
        get_info_user(representative) for representative in representatives
    ]
    return constant.SUCCESS, 200, representatives


def create_representative(db: Session, data: dict):
    try:
        data["role"] = Role.REPRESENTATIVE
        manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
        representative_data = schema_representative.RepresentativeCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    manager_base = manager_baseCRUD.get_by_email(db, manager_base_data.email)
    if manager_base:
        return constant.ERROR, 409, "Email already registered"
    province = provinceCRUD.get(db, representative_data.province_id)
    if not province:
        return constant.ERROR, 404, "Province not found"
    if representative_data.district_id:
        district = districtCRUD.get(db, representative_data.district_id)
        districts = province.district
        if district not in districts:
            return constant.ERROR, 404, "District not found"

    manager_base = manager_baseCRUD.create(
        db,
        obj_in=manager_base_data,
    )

    representative_input = dict(representative_data)
    representative_input["manager_base_id"] = manager_base.id
    representative = representativeCRUD.create(
        db,
        obj_in=representative_input,
    )

    manager_base.id
    data_response = {
        **representative.__dict__,
        **manager_base.__dict__,
    }
    representative_response = schema_representative.RepresentativeItemResponse(
        **data_response
    )
    province = schema_province.ProvinceItemResponse(**representative.province.__dict__)
    district = (
        schema_district.DistrictItemResponse(**representative.district.__dict__)
        if representative.district
        else None
    )

    token = {
        "email": representative_response.email,
        "id": representative_response.id,
        "is_active": representative_response.is_active,
        "role": representative_response.role,
        "type": "access_token",
        "type_account": TypeAccount.BUSINESS,
    }
    access_token = signJWT(token)
    token["type"] = "refresh_token"
    refresh_token = signJWTRefreshToken(token)

    response = (
        constant.SUCCESS,
        201,
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                **representative_response.__dict__,
                "province": province,
                "district": district,
            },
        },
    )
    return response


def update_representative(db: Session, data: dict, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if current_user.role != Role.REPRESENTATIVE:
        return constant.ERROR, 401, "Unauthorized"
    if data["id"] != current_user.id:
        return constant.ERROR, 401, "Unauthorized"
    try:
        representative = schema_representative.RepresentativeUpdateRequest(**data)
        manager_base = schema_manager_base.ManagerBaseUpdateRequest(**data)
    except Exception as e:
        error = [f'{error["loc"][0]}: {error["msg"]}' for error in e.errors()]
        return constant.ERROR, 400, error

    if representative.province_id:
        province = provinceCRUD.get(db, representative.province_id)
        if not province:
            return constant.ERROR, 404, "Province not found"

    if representative.district_id:
        district = districtCRUD.get(db, representative.district_id)
        districts = province.district
        if district not in districts:
            return constant.ERROR, 404, "District not found"

    manager_base = manager_baseCRUD.update(
        db=db, db_obj=current_user, obj_in=manager_base
    )
    representative = representativeCRUD.update(
        db=db, db_obj=current_user.representative, obj_in=representative
    )
    representative_response = get_info_user(manager_base)

    return constant.SUCCESS, 200, representative_response


def delete_representative(db: Session, id: int, current_user):
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

    representative = manager_base.representative
    data_response = {**representative.__dict__, **manager_base.__dict__}
    user = schema_representative.RepresentativeItemResponse(**data_response)

    province = schema_province.ProvinceItemResponse(**representative.province.__dict__)
    district = (
        schema_district.DistrictItemResponse(**representative.district.__dict__)
        if representative.district
        else None
    )

    return {
        **user.__dict__,
        "province": province,
        "district": district,
    }

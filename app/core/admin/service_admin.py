from sqlalchemy.orm import Session

from app.core.security import pwd_context
from app.crud.manager_base import manager_base as manager_baseCRUD
from app.crud.representative import representative as representativeCRUD
from app.crud.province import province as provinceCRUD
from app.crud.district import district as districtCRUD
from app.crud.admin import admin as adminCRUD
from app.core import constant
from app.schema import (
    representative as schema_representative,
    page as schema_page,
    manager_base as schema_manager_base,
    province as schema_province,
    admin as schema_admin,
)
from app.core.auth.service_business_auth import signJWT, signJWTRefreshToken
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role, TypeAccount
from app.core.representative.service_representative import get_info_user


def get_admin_by_email(db: Session, data: dict):
    try:
        admin_data = schema_admin.AdminGetByEmailRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    admin = manager_baseCRUD.get_by_email(db, admin_data.email)
    if not admin:
        return constant.ERROR, 404, "Admin not found"

    admin_response = get_info_user(admin)

    return constant.SUCCESS, 200, admin_response


def get_admin_by_id(db: Session, id: int):
    admin = manager_baseCRUD.get_by_admin(db, id)
    if not admin:
        return constant.ERROR, 404, "Admin not found"

    admin_response = get_info_user(admin)

    return constant.SUCCESS, 200, admin_response


def get_list_admin(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    admins = manager_baseCRUD.get_multi_by_admin(db, **page.dict())
    if not admins:
        return constant.ERROR, 404, "Admin not found"
    admin = [get_info_user(admin) for admin in admins]
    return constant.SUCCESS, 200, admin


def create_admin(db: Session, data: dict):
    try:
        data["role"] = Role.ADMIN
        manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
        admin_data = schema_admin.AdminCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    manager_base = manager_baseCRUD.get_by_email(db, manager_base_data.email)
    if manager_base:
        return constant.ERROR, 409, "Email already registered"

    manager_base = manager_baseCRUD.create(
        db,
        obj_in=manager_base_data,
    )

    admin_input = dict(admin_data)
    admin_input["manager_base_id"] = manager_base.id
    admin = adminCRUD.create(
        db,
        obj_in=admin_input,
    )

    manager_base.id
    data_response = {
        **admin.__dict__,
        **manager_base.__dict__,
    }
    admin_response = schema_admin.AdminItemResponse(**data_response)

    token = {
        "email": admin_response.email,
        "id": admin_response.id,
        "is_active": admin_response.is_active,
        "role": admin_response.role,
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
                **admin_response.__dict__,
            },
        },
    )
    return response


def update_admin(db: Session, data: dict, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if data["id"] != current_user.id:
        return constant.ERROR, 401, "Unauthorized"
    try:
        admin = schema_admin.AdminUpdateRequest(**data)
        manager_base = schema_manager_base.ManagerBaseUpdateRequest(**data)
    except Exception as e:
        error = [f'{error["loc"][0]}: {error["msg"]}' for error in e.errors()]
        return constant.ERROR, 400, error

    manager_base = manager_baseCRUD.update(db, current_user, manager_base)
    admin = adminCRUD.update(
        db=db,
        db_obj=current_user,
        obj_in=admin,
    )
    admin_response = get_info_user(manager_base)

    return constant.SUCCESS, 200, admin_response


def delete_admin(db: Session, id: int, current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    if id != current_user.id and current_user.role != Role.SUPER_USER:
        return constant.ERROR, 401, "Unauthorized"
    if id is None:
        return constant.ERROR, 400, "Id is required"
    manager_baseCRUD.remove(db, id)
    response = constant.SUCCESS, 200, "Admin has been deleted successfully"
    return response

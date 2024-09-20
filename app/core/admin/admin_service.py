from sqlalchemy.orm import Session

from app.crud.manager_base import manager_base as manager_baseCRUD
from app.crud.admin import admin as adminCRUD
from app.core import constant
from app.schema import (
    page as schema_page,
    manager_base as schema_manager_base,
    admin as schema_admin,
)
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role
from app.core.business.business_helper import business_hepler


class AdminService:
    async def get_by_email(self, db: Session, data: dict):
        try:
            admin_data = schema_admin.AdminGetByEmailRequest(**data)
        except Exception as e:
            return constant.ERROR, 400, get_message_validation_error(e)
        admin = manager_baseCRUD.get_by_email(db, admin_data.email)
        if not admin:
            return constant.ERROR, 404, "Admin not found"

        admin_response = await business_hepler.get_info(db, admin)

        return constant.SUCCESS, 200, admin_response

    async def get_by_id(self, db: Session, id: int):
        admin = manager_baseCRUD.get_by_admin(db, id)
        if not admin:
            return constant.ERROR, 404, "Admin not found"

        admin_response = await business_hepler.get_info(db, admin)

        return constant.SUCCESS, 200, admin_response

    async def get(self, db: Session, data: dict):
        try:
            page = schema_page.Pagination(**data)
        except Exception as e:
            return constant.ERROR, 400, get_message_validation_error(e)
        admins = manager_baseCRUD.get_list_admin(db, **page.model_dump())
        if not admins:
            return constant.ERROR, 404, "Admin not found"
        admin = await [business_hepler.get_info(db, admin) for admin in admins]
        return constant.SUCCESS, 200, admin

    async def create(self, db: Session, data: dict):
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
        admin_input["id"] = manager_base.id
        admin = adminCRUD.create(
            db,
            obj_in=admin_input,
        )

        admin_response = await business_hepler.get_info(db, manager_base)

        access_token = token_manager.signJWT(admin_response)
        refresh_token = token_manager.signJWTRefreshToken(admin_response)

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

    async def update(self, db: Session, data: dict, current_user):
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
        admin_response = business_hepler.get_info(db, manager_base)

        return constant.SUCCESS, 200, admin_response

    async def delete(self, db: Session, id: int, current_user):
        if current_user is None:
            return constant.ERROR, 401, "Unauthorized"
        if id != current_user.id and current_user.role != Role.SUPER_USER:
            return constant.ERROR, 401, "Unauthorized"
        if id is None:
            return constant.ERROR, 400, "Id is required"
        manager_baseCRUD.remove(db, id)
        response = constant.SUCCESS, 200, "Admin has been deleted successfully"
        return response


admin_service = AdminService()

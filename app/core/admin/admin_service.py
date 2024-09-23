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
from app.hepler.enum import Role
from app.core.business.business_helper import business_hepler
from app.common.exception import CustomException
from app.model import ManagerBase
from fastapi import status
from app.common.response import CustomResponse


class AdminService:
    async def get_by_email(self, db: Session, data: dict):
        admin_data = schema_admin.AdminGetByEmailRequest(**data)

        admin = manager_baseCRUD.get_by_email(db, admin_data.email)
        if not admin:
            raise CustomException(status_code=404, msg="Admin not found")

        admin_response = await business_hepler.get_info(db, admin)

        return CustomResponse(data=admin_response)

    async def get_by_id(self, db: Session, id: int):
        admin = manager_baseCRUD.get_by_admin(db, id)
        if not admin:
            raise CustomException(status_code=404, msg="Admin not found")

        admin_response = await business_hepler.get_info(db, admin)

        return CustomResponse(data=admin_response)

    async def get(self, db: Session, data: dict):
        page = schema_page.Pagination(**data)

        admins = manager_baseCRUD.get_list_admin(db, **page.model_dump())
        if not admins:
            raise CustomException(status_code=404, msg="Admin not found")

        admin = await [business_hepler.get_info(db, admin) for admin in admins]

        return CustomResponse(data=admin)

    async def create(self, db: Session, data: dict):
        data["role"] = Role.ADMIN
        manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
        admin_data = schema_admin.AdminCreateRequest(**data)

        manager_base = manager_baseCRUD.get_by_email(db, manager_base_data.email)
        if manager_base:
            raise CustomException(status_code=409, msg="Email already registered")

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

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                **admin_response.__dict__,
            },
        }
        return CustomResponse(status_code=201, data=response)

    async def update(self, db: Session, data: dict, current_user: ManagerBase):
        if current_user is None:
            return constant.ERROR, 401, "Unauthorized"
        if data["id"] != current_user.id:
            return constant.ERROR, 401, "Unauthorized"

        admin = schema_admin.AdminUpdateRequest(**data)
        manager_base = schema_manager_base.ManagerBaseUpdateRequest(**data)

        manager_base = manager_baseCRUD.update(db, current_user, manager_base)
        admin = adminCRUD.update(
            db=db,
            db_obj=current_user,
            obj_in=admin,
        )
        admin_response = business_hepler.get_info(db, manager_base)

        return CustomResponse(data=admin_response)

    async def delete(self, db: Session, id: int, current_user: ManagerBase):
        if current_user is None or (
            id != current_user.id and current_user.role != Role.SUPER_USER
        ):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        if id is None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Id is required"
            )

        manager_baseCRUD.remove(db, id)

        return CustomResponse(msg="Admin has been deleted successfully")


admin_service = AdminService()

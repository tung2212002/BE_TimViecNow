from sqlalchemy.orm import Session
from fastapi import status

from app.crud.manager import manager as managerCRUD
from app.crud.admin import admin as adminCRUD
from app.crud.account import account as accountCRUD
from app.core import constant
from app.schema.page import Pagination
from app.schema.account import AccountCreate, AccountUpdate
from app.schema.manager import ManagerCreate, ManagerUpdate
from app.schema.admin import (
    AdminCreateRequest,
    AdminUpdateRequest,
    AdminGetByEmailRequest,
    AdminCreate,
    AdminUpdate,
    AdminItemResponse,
)
from app.core.auth.jwt.auth_handler import token_manager
from app.hepler.enum import Role
from app.core.admin.admin_helper import admin_helper
from app.common.exception import CustomException
from app.model import Manager, Account, Admin
from fastapi import status
from app.common.response import CustomResponse


class AdminService:
    async def get_by_email(self, db: Session, data: dict):
        admin_data = AdminGetByEmailRequest(**data)

        admin = managerCRUD.get_by_email(db, admin_data.email)
        if not admin:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Admin not found"
            )

        admin_response = await admin_helper.get_info_by_admin(db, admin)

        return CustomResponse(data=admin_response)

    async def get_by_id(self, db: Session, id: int):
        admin = adminCRUD.get(db, id)
        if not admin:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Admin not found"
            )

        admin_response = await admin_helper.get_info_by_admin(db, admin)

        return CustomResponse(data=admin_response)

    async def get(self, db: Session, data: dict):
        page = Pagination(**data)

        admins = managerCRUD.get_multi(db, **page.model_dump())
        if not admins:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Admin not found"
            )

        admin = await [admin_helper.get_info_by_admin(db, admin) for admin in admins]

        return CustomResponse(data=admin)

    async def create(self, db: Session, data: dict):
        data["role"] = Role.ADMIN
        admin_data = AdminCreateRequest(**data)

        manager = managerCRUD.get_by_email(db, admin_data.email)
        if manager:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT, msg="Email already registered"
            )

        account = accountCRUD.create(
            db, obj_in=AccountCreate(**admin_data.model_dump())
        )
        manager = managerCRUD.create(
            db, obj_in=ManagerCreate(**admin_data.model_dump(), id=account.id)
        )
        admin = adminCRUD.create(
            db, obj_in=AdminCreate(**admin_data.model_dump(), id=manager.id)
        )

        admin_response: AdminItemResponse = await admin_helper.get_info(
            db, account, manager, admin
        )
        payload = {
            "role": Role.ADMIN,
            "id": admin_response.id,
        }

        access_token = token_manager.signJWT(payload)
        refresh_token = token_manager.signJWTRefreshToken(payload)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": admin_response,
        }

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def update(self, db: Session, data: dict, current_user: Account):
        admin_data = AdminUpdateRequest(**data)

        manager: Manager = current_user.manager
        admin: Admin = manager.admin

        account = accountCRUD.update(
            db=db,
            db_obj=current_user,
            obj_in=AccountUpdate(**admin_data.model_dump()),
        )
        manager = managerCRUD.update(
            db, db_obj=manager, obj_in=ManagerUpdate(**admin_data.model_dump())
        )
        admin = adminCRUD.update(
            db=db,
            db_obj=admin,
            obj_in=AdminUpdate(**admin_data.model_dump()),
        )

        admin_response = admin_helper.get_info(db, account, manager, admin)

        return CustomResponse(data=admin_response)

    async def delete(self, db: Session, id: int, current_user: Account):
        if id != current_user.id and not adminCRUD.is_superuser(current_user):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                msg="Unauthorized",
            )

        if id is None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Id is required"
            )

        managerCRUD.remove(db, id)

        return CustomResponse(msg="Admin has been deleted successfully")


admin_service = AdminService()

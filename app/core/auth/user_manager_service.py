from fastapi import HTTPException, status, Depends, Request
from typing import List
from datetime import datetime, timezone

from app import crud
from app.db.base import CurrentSession
from app.core.auth.jwt.auth_bearer import JWTBearer
from app import crud
from app.core import constant
from app.hepler.enum import Role, TypeAccount, VerifyType
from app.core.security import PasswordManager
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


class UserManagerService:
    def __init__(self):
        self.db = CurrentSession

    def get_current_user(self, data: dict = Depends(JWTBearer())):
        token_decode = data["payload"]
        if token_decode["type_account"] != TypeAccount.NORMAL:
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = data["token"]
        if self.check_blacklist(self.db, token):
            raise HTTPException(status_code=401, detail="Token revoked")
        id = token_decode["id"]
        if token_decode["role"] == Role.USER:
            user = crud.user.get(self.db, id)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        elif token_decode["role"] == Role.SOCIAL_NETWORK:
            social_network = crud.social_network.get(self.db, id)
            if social_network is None:
                raise HTTPException(status_code=404, detail="User not found")
            if not social_network.is_verified:
                return social_network
            return social_network.user

    def get_current_business_by_role(self, data: dict, allowed_roles: List[Role]):
        token_decode = data["payload"]
        if token_decode["type_account"] != TypeAccount.BUSINESS:
            raise HTTPException(status_code=403, detail="Not permission")
        token = data["token"]
        if self.check_blacklist(token):
            raise HTTPException(status_code=401, detail="Token revoked")
        id = token_decode["id"]
        role = token_decode["role"]
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not permission")
        user = crud.manager_base.get_by_admin(id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_current_business_admin(self, data: dict = Depends(JWTBearer())):
        return self.get_current_business_by_role(data, [Role.BUSINESS, Role.ADMIN])

    def get_current_business_admin_superuser(self, data: dict = Depends(JWTBearer())):
        return self.get_current_business_by_role(
            data, [Role.BUSINESS, Role.ADMIN, Role.SUPER_USER]
        )

    def get_current_business(self, data: dict = Depends(JWTBearer())):
        return self.get_current_business_by_role(data, [Role.BUSINESS])

    def get_current_admin(self, data: dict = Depends(JWTBearer())):
        return self.get_current_business_by_role(data, [Role.ADMIN, Role.SUPER_USER])

    def get_current_superuser(self, data: dict = Depends(JWTBearer())):
        return self.get_current_business_by_role(data, [Role.SUPER_USER])

    def check_permission_business(
        current_user, roles: List[Role], business_id: int = None
    ):
        if business_id:
            if current_user.role not in [Role.SUPER_USER, Role.ADMIN]:
                if current_user.id != business_id:
                    custom_response_error(
                        status_code=403,
                        status=constant.ERROR,
                        response="Permission denied",
                    )
                else:
                    return Role.BUSINESS
        else:
            if current_user.role not in roles:
                custom_response_error(
                    status_code=403, status=constant.ERROR, response="Permission denied"
                )
            elif current_user.role == Role.BUSINESS:
                return Role.BUSINESS
        return Role.ADMIN

    def check_blacklist(self, token: str):
        return crud.blacklist.get_by_token(self.db, token)


user_manager_service = UserManagerService()

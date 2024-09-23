from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session

from app import crud
from app.db.base import get_db
from app.core.auth.jwt.auth_bearer import JWTBearer
from app import crud
from app.hepler.enum import Role, TypeAccount
from fastapi import status
from app.common.exception import CustomException
from app.model import ManagerBase


class UserManagerService:
    def get_current_user(
        self, data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):
        token_decode = data["payload"]
        if token_decode["type_account"] != TypeAccount.NORMAL:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Unauthorized"
            )

        token = data["token"]
        if self.check_blacklist(db, token):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Token revoked"
            )

        id = token_decode["id"]
        if token_decode["role"] == Role.USER:
            user = crud.user.get(db, id)
            if user is None:
                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
                )

            return user
        elif token_decode["role"] == Role.SOCIAL_NETWORK:
            social_network = crud.social_network.get(db, id)
            if social_network is None:
                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
                )

            if not social_network.is_verified:
                return social_network
            return social_network.user

    def get_current_business_by_role(self, db, data: dict, allowed_roles: List[Role]):
        token_decode = data["payload"]
        if token_decode["type_account"] != TypeAccount.BUSINESS:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Not permission"
            )

        token = data["token"]
        if self.check_blacklist(db, token):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, msg="Token revoked"
            )

        id = token_decode["id"]
        role = token_decode["role"]
        if role not in allowed_roles:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
            )

        user = crud.manager_base.get_by_admin(db, id)
        if user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="User not found"
            )

        return user

    def get_current_business_admin(
        self, data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):
        return self.get_current_business_by_role(db, data, [Role.BUSINESS, Role.ADMIN])

    def get_current_business_admin_superuser(
        self, data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):
        return self.get_current_business_by_role(
            db, data, [Role.BUSINESS, Role.ADMIN, Role.SUPER_USER]
        )

    def get_current_business(
        self, data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):
        return self.get_current_business_by_role(db, data, [Role.BUSINESS])

    def get_current_admin(
        self, data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):
        return self.get_current_business_by_role(
            db, data, [Role.ADMIN, Role.SUPER_USER]
        )

    def get_current_superuser(
        self, data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):
        return self.get_current_business_by_role(db, data, [Role.SUPER_USER])

    def check_permission_business(
        db: Session,
        current_user: ManagerBase,
        roles: List[Role],
        business_id: int = None,
    ):
        if business_id:
            if current_user.role not in [Role.SUPER_USER, Role.ADMIN]:
                if current_user.id != business_id:
                    raise CustomException(
                        status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
                    )

                else:
                    return Role.BUSINESS
        else:
            if current_user.role not in roles:
                raise CustomException(
                    status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
                )

            elif current_user.role == Role.BUSINESS:
                return Role.BUSINESS

        return Role.ADMIN

    def check_blacklist(self, db: Session, token: str):
        return crud.blacklist.get_by_token(db, token)


user_manager_service = UserManagerService()

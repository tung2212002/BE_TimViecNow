from typing import List

from app.hepler.enum import VerifyType
from app.model import Business
from app.common.exception import CustomException
from fastapi import status
from app.hepler.enum import Role
from app.model import ManagerBase


class BusinessAuthHelper:
    def verified_email(self, user: Business) -> bool:
        if not user.is_verified_email:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                msg="Email not verified",
            )

    def verified_phone(self, user: Business) -> bool:
        return True
        if not user.is_verified_phone:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                msg="Phone not verified",
            )

    def verified_company(self, user: Business) -> bool:
        if not user.is_verified_company:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                msg="Company not verified",
            )

    def verified_identity(self, user: Business) -> bool:
        if not user.is_verified_identity:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                msg="Indentity not verified",
            )

    def verified(self, user, verify_types: List[VerifyType]) -> None:
        for verify_type in verify_types:
            if verify_type == VerifyType.EMAIL:
                self.verified_email(user)
            elif verify_type == VerifyType.PHONE:
                self.verified_phone(user)
            elif verify_type == VerifyType.COMPANY:
                self.verified_company(user)
            elif verify_type == VerifyType.IDENTIFY:
                self.verified_identity(user)

    def verified_level(self, user, level: int) -> None:
        if level == 1:
            self.verified(user, [VerifyType.EMAIL])
        elif level == 2:
            self.verified(user, [VerifyType.EMAIL, VerifyType.PHONE])
        elif level == 3:
            self.verified(
                user, [VerifyType.EMAIL, VerifyType.PHONE, VerifyType.COMPANY]
            )
        elif level == 4:
            self.verified(
                user,
                [
                    VerifyType.EMAIL,
                    VerifyType.PHONE,
                    VerifyType.COMPANY,
                    VerifyType.IDENTIFY,
                ],
            )

    def check_permission_business(
        self, current_user: ManagerBase, roles: List[Role], business_id: int = None
    ) -> Role:
        if business_id:
            if current_user.role not in [Role.SUPER_USER, Role.ADMIN]:
                if current_user.id != business_id:
                    raise CustomException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        msg="Permission denied",
                    )
                else:
                    return Role.BUSINESS
        else:
            if current_user.role not in roles:
                raise CustomException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    msg="Permission denied",
                )
            elif current_user.role == Role.BUSINESS:
                return Role.BUSINESS
        return Role.ADMIN


business_auth_helper = BusinessAuthHelper()

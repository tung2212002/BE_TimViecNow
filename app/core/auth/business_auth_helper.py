from fastapi import HTTPException
from typing import List

from app.hepler.enum import VerifyType
from app.model import Business


class BusinessAuthHelper:
    def verified_email(self, user: Business) -> bool:
        try:
            if not user.is_verified_email:
                raise HTTPException(status_code=401, detail="Email not verified")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Email not verified")

    def verified_phone(self, user: Business) -> bool:
        return True
        if not user.is_verified_phone:
            raise HTTPException(status_code=401, detail="Phone not verified")

    def verified_company(self, user: Business) -> bool:
        try:
            if not user.is_verified_company:
                raise HTTPException(status_code=401, detail="Company not verified")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Company not verified")

    def verified_identity(self, user: Business) -> bool:
        if not user.is_verified_identity:
            raise HTTPException(status_code=401, detail="Indentity not verified")

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


business_auth_helper = BusinessAuthHelper()

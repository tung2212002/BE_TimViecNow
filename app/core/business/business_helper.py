from sqlalchemy.orm import Session

from app.model import ManagerBase
from app.hepler.enum import Role
from app.schema.admin import AdminItemResponse
from app.schema.business import (
    BusinessItemResponse,
)
from app.schema.manager_base import (
    ManagerBaseItemResponse,
)
from app.schema.province import ProvinceItemResponse
from app.schema.district import DistrictItemResponse

from app import crud
from app.core.company.company_helper import company_helper
from app.hepler.enum import Role


class BusinessHepler:
    def get_info(self, db: Session, user: ManagerBase):
        role = user.role
        if role in [Role.ADMIN, Role.SUPER_USER]:
            admin = user.admin
            if not admin:
                return ManagerBaseItemResponse(**user.__dict__)
            data_response = {**admin.__dict__, **user.__dict__}
            user = AdminItemResponse(**data_response)
            return user

        business = user.business
        data_response = {**business.__dict__, **user.__dict__}
        user = BusinessItemResponse(**data_response)

        province = ProvinceItemResponse(**business.province.__dict__)
        district = (
            DistrictItemResponse(**business.district.__dict__)
            if business.district
            else None
        )
        company = crud.company.get_by_business_id(db, business.id)
        company_response = company_helper.get_info(db, company)

        return {
            **user.__dict__,
            "province": province,
            "district": district,
            "company": company_response,
        }


business_hepler = BusinessHepler()

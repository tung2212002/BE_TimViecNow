from sqlalchemy.orm import Session
from typing import List, Tuple

from app.model import ManagerBase
from app.hepler.enum import Role
from app.schema import (
    admin as schema_admin,
    business as schema_business,
    manager_base as schema_manager_base,
    province as schema_province,
    district as schema_district,
    company as schema_company,
    page as schema_page,
)
from app import crud
from app.core.company import company_service
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.enum import Role


class BusinessHepler:
    def validate_get_by_email(
        self, db: Session, data: dict
    ) -> schema_business.BusinessGetByEmailRequest:
        try:
            return schema_business.BusinessGetByEmailRequest(**data)
        except Exception as e:
            return get_message_validation_error(e)

    def validate_pagination(self, data: dict) -> schema_page.Pagination:
        try:
            return schema_page.Pagination(**data)
        except Exception as e:
            return get_message_validation_error(e)

    def validate_create(self, data: dict) -> Tuple[
        dict,
        schema_manager_base.ManagerBaseCreateRequest,
        schema_business.BusinessCreateRequest,
    ]:
        try:
            data["role"] = Role.BUSINESS
            manager_base_data = schema_manager_base.ManagerBaseCreateRequest(**data)
            business_data = schema_business.BusinessCreateRequest(**data)
            return data, manager_base_data, business_data
        except Exception as e:
            return get_message_validation_error(e)

    def validate_update(self, data: dict) -> Tuple[
        schema_manager_base.ManagerBaseUpdateRequest,
        schema_business.BusinessUpdateRequest,
    ]:
        try:
            manager_base_data = schema_manager_base.ManagerBaseUpdateRequest(**data)
            business_data = schema_business.BusinessUpdateRequest(**data)
            return manager_base_data, business_data
        except Exception as e:
            return get_message_validation_error(e)

    def get_info(self, db: Session, user: ManagerBase):
        role = user.role
        if role in [Role.ADMIN, Role.SUPER_USER]:
            admin = user.admin
            if not admin:
                return schema_manager_base.ManagerBaseItemResponse(**user.__dict__)
            data_response = {**admin.__dict__, **user.__dict__}
            user = schema_admin.AdminItemResponse(**data_response)
            return user

        business = user.business
        data_response = {**business.__dict__, **user.__dict__}
        user = schema_business.BusinessItemResponse(**data_response)

        province = schema_province.ProvinceItemResponse(**business.province.__dict__)
        district = (
            schema_district.DistrictItemResponse(**business.district.__dict__)
            if business.district
            else None
        )
        company = crud.company.get_by_business_id(db, business.id)
        company_response = company_service.get_company_info(db, company)
        return {
            **user.__dict__,
            "province": province,
            "district": district,
            "company": company_response,
        }


business_hepler = BusinessHepler()

from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    company as schema_company,
    page as schema_page,
)
from app.hepler.enum import Role
from app.storage.s3 import s3_service
from app.core.auth.business_auth_helper import business_auth_helper
from app.core.field.field_helper import field_helper
from app.model import ManagerBase
from app.core.company.company_helper import company_helper
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.model import ManagerBase


class CompanyService:
    async def get(self, db: Session, data: dict, current_user: ManagerBase = None):
        page = schema_page.Pagination(**data)

        if (
            data.get("business_id")
            and current_user
            and current_user.role == Role.BUSINESS
        ):
            if data.get("business_id") != current_user.id:
                raise CustomException(
                    status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
                )

            company = current_user.business.company
            response = company_helper.get_info(db, company)

            return CustomResponse(data=response)

        companies = crud.company.get_multi(db, **page.model_dump())
        response = []
        if data.get("fields"):
            response = company_helper.get_list_info(db, companies, detail=True)
        else:
            response = company_helper.get_list_info(db, companies)

        return CustomResponse(data=response)

    async def search(self, db: Session, data: dict):
        page = schema_company.CompanyPagination(**data)

        total, companies = crud.company.search_multi(db, **page.model_dump())
        response = company_helper.get_list_info(db, companies, detail=True)

        return CustomResponse(
            data={
                "total": total,
                "companies": response,
            }
        )

    async def get_by_id(self, db: Session, company_id: int):
        company = crud.company.get(db, company_id)
        if not company:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Company not found"
            )

        response = company_helper.get_info(db, company)

        return CustomResponse(data=response)

    async def create(self, db: Session, data: dict, current_user: ManagerBase):
        business = current_user.business
        if not business:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
            )

        business_auth_helper.verified_level(business, 2)
        if crud.company.get_by_business_id(db=db, business_id=current_user.id):
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
            )

        if crud.company.get_company_by_tax_code(db, data.get("tax_code")):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Tax code already exists"
            )

        if crud.company.get_company_by_email(db, data.get("email")):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Email already exists"
            )

        company_data = schema_company.CompanyCreateRequest(**data)

        fields = company_data.fields
        if fields:
            field_helper.check_list_valid(db, fields)

        logo = company_data.logo
        if logo:
            key = logo.filename
            s3_service.upload_file(logo, key)
            company_data.logo = key

        if current_user.role == Role.BUSINESS:
            company_data = {
                **company_data.model_dump(),
                "business_id": current_user.id,
            }
        obj_in = schema_company.CompanyCreate(**company_data)
        company = crud.company.create(db, obj_in=obj_in)
        if fields:
            field_helper.create_with_company_id(db, company.id, fields)
        response = company_helper.get_private_info(db, company)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def update(self, db: Session, data: dict, current_user):
        company_id = data.get("company_id")
        company = crud.company.get(db, company_id)
        if not company:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Company not found"
            )

        if company.business_id != current_user.id:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
            )

        company_data = schema_company.CompanyUpdateRequest(**data)

        logo = company_data.logo
        new_fields = company_data.fields
        if new_fields:
            field_helper.check_list_valid(db, new_fields)
        if logo:
            key = logo.filename
            s3_service.upload_file(logo, key)
            company_data.logo = key

        obj_in = schema_company.CompanyUpdate(**company_data.model_dump())
        company = crud.company.update(db, db_obj=company, obj_in=obj_in)
        field_helper.update_with_company_id(db, company.id, new_fields)

        response = company_helper.get_private_info(db, company)

        return CustomResponse(data=response)

    async def delete(self, db: Session, company_id: int, current_user: ManagerBase):
        company = crud.company.get(db, company_id)
        business = current_user.business
        if not business:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
            )

        if not company:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Company not found"
            )

        if company.business_id != business.id:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Permission denied"
            )

        response = crud.company.remove(db, id=company_id)

        return CustomResponse(data=response)


company_service = CompanyService()

from sqlalchemy.orm import Session
from datetime import datetime

from app import crud
from app.schema import (
    company as schema_company,
)
from app.hepler.enum import Role
from app.core import constant
from app.storage.s3 import s3_service
from app.core.auth.business_auth_helper import business_auth_helper
from app.core.field.field_helper import field_helper
from app.model import ManagerBase
from app.core.company.company_helper import company_helper


class CompanyService:
    async def get(self, db: Session, data: dict, current_user: ManagerBase = None):
        page = company_helper.validate_pagination(data)

        if (
            data.get("business_id")
            and current_user
            and current_user.role == Role.BUSINESS
        ):
            if data.get("business_id") != current_user.id:
                return constant.ERROR, 403, "Permission denied"
            company = current_user.business.company
            companies_response = company_helper.get_info(db, company)
            return constant.SUCCESS, 200, companies_response

        companies = crud.company.get_multi(db, **page.model_dump())
        companies_response = []
        if data.get("fields"):
            companies_response = company_helper.get_info(db, companies, detail=True)
        else:
            companies_response = company_helper.get_list_info(db, company)
        return constant.SUCCESS, 200, companies_response

    async def search(self, db: Session, data: dict):
        page = company_helper.validate_pagination(data)

        total, companies = crud.company.search_multi(db, **page.model_dump())
        companies_response = company_helper.get_list_info(db, companies, detail=True)
        # companies_response = await [
        #     get_company_info(db, company, detail=True) for company in companies
        # ]
        # if data.get("fields"):
        #     companies_response = [
        #         get_company_info(db, company, detail=True) for company in companies
        #     ]
        # else:
        #     companies_response = [get_company_info(db, company) for company in companies]

        return (
            constant.SUCCESS,
            200,
            {
                "total": total,
                "companies": companies_response,
                # "time": (end_time - start_time).total_seconds(),
            },
        )

    async def get_by_id(self, db: Session, company_id: int):
        company = crud.company.get(db, company_id)
        if not company:
            return constant.ERROR, 404, "Company not found"
        company_response = company_helper.get_info(db, company)
        return constant.SUCCESS, 200, company_response

    async def create(self, db: Session, data: dict, current_user: ManagerBase):
        business = current_user.business
        if not business:
            return constant.ERROR, 404, "Business not found"
        business_auth_helper.verified_level(business, 2)
        if crud.company.get_by_business_id(db=db, business_id=current_user.id):
            return constant.ERROR, 403, "Permission denied"
        if crud.company.get_company_by_tax_code(db, data.get("tax_code")):
            return constant.ERROR, 400, "Tax code already exists"
        if crud.company.get_company_by_email(db, data.get("email")):
            return constant.ERROR, 400, "Email already exists"
        company_data = company_helper.validate_create(data)

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
        company_response = company_helper.get_private_info(db, company)
        return constant.SUCCESS, 201, company_response

    async def update(self, db: Session, data: dict, current_user):
        company_id = data.get("company_id")
        company = crud.company.get(db, company_id)
        if not company:
            return constant.ERROR, 404, "Company not found"
        if company.business_id != current_user.id:
            return constant.ERROR, 403, "Permission denied"
        company_data = company_helper.validate_update(data)

        logo = company_data.logo
        old_fields = company.company_field_secondary
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

        company_response = company_helper.get_private_info(db, company)
        return constant.SUCCESS, 200, company_response

    async def delete(self, db: Session, company_id: int, current_user: ManagerBase):
        company = crud.company.get(db, company_id)
        business = current_user.business
        if not business:
            return constant.ERROR, 404, "Business not found"
        if not company:
            return constant.ERROR, 404, "Company not found"
        if company.business_id != business.id:
            return constant.ERROR, 403, "Permission denied"
        company = crud.company.remove(db, id=company_id)
        return constant.SUCCESS, 200, "Company has been deleted"


company_service = CompanyService()

from sqlalchemy.orm import Session

from app.crud.company import company as companyCRUD
from app.schema import (
    page as schema_page,
    company as schema_company,
    job as schema_job,
)
from app.hepler.enum import Role
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error


def get_list_company(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    companies = companyCRUD.get_multi(db, **page.dict())
    companies_response = [get_company_info(company) for company in companies]
    return constant.SUCCESS, 200, companies_response


def get_company_by_id(db: Session, company_id: int):
    company = companyCRUD.get(db, company_id)
    if not company:
        return constant.ERROR, 404, "Company not found"
    company_response = get_company_info(company)
    return constant.SUCCESS, 200, company_response


def create_company(db: Session, data: dict, current_user):
    if companyCRUD.get_company_by_business_id(
        db=db, business_id=current_user.business.id
    ):
        return constant.ERROR, 403, "Permission denied"
    try:
        company_data = schema_company.CompanyCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if current_user.role == Role.BUSINESS:
        company_data = {
            **company_data.dict(),
            "business_id": current_user.business.id,
        }
    company = companyCRUD.create(db, obj_in=company_data)
    company_response = get_company_info_private(company)
    return constant.SUCCESS, 201, company_response


def update_company(db: Session, data: dict, current_user):
    company_id = data.get("company_id")
    company = companyCRUD.get(db, company_id)
    if not company:
        return constant.ERROR, 404, "Company not found"
    if company.business_id != current_user.business.id:
        return constant.ERROR, 403, "Permission denied"
    try:
        company_data = schema_company.CompanyUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    company = companyCRUD.update(db, db_obj=company, obj_in=company_data)
    company_response = get_company_info_private(company)
    return constant.SUCCESS, 200, company_response


def delete_company(db: Session, company_id: int, current_user):
    company = companyCRUD.get(db, company_id)
    if not company:
        return constant.ERROR, 404, "Company not found"
    if company.business_id != current_user.business.id:
        return constant.ERROR, 403, "Permission denied"
    company = companyCRUD.remove(db, id=company_id)
    return constant.SUCCESS, 200, "Company has been deleted"


def get_company_info(company):
    if not company:
        return None
    company_response = schema_company.CompanyItemResponse(**company.__dict__)
    return company_response


def get_company_info_private(company):
    if not company:
        return None
    company_response = schema_company.CompanyPrivateResponse(**company.__dict__)
    return company_response

from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.company import company as companyCRUD
from app.crud.business import business as businessCRUD
from app.crud.company_business import company_business as company_businessCRUD
from app.schema import (
    company as schema_company,
    field as schema_field,
)
from app.hepler.enum import Role
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.storage.s3 import s3_service
from app.core.auth import service_business_auth
from app.core.field import service_field
from app.core.job import service_job


def get(db: Session, data: dict, current_user=None):
    try:
        page = schema_company.CompanyPagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if data.get("business_id") and current_user and current_user.role == Role.BUSINESS:
        if data.get("business_id") != current_user.id:
            return constant.ERROR, 403, "Permission denied"
        company = current_user.business.company
        return constant.SUCCESS, 200, get_company_info(db, company)

    companies = companyCRUD.get_multi(db, **page.model_dump())
    companies_response = []
    if data.get("fields"):
        companies_response = [
            get_company_info(db, company, detail=True) for company in companies
        ]
    else:
        companies_response = [get_company_info(db, company) for company in companies]

    return constant.SUCCESS, 200, companies_response


def search(db: Session, data: dict):
    try:
        page = schema_company.CompanyPagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    start_time = datetime.now()
    total, companies = companyCRUD.search_multi(db, **page.model_dump())
    end_time = datetime.now()
    # companies_response = []
    companies_response = [
        get_company_info(db, company, detail=True) for company in companies
    ]
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
            "time": (end_time - start_time).total_seconds(),
        },
    )


def get_by_id(db: Session, company_id: int):
    company = companyCRUD.get(db, company_id)
    if not company:
        return constant.ERROR, 404, "Company not found"
    company_response = get_company_info(db, company)
    return constant.SUCCESS, 200, company_response


def create(db: Session, data: dict, current_user):
    business = current_user.business
    if not business:
        return constant.ERROR, 404, "Business not found"
    service_business_auth.verified_level(business, 2)
    if companyCRUD.get_company_by_business_id(db=db, business_id=current_user.id):
        return constant.ERROR, 403, "Permission denied"
    if companyCRUD.get_company_by_tax_code(db, data.get("tax_code")):
        return constant.ERROR, 400, "Tax code already exists"
    if companyCRUD.get_company_by_email(db, data.get("email")):
        return constant.ERROR, 400, "Email already exists"
    try:
        company_data = schema_company.CompanyCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    fields = company_data.fields
    if fields:
        service_field.check_fields_exist(db, fields)

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
    company = companyCRUD.create(db, obj_in=obj_in)
    if fields:
        service_field.create_fields_company(db, company.id, fields)
    company_response = get_company_info_private(db, company)
    return constant.SUCCESS, 201, company_response


def update(db: Session, data: dict, current_user):
    company_id = data.get("company_id")
    company = companyCRUD.get(db, company_id)
    if not company:
        return constant.ERROR, 404, "Company not found"
    if company.business_id != current_user.id:
        return constant.ERROR, 403, "Permission denied"
    try:
        company_data = schema_company.CompanyUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    logo = company_data.logo
    old_fields = company.company_field_secondary
    new_fields = company_data.fields
    if new_fields:
        service_field.check_fields_exist(db, new_fields)
    if logo:
        key = logo.filename
        s3_service.upload_file(logo, key)
        company_data.logo = key

    obj_in = schema_company.CompanyUpdate(**company_data.model_dump())
    company = companyCRUD.update(db, db_obj=company, obj_in=obj_in)
    service_field.update_fields_company(db, company.id, new_fields, old_fields)

    company_response = get_company_info_private(db, company)
    return constant.SUCCESS, 200, company_response


def delete(db: Session, company_id: int, current_user):
    company = companyCRUD.get(db, company_id)
    business = current_user.business
    if not business:
        return constant.ERROR, 404, "Business not found"
    if not company:
        return constant.ERROR, 404, "Company not found"
    if company.business_id != business.id:
        return constant.ERROR, 403, "Permission denied"
    company = companyCRUD.remove(db, id=company_id)
    return constant.SUCCESS, 200, "Company has been deleted"


def get_company_info(db: Session, company, detail=False):
    if not company:
        return None
    fields = company.fields
    company_response = schema_company.CompanyItemResponse(
        **company.__dict__,
    )

    if detail:
        count_job_published = service_job.get_jobs_active_by_company(db, company.id)
        company_response.total_active_jobs = count_job_published
    return {
        **company_response.__dict__,
        "fields": [
            schema_field.FieldItemResponse(**field.__dict__) for field in fields
        ],
    }


def get_company_info_private(db: Session, company):
    if not company:
        return None
    fields = company.fields
    company_response = schema_company.CompanyPrivateResponse(
        **company.__dict__,
    )

    return {
        **company_response.__dict__,
        "fields": [
            schema_field.FieldItemResponse(**field.__dict__) for field in fields
        ],
    }

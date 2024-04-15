from sqlalchemy.orm import Session

from app.crud.company import company as companyCRUD
from app.crud.field import field as fieldCRUD
from app.crud.company_field import company_field as company_fieldCRUD
from app.schema import (
    page as schema_page,
    company as schema_company,
    job as schema_job,
    field as schema_field,
)
from app.hepler.enum import Role
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.storage.s3 import s3_service


def get_list_company(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    companies = companyCRUD.get_multi(db, **page.dict())
    companies_response = [get_company_info(db, company) for company in companies]
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
    if companyCRUD.get_company_by_tax_code(db, data.get("tax_code")):
        return constant.ERROR, 400, "Tax code already exists"
    if companyCRUD.get_company_by_email(db, data.get("email")):
        return constant.ERROR, 400, "Email already exists"
    try:
        company_data = schema_company.CompanyCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    fileds = company_data.fields
    if fileds:
        for field in fileds:
            field_data = fieldCRUD.get(db, field)
            if not field_data:
                return constant.ERROR, 404, "Field id ${field} not found"

    logo = company_data.logo
    if logo:
        key = logo.filename
        s3_service.upload_file(logo, key)
        company_data.logo = key

    if current_user.role == Role.BUSINESS:
        company_data = {
            **company_data.dict(),
            "business_id": current_user.business.id,
        }
    obj_in = schema_company.CompanyCreate(**company_data)
    company = companyCRUD.create(db, obj_in=obj_in)
    if fileds:
        for field in fileds:
            company_field_data = {
                "company_id": company.id,
                "field_id": field,
            }
            company_fieldCRUD.create(db, obj_in=company_field_data)
    company_response = get_company_info_private(db, company)
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
    logo = company_data.logo
    if logo:
        key = logo.filename
        s3_service.upload_file(logo, key)
        company_data.logo = key
    old_fields = company.fields
    new_fields = company_data.fields
    if old_fields:
        for field in old_fields:
            if field.id not in new_fields:
                company_fieldCRUD.remove_by_company_id_and_field_id(
                    db, company_id, field.id
                )
    if new_fields:
        for field in new_fields:
            field_data = fieldCRUD.get(db, field)
            if not field_data:
                return constant.ERROR, 404, "Field id {field} not found"
            if not company_fieldCRUD.get_by_company_id_and_field_id(
                db, company_id, field
            ):
                company_field_data = {
                    "company_id": company_id,
                    "field_id": field,
                }
                company_fieldCRUD.create(db, obj_in=company_field_data)
    obj_in = schema_company.CompanyUpdate(**company_data.dict())
    company = companyCRUD.update(db, db_obj=company, obj_in=obj_in)

    company_response = get_company_info_private(db, company)
    return constant.SUCCESS, 200, company_response


def delete_company(db: Session, company_id: int, current_user):
    company = companyCRUD.get(db, company_id)
    if not company:
        return constant.ERROR, 404, "Company not found"
    if company.business_id != current_user.business.id:
        return constant.ERROR, 403, "Permission denied"
    company = companyCRUD.remove(db, id=company_id)
    return constant.SUCCESS, 200, "Company has been deleted"


def get_company_info(db: Session, company):
    if not company:
        return None
    fields = company.fields
    company_response = schema_company.CompanyItemResponse(
        **company.__dict__,
    )

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

from sqlalchemy.orm import Session

from app.crud.field import field as fieldCRUD
from app.crud.company_field import company_field as company_fieldCRUD
from app.schema import (
    field as schema_field,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get_list_field(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    categories = fieldCRUD.get_multi(db, **page.dict())

    categories_response = [
        schema_field.FieldItemResponse(**field.__dict__) for field in categories
    ]
    return constant.SUCCESS, 200, categories_response


def get_field_by_id(db: Session, field_id: int):
    field = fieldCRUD.get(db, field_id)
    if not field:
        return constant.ERROR, 404, "Field not found"
    field_response = schema_field.FieldItemResponse(**field.__dict__)
    return constant.SUCCESS, 200, field_response


def create_field(db: Session, data: dict):
    try:
        field_data = schema_field.FieldCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    field = fieldCRUD.get_by_name(db, field_data.name)
    if field:
        return constant.ERROR, 409, "Field already registered"

    field = fieldCRUD.create(db, obj_in=field_data)
    return constant.SUCCESS, 201, field


def update_field(db: Session, field_id: int, data: dict):
    field = fieldCRUD.get(db, field_id)
    if not field:
        return constant.ERROR, 404, "Field not found"

    try:
        field_data = schema_field.FieldUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    field = fieldCRUD.update(db, db_obj=field, obj_in=field_data)
    return constant.SUCCESS, 200, field


def delete_field(db: Session, field_id: int):
    field = fieldCRUD.get(db, field_id)
    if not field:
        return constant.ERROR, 404, "Field not found"

    field = fieldCRUD.remove(db, id=field_id)
    return constant.SUCCESS, 200, field


def check_fields_exist(db: Session, fields: list):
    for field in fields:
        field_data = fieldCRUD.get(db, field)
        if not field_data:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response=f"Field id {field} not found",
            )


def create_fields_company(db: Session, company_id: int, fields: list):
    for field in fields:
        company_field_data = {
            "company_id": company_id,
            "field_id": field,
        }
        company_fieldCRUD.create(db, obj_in=company_field_data)
        field_data = fieldCRUD.get(db, field)
        fieldCRUD.update(db, db_obj=field_data, obj_in={"count": field_data.count + 1})
    return True


def update_fields_company(
    db: Session, company_id: int, new_field_ids: list, old_fields: list
):
    new_field_ids = list(set(new_field_ids))
    current_field_ids = [field.field_id for field in old_fields]
    add_field_ids = list(set(new_field_ids) - set(current_field_ids))
    for field in old_fields:
        if field.field_id not in new_field_ids:
            company_fieldCRUD.remove(db, id=field.id)
    for field_id in add_field_ids:
        company_field_data = {
            "company_id": company_id,
            "field_id": field_id,
        }
        company_fieldCRUD.create(db, obj_in=company_field_data)
    return new_field_ids

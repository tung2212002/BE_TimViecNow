from sqlalchemy.orm import Session

from app.crud.category import category as categoryCRUD
from app.schema import (
    category as schema_category,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error


def get_list_category(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    categories = categoryCRUD.get_multi(db, **page.dict())

    categories_response = [
        schema_category.CategoryItemResponse(**category.__dict__)
        for category in categories
    ]
    return constant.SUCCESS, 200, categories_response


def get_category_by_id(db: Session, category_id: int):
    category = categoryCRUD.get(db, category_id)
    if not category:
        return constant.ERROR, 404, "Category not found"
    category_response = schema_category.CategoryItemResponse(**category.__dict__)
    return constant.SUCCESS, 200, category_response


def create_category(db: Session, data: dict):
    try:
        category_data = schema_category.CategoryCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    category = categoryCRUD.get_by_name(db, category_data.name)
    if category:
        return constant.ERROR, 409, "Category already registered"

    category = categoryCRUD.create(db, obj_in=category_data)
    return constant.SUCCESS, 201, category


def update_category(db: Session, category_id: int, data: dict):
    category = categoryCRUD.get(db, category_id)
    if not category:
        return constant.ERROR, 404, "Category not found"

    try:
        category_data = schema_category.CategoryUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    category = categoryCRUD.update(db, db_obj=category, obj_in=category_data)
    return constant.SUCCESS, 200, category


def delete_category(db: Session, category_id: int):
    category = categoryCRUD.get(db, category_id)
    if not category:
        return constant.ERROR, 404, "Category not found"

    category = categoryCRUD.remove(db, id=category_id)
    return constant.SUCCESS, 200, category

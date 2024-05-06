from sqlalchemy.orm import Session

from app.crud.category import category as categoryCRUD
from app.crud.job_category import job_category as job_categoryCRUD
from app.schema import (
    category as schema_category,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get_list_category(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    categories_response = get_list_category_info(db, page.dict())
    return constant.SUCCESS, 200, categories_response


def get_category_by_id(db: Session, category_id: int):
    category_response = get_category_info(db, category_id)
    if not category_response:
        return constant.ERROR, 404, "Category not found"
    return constant.SUCCESS, 200, category_response


def get_category_info(db: Session, category):
    return (
        schema_category.CategoryItemResponse(**category.__dict__) if category else None
    )


def get_list_category_by_model(db: Session, categories):
    return [
        schema_category.CategoryItemResponse(**category.__dict__)
        for category in categories
    ]


def get_category_info_by_id(db: Session, category_id: int):
    category = categoryCRUD.get(db, category_id)
    return (
        schema_category.CategoryItemResponse(**category.__dict__) if category else None
    )


def get_list_category_info(db: Session, data: dict):
    categories = categoryCRUD.get_multi(db, **data)
    return [
        schema_category.CategoryItemResponse(**category.__dict__) if category else None
        for category in categories
    ]


def get_list_category_by_ids(db: Session, category_ids: list):
    categories_response = [
        get_category_info_by_id(db, category_id) for category_id in category_ids
    ]
    return categories_response


def check_category_exist(db: Session, category_id: int):
    category = categoryCRUD.get(db, category_id)
    if not category:
        return custom_response_error(
            status_code=404,
            status=constant.ERROR,
            response=f"Category id {category_id} not found",
        )
    return category


def check_categories_exist(db: Session, category_ids: list):
    list_categories = []
    for category_id in category_ids:
        category = check_category_exist(db, category_id)
        list_categories.append(category)
    return list_categories


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


def create_category_job(db: Session, job_id: int, category_ids: list):
    category_ids = list(set(category_ids))
    for category_id in category_ids:
        job_categoryCRUD.create(
            db, obj_in={"job_id": job_id, "category_id": category_id}
        )
        category = categoryCRUD.get(db, category_id)
        categoryCRUD.update(db, db_obj=category, obj_in={"count": category.count + 1})
    return category_ids


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


def update_category_job(db: Session, new_category_ids: list, categories: list):
    new_category_ids = list(set(new_category_ids))
    current_category_ids = [category.category_id for category in categories]
    add_category_ids = list(set(new_category_ids) - set(current_category_ids))
    for category in categories:
        if category.category_id not in new_category_ids:
            job_categoryCRUD.remove(db, id=category.id)
    for category_id in add_category_ids:
        job_categoryCRUD.create(
            db, obj_in={"job_id": category.job_id, "category_id": category_id}
        )
    return new_category_ids


def delete_category(db: Session, category_id: int):
    category = categoryCRUD.get(db, category_id)
    if not category:
        return constant.ERROR, 404, "Category not found"

    category = categoryCRUD.remove(db, id=category_id)
    return constant.SUCCESS, 200, category

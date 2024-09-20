from sqlalchemy.orm import Session

from app import crud
from app.core import constant
from app.core.category.category_helper import category_helper


class CategoryService:
    async def get(self, db: Session, data: dict):
        page = category_helper.validate_pagination(data)

        categories = crud.category.get_multi(db, **page.model_dump())
        return constant.SUCCESS, 200, category_helper.get_list_info(categories)

    async def get_by_id(self, db: Session, category_id: int):
        category = crud.category.get(db, category_id)

        if not category:
            return constant.ERROR, 404, "Category not found"
        return constant.SUCCESS, 200, category_helper.get_info(category)

    async def create(self, db: Session, data: dict):
        category_data = category_helper.validate_create(data)

        category = crud.category.get_by_name(db, category_data.name)
        if category:
            return constant.ERROR, 409, "Category already registered"

        category = crud.category.create(db, obj_in=category_data)
        return constant.SUCCESS, 201, category

    async def update(self, db: Session, category_id: int, data: dict):
        category_data = category_helper.validate_update(data)

        category = crud.category.get(db, category_id)
        if not category:
            return constant.ERROR, 404, "Category not found"
        response = crud.category.update(db, db_obj=category, obj_in=category_data)
        return constant.SUCCESS, 200, response

    async def delete(self, db: Session, category_id: int):
        category = crud.category.get(db, category_id)
        if not category:
            return constant.ERROR, 404, "Category not found"
        response = crud.category.remove(db, id=category_id)
        return constant.SUCCESS, 200, response


category_service = CategoryService()

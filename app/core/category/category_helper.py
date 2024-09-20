from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.core import constant
from app.hepler.response_custom import custom_response_error
from app.schema import (
    category as schema_category,
    page as schema_page,
)
from app.model import Category
from app.core.helper_base import HelperBase


class CategoryHelper(HelperBase):
    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        category = crud.category.get(db, id)
        if not category:
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Category not found"
            )
        return int

    def check_list_valid(
        self,
        db: Session,
        ids: List[int],
    ) -> List[int]:
        if not ids or ids is None:
            return []

        return [self.check_valid(db, id) for id in ids]

    def get_info(self, category: Category) -> schema_category.CategoryItemResponse:
        return schema_category.CategoryItemResponse(**category.__dict__)

    def get_info_by_id(
        self, db: Session, id: int
    ) -> schema_category.CategoryItemResponse:
        category = crud.category.get(db, id)
        return self.get_info(category)

    def get_list_info(self, categories: List[Category]) -> List:
        return [self.get_info(category) for category in categories]

    def get_list_info_by_ids(self, db: Session, ids: List[int]) -> List:
        return [self.get_info_by_id(db, id) for id in ids]

    def create_with_job_id(
        self,
        db: Session,
        job_id: int,
        ids: List[int],
    ) -> None:
        ids = list(set(ids))
        for category_id in ids:
            job_category_data = {
                "job_id": job_id,
                "category_id": category_id,
            }
            crud.job_category.create(db, obj_in=job_category_data)

    def update_with_job_id(
        self,
        db: Session,
        job_id: int,
        new_category_ids: List[int],
    ) -> None:
        current_category_ids = crud.job_category.get_ids_by_job_id(db, job_id)
        new_category_ids = list(set(new_category_ids))
        remove_category_ids = list(set(current_category_ids) - set(new_category_ids))
        add_category_ids = list(set(new_category_ids) - set(current_category_ids))

        for category_id in remove_category_ids:
            crud.job_category.remove_by_job_id_and_category_id(db, job_id, category_id)
        for category_id in add_category_ids:
            job_category_data = {
                "job_id": job_id,
                "category_id": category_id,
            }
            crud.job_category.create(db, obj_in=job_category_data)


category_helper = CategoryHelper(
    schema_page.Pagination,
    schema_category.CategoryCreateRequest,
    schema_category.CategoryUpdateRequest,
)

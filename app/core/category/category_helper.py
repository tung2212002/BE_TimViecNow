from sqlalchemy.orm import Session
from typing import List

from app.crud import category as categoryCRUD, job_category as job_categoryCRUD
from app.schema.category import (
    CategoryItemResponse,
)
from app.model import Category
from fastapi import status
from app.common.exception import CustomException


class CategoryHelper:
    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        category = categoryCRUD.get(db, id)
        if not category:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Category not found"
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

    def get_info(self, category: Category) -> CategoryItemResponse:
        return CategoryItemResponse(**category.__dict__)

    def get_info_by_id(self, db: Session, id: int) -> CategoryItemResponse:
        category = categoryCRUD.get(db, id)
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
            job_categoryCRUD.create(db, obj_in=job_category_data)

    def update_with_job_id(
        self,
        db: Session,
        job_id: int,
        new_category_ids: List[int],
    ) -> None:
        current_category_ids = job_categoryCRUD.get_ids_by_job_id(db, job_id)
        new_category_ids = list(set(new_category_ids))
        remove_category_ids = list(set(current_category_ids) - set(new_category_ids))
        add_category_ids = list(set(new_category_ids) - set(current_category_ids))

        for category_id in remove_category_ids:
            job_categoryCRUD.remove_by_job_id_and_category_id(db, job_id, category_id)
        for category_id in add_category_ids:
            job_category_data = {
                "job_id": job_id,
                "category_id": category_id,
            }
            job_categoryCRUD.create(db, obj_in=job_category_data)


category_helper = CategoryHelper()

from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.schema import (
    field as schema_field,
    page as schema_page,
)
from app.model import Field
from app.core.helper_base import HelperBase


class FieldHelper(HelperBase):
    def get_info(self, field: Field):
        return schema_field.FieldItemResponse(**field.__dict__)

    def get_list_info(self, fields: List[Field]):
        return [self.get_info(field) for field in fields]

    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        field = crud.field.get(db, id)
        if not field:
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Field not found"
            )
        return id

    def check_list_valid(
        self,
        db: Session,
        ids: List[int],
    ) -> List[int]:
        return [self.check_valid(db, id) for id in ids]

    def create_with_company_id(
        self,
        db: Session,
        company_id: int,
        ids: List[int],
    ) -> None:
        for field in ids:
            company_field_data = {
                "company_id": company_id,
                "field_id": field,
            }
            crud.company_field.create(db, obj_in=company_field_data)

    def update_with_company_id(
        self,
        db: Session,
        company_id: int,
        new_field_ids: List[int],
    ) -> None:
        current_field_ids = crud.company_field.get_field_ids_by_company_id(
            db, company_id
        )
        new_field_ids = list(set(new_field_ids))
        remove_field_ids = list(set(current_field_ids) - set(new_field_ids))
        add_field_ids = list(set(new_field_ids) - set(current_field_ids))
        for field_id in remove_field_ids:
            crud.company_field.remove_by_company_id_and_field_id(
                db, company_id, field_id
            )
        self.create_with_company_id(db, company_id, add_field_ids)


field_helper = FieldHelper(
    schema_page.Pagination,
    schema_field.FieldCreateRequest,
    schema_field.FieldUpdateRequest,
)

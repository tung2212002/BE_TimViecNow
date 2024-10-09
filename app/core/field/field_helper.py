from sqlalchemy.orm import Session
from typing import List

from app.crud import field as fieldCRUD, company_field as company_fieldCRUD
from app.schema.field import FieldItemResponse
from app.model import Field
from app.common.exception import CustomException
from fastapi import status


class FieldHelper:
    def get_info(self, field: Field) -> FieldItemResponse:
        return FieldItemResponse(**field.__dict__)

    def get_list_info(self, fields: List[Field]) -> List[FieldItemResponse]:
        return [self.get_info(field) for field in fields]

    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        field = fieldCRUD.get(db, id)
        if not field:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Field not found"
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
            company_fieldCRUD.create(db, obj_in=company_field_data)

    def update_with_company_id(
        self,
        db: Session,
        company_id: int,
        new_field_ids: List[int],
    ) -> None:
        current_field_ids = company_fieldCRUD.get_field_ids_by_company_id(
            db, company_id
        )
        new_field_ids = list(set(new_field_ids))
        remove_field_ids = list(set(current_field_ids) - set(new_field_ids))
        add_field_ids = list(set(new_field_ids) - set(current_field_ids))

        for field_id in remove_field_ids:
            company_fieldCRUD.remove_by_company_id_and_field_id(
                db, company_id, field_id
            )
        self.create_with_company_id(db, company_id, add_field_ids)


field_helper = FieldHelper()

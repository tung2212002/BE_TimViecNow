from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    field as schema_field,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.core.field.field_helper import field_helper


class FieldService:
    async def get_field(self, db: Session, data: dict):
        page = field_helper.validate_pagination(data)

        fields = crud.field.get_multi(db, **page.model_dump())

        return constant.SUCCESS, 200, field_helper.get_list_info(fields)

    async def get_by_id(self, db: Session, id: int):
        field = crud.field.get(db, id)
        if not field:
            return constant.ERROR, 404, "Field not found"

        return constant.SUCCESS, 200, field_helper.get_info(field)

    async def create(self, db: Session, data: dict):
        field_data = field_helper.validate_create(data)

        field = crud.field.get_by_name(db, field_data.name)
        if field:
            return constant.ERROR, 409, "Field already registered"

        field = crud.field.create(db, obj_in=field_data)
        return constant.SUCCESS, 201, field

    async def update(self, db: Session, id: int, data: dict):
        field = crud.field.get(db, id)
        if not field:
            return constant.ERROR, 404, "Field not found"

        field_data = field_helper.validate_update(data)

        field = crud.field.update(db, db_obj=field, obj_in=field_data)
        return constant.SUCCESS, 200, field

    async def delete(self, db: Session, id: int):
        field = crud.field.get(db, id)
        if not field:
            return constant.ERROR, 404, "Field not found"

        field = crud.field.remove(db, id=id)
        return constant.SUCCESS, 200, field


field_service = FieldService()

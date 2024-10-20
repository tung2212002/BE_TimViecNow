from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.crud import field as fieldCRUD
from app.core.field.field_helper import field_helper
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.schema.field import FieldCreateRequest, FieldUpdateRequest
from app.schema.page import Pagination
from app.storage.cache.config_cache_service import config_cache_service


class FieldService:
    async def get_field(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_field(redis, key)
        except Exception as e:
            print(e)

        if not response:
            fields = fieldCRUD.get_multi(db, **page.model_dump())
            response = field_helper.get_list_info(fields)
            try:
                await config_cache_service.cache_field(
                    redis,
                    key,
                    response,
                )
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_by_id(self, db: Session, id: int):
        field = fieldCRUD.get(db, id)
        if not field:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Field not found"
            )

        response = field_helper.get_info(field)

        return CustomResponse(data=response)

    async def create(self, db: Session, data: dict):
        field_data = FieldCreateRequest(**data)

        field = fieldCRUD.get_by_name(db, field_data.name)
        if field:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT, msg="Field already registered"
            )

        response = fieldCRUD.create(db, obj_in=field_data)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def update(self, db: Session, id: int, data: dict):
        field = fieldCRUD.get(db, id)
        if not field:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Field not found"
            )

        field_data = FieldUpdateRequest(**data)

        response = fieldCRUD.update(db, db_obj=field, obj_in=field_data)

        return CustomResponse(data=response)

    async def delete(self, db: Session, id: int):
        field = fieldCRUD.get(db, id)
        if not field:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Field not found"
            )

        response = fieldCRUD.remove(db, id=id)

        return CustomResponse(data=response)


field_service = FieldService()

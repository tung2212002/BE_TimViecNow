from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.crud import category as categoryCRUD
from app.core.category.category_helper import category_helper
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.schema.page import Pagination
from app.schema.category import CategoryCreateRequest, CategoryUpdateRequest
from app.storage.cache.config_cache_service import config_cache_service


class CategoryService:
    async def get(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_category(redis, key)
        except Exception as e:
            print(e)
        if not response:
            categories = categoryCRUD.get_multi(db, **page.model_dump())
            response = category_helper.get_list_info(categories)
            try:
                await config_cache_service.cache_category(
                    redis,
                    key,
                    response,
                )
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_by_id(self, db: Session, category_id: int):
        category = categoryCRUD.get(db, category_id)

        if not category:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Category not found"
            )

        response = category_helper.get_info(category)

        return CustomResponse(data=response)

    async def create(self, db: Session, data: dict):
        category_data = CategoryCreateRequest(**data)

        category = categoryCRUD.get_by_name(db, category_data.name)
        if category:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT, msg="Category already registered"
            )

        category = categoryCRUD.create(db, obj_in=category_data)
        response = category_helper.get_info(category)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def update(self, db: Session, category_id: int, data: dict):
        category_data = CategoryUpdateRequest(**data)

        category = categoryCRUD.get(db, category_id)
        if not category:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Category not found"
            )

        response = categoryCRUD.update(db, db_obj=category, obj_in=category_data)

        return CustomResponse(data=response)

    async def delete(self, db: Session, category_id: int):
        category = categoryCRUD.get(db, category_id)
        if not category:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Category not found"
            )

        response = categoryCRUD.remove(db, id=category_id)

        return CustomResponse(data=response)


category_service = CategoryService()

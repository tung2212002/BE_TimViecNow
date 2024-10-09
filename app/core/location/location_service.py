from fastapi import status
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.core import constant
from app.schema.page import Pagination
from app.storage.cache.location_cache_service import location_cache_service
from app.core.location.location_helper import location_helper
from app.common.exception import CustomException
from app.common.response import CustomResponse


class LocationService:
    async def get_province(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await location_cache_service.get_cache_list_province(redis, key)
        except Exception as e:
            print(e)

        if not response:
            response = location_helper.get_list_province_info(db, page.model_dump())
            try:
                await location_cache_service.cache_list_province(redis, key, response)
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_district(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        province_id = data.get("province_id")
        response = None
        key = page.get_key() + f"_{province_id}"

        if not province_id:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Province id is required"
            )

        try:
            response = await location_cache_service.get_cache_district_of_province(
                redis, key
            )
        except Exception as e:
            print(e)

        if not response:
            response = location_helper.get_list_district_info(
                db, {**page.model_dump(), "province_id": province_id}
            )
            try:
                await location_cache_service.cache_district_of_province(
                    redis, key, response
                )
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_province_by_id(self, db: Session, redis: Redis, id: int):
        response = None
        try:
            await location_cache_service.get_cache_province(redis, id)
        except Exception as e:
            print(e)

        if not response:
            response = location_helper.get_province_info_by_id(db, id)
            if not response:
                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="Province not found"
                )

            try:
                await location_cache_service.cache_province(redis, id, response)
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_district_by_id(self, db: Session, redis: Redis, id: int):
        response = None
        try:
            response = await location_cache_service.get_cache_district(redis, id)
        except Exception as e:
            print(e)

        if not response:
            response = location_helper.get_district_info_by_id(db, id)
            if not response:
                return constant.ERROR, 404, "District not found"
            try:
                await location_cache_service.cache_district(redis, id, response)
            except Exception as e:
                print(e)

        return CustomResponse(data=response)


location_service = LocationService()

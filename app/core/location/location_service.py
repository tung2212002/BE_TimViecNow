from sqlalchemy.orm import Session
from typing import List
from redis.asyncio import Redis

from app.core import constant
from app.storage.cache.location_cache_service import location_cache_service
from app.core.location.location_helper import location_helper


class LocationService:
    async def get_province(self, db: Session, redis: Redis, data: dict):
        page = location_helper.validate_pagination(data)

        provinces_response = None
        try:
            provinces_response = await location_cache_service.get_cache_list_province(
                redis
            )
        except Exception as e:
            print(e)

        if not provinces_response:
            provinces_response = location_helper.get_list_province_info(
                db, page.model_dump()
            )
            try:
                await location_cache_service.cache_list_province(
                    redis,
                    [province.__dict__ for province in provinces_response],
                )
            except Exception as e:
                print(e)

        return constant.SUCCESS, 200, provinces_response

    async def get_district(self, db: Session, redis: Redis, data: dict):
        page = location_helper.validate_pagination(data)

        province_id = data.get("province_id")
        if not province_id:
            return constant.ERROR, 400, "Province id is required"

        districts_response = None
        try:
            districts_response = (
                await location_cache_service.get_cache_district_of_province(
                    redis, province_id
                )
            )
        except Exception as e:
            print(e)

        if not districts_response:
            districts_response = location_helper.get_list_district_info(
                db, {**page.model_dump(), "province_id": province_id}
            )
            try:
                await location_cache_service.cache_district_of_province(
                    redis,
                    province_id,
                    [district.__dict__ for district in districts_response],
                )
            except Exception as e:
                print(e)

        return constant.SUCCESS, 200, districts_response

    async def get_province_by_id(self, db: Session, redis: Redis, id: int):
        province_response = None
        try:
            await location_cache_service.get_cache_province(redis, id)
        except Exception as e:
            print(e)

        if not province_response:
            province_response = location_helper.get_province_info_by_id(db, id)
            if not province_response:
                return constant.ERROR, 404, "Province not found"
            dict_province = province_response.__dict__
            try:
                await location_cache_service.set_dict(redis, id, dict_province)
            except Exception as e:
                print(e)

        return constant.SUCCESS, 200, province_response

    async def get_district_by_id(self, db: Session, redis: Redis, id: int):
        district_response = None
        try:
            district_response = await location_cache_service.get_dict(redis, id)
        except Exception as e:
            print(e)

        if not district_response:
            district_response = await location_helper.get_district_info_by_id(db, id)

            if not district_response:
                return constant.ERROR, 404, "District not found"
            try:
                await location_cache_service.cache_district(
                    redis, id, district_response.__dict__
                )
            except Exception as e:
                print(e)

        return constant.SUCCESS, 200, district_response


location_service = LocationService()

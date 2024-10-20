from redis.asyncio import Redis
from typing import List
import json

from app.storage.base_cache import BaseCache
from app.schema.province import ProvinceItemResponse
from app.schema.district import DistrictItemResponse


class LocationCacheService(BaseCache):
    def __init__(self):
        super().__init__("location_cache_", 86400)
        self.province_key = "province"
        self.district_key = "district"
        self.province_district_key = "province_district"

    async def cache_list_province(
        self, redis: Redis, key: str, value: List[ProvinceItemResponse]
    ):
        expire_time = 60 * 60 * 24
        serialized_value = json.dumps([province.model_dump() for province in value])
        await self.set(redis, self.province_key + key, serialized_value, expire_time)

    async def get_cache_list_province(
        self, redis, key: str
    ) -> List[ProvinceItemResponse]:
        response = await self.get(redis, self.province_key + key)
        return (
            [ProvinceItemResponse(**province) for province in json.loads(response)]
            if response
            else None
        )

    async def cache_province(self, redis: Redis, key: int, value: ProvinceItemResponse):
        expire_time = 60 * 60 * 24
        await self.set(
            redis,
            self.province_key + str(key),
            json.dumps(value.model_dump()),
            expire_time,
        )

    async def get_cache_province(self, redis: Redis, key: int) -> ProvinceItemResponse:
        response = await self.get(redis, self.province_key + str(key))
        return ProvinceItemResponse(**json.loads(response)) if response else None

    async def cache_district_of_province(
        self, redis: Redis, key: str, value: List[DistrictItemResponse]
    ):
        expire_time = 60 * 60 * 24
        seriallized_value = json.dumps([district.model_dump() for district in value])
        await self.set(redis, self.district_key + key, seriallized_value, expire_time)

    async def get_cache_district_of_province(
        self, redis: Redis, key: str
    ) -> List[DistrictItemResponse]:
        response = await self.get(redis, self.district_key + key)
        return (
            [DistrictItemResponse(**district) for district in json.loads(response)]
            if response
            else None
        )

    async def cache_district(self, redis: Redis, key: int, value: DistrictItemResponse):
        expire_time = 60 * 60 * 24
        await self.set(
            redis,
            self.district_key + str(key),
            json.dumps(value.model_dump()),
            expire_time,
        )

    async def get_cache_district(self, redis: Redis, key: int) -> DistrictItemResponse:
        response = await self.get(redis, self.district_key + str(key))
        return DistrictItemResponse(**json.loads(response)) if response else None


location_cache_service = LocationCacheService()

from redis.asyncio import Redis
from typing import List

from app.storage.base_cache import BaseCache


class LocationCacheService(BaseCache):
    def __init__(self):
        super().__init__("location_cache_", 86400)
        self.province_key = "province"
        self.district_key = "district"
        self.province_district_key = "province_district"

    async def cache_list_province(self, redis: Redis, value):
        expire_time = 60 * 60 * 24
        await self.set_list(redis, self.province_key, value, expire_time)

    async def get_cache_list_province(self, redis) -> List:
        response = await self.get_list(redis, self.province_key)
        return response if response else None

    async def cache_province(self, redis: Redis, key: int, value: List):
        expire_time = 60 * 60 * 24
        await self.set_list(redis, self.province_key + key, value, expire_time)

    async def get_cache_province(self, redis: Redis, key: int) -> List:
        response = await self.get_list(redis, self.province_key + key)
        return response if response else None

    async def cache_district_of_province(self, redis: Redis, key: int, value: List):
        expire_time = 60 * 60 * 24
        await self.set_list(redis, self.district_key + key, value, expire_time)

    async def get_cache_district_of_province(self, redis: Redis, key: int) -> List:
        response = await self.get_list(redis, self.district_key + key)
        return response if response else None

    async def cache_province_district(self, redis: Redis, value: List):
        expire_time = 60 * 60 * 24
        await self.set_list(redis, self.province_district_key, value, expire_time)

    async def get_cache_province_district(self, redis: Redis) -> List:
        response = await self.get_list(redis, self.province_district_key)
        return response if response else None

    async def cache_district(self, redis: Redis, key: int, value: List):
        expire_time = 60 * 60 * 24
        await self.set_list(redis, self.district_key + key, value, expire_time)

    async def get_cache_district(self, redis: Redis, key: int) -> List:
        response = await self.get_list(redis, self.district_key + key)
        return response if response else None


location_cache_service = LocationCacheService()

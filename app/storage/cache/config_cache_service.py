from redis.asyncio import Redis
from typing import List

from app.storage.base_cache import BaseCache


class ConfigCacheService(BaseCache):
    def __init__(self):
        super().__init__("config_cache_", 86400)
        self.category_key = "category"
        self.field_key = "field"
        self.position_key = "position"
        self.position_group_key = "position_group"
        self.skill_key = "skill"

    async def cache_category(self, redis: Redis, key: str, value: List):
        expire_time = 60 * 60 * 24 * 30
        await self.set_list(redis, self.category_key + key, value, expire_time)

    async def get_cache_category(self, redis: Redis, key: str) -> List:
        response = await self.get_list(redis, self.category_key + key)
        return response if response else None

    async def cache_field(self, redis: Redis, key: str, value: List):
        expire_time = 60 * 60 * 24 * 30
        await self.set_list(redis, self.field_key + key, value, expire_time)

    async def get_cache_field(self, redis: Redis, key: str) -> List:
        response = await self.get_list(redis, self.field_key + key)
        return response if response else None

    async def cache_position(self, redis: Redis, key: str, value: List):
        expire_time = 60 * 60 * 24 * 30
        await self.set_list(redis, self.position_key + key, value, expire_time)

    async def get_cache_position(self, redis: Redis, key: str) -> List:
        response = await self.get_list(redis, self.position_key + key)
        return response if response else None

    async def cache_position_group(self, redis: Redis, key: str, value: List):
        expire_time = 60 * 60 * 24 * 30
        await self.set_list(redis, self.position_group_key + key, value, expire_time)

    async def get_cache_position_group(self, redis: Redis, key: str) -> List:
        response = await self.get_list(redis, self.position_group_key + key)
        return response if response else None

    async def cache_skill(self, redis: Redis, key: str, value: List):
        expire_time = 60 * 60 * 24 * 30
        await self.set_list(redis, self.skill_key + key, value, expire_time)

    async def get_cache_skill(self, redis: Redis, key: str) -> List:
        response = await self.get_list(redis, self.skill_key + key)
        return response if response else None


config_cache_service = ConfigCacheService()

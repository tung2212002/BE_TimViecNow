import json
from redis.asyncio import Redis
from datetime import datetime, date
from enum import Enum

from app.storage.base_cache import BaseCache


class CVCacheService(BaseCache):
    def __init__(self):
        super().__init__("cv_cache_", 86400)
        self.cv_user_count_key = "cv_user_count"

    async def cache_cv_user_count(self, redis: Redis, key: str, value: int):
        expire_time = 60 * 60 * 24 * 30
        await self.set(redis, self.cv_user_count_key + key, value, expire_time)

    async def get_cache_cv_user_count(self, redis: Redis, key: str) -> int:
        response = await self.get(redis, self.cv_user_count_key + key)
        return int(response) if response else None

    async def increase_cv_user_count(self, redis: Redis, key: str, value: int):
        await self.incr(redis, self.cv_user_count_key + key)


cv_cache_service = CVCacheService()

import json
from redis.asyncio import Redis
from datetime import datetime, date
from enum import Enum

from app.storage.base_cache import BaseCache


class JobCacheService(BaseCache):
    def __init__(self):
        super().__init__("job_cache_", 86400)
        self.user_search_count_key = "user_search_count"
        self.province_district_search_key = "province_district_search"
        self.count_job_by_salary_key = "count_job_by_salary"
        self.count_job_by_category_key = "count_job_by_category"
        self.count_job_active_key = "count_job_active"
        self.count_job_24h_key = "count_job_24h"
        self.job_cruiment_demand_key = "job_cruiment_demand"
        self.job_info_key = "job_info"
        self.user_search_key = "user_search"

    async def cache_count_search_by_user(self, redis: Redis, key: str, value: int):
        expire_time = 60 * 60
        await self.set(redis, self.user_search_count_key + key, value, expire_time)

    async def get_cache_count_search_by_user(self, redis: Redis, key: str) -> int:
        response = await self.get(redis, self.user_search_count_key + key)
        return int(response) if response else None

    async def cache_province_district_search_by_user(
        self, redis: Redis, key: str, value: list
    ):
        expire_time = 60 * 10
        await self.set_list(
            redis, self.province_district_search_key + key, value, expire_time
        )

    async def get_cache_province_district_search_by_user(
        self, redis: Redis, key: str
    ) -> list:
        response = await self.get_list(redis, self.province_district_search_key + key)
        return response if response else None

    async def cache_count_job_by_salary(self, redis: Redis, value: list):
        expire_time = 60 * 60 * 12
        value = [(idx, count) for (idx, count) in value]
        await self.set_list(redis, self.count_job_by_salary_key, value, expire_time)

    async def get_cache_count_job_by_salary(self, redis: Redis) -> list:
        response = await self.get_list(redis, self.count_job_by_salary_key)
        return response if response else None

    async def cache_count_job_by_category(self, redis: Redis, value: list):
        expire_time = 60 * 60 * 12
        await self.set_list(redis, self.count_job_by_category_key, value, expire_time)

    async def get_cache_count_job_by_category(self, redis: Redis) -> list:
        response = await self.get_list(redis, self.count_job_by_category_key)
        return response if response else None

    async def cache_count_job_active(self, redis: Redis, value: int):
        expire_time = 60 * 60 * 12
        await self.set(redis, self.count_job_active_key, value, expire_time)

    async def get_cache_count_job_active(self, redis: Redis) -> int:
        response = await self.get(redis, self.count_job_active_key)
        return int(response) if response else None

    async def cache_count_job_24h(self, redis: Redis, value: int):
        expire_time = 60 * 60 * 12
        await self.set(redis, self.count_job_active_key, value, expire_time)

    async def get_cache_count_job_24h(self, redis: Redis) -> int:
        response = await self.get(redis, self.count_job_active_key)
        return int(response) if response else None

    async def cache_job_cruiment_demand(self, redis: Redis, value: object):
        expire_time = 60 * 60 * 12
        await self.set(
            redis, self.job_cruiment_demand_key, json.dumps(value), expire_time
        )

    async def get_cache_job_cruiment_demand(self, redis: Redis) -> object:
        response = await self.get(redis, self.job_cruiment_demand_key)
        return json.loads(response) if response else None

    async def cache_job_info(self, redis: Redis, key: int, value: dict):
        deadline = str(value["deadline"])
        value = json.dumps(
            value, default=custom_serializer, ensure_ascii=False, indent=4
        )
        expire_time = int(
            (datetime.fromisoformat(deadline) - datetime.now()).total_seconds()
        )
        await self.set(
            redis,
            self.job_info_key + str(key),
            value,
            expire_time,
        )

    async def get_cache_job_info(self, redis: Redis, key: int):
        response = await self.get(redis, self.job_info_key + str(key))
        return json.loads(response) if response else None

    async def cache_user_search(self, redis: Redis, key: str, value: dict):
        expire_time = 60
        await self.set(
            redis,
            self.user_search_key + key,
            json.dumps(value, default=custom_serializer),
            expire_time,
        )

    async def get_cache_user_search(self, redis: Redis, key: str) -> dict:
        response = await self.get(redis, self.user_search_key + key)
        return json.loads(response) if response else None


def custom_serializer(obj):
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


job_cache_service = JobCacheService()

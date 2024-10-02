from redis.asyncio import Redis
from typing import List
import json

from app.storage.base_cache import BaseCache
from app.schema.category import CategoryItemResponse
from app.schema.field import FieldItemResponse
from app.schema.job_position import JobPositionItemResponse
from app.schema.group_position import GroupPositionItemResponse
from app.schema.skill import SkillItemResponse


class ConfigCacheService(BaseCache):
    def __init__(self):
        super().__init__("config_cache_", 86400)
        self.category_key = "category"
        self.field_key = "field"
        self.position_key = "position"
        self.position_group_key = "position_group"
        self.skill_key = "skill"

    async def cache_category(
        self, redis: Redis, key: str, value: List[CategoryItemResponse]
    ):
        expire_time = 60 * 60 * 24 * 30
        serialized_value = json.dumps([category.model_dump() for category in value])
        await self.set(redis, self.category_key + key, serialized_value, expire_time)

    async def get_cache_category(
        self, redis: Redis, key: str
    ) -> List[CategoryItemResponse]:
        response = await self.get(redis, self.category_key + key)
        return (
            [CategoryItemResponse(**category) for category in json.loads(response)]
            if response
            else None
        )

    async def cache_field(self, redis: Redis, key: str, value: List[FieldItemResponse]):
        expire_time = 60 * 60 * 24 * 30
        serialized_value = json.dumps([field.model_dump() for field in value])
        await self.set(redis, self.field_key + key, serialized_value, expire_time)

    async def get_cache_field(self, redis: Redis, key: str) -> List[FieldItemResponse]:
        response = await self.get(redis, self.field_key + key)
        return (
            [FieldItemResponse(**field) for field in json.loads(response)]
            if response
            else None
        )

    async def cache_position(
        self, redis: Redis, key: str, value: List[JobPositionItemResponse]
    ):
        expire_time = 60 * 60 * 24 * 30
        serialized_value = json.dumps([position.model_dump() for position in value])
        await self.set(redis, self.position_key + key, serialized_value, expire_time)

    async def get_cache_position(
        self, redis: Redis, key: str
    ) -> List[JobPositionItemResponse]:
        response = await self.get(redis, self.position_key + key)
        return (
            [JobPositionItemResponse(**position) for position in json.loads(response)]
            if response
            else None
        )

    async def cache_position_group(
        self, redis: Redis, key: str, value: List[GroupPositionItemResponse]
    ):
        expire_time = 60 * 60 * 24 * 30
        serialized_value = json.dumps(
            [position_group.model_dump() for position_group in value]
        )
        await self.set(
            redis, self.position_group_key + key, serialized_value, expire_time
        )

    async def get_cache_position_group(
        self, redis: Redis, key: str
    ) -> List[GroupPositionItemResponse]:
        response = await self.get(redis, self.position_group_key + key)
        return (
            [
                GroupPositionItemResponse(**position_group)
                for position_group in json.loads(response)
            ]
            if response
            else None
        )

    async def cache_skill(self, redis: Redis, key: str, value: List[SkillItemResponse]):
        expire_time = 60 * 60 * 24 * 30
        serialized_value = json.dumps([skill.model_dump() for skill in value])
        await self.set(redis, self.skill_key + key, serialized_value, expire_time)

    async def get_cache_skill(self, redis: Redis, key: str) -> List[SkillItemResponse]:
        response = await self.get(redis, self.skill_key + key)
        return (
            [SkillItemResponse(**skill) for skill in json.loads(response)]
            if response
            else None
        )


config_cache_service = ConfigCacheService()

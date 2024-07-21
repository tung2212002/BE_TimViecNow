from redis.asyncio import Redis
import json
from typing import Any, Optional, Set

from app.storage.redis import redis_dependency


class BaseCache:
    def __init__(self, redis_backend: Redis, key_prefix: str, expire: int):
        self.expire = expire
        self.connection = redis_backend
        self.key_prefix = key_prefix

    async def get(self, key: str) -> Any:
        """Get Value from Key"""
        response = await self.connection.get(
            self.key_prefix + key,
        )
        return response

    async def set(self, key: str, value: str, expire: int = None):
        """Set Value to Key"""
        await self.connection.set(self.key_prefix + key, value, expire or self.expire)

    async def keys(self, pattern: str) -> Set[str]:
        """Get Keys by Pattern"""
        return await self.connection.keys(self.key_prefix + pattern)

    async def set_list(self, key: str, value: list, expire: int = None):
        """Set Value to Key"""
        for v in value:
            await self.connection.rpush(self.key_prefix + key, json.dumps(v))
        await self.connection.expire(self.key_prefix + key, expire or self.expire)

    async def get_list(self, key: str) -> list:
        """Get Value from Key"""
        return [
            json.loads(v)
            for v in await self.connection.lrange(self.key_prefix + key, 0, -1)
        ]

    async def set_dict(self, key: str, value: dict, expire: int = None):
        """Set Value to Key"""
        await self.connection.hmset(self.key_prefix + key, value)
        await self.connection.expire(self.key_prefix + key, expire or self.expire)

    async def get_dict(self, key: str) -> dict:
        """Get Value from Key"""
        return await self.connection.hgetall(self.key_prefix + key)

    async def delete(self, key: str):
        """Delete Key"""
        await self.connection.delete(self.key_prefix + key)

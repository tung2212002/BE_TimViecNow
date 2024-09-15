from redis.asyncio import Redis
import json
from typing import Any, Optional, Set

from app.storage.redis import redis_dependency


class BaseCache:
    def __init__(self, key_prefix: str, expire: int):
        self.key_prefix = key_prefix
        self.expire = expire

    async def get(self, redis: Redis, key: str) -> Any:
        """Get Value from Key"""
        response = await redis.get(
            self.key_prefix + key,
        )
        return response

    async def set(self, redis: Redis, key: str, value: Any, expire: int = None):
        """Set Value to Key"""
        await redis.set(self.key_prefix + key, value, expire or self.expire)

    async def keys(self, redis: Redis, pattern: str) -> Set[str]:
        """Get Keys by Pattern"""
        return await redis.keys(self.key_prefix + pattern)

    async def set_list(self, redis: Redis, key: str, value: list, expire: int = None):
        """Set Value to Key"""
        for v in value:
            await redis.rpush(self.key_prefix + key, json.dumps(v))
        await redis.expire(self.key_prefix + key, expire or self.expire)

    async def get_list(self, redis: Redis, key: str) -> list:
        """Get Value from Key"""
        return [json.loads(v) for v in await redis.lrange(self.key_prefix + key, 0, -1)]

    async def set_dict(self, redis: Redis, key: str, value: dict, expire: int = None):
        """Set Value to Key"""
        await redis.hmset(self.key_prefix + key, value)
        await redis.expire(self.key_prefix + key, expire or self.expire)

    async def get_dict(self, redis: Redis, key: str) -> dict:
        """Get Value from Key"""
        return await redis.hgetall(self.key_prefix + key)

    async def delete(self, redis: Redis, key: str):
        """Delete Key"""
        await redis.delete(self.key_prefix + key)

from redis.asyncio import Redis, ConnectionPool
import json
from typing import Any, Optional, Annotated
from fastapi import Depends

from app.core.config import settings
from typing import Set, Any, Optional
from app.core.loggers import get_logger

logger = get_logger(__name__)


class RedisBackend:
    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        db: int,
        expire: int,
    ):
        self.expire = expire
        self.connection_pool = ConnectionPool(
            host=host,
            port=port,
            password=password,
            db=db,
            max_connections=settings.REDIS_MAX_CONNECTIONS or 10,
        )
        self.connection = Redis(connection_pool=self.connection_pool)

    async def get(self, key: str) -> Any:
        """Get Value from Key"""
        response = await self.connection.get(
            key,
        )
        return response

    async def set(self, key: str, value: str, expire: int = None):
        """Set Value to Key"""
        await self.connection.set(key, value, expire or self.expire)

    async def keys(self, pattern: str) -> Set[str]:
        """Get Keys by Pattern"""
        return await self.connection.keys(pattern)

    async def set_list(self, key: str, value: list, expire: int = None):
        """Set Value to Key"""
        for v in value:
            await self.connection.rpush(key, json.dumps(v))
        await self.connection.expire(key, expire or self.expire)

    async def get_list(self, key: str) -> list:
        """Get Value from Key"""
        return [json.loads(v) for v in await self.connection.lrange(key, 0, -1)]

    async def set_dict(self, key: str, value: dict, expire: int = None):
        """Set Value to Key"""
        await self.connection.hmset(key, value)
        await self.connection.expire(key, expire or self.expire)

    async def get_dict(self, key: str) -> dict:
        """Get Value from Key"""
        return await self.connection.hgetall(key)

    async def delete(self, key: str):
        """Delete Key"""
        await self.connection.delete(key)


class RedisDependency:
    redis: Optional[RedisBackend] = None

    async def __call__(self):
        return self.redis

    async def init(self):
        try:
            self.redis = RedisBackend(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                expire=settings.REDIS_EXPIRE,
            )
            await self.redis.connection.ping()
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def close(self):
        if self.redis:
            await self.redis.connection.close()

    async def get_redis(self):
        return self.redis.connection


redis_dependency = RedisDependency()


async def get_redis() -> Redis:
    if redis_dependency.redis is None:
        await redis_dependency.init()
    return await redis_dependency.get_redis()


CurrentRedis = Annotated[Redis, Depends(get_redis)]

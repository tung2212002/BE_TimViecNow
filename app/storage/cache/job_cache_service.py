from app.storage.base_cache import BaseCache
from app.storage.redis import redis_dependency
from app.storage.redis import RedisBackend
from app.storage.redis import Redis
import json
from typing import Any, Optional, Set


class JobCacheService(BaseCache):
    def __init__(self, redis_backend: RedisBackend):
        super().__init__(redis_backend, "job_cache_", 86400)


job_cache_service = JobCacheService(redis_dependency)

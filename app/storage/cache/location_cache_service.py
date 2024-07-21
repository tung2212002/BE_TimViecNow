from app.storage.base_cache import BaseCache
from app.storage.redis import redis_dependency
from app.storage.redis import RedisBackend
from app.storage.redis import Redis
import json
from typing import Any, Optional, Set


class LocationCacheService(BaseCache):
    def __init__(self, redis_backend: RedisBackend):
        super().__init__(redis_backend, "location_cache_", 86400)


location_cache_service = LocationCacheService(redis_dependency)

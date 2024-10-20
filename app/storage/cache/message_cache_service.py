from redis.asyncio import Redis
from typing import List

from app.storage.base_cache import BaseCache


class MessageCacheService(BaseCache):
    def __init__(self):
        super().__init__("message_cache_", 86400)
        self.unread_count = "unread_count"
        self.list_conversation_id = "list_conversation_id"

    async def cache_unread_count_message(
        self, redis: Redis, *, user_id: int, conversation_id: int, count: int
    ) -> None:
        expire_time = 60 * 60 * 24 * 30
        await self.set(
            redis,
            f"{self.unread_count}:{user_id}:{conversation_id}",
            count,
            expire_time,
        )

    async def get_cache_unread_count_message(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> int:
        response = await self.get(
            redis,
            f"{self.unread_count}:{user_id}:{conversation_id}",
        )
        return response if response else None

    async def increase_unread_count_message(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> None:
        await self.incr(redis, f"{self.unread_count}:{user_id}:{conversation_id}")

    async def reset_unread_count_message(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> None:
        await self.set(redis, f"{self.unread_count}:{user_id}:{conversation_id}", 0)

    async def delete_cache_unread_count_message(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> None:
        await self.delete(redis, f"{self.unread_count}:{user_id}:{conversation_id}")

    async def cache_list_conversation_id(
        self, redis: Redis, *, user_id: int, conversation_ids: List[int]
    ) -> None:
        await self.set_list(
            redis,
            f"{self.list_conversation_id}:{user_id}",
            conversation_ids,
        )

    async def get_cache_list_conversation_id(
        self, redis: Redis, *, user_id: int
    ) -> List[int]:
        response = await self.get_list(
            redis,
            f"{self.list_conversation_id}:{user_id}",
        )
        return response if response else None

    async def delete_cache_list_conversation_id(
        self, redis: Redis, *, user_id: int
    ) -> None:
        await self.delete(redis, f"{self.list_conversation_id}:{user_id}")

    async def add_conversation_id_to_list(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> None:
        await self.add_to_list(
            redis,
            f"{self.list_conversation_id}:{user_id}",
            conversation_id,
        )

    async def remove_conversation_id_from_list(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> None:
        await self.remove_from_list(
            redis,
            f"{self.list_conversation_id}:{user_id}",
            conversation_id,
        )

    async def exists_conversation_id_in_list(
        self, redis: Redis, *, user_id: int, conversation_id: int
    ) -> bool:
        return conversation_id in await self.get_cache_list_conversation_id(
            redis, user_id=user_id
        )


message_cache_service = MessageCacheService()

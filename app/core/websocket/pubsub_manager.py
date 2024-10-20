from redis.asyncio import Redis

from app.storage.redis import get_redis


class RedisPubSubManager:
    def __init__(self):
        self.redis: Redis = None

    async def connect(self) -> None:
        self.redis = await get_redis()
        self.pubsub = self.redis.pubsub()

    async def subscribe(self, chat_id: int) -> Redis:
        await self.pubsub.subscribe(chat_id)
        return self.pubsub

    async def unsubscribe(self, chat_id: int) -> None:
        await self.pubsub.unsubscribe(chat_id)

    async def publish(self, chat_id: int, message: str) -> None:
        await self.redis.publish(chat_id, message)

    async def close(self) -> None:
        await self.pubsub.close()

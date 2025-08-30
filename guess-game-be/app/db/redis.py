from redis import asyncio as aioredis
from functools import lru_cache
from app.core.config import settings


class RedisSettings():
    def get_redis_url(self, db_number: str | None = None) -> str:
        return f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}{'/' + str(db_number) if db_number is not None else ''}"


@lru_cache()
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


redis_settings = get_redis_settings()

# Initialize the Redis client
redis_client: aioredis.Redis = aioredis.from_url(
    redis_settings.get_redis_url(db_number=settings.REDIS_DB),
    decode_responses=True,  # Automatically decode responses to strings
)

from redis import asyncio as aioredis
from fastapi import Depends
from app.db.redis import redis_client
from app.core.utils.chat import ChatManager
from typing import AsyncGenerator


async def get_redis_client() -> AsyncGenerator:
    """ Dependency to inject Redis client into routes/services """
    try:
        yield redis_client
    finally:
        await redis_client.close()


def get_chat_manager(redis_client: aioredis.Redis = Depends(get_redis_client)) -> ChatManager:
    chat_manager = ChatManager(redis_client=redis_client)
    return chat_manager

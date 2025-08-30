import logging
from redis import asyncio as aioredis
from enum import StrEnum
from app.core.config import settings
import uuid
import json


class ChatRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatManager:
    def __init__(self, redis_client: aioredis.Redis):
        self.redis_client = redis_client

    async def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        return session_id

    async def session_exists(self, session_id: str) -> bool:
        count = await self.redis_client.exists(f"chat_history:{session_id}")
        return count > 0

    async def add_message(self, *, session_id: str, role: ChatRole, content: str) -> bool:
        try:
            await self.redis_client.rpush(f"chat_history:{session_id}", json.dumps({"role": role, "content": content}))
            count = await self.redis_client.exists(f"chat_history:{session_id}")
            if (count == 1):
                await self.redis_client.expire(f"chat_history:{session_id}", time=settings.REDIS_CHAT_TTL)
            return True
        except Exception as e:
            logging.error(
                f"Error adding message to Redis for session {session_id}: {e}")
            return False

    async def get_history(self, session_id: str) -> list[dict[str, str]] | None:
        results = await self.redis_client.lrange(f"chat_history:{session_id}", 0, -1)
        results = [json.loads(item) for item in (results)]
        return results

    async def remove_session(self, session_id: str) -> bool:
        try:
            if await self.session_exists(session_id):
                await self.redis_client.delete(f"chat_history:{session_id}")
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Error removing session {session_id}: {e}")
            return False

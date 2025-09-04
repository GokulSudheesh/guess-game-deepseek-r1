from typing import List
from app.core.models.generic import AppResponse
from pydantic import BaseModel


class ChatItem(BaseModel):
    role: str
    content: str


class ChatHistoryResponse(AppResponse):
    data: List[ChatItem]

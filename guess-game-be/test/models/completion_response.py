from pydantic import BaseModel
from models.guess import Guess


class CompletionResponse(BaseModel):
    content: str
    data: dict | None = None
    usage_metadata: dict | None = None

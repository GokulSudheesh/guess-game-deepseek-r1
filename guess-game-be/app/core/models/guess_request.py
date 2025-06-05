from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.core.models.generic import AppResponse


class AnswerEnum(str, Enum):
    YES = "YES"
    NO = "NO"
    MAYBE = "MAYBE"
    DONT_THINK_SO = "DONT_THINK_SO"
    DONT_KNOW = "DONT_KNOW"


class GuessRequestBody(BaseModel):
    session_id: str
    answer: AnswerEnum


class GuessResponse(BaseModel):
    session_id: str
    question: str
    guess: Optional[str] = None
    confidence: float
    question_number: int


class GuessResponseWrapper(AppResponse):
    data: GuessResponse

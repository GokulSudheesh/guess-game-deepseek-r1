from pydantic import BaseModel, Field


class Guess(BaseModel):
    question: str = Field(
        description="yes or no question to ask the user. The question should be phrased in a way that can be answered with 'yes' or 'no'.")
    guess: str | None = Field(
        description="current guess of the person it can be null when the model is not sure")
    confidence: float = Field(
        description="confidence of the guess, a value between 0 and 1, where 1 means the model is very sure about the guess.")

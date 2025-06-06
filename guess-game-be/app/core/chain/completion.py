import math
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_ollama import ChatOllama
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda
from app.core.chain.prompts import chat_prompt_template, output_parser
from app.core.config import settings, Platform
import re
from app.core.models.completion_response import CompletionResponse
import logging


class Completion:
    def __init__(self):
        logging.info(
            f"Using {settings.PLATFORM_TO_USE.upper()} platform for completion")
        match settings.PLATFORM_TO_USE:
            case Platform.NVIDIA:
                rate_limiter = InMemoryRateLimiter(
                    # <-- Super slow! Sadly, we can only make a request once every 10 seconds!!
                    requests_per_second=0.1,
                    # Wake up every 100 ms to check whether allowed to make a request,
                    check_every_n_seconds=0.1,
                    max_bucket_size=10,  # Controls the maximum burst size.
                )
                self.model = ChatNVIDIA(
                    **settings.NVIDIA_MODEL_CONFIG,
                    rate_limiter=rate_limiter
                )
            case Platform.OLLAMA:
                self.model = ChatOllama(
                    **settings.OLLAMA_MODEL_CONFIG,
                )
        self.chain = chat_prompt_template | self.model.with_retry(
            stop_after_attempt=6, wait_exponential_jitter=True)

    async def invoke(self, params: dict) -> CompletionResponse:
        logging.info(f"Invoking completion with query: {params.get('query')}")
        query = params.get("query")
        chat_history = params.get("chat_history") or []
        response = await self.chain.ainvoke({"user_input": query, "history": chat_history})
        usage_metadata = (response.to_json().get(
            "kwargs", {}).get("usage_metadata", {}))
        content = response.text()
        return CompletionResponse(content=content, data={**self.clean_and_parse(content), "question_number": math.ceil(len(chat_history) / 2) + 1}, usage_metadata=usage_metadata)

    async def invoke_with_retry(self, *, query: str, chat_history: list[dict] | None = []) -> CompletionResponse:
        runnable = RunnableLambda(self.invoke)
        return await runnable.with_retry(
            stop_after_attempt=3,
            wait_exponential_jitter=True
        ).ainvoke({"query": query, "chat_history": chat_history})

    @staticmethod
    def clean_output(output: str):
        return re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)

    @staticmethod
    def clean_and_parse(output: str) -> dict | None:
        output = output_parser.parse(Completion.clean_output(
            output))
        return output


completion = Completion()

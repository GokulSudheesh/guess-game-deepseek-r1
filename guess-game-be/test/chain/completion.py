from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_ollama import ChatOllama
from langchain_core.rate_limiters import InMemoryRateLimiter
from chain.prompts import chat_prompt_template, output_parser
from config import config, Platform
import re
from models.completion_response import CompletionResponse


class Completion:
    def __init__(self):
        rate_limiter = InMemoryRateLimiter(
            # <-- Super slow! We can only make a request once every 10 seconds!!
            requests_per_second=0.1,
            # Wake up every 100 ms to check whether allowed to make a request,
            check_every_n_seconds=0.1,
            max_bucket_size=10,  # Controls the maximum burst size.
        )
        print(
            f"Using {config.PLATFORM_TO_USE.upper()} platform for completion")
        match config.PLATFORM_TO_USE:
            case Platform.NVIDIA:
                self.model = ChatNVIDIA(
                    **config.NVIDIA_MODEL_CONFIG,
                    rate_limiter=rate_limiter
                )
            case Platform.OLLAMA:
                self.model = ChatOllama(
                    **config.OLLAMA_MODEL_CONFIG,
                )
        self.chain = chat_prompt_template | self.model

    async def invoke(self, *, query: str, chat_history: list[dict] | None = None) -> CompletionResponse:
        response = await self.chain.ainvoke({"user_input": query, "history": chat_history or []})
        content = response.text()
        return CompletionResponse(content=content, data=self.clean_and_parse(content))

    @staticmethod
    def clean_output(output: str):
        return re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)

    @staticmethod
    def clean_and_parse(output: str) -> dict | None:
        try:
            output = output_parser.parse(Completion.clean_output(
                output))
            return output
        except Exception as e:
            print(f"Error parsing output: {e}")
            return None


completion = Completion()

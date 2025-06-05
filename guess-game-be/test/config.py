import os
from dataclasses import dataclass
from dotenv import load_dotenv
from dataclasses import field
from enum import StrEnum
from datetime import datetime
import re

# Load environment variables from .env file
load_dotenv()


class Platform(StrEnum):
    NVIDIA = "nvidia"
    OLLAMA = "ollama"


@dataclass
class Config():
    # Should be either "ollama" or "nvidia"
    PLATFORM_TO_USE: Platform = os.getenv("PLATFORM_TO_USE")
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY")
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL")
    NVIDIA_MODEL_NAME: str = os.getenv(
        "NVIDIA_MODEL_NAME", "deepseek-ai/deepseek-r1")

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_MODEL_NAME: str = os.getenv(
        "OLLAMA_MODEL_NAME")

    FILEPATH: str = os.path.join(
        os.path.dirname(__file__),
        "logs",
        f"log-{re.sub(r'[:.]', '-', datetime.now().isoformat())}.txt"
    )
    NVIDIA_MODEL_CONFIG: dict = field(default_factory=lambda: {
        "model": Config.NVIDIA_MODEL_NAME,
        "api_key": Config.NVIDIA_API_KEY,
        "temperature": 0.3,
        "max_tokens": 4096
    })

    OLLAMA_MODEL_CONFIG: dict = field(default_factory=lambda: {
        "base_url": Config.OLLAMA_BASE_URL,
        "model": Config.OLLAMA_MODEL_NAME,
        "temperature": 0.5,
        "max_tokens": 4096
    })


config = Config()

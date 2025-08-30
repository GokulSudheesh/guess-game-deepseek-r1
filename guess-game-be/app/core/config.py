import os
from dataclasses import dataclass
import sys
from dotenv import load_dotenv
from dataclasses import field
from enum import StrEnum
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    stream=sys.stdout,
)

# Load environment variables from .env file
load_dotenv()


class Platform(StrEnum):
    NVIDIA = "nvidia"
    OLLAMA = "ollama"


class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


@dataclass
class Settings():
    ENVIRONMENT: Environment = os.getenv("ENVIRONMENT")
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Guess Who"
    PROJECT_VERSION: str = "0.1.0"
    # Should be either "ollama" or "nvidia"
    PLATFORM_TO_USE: Platform = os.getenv("PLATFORM_TO_USE")
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY")
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL")
    NVIDIA_MODEL_NAME: str = os.getenv(
        "NVIDIA_MODEL_NAME", "deepseek-ai/deepseek-r1")

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_MODEL_NAME: str = os.getenv(
        "OLLAMA_MODEL_NAME")

    NVIDIA_MODEL_CONFIG: dict = field(default_factory=lambda: {
        "model": Settings.NVIDIA_MODEL_NAME,
        "api_key": Settings.NVIDIA_API_KEY,
        "temperature": 0.3,
        "max_tokens": 4096
    })

    OLLAMA_MODEL_CONFIG: dict = field(default_factory=lambda: {
        "base_url": Settings.OLLAMA_BASE_URL,
        "model": Settings.OLLAMA_MODEL_NAME,
        "temperature": 0.5,
        "max_tokens": 4096
    })

    # REDIS
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_DB: str = os.getenv("REDIS_DB", "0")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_CHAT_TTL: int = 5 * 60 * 60


settings = Settings()

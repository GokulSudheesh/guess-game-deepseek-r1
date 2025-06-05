import os
from dataclasses import dataclass
import sys
from dotenv import load_dotenv
from dataclasses import field
from enum import StrEnum
from datetime import datetime
import re
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

    FILEPATH: str = os.path.join(
        os.path.dirname(__file__),
        "logs",
        f"log-{re.sub(r'[:.]', '-', datetime.now().isoformat())}.txt"
    )
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


settings = Settings()

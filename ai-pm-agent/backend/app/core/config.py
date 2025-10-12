import os
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv


# Load nearest .env by searching upward from CWD
load_dotenv(find_dotenv(usecwd=True))


@dataclass
class Settings:
    env: str = os.getenv("ENV", "development")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    tavily_api_key: str | None = os.getenv("TAVILY_API_KEY")


settings = Settings()

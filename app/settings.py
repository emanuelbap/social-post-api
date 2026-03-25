from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/posts.db")
    users_api_url: str = os.getenv("USERS_API_URL", "http://localhost:8001/users")
    users_api_timeout: float = float(os.getenv("USERS_API_TIMEOUT", "5"))
    users_api_token: str | None = os.getenv("USERS_API_TOKEN")


@lru_cache
def get_settings() -> Settings:
    return Settings()
from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:98765@db:5432/pagamentos",
    )
    users_api_url: str = os.getenv("USERS_API_URL", "http://18.228.48.67/users")
    users_api_timeout: float = float(os.getenv("USERS_API_TIMEOUT", "5"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
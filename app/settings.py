from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:98765@db:5432/courses",
    )
    auth0_domain: str = os.getenv("AUTH0_DOMAIN", "")
    auth0_client_id: str = os.getenv("AUTH0_CLIENT_ID", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()
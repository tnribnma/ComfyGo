from functools import lru_cache
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ComfyGo API"
    APP_ENV: str = Field(
        default="development",
        description="development | staging | production",
    )
    APP_DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    FRONTEND_URL: str = "http://localhost:5500"

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "postgres"
    PG_PASS: str = 1234
    PG_DB: str = "comfygo"
    DATABASE_URL: Optional[str] = None  

    JWT_SECRET: str = "change-me-in-production-please"
    JWT_ALG: str = "HS256"
    JWT_EXP_MIN: int = 60
    JWT_REFRESH_EXP_DAYS: int = 7

    CORS_ORIGINS: List[str] = [
        "http://localhost:5500",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ]

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Resolved SQLAlchemy URL — uses DATABASE_URL if explicitly set."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg2://{self.PG_USER}:{self.PG_PASS}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Singleton accessor — returns one Settings instance for app lifetime."""
    return Settings()

settings: Settings = get_settings()
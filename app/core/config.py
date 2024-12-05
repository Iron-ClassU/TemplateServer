from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Basic Settings
    PROJECT_NAME: str = "Template Server"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Path Settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"  # Changed from TEMPLATE_DIR
    STATIC_DIR: Path = BASE_DIR / "static"

    # Database Settings
    SQLITE_URL: str = "sqlite+aiosqlite:///./dashboard.db"

    # Security Settings
    SECRET_KEY: str = "development_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_USERNAME: Optional[str] = None

    # Cache Settings
    CACHE_ENABLED: bool = False
    CACHE_TTL: int = 300  # 5 minutes
    CACHE_EXPIRE_MINUTES: int = 5

    # CORS Settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    PYTHONPATH: str = "."

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

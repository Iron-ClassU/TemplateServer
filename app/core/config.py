from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Base Settings
    PROJECT_NAME: str = "Dashboard Generator"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    SQLITE_URL: str = "sqlite+aiosqlite:///./dashboard.db"
    
    # Security
    SECRET_KEY: str = "development_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Cache Settings (will be used later with Redis)
    CACHE_ENABLED: bool = False
    CACHE_EXPIRE_MINUTES: int = 5
    
    # Template Settings
    TEMPLATE_DIR: str = "app/templates"
    STATIC_DIR: str = "app/static"

    class Config:
        case_sensitive = True

settings = Settings() 
"""
StudyChart AI - Application Settings and Configuration.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "StudyChart AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Security & Tokens
    SECRET_KEY: str = "studychart-super-secret-production-key-change-in-env-985dabbe23c3"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite:///./studychart.db"  # Works out of box, PostgreSQL URL in prod

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 120
    AUTH_RATE_LIMIT_PER_MINUTE: int = 15
    AI_RATE_LIMIT_PER_MINUTE: int = 30
    CODE_EXEC_RATE_LIMIT_PER_MINUTE: int = 20

    # AI Configuration
    AI_PROVIDER: str = "auto"  # auto | openai | gemini | anthropic | groq | ollama | local
    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gemini-1.5-flash"
    DAILY_AI_REQUEST_LIMIT: int = 100

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Sandboxed Code Execution
    CODE_EXECUTION_TIMEOUT_SECONDS: int = 5
    MAX_MEMORY_MB: int = 128

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()

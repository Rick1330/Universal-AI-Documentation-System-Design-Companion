from pydantic_settings import BaseSettings # Updated import for Pydantic v2
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Universal Data Extractor + Analyzer"
    API_V1_STR: str = "/api/v1"

    # PostgreSQL Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "your_db_user"
    POSTGRES_PASSWORD: str = "your_db_password"
    POSTGRES_DB: str = "udea_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # MinIO Object Storage
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "udea-uploads"
    MINIO_USE_SSL: bool = False

    # Celery Task Queue (using Redis as broker and backend)
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # OpenAI API Key (or other LLM provider)
    OPENAI_API_KEY: str = "your_openai_api_key_here"

    # Logging Configuration
    LOG_LEVEL: str = "INFO" # DEBUG, INFO, WARNING, ERROR, CRITICAL

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True # Default, but good to be explicit

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()


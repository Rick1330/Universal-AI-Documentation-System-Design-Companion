from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Universal Data Extractor + Analyzer"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: str | None = None

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "uploads"
    MINIO_USE_SSL: bool = False

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # OpenAI API Key
    OPENAI_API_KEY: str = "your_openai_api_key_here"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()


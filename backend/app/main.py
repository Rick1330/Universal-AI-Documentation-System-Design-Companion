from fastapi import FastAPI
from .api.v1.router import api_router # Corrected import
from .core.config import settings # Corrected import
from .db.session import engine # Corrected import
from .db import base as db_base # Corrected import
from .core.logging_config import setup_logging, logger # Corrected import, ensure logger is available
import os # Import os

# Create database tables - only if not running under pytest
# In a production setup with Alembic, this would be handled by migrations
if os.getenv("RUNNING_PYTEST") != "true":
    logger.info("Application not running under pytest, creating database tables if they don't exist.")
    db_base.Base.metadata.create_all(bind=engine)
else:
    logger.info("Application running under pytest, skipping automatic table creation in main.py.")

# Setup logging - logger is now imported from logging_config
# logger = setup_logging() # This is already done in logging_config.py and logger is imported

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup...")
    # You can add other startup logic here, like connecting to a message broker if not handled by Celery worker
    # For example, ensure MinIO bucket exists (though file_handler does this on first use)
    try:
        from .services.file_handler import client as minio_client # Corrected import
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
            logger.info(f"MinIO bucket 	'{settings.MINIO_BUCKET_NAME}	' created.")
        else:
            logger.info(f"MinIO bucket 	'{settings.MINIO_BUCKET_NAME}	' already exists.")
    except Exception as e:
        logger.error(f"Error checking/creating MinIO bucket during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown...")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["healthcheck"])
async def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "ok"}

# For local development without Docker, you might run with uvicorn directly:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL.lower())


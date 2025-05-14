from fastapi import FastAPI
from ..app.api.v1.router import api_router
from ..app.core.config import settings
from ..app.db.session import engine #, SessionLocal
from ..app.db import base as db_base # To create tables
from ..app.core.logging_config import setup_logging # Import the setup function

# Create database tables
# In a production setup with Alembic, this would be handled by migrations
db_base.Base.metadata.create_all(bind=engine)

# Setup logging
logger = setup_logging() # Initialize and get the logger instance

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
        from ..app.services.file_handler import client as minio_client, settings as minio_settings
        if not minio_client.bucket_exists(minio_settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(minio_settings.MINIO_BUCKET_NAME)
            logger.info(f"MinIO bucket 	ható{minio_settings.MINIO_BUCKET_NAME}" created.")
        else:
            logger.info(f"MinIO bucket 	ható{minio_settings.MINIO_BUCKET_NAME}" already exists.")
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


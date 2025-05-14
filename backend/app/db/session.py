from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os # Import os module

from app.core.config import settings # Corrected import

# Check if running under pytest
if os.getenv("RUNNING_PYTEST") == "true":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Construct PostgreSQL URI from settings if not fully provided
    if settings.SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
    else:
        SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


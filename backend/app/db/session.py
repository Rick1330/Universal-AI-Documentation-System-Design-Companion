from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

if settings.POSTGRES_SERVER and settings.POSTGRES_USER and settings.POSTGRES_PASSWORD and settings.POSTGRES_DB:
    settings.SQLALCHEMY_DATABASE_URI = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
else:
    # Fallback to SQLite if not all PostgreSQL settings are provided (for local dev without full setup)
    settings.SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    print("Warning: PostgreSQL credentials not fully provided, falling back to SQLite for DB.")

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    # connect_args={"check_same_thread": False} # Only for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import SQLALCHEMY_DATABASE_URL
from .models import Base # Import Base from your models.py

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # connect_args={"check_same_thread": False} # Only needed for SQLite if using threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    # This function will create all tables defined in models.py
    # that inherit from Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist already).")

# If you want to run this directly to create tables:
# if __name__ == "__main__":
#     create_db_and_tables()


from contextlib import asynccontextmanager # Moved to the top
from fastapi import FastAPI
from .database import create_db_and_tables, engine # Import create_db_and_tables
from .models import Base # Ensure Base is imported if not already via database.py

# Create database tables on startup
# This is suitable for development/testing. 
# For production, you would typically use a migration tool like Alembic.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Creating database tables...")
    create_db_and_tables()
    yield
    # Shutdown (if any cleanup needed)
    print("Application shutdown.")

app = FastAPI(
    title="Universal AI Documentation System Design Companion Backend",
    lifespan=lifespan
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Universal AI Documentation System Design Companion Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


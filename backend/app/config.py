import os

# For local development, we can use a SQLite database.
# In a production environment, this would typically be a PostgreSQL connection string.
# Example for PostgreSQL: "postgresql://user:password@host:port/database"

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres_db:5432/app_db")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


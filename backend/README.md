# Backend for Universal AI Documentation System Design Companion

This directory contains the backend services for the Universal AI Documentation System Design Companion project.

## Database Setup

The backend uses SQLAlchemy to define and interact with the database. The initial schema includes tables for `jobs` and `uploaded_files`.

-   **Models**: Defined in `app/models.py`.
-   **Database Configuration**: Managed in `app/config.py`. By default, it uses a local SQLite database (`./test.db`) for development. This can be configured via the `DATABASE_URL` environment variable for PostgreSQL in production.
-   **Database Initialization**: Tables are automatically created on application startup (see `app/main.py` and `app/database.py`). For production, a migration tool like Alembic would be recommended.

To initialize the database manually (if not running the FastAPI app), you can adapt the `create_db_and_tables()` function in `app/database.py`.


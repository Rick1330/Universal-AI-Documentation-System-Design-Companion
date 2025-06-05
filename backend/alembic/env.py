from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Configure more verbose logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("alembic.env")

# Import your Base from models.py
# Ensure that your application modules are importable from here.
import sys
import os

# Explicitly add the project root (backend directory) to sys.path
# This allows alembic to find the 'app' module
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
logger.debug(f"Added to sys.path: {PROJECT_ROOT}")

try:
    from app.models import Base  # Now app.models should be reliably importable
    from app.config import SQLALCHEMY_DATABASE_URL # To use the same URL as the app
    
    # Debug: Print metadata information
    logger.debug(f"Base.metadata tables: {list(Base.metadata.tables.keys())}")
    for table_name in Base.metadata.tables:
        logger.debug(f"Table {table_name} columns: {[c.name for c in Base.metadata.tables[table_name].columns]}")
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Current sys.path: {sys.path}")
    raise

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLAlchemy URL from our application's config
# This ensures Alembic uses the same database as the application.
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
logger.debug(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata
logger.debug(f"target_metadata tables: {list(target_metadata.tables.keys())}")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    logger.debug(f"Offline mode using URL: {url}")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Add this to compare column types
        compare_server_default=True,  # Add this to compare default values
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    logger.debug(f"Online mode using engine: {connectable}")

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,  # Add this to compare column types
            compare_server_default=True,  # Add this to compare default values
        )
        
        logger.debug("Starting migration transaction")
        with context.begin_transaction():
            context.run_migrations()
        logger.debug("Completed migration transaction")


if context.is_offline_mode():
    logger.debug("Running in offline mode")
    run_migrations_offline()
else:
    logger.debug("Running in online mode")
    run_migrations_online()

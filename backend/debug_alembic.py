"""
Debug script to modify alembic/env.py to print debug information during migration generation.
This will help us understand why Alembic isn't detecting our models.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alembic_debug")

# Add the project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Import the models
from app.models import Base

def debug_alembic_metadata():
    """Print detailed information about Base.metadata for Alembic debugging."""
    logger.info("Debugging Base.metadata for Alembic")
    logger.info("-" * 50)
    
    # Check if Base.metadata contains tables
    table_names = list(Base.metadata.tables.keys())
    logger.info(f"Base.metadata tables: {table_names}")
    
    # Print details of each table
    for table_name in table_names:
        table = Base.metadata.tables[table_name]
        logger.info(f"\nTable: {table_name}")
        logger.info(f"Columns: {[c.name for c in table.columns]}")
        logger.info(f"Primary key: {table.primary_key.columns.keys()}")
        
        # Print foreign keys if any
        fkeys = []
        for c in table.columns:
            if c.foreign_keys:
                for fk in c.foreign_keys:
                    fkeys.append(f"{c.name} -> {fk.target_fullname}")
        if fkeys:
            logger.info(f"Foreign keys: {fkeys}")
    
    logger.info("-" * 50)

if __name__ == "__main__":
    debug_alembic_metadata()

#!/usr/bin/env python
"""
Debug script to verify SQLAlchemy models and metadata.
This script checks if the models are properly defined and if Base.metadata contains the expected tables.
"""

import os
import sys

# Add the project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Import the models
from app.models import Base, Job, UploadedFile

def debug_models():
    """Print information about the SQLAlchemy models and metadata."""
    print("Debugging SQLAlchemy Models and Metadata")
    print("-" * 50)
    
    # Check if Base.metadata contains tables
    print(f"Base.metadata tables: {Base.metadata.tables.keys()}")
    
    # Check if the models are properly defined
    print(f"\nJob.__table__: {getattr(Job, '__table__', None)}")
    print(f"UploadedFile.__table__: {getattr(UploadedFile, '__table__', None)}")
    
    # Print table details if available
    if hasattr(Job, '__table__'):
        print(f"\nJob table columns: {[c.name for c in Job.__table__.columns]}")
    
    if hasattr(UploadedFile, '__table__'):
        print(f"UploadedFile table columns: {[c.name for c in UploadedFile.__table__.columns]}")

if __name__ == "__main__":
    debug_models()

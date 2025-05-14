import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

# Try to import the app and the original get_db function
# This structure helps in making conftest.py more self-contained for setup
try:
    from backend.app.main import app
    from backend.app.db.session import get_db as original_get_db
    APP_IMPORTED = True
except ImportError:
    APP_IMPORTED = False
    app = None # Placeholder if import fails, tests relying on app will skip or fail clearly
    original_get_db = None

@pytest.fixture(scope="function")
def db_session_mock():
    """Mocks the database session."""
    session = MagicMock(spec=Session)
    session.commit = MagicMock()
    session.add = MagicMock()
    session.refresh = MagicMock()
    session.rollback = MagicMock()
    session.query = MagicMock()
    # Example of how to mock a query result:
    # mock_instance = MagicMock()
    # session.query.return_value.filter.return_value.first.return_value = mock_instance
    return session

@pytest.fixture(scope="function")
def client(db_session_mock):
    """Provides a TestClient instance with the database dependency overridden."""
    if not APP_IMPORTED or not app or not original_get_db:
        pytest.skip("FastAPI app or original_get_db could not be imported. Skipping API tests.")

    def get_db_override():
        return db_session_mock

    # Apply the override before creating the TestClient
    app.dependency_overrides[original_get_db] = get_db_override
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up the override after the test session
    app.dependency_overrides.pop(original_get_db, None)


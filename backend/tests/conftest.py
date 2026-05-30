"""Pytest configuration and fixtures for testing."""
import pytest
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from config import TestingConfig
from services import init_container


@pytest.fixture(scope="session")
def app():
    """Create Flask app for testing."""
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def container():
    """Provide service container for testing."""
    container = init_container()
    yield container
    # Cleanup after test
    container.reset()


@pytest.fixture
def mock_db(monkeypatch):
    """Mock database for unit testing repositories."""
    class MockDB:
        def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
            return None

        def execute_update(self, query, params=None):
            return 1

        def execute_insert(self, query, params=None):
            return 1

    return MockDB()

"""
Pytest configuration and fixtures for backend tests.
"""
import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_path = str(Path(__file__).parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def test_db():
    """Provide a test database connection."""
    # This can be expanded to set up test database
    pass

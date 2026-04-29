"""
Pytest configuration and fixtures for backend tests.
"""
import pytest


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "query": "machine learning",
        "results": [],
        "status": "success"
    }


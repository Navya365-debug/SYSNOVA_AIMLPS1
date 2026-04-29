"""
API Tests for SYSNOVA_AIMLPS1 Backend
"""
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_api_info_endpoint(client):
    """Test API info endpoint."""
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "services" in data


def test_detailed_health_check(client):
    """Test detailed health check endpoint."""
    response = client.get("/api/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data


def test_search_endpoint(client):
    """Test search endpoint."""
    response = client.post(
        "/api/search/",
        json={
            "query": "machine learning",
            "sources": ["arxiv", "pubmed"],
            "max_results": 5,
            "use_personalization": True,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert "total_results" in data
    assert isinstance(data["results"], list)


def test_search_suggestions(client):
    """Test search suggestions endpoint."""
    response = client.get("/api/search/suggestions?query=machine&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_trending_topics(client):
    """Test trending topics endpoint."""
    response = client.get("/api/search/trending?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_user_profile(client):
    """Test user profile endpoint."""
    response = client.get("/api/user/profile?user_id=test_user")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "research_interests" in data


def test_graph_explore(client):
    """Test graph explore endpoint."""
    response = client.post(
        "/api/graph/explore",
        json={
            "query": "machine learning",
            "max_nodes": 10,
            "max_depth": 2,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)


def test_graph_statistics(client):
    """Test graph statistics endpoint."""
    response = client.get("/api/graph/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "total_nodes" in data
    assert "total_edges" in data


def test_cors_headers(client):
    """Test CORS headers are present."""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

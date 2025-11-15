"""
Test suite for InfinityInsight
Run with: pytest tests/
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "InfinityInsight" in response.json()["message"]


def test_api_docs():
    """Test API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


# Add more tests as needed

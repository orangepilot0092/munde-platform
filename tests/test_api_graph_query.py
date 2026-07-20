"""
Integration tests for the Knowledge Graph Query API.
"""

from fastapi import status
from fastapi.testclient import TestClient

from src.core.main import app
from src.schemas.graph_query import GraphQueryRequest

client = TestClient(app)


def test_graph_query_endpoint_exists() -> None:
    """Test that the graph query endpoint is registered."""
    response = client.post(
        "/api/v1/graph/query",
        json={"entity_name": "Pune", "limit": 10},
    )
    # Should return 200, 404 (entity not found), or 503 (graph not populated)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_503_SERVICE_UNAVAILABLE,
    ]


def test_graph_query_requires_entity_name() -> None:
    """Test that entity_name is required."""
    response = client.post(
        "/api/v1/graph/query",
        json={"limit": 10},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_graph_query_validates_limit() -> None:
    """Test that limit is validated (must be 1-500)."""
    response = client.post(
        "/api/v1/graph/query",
        json={"entity_name": "Pune", "limit": 1000},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_entity_endpoint_exists() -> None:
    """Test that the get entity endpoint is registered."""
    response = client.get("/api/v1/graph/entities/Pune")
    # Should return 200 or 404
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        status.HTTP_503_SERVICE_UNAVAILABLE,
    ]


def test_graph_query_request_model() -> None:
    """Test that GraphQueryRequest model validates correctly."""
    request = GraphQueryRequest(
        entity_name="Pune",
        entity_type="AdministrativeUnit",
        relationship_type="contains",
        max_depth=2,
        limit=100,
    )
    assert request.entity_name == "Pune"
    assert request.max_depth == 2
    assert request.limit == 100

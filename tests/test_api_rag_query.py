"""
Integration tests for the Production RAG Query API.
Validates RBAC, structured responses, guardrails, and error handling.
"""

from unittest.mock import MagicMock, patch

from fastapi import status
from fastapi.testclient import TestClient

from src.core.main import app

client = TestClient(app)


def test_rag_query_requires_authentication() -> None:
    """Test that the RAG query endpoint rejects unauthenticated requests."""
    response = client.post(
        "/api/v1/intelligence/query",
        json={"query": "What is the rainfall in Pune?"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_rag_query_succeeds_with_valid_role() -> None:
    """Test that the RAG query endpoint succeeds with a valid role header."""
    mock_results = [
        {
            "id": "doc_1",
            "name": "Pune Rainfall Data",
            "type": "dataset",
            "description": "Rainfall data for Pune district is 900mm annually.",
            "vec_score": 0.95,
        }
    ]

    mock_llm_response = MagicMock()
    mock_llm_response.response = (
        "The rainfall in Pune is 900mm annually, according to Pune Rainfall Data."
    )

    with patch(
        "src.api.v1.rag_query.SearchService.search_datasets", return_value=mock_results
    ):
        with patch(
            "src.api.v1.rag_query.LLMService.generate", return_value=mock_llm_response
        ):
            response = client.post(
                "/api/v1/intelligence/query",
                json={
                    "query": "What is the rainfall in Pune?",
                    "domain": "agriculture",
                    "include_knowledge_graph": True,
                    "max_results": 5,
                },
                headers={
                    "X-User-ID": "user_123",
                    "X-User-Role": "officer",
                    "X-User-Department": "Agriculture",
                },
            )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "answer" in data
    assert "confidence_score" in data
    assert 0.0 <= data["confidence_score"] <= 1.0
    assert "citations" in data
    assert isinstance(data["citations"], list)
    assert len(data["citations"]) > 0
    assert "reasoning_steps" in data
    assert "metadata" in data
    assert "latency_ms" in data["metadata"]
    assert "faithfulness_score" in data["metadata"]


def test_rag_query_validates_query_length() -> None:
    """Test that the RAG query endpoint validates minimum query length."""
    response = client.post(
        "/api/v1/intelligence/query",
        json={"query": "Hi"},  # Less than min_length=3
        headers={"X-User-Role": "officer"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_rag_query_validates_max_results() -> None:
    """Test that max_results is bounded (1-20)."""
    response = client.post(
        "/api/v1/intelligence/query",
        json={"query": "Test query", "max_results": 100},
        headers={"X-User-Role": "officer"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_rag_query_pii_redaction_in_logs() -> None:
    """Test that the PII redaction guardrail functions correctly."""
    from src.api.v1.rag_query import _redact_pii

    test_string = "Contact me at test@example.com or call 9876543210"
    redacted = _redact_pii(test_string)

    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_PHONE]" in redacted
    assert "test@example.com" not in redacted
    assert "9876543210" not in redacted

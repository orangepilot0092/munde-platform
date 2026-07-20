import pytest
from fastapi.testclient import TestClient
from src.core.main import app


@pytest.fixture
def client():
    """Provide a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def test_db_url():
    """Provide a test database URL."""
    return "postgresql://sahyadri:sahyadri_secret@localhost:5432/sahyadri_db_test"


# Note: In a production setup, we would use docker-compose to spin up
# isolated test containers for Postgres and Redis. For now, we use
# the local dev instances but target a different DB name if possible,
# or rely on transaction rollbacks.

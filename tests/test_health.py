from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics_endpoint(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_gc_objects_collected_total" in response.text


def test_api_versioning_root(client: TestClient):
    # Ensure the v1 router is mounted
    # We can check the OpenAPI schema for paths starting with /api/v1
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    # Check if any path starts with /api/v1
    v1_paths = [p for p in paths.keys() if p.startswith("/api/v1")]
    assert len(v1_paths) > 0, "No /api/v1 paths found"

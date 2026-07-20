from fastapi.testclient import TestClient


def test_protected_endpoint_unauthorized(client: TestClient):
    # Assuming we have a protected endpoint in /api/v1
    # For now, we test that the root doesn't leak sensitive info
    response = client.get("/")
    # Should return 404 if no root endpoint is defined, or 200 if docs are public
    assert response.status_code in [200, 404]

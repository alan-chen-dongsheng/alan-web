from fastapi.testclient import TestClient

from app.main import app
from app.schemas.health import HealthResponse


def test_health_endpoint_returns_pydantic_response() -> None:
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert HealthResponse.model_validate(response.json()).status == "ok"

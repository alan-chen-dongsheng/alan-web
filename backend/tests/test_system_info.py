from fastapi.testclient import TestClient

from app.main import app
from app.schemas.system_info import SystemInfoResponse


def test_system_info_endpoint_returns_basic_platform_details() -> None:
    response = TestClient(app).get("/api/system-info")

    assert response.status_code == 200
    system_info = SystemInfoResponse.model_validate(response.json())
    assert system_info.os
    assert system_info.os_version
    assert system_info.python_version

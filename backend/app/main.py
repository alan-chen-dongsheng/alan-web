import platform

from fastapi import FastAPI

from app.schemas.health import HealthResponse
from app.schemas.system_info import SystemInfoResponse

app = FastAPI(title="项目 API", version="0.1.0")


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/system-info", response_model=SystemInfoResponse)
def system_info() -> SystemInfoResponse:
    return SystemInfoResponse(
        os=platform.system(),
        os_version=platform.release(),
        python_version=platform.python_version(),
    )

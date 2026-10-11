from pydantic import BaseModel


class SystemInfoResponse(BaseModel):
    os: str
    os_version: str
    python_version: str

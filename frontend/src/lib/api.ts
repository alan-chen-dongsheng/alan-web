export interface HealthResponse {
  status: string;
}

export interface SystemInfoResponse {
  os: string;
  os_version: string;
  python_version: string;
}

function isHealthResponse(value: unknown): value is HealthResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'status' in value &&
    typeof value.status === 'string'
  );
}

export async function getHealth(signal?: AbortSignal): Promise<HealthResponse> {
  const response = await fetch('/api/health', { signal });
  if (!response.ok) {
    throw new Error(`健康检查请求失败（HTTP ${response.status}）`);
  }

  const payload: unknown = await response.json();
  if (!isHealthResponse(payload)) {
    throw new Error('健康检查响应格式无效');
  }

  return payload;
}

function isSystemInfoResponse(value: unknown): value is SystemInfoResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'os' in value &&
    typeof value.os === 'string' &&
    'os_version' in value &&
    typeof value.os_version === 'string' &&
    'python_version' in value &&
    typeof value.python_version === 'string'
  );
}

export async function getSystemInfo(signal?: AbortSignal): Promise<SystemInfoResponse> {
  const response = await fetch('/api/system-info', { signal });
  if (!response.ok) {
    throw new Error(`系统信息请求失败（HTTP ${response.status}）`);
  }

  const payload: unknown = await response.json();
  if (!isSystemInfoResponse(payload)) {
    throw new Error('系统信息响应格式无效');
  }

  return payload;
}

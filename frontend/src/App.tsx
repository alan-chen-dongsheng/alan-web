import { useEffect, useState } from 'react';
import { StyleProvider } from '@ant-design/cssinjs';
import { Alert, Button, Card, ConfigProvider, Descriptions, Spin, Typography } from 'antd';
import { getHealth, getSystemInfo, type SystemInfoResponse } from './lib/api';

type HealthState =
  | { kind: 'loading' }
  | { kind: 'ready'; status: string }
  | { kind: 'error' };

type SystemInfoState =
  | { kind: 'loading' }
  | { kind: 'ready'; info: SystemInfoResponse }
  | { kind: 'error' };

function navigate(path: string, setPath: (path: string) => void) {
  window.history.pushState(null, '', path);
  setPath(path);
}

function HomePage({ setPath }: { setPath: (path: string) => void }) {
  const [health, setHealth] = useState<HealthState>({ kind: 'loading' });

  useEffect(() => {
    const controller = new AbortController();

    getHealth(controller.signal)
      .then(({ status }) => setHealth({ kind: 'ready', status }))
      .catch(() => {
        if (!controller.signal.aborted) {
          setHealth({ kind: 'error' });
        }
      });

    return () => controller.abort();
  }, []);

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-6 py-16">
      <Typography.Title level={1}>全栈项目</Typography.Title>
      <Typography.Paragraph className="text-gray-600">
        前端和 FastAPI 后端连接状态
      </Typography.Paragraph>
      <Card title="API 健康检查" className="mt-8 max-w-xl">
        {health.kind === 'loading' && <Spin aria-label="正在连接后端" />}
        {health.kind === 'ready' && (
          <Alert type="success" showIcon message={`API 状态正常：${health.status}`} />
        )}
        {health.kind === 'error' && (
          <Alert type="error" showIcon message="无法连接后端 API，请确认 FastAPI 正在运行。" />
        )}
        <Button className="mt-6" type="primary" onClick={() => navigate('/system-info', setPath)}>
          查看系统信息
        </Button>
      </Card>
    </main>
  );
}

function SystemInfoPage({ setPath }: { setPath: (path: string) => void }) {
  const [state, setState] = useState<SystemInfoState>({ kind: 'loading' });

  useEffect(() => {
    const controller = new AbortController();

    getSystemInfo(controller.signal)
      .then((info) => setState({ kind: 'ready', info }))
      .catch(() => {
        if (!controller.signal.aborted) {
          setState({ kind: 'error' });
        }
      });

    return () => controller.abort();
  }, []);

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-6 py-16">
      <Typography.Title level={1}>系统信息</Typography.Title>
      <Typography.Paragraph className="text-gray-600">
        以下信息由 FastAPI 后端所在的系统提供。
      </Typography.Paragraph>
      <Card className="mt-8 max-w-xl">
        {state.kind === 'loading' && <Spin aria-label="正在获取系统信息" />}
        {state.kind === 'error' && (
          <Alert type="error" showIcon message="无法获取系统信息，请确认 FastAPI 正在运行。" />
        )}
        {state.kind === 'ready' && (
          <Descriptions column={1}>
            <Descriptions.Item label="操作系统">{state.info.os}</Descriptions.Item>
            <Descriptions.Item label="系统版本">{state.info.os_version}</Descriptions.Item>
            <Descriptions.Item label="Python 版本">{state.info.python_version}</Descriptions.Item>
          </Descriptions>
        )}
        <Button className="mt-6" onClick={() => navigate('/', setPath)}>
          返回首页
        </Button>
      </Card>
    </main>
  );
}

export function App() {
  const [path, setPath] = useState(window.location.pathname);

  useEffect(() => {
    const handlePopState = () => setPath(window.location.pathname);
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  return (
    <StyleProvider layer>
      <ConfigProvider>
        {path === '/system-info' ? (
          <SystemInfoPage setPath={setPath} />
        ) : (
          <HomePage setPath={setPath} />
        )}
      </ConfigProvider>
    </StyleProvider>
  );
}

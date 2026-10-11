import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { App } from './App';

describe('App API health status', () => {
  beforeEach(() => {
    window.history.replaceState(null, '', '/');
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('shows the backend status when the health endpoint responds', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok' }),
    } as Response);

    render(<App />);

    expect(await screen.findByText('API 状态正常：ok')).toBeInTheDocument();
  });

  it('shows a useful message when the health endpoint cannot be reached', async () => {
    vi.mocked(fetch).mockRejectedValue(new Error('offline'));

    render(<App />);

    expect(await screen.findByRole('alert')).toHaveTextContent('无法连接后端 API');
  });

  it('navigates to a new page and displays system information from the backend', async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'ok' }),
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ os: 'Darwin', os_version: '24.0.0', python_version: '3.12.0' }),
      } as Response);

    render(<App />);
    fireEvent.click(await screen.findByRole('button', { name: '查看系统信息' }));

    expect(await screen.findByText('系统信息')).toBeInTheDocument();
    expect(await screen.findByText('Darwin')).toBeInTheDocument();
    expect(screen.getByText('24.0.0')).toBeInTheDocument();
    expect(screen.getByText('3.12.0')).toBeInTheDocument();
    expect(window.location.pathname).toBe('/system-info');
    expect(fetch).toHaveBeenLastCalledWith('/api/system-info', { signal: expect.any(AbortSignal) });
  });
});

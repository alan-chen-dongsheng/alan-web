# 全栈项目

本项目在同一个目录中维护前端、后端、本地数据和独立 Python 工具。

## 目录

- `frontend/`：React、TypeScript、Vite、Tailwind CSS 和 Ant Design 前端。
- `backend/`：Python 3.12、FastAPI 与 Pydantic API。
- `data/`：本地运行数据；目录内容默认不纳入版本控制。
- `python-tools/`：各自使用 uv 环境的外部 Python 命令行工具。

## 环境

- Node.js 24 LTS；根目录 `.nvmrc` 选择 24 主版本。
- pnpm 12；前端依赖定义在 `frontend/package.json`。
- Python 3.12；`backend/` 和每个工具目录通过 `.python-version` 固定版本。
- uv 0.9 或兼容的稳定版。
- 前端选择 React 19.3、Ant Design 6.6、Vite 8.1、Tailwind CSS 4.3 和 TypeScript 7；依赖范围见 `frontend/package.json`。

## 安装依赖

确保 Node.js 24 和 pnpm 12 可用，然后运行：

```bash
cd frontend
pnpm install

cd ../backend
uv python install 3.12
uv sync

cd ../python-tools/example_tool
uv python install 3.12
uv sync
```

## 启动开发服务

在两个终端分别运行：

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
pnpm dev
```

Vite 将前端 `/api` 请求代理到 `http://127.0.0.1:8000`。健康检查地址为 `/api/health`。
首页的“查看系统信息”按钮会跳转到 `/system-info`，并通过 `/api/system-info` 获取后端所在系统的操作系统名称、系统版本和 Python 版本。

## 运行独立 Python 工具

```bash
cd python-tools/example_tool
uv run python main.py --value "示例输入"
```

后端的 `app.services.tool_runner.run_tool` 通过参数数组运行工具，默认超时为 30 秒，并返回退出码、标准输出和错误输出。

## 检查前端

```bash
cd frontend
pnpm test -- --run
pnpm build
```

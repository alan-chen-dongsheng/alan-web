# 全栈项目基础架构设计

## 目标

在同一个项目目录中建立本地开发基础环境，清晰划分前端、后端、数据和外部 Python 工具，并采用用户确认的技术栈。

## 已确认的技术栈

- 前端：兼容的当前 Node.js LTS、pnpm、稳定版 React、严格模式 TypeScript、Vite、Tailwind CSS 和 Ant Design。
- 后端：Python 3.12、uv、FastAPI 和 Pydantic。
- 项目结构：同一项目目录下包含 `frontend/`、`backend/`、`data/` 和 `python-tools/`。
- 外部 Python 工具：使用独立 uv 环境，由后端作为命令行程序调用。

## 架构

### `frontend/`

存放 React 应用、TypeScript 配置、Vite 开发与构建配置、Tailwind CSS 配置和 Ant Design 组件。初始页面可以调用后端健康检查接口。开发时，Vite 将约定的 API 路径代理到本地 FastAPI 服务。

### `backend/`

存放 FastAPI 应用、Pydantic 请求与响应模型，并通过自己的 `pyproject.toml` 使用 uv 管理依赖。后端提供健康检查接口，并提供明确的命令行调用边界来运行 `python-tools/` 下的工具。

### `data/`

存放本地运行数据和生成文件，不放源代码或依赖。运行时数据应被版本控制忽略，同时保留一个占位文件，确保新检出项目时目录存在。

### `python-tools/`

存放独立于 API 包的 Python 命令行工具。每个工具可以有自己的 `pyproject.toml` 和 uv 环境。后端使用参数数组启动工具进程，并收集退出状态和输出；不在后端进程中导入工具模块。

## 本地开发流程

- 在 `frontend/` 中使用 pnpm 安装前端依赖。
- 在 `backend/` 中使用 uv 同步后端依赖。
- 分别运行 Vite 和 FastAPI；前端的 `/api` 请求由 Vite 代理到 FastAPI。
- 需要运行工具时，在对应工具的 uv 项目中管理并安装其依赖。
- 根目录 README 记录准确的命令和环境版本要求。实施脚手架时，选择当时兼容的 Node.js LTS。

## 范围与边界

此基础环境不包含数据库、身份验证、部署流水线、容器配置或通用任务队列。后续功能确定持久化需求之前，`data/` 仅作为本地文件系统目录。初始工具调用采用同步命令行执行；长时间运行任务和后台任务编排不在本次范围内。

## 验收标准

1. 新检出的项目包含四个顶层目录，根目录 README 说明安装和启动命令。
2. 前后端依赖分别由 pnpm 和 uv 管理。
3. TypeScript 启用严格类型检查。
4. React 使用稳定版本，Node.js 使用实施时选定的兼容 LTS 版本。
5. 前端同时配置 Tailwind CSS 和 Ant Design。
6. FastAPI 健康检查接口返回经 Pydantic 校验的响应，前端可以通过 Vite `/api` 代理访问。
7. 本地运行数据不纳入版本控制。
8. Python 工具作为独立 uv 管理的命令行项目运行，后端可通过清晰边界调用。

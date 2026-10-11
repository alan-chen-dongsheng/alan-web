# Repository Guidelines

本文档面向本仓库的贡献者。请保持项目边界清晰，新增说明文档使用简体中文。

## 项目结构与模块

- `frontend/`：React、TypeScript、Vite、Tailwind CSS 与 Ant Design；页面和组件位于 `src/`，界面测试与源码同目录并以 `.test.tsx` 结尾。
- `backend/`：FastAPI、Pydantic 服务；应用代码在 `app/`，pytest 测试在 `tests/`。
- `data/`：本地运行数据目录。运行时数据默认忽略，不要提交数据库、缓存或用户数据。
- `python-tools/<工具名>/`：独立 uv 管理的 Python CLI 项目，每个工具包含自己的 `pyproject.toml` 和 `.python-version`。
- `scripts/`：仓库级维护脚本；`docs/`：设计和实施文档。

## 开发、构建与测试

按模块安装依赖，命令从相应目录执行：

```bash
cd frontend && pnpm install
cd frontend && pnpm dev                 # 启动 Vite
cd frontend && pnpm test -- --run       # 运行 Vitest
cd frontend && pnpm build               # TypeScript 检查并构建
cd backend && uv sync --group dev        # 安装后端及开发依赖
cd backend && uv run uvicorn app.main:app --reload --port 8000
cd backend && uv run pytest             # 运行后端测试
cd python-tools/example_tool && uv run python main.py --value "示例输入"
python3 scripts/check_structure.py      # 检查仓库必需结构
```

使用 Node.js 24、pnpm 12、Python 3.12 和 uv。前端 `/api` 通过 Vite 代理到本地后端。
通常在不同终端分别启动前端和后端；独立工具从自身目录执行，以确保 uv 读取该工具的依赖配置。

## 编码风格与命名

TypeScript 启用严格类型检查；组件和类型使用 PascalCase，变量、函数与文件使用 camelCase（测试文件遵循已有 `.test.tsx` 命名）。Python 使用 4 空格缩进，函数和模块采用 `snake_case`，类型采用 `PascalCase`。新增 API 请求和响应应使用 Pydantic 模型定义；运行独立工具时传递参数数组，避免 shell 拼接。仓库未配置自动格式化或 lint 工具，请沿用邻近代码风格。
保持前后端健康检查契约 `/api/health` 一致。新增 Python 工具时，为工具建立单独目录和 `pyproject.toml`，不要把第三方工具依赖并入后端环境。

## 测试指南

新增行为时，为前端交互/API 状态添加 Vitest 与 Testing Library 用例；后端使用 pytest，文件名为 `test_*.py`。覆盖正常结果、失败响应和边界条件。提交前运行相关模块测试，以及前端 `pnpm build` 或后端 `uv run pytest`。

## 提交与 Pull Request

当前仓库没有可参考的提交历史。提交信息建议使用简短的 Conventional Commits 前缀，例如 `feat: add tool runner`、`fix: handle API errors`、`docs: clarify setup`。PR 应说明变更目的、受影响模块、运行过的检查及结果；界面变更附截图，接口变更说明请求/响应影响，并关联相关 issue（如有）。

## 安全与配置

不要提交密钥、`.env`、虚拟环境、依赖目录或 `data/` 中的运行数据。修改工具执行逻辑时，保持工具项目位于 `python-tools/` 内并保留超时限制。

## 文件与依赖清理

除非完成任务确实需要删除文件、目录或依赖，否则不要执行删除或清理操作。确有必要时，先说明影响并取得用户明确同意；不要因安装失败或测试失败自行清空 `node_modules`、包缓存或其他工作区内容。

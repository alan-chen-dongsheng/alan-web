# 全栈项目基础环境实施计划

> **执行要求：** 必须逐项执行计划并记录进度。计划步骤使用 `- [ ]` 格式。若当前环境仍未初始化 Git，应先在允许写入 `.git` 的环境中初始化仓库，再执行提交步骤。

**目标：** 在一个项目文件夹中建立可本地运行的前端、后端、数据目录和独立 Python 命令行工具基础环境。

**架构：** 前端和后端分别管理依赖，Vite 将 `/api` 请求代理到 FastAPI。后端通过安全的参数数组调用由 uv 管理的外部 Python 工具，不在后端进程内导入工具代码。

**技术栈：** 当前兼容的 Node.js LTS、pnpm、稳定版 React、严格模式 TypeScript、Vite、Tailwind CSS、Ant Design、Python 3.12、uv、FastAPI、Pydantic。

**设计说明：** [全栈项目基础架构设计](../specs/2026-10-10-fullstack-foundation-design.md)

## 全局约束

- 项目统一放在一个根目录，包含 `frontend/`、`backend/`、`data/` 和 `python-tools/`。
- 前端：兼容的当前 Node.js LTS、pnpm、稳定版 React、严格模式 TypeScript、Vite、Tailwind CSS 和 Ant Design。
- 后端：Python 3.12、uv、FastAPI 和 Pydantic。
- 前后端分别管理依赖；每个外部 Python 工具使用独立 uv 项目。
- 后端调用工具时使用参数数组，不通过 shell 拼接命令；设置执行超时并收集退出码、标准输出和错误输出。
- 本地运行数据不纳入版本控制。
- README 和后续新增文档使用简体中文；代码标识符使用英文。
- 版本号以实施时官方稳定版和兼容 LTS 为准，并在 README 中记录实际选用版本。

## 评审重点

- 工具参数含空格或 shell 元字符时仍作为单独参数传递，不被解释执行；在工具运行器测试中覆盖。
- 工具超时或返回非零退出码时，后端保留退出状态并提供可诊断输出；在工具运行器测试中覆盖。
- 外部工具缺失或 uv 执行失败时，调用方能得到明确错误且不泄露堆栈；在工具运行器测试中覆盖。
- 后端服务不可用时，前端显示可理解的失败状态；在前端健康接口测试中覆盖。
- `data/` 下的运行时文件不会被纳入版本控制；在仓库忽略规则检查中覆盖。

---

### 任务 1：建立根目录约定和开发文档

**文件：**
- 新建：`.gitignore`
- 新建：`.nvmrc`
- 新建：`pnpm-workspace.yaml`
- 新建：`README.md`
- 新建：`scripts/check_structure.py`
- 新建：`data/.gitkeep`
- 创建目录：`frontend/`、`backend/`、`python-tools/`

**接口：**
- 消费：设计说明中的目录、版本和运行要求。
- 产出：根目录约定、数据忽略规则，以及前后端分别启动的中文说明。

- [ ] **步骤 1：写仓库结构检查**

编写一个轻量级脚本或仓库检查，确认四个目录存在、根 README 存在，并检查 `data/` 下普通运行文件受 `.gitignore` 忽略。

- [ ] **步骤 2：运行检查并确认失败**

预期：由于目录和文件尚不存在，检查失败并指出缺少项。

- [ ] **步骤 3：创建根目录文件**

新增 `.gitignore`，忽略 `data/` 中运行时内容但保留 `.gitkeep`；新增中文 `README.md`，先记录项目结构、计划选用的版本策略和稍后补全的启动命令；建立四个目录。

- [ ] **步骤 4：运行仓库结构检查**

预期：四个目录、README 和数据忽略规则检查通过。

- [ ] **步骤 5：提交根目录基础约定**

```bash
git add .gitignore README.md data/.gitkeep
# 同时暂存空目录中的后续占位文件（如有）
git commit -m "chore: establish project structure"
```

### 任务 2：建立 FastAPI 后端和独立工具调用边界

**文件：**
- 新建：`backend/pyproject.toml`
- 新建：`backend/.python-version`
- 新建：`backend/app/__init__.py`
- 新建：`backend/app/main.py`
- 新建：`backend/app/schemas/health.py`
- 新建：`backend/app/services/tool_runner.py`
- 新建：`backend/tests/test_health.py`
- 新建：`backend/tests/test_tool_runner.py`
- 新建：`python-tools/example_tool/pyproject.toml`
- 新建：`python-tools/example_tool/.python-version`
- 新建：`python-tools/example_tool/main.py`

**接口：**
- 消费：任务 1 的项目目录约定。
- 产出：`GET /api/health`，响应模型 `HealthResponse(status: str)`；工具运行函数 `run_tool(project_dir: Path, args: Sequence[str], timeout_seconds: float = 30.0) -> ToolResult`，其中 `ToolResult` 包含 `return_code: int`、`stdout: str`、`stderr: str`。

- [ ] **步骤 1：编写健康接口和工具运行器测试**

先创建最小 `backend/pyproject.toml`，声明 FastAPI、Pydantic 及开发测试依赖（pytest、httpx），使测试命令可以运行；该配置只建立项目入口，不实现应用行为。

健康接口测试断言 `GET /api/health` 返回 HTTP 200 和 `{"status":"ok"}`，并验证响应使用 Pydantic 模型。工具运行器测试覆盖参数作为独立 argv 传递、超时、非零退出状态和缺少 uv 可执行文件。

- [ ] **步骤 2：运行后端测试并确认失败**

在 `backend/` 运行 `uv run pytest`。预期：由于应用和工具运行器尚未创建，测试失败。

- [ ] **步骤 3：实现健康接口和 Pydantic 响应**

在 `backend/app/schemas/health.py` 定义 `HealthResponse`；在 `backend/app/main.py` 创建 FastAPI 应用并将 `GET /api/health` 声明为 `response_model=HealthResponse`。

- [ ] **步骤 4：实现独立 uv 工具和安全运行器**

工具示例使用标准库 `argparse` 接收参数。在 `tool_runner.py` 用 `subprocess.run` 参数数组执行 `uv run --project <project_dir> python main.py ...`，设置超时、捕获文本输出、返回 `ToolResult`；不使用 `shell=True`。将不可执行工具和超时转换为可诊断的应用异常。

- [ ] **步骤 5：运行后端测试**

在 `backend/` 运行 `uv run pytest`。预期：健康响应、argv 传递、超时、非零退出状态和 uv 缺失场景均通过。

- [ ] **步骤 6：提交后端基础环境**

```bash
git add backend python-tools

git commit -m "feat: add FastAPI backend and Python tool runner"
```

### 任务 3：建立 React 前端、代理和端到端本地启动说明

**文件：**
- 新建：`frontend/package.json`
- 新建：`frontend/pnpm-lock.yaml`
- 新建：`frontend/index.html`
- 新建：`frontend/tsconfig.json`
- 新建：`frontend/vite.config.ts`
- 新建：`frontend/src/test-setup.ts`
- 新建：`frontend/src/main.tsx`
- 新建：`frontend/src/App.tsx`
- 新建：`frontend/src/lib/api.ts`
- 新建：`frontend/src/index.css`
- 新建：`frontend/src/App.test.tsx`
- 修改：`README.md`

**接口：**
- 消费：任务 2 的 `GET /api/health` 与 `HealthResponse(status: string)`。
- 产出：严格模式 TypeScript 的 React 应用；开发服务器将 `/api` 转发到本地 FastAPI；页面显示健康状态或服务连接错误。

- [ ] **步骤 1：编写前端健康状态组件测试**

先创建最小 `frontend/package.json`，声明 React、测试库和 Vitest 测试脚本，并配置测试运行环境；使用 pnpm 安装依赖并生成 lockfile。此步骤只建立测试入口，不实现页面行为。

测试成功响应时页面显示 API 状态，失败响应时显示连接失败提示。测试通过 fetch mock 覆盖成功和失败结果。

- [ ] **步骤 2：运行前端测试并确认失败**

在 `frontend/` 运行 `pnpm test -- --run`。预期：由于应用组件尚未创建，测试失败。

- [ ] **步骤 3：初始化前端依赖和工具配置**

核对 Node.js 官方发布页选择当前兼容 LTS，并核对 React、Vite、Tailwind CSS、Ant Design 和测试工具的官方稳定版本。补齐项目依赖并更新 pnpm lockfile；TypeScript 开启 `strict`；使用 Tailwind CSS 官方 Vite 插件接入样式，不添加未使用的旧式 Tailwind/PostCSS 配置文件；配置 Ant Design 样式层。

- [ ] **步骤 4：实现 API 客户端和页面状态**

在 `src/lib/api.ts` 定义健康响应类型与请求函数；在 `App.tsx` 请求 `/api/health`，使用 Ant Design 展示加载、成功和失败状态；`src/main.tsx` 挂载 React 应用并引入 Tailwind 样式。

- [ ] **步骤 5：配置 Vite API 代理并运行前端测试**

Vite 将 `/api` 代理至默认本地 FastAPI 地址。运行 `pnpm test -- --run` 和 `pnpm build`。预期：组件测试和生产构建通过，TypeScript 严格检查无错误。

- [ ] **步骤 6：补全中文 README 并完成联调检查**

README 写明实际 Node.js LTS、pnpm、Python 3.12、uv 版本以及前后端依赖安装和分别启动命令。按 README 启动 FastAPI 与 Vite，确认页面能通过代理显示健康状态，并确认 `data/` 的运行文件不会出现在版本控制变更中。

- [ ] **步骤 7：提交前端和启动文档**

```bash
git add frontend README.md

git commit -m "feat: add React frontend and local development guide"
```

import subprocess
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

TOOLS_ROOT = Path(__file__).resolve().parents[3] / "python-tools"


@dataclass(frozen=True)
class ToolResult:
    return_code: int
    stdout: str
    stderr: str


class ToolExecutionError(RuntimeError):
    def __init__(self, message: str, *, stdout: str = "", stderr: str = "") -> None:
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr


def _as_text(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def run_tool(
    project_dir: Path,
    args: Sequence[str],
    timeout_seconds: float = 30.0,
) -> ToolResult:
    """Run a uv-managed Python CLI project without shell interpolation."""
    project_dir = Path(project_dir).resolve()
    tools_root = TOOLS_ROOT.resolve()
    if not project_dir.is_relative_to(tools_root):
        raise ToolExecutionError("Python 工具项目必须位于仓库的 python-tools/ 目录内。")
    if not project_dir.is_dir() or not (project_dir / "pyproject.toml").is_file() or not (project_dir / "main.py").is_file():
        raise ToolExecutionError("Python 工具项目必须包含 pyproject.toml 和 main.py。")

    uv_executable = shutil.which("uv")
    if uv_executable is None:
        raise ToolExecutionError("找不到 uv 命令，请先安装 uv 并加入 PATH。")

    command = [uv_executable, "run", "--project", str(project_dir), "python", "main.py", *args]

    try:
        completed = subprocess.run(
            command,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            shell=False,
        )
    except FileNotFoundError as error:
        raise ToolExecutionError("无法启动 Python 工具进程，请检查 uv 路径和项目目录。") from error
    except subprocess.TimeoutExpired as error:
        raise ToolExecutionError(
            f"Python 工具执行超时（{timeout_seconds:g} 秒）。",
            stdout=_as_text(error.stdout),
            stderr=_as_text(error.stderr),
        ) from error

    return ToolResult(
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )

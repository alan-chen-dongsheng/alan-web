import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from app.services.tool_runner import ToolExecutionError, run_tool

TOOL_PROJECT = Path(__file__).resolve().parents[2] / "python-tools" / "example_tool"


class ToolRunnerTests(unittest.TestCase):
    def test_run_tool_passes_arguments_without_shell_interpolation(self) -> None:
        with patch("app.services.tool_runner.shutil.which", return_value="uv"):
            with patch(
                "app.services.tool_runner.subprocess.run",
                return_value=subprocess.CompletedProcess(args=[], returncode=0, stdout="done\n", stderr=""),
            ) as run:
                result = run_tool(TOOL_PROJECT, ["--value", "hello; echo unsafe"])

        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.stdout, "done\n")
        command = run.call_args.args[0]
        self.assertEqual(
            command,
            [
                "uv",
                "run",
                "--project",
                str(TOOL_PROJECT),
                "python",
                "main.py",
                "--value",
                "hello; echo unsafe",
            ],
        )
        self.assertFalse(run.call_args.kwargs["shell"])

    def test_run_tool_resolves_project_path_before_changing_directory(self) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch("app.services.tool_runner.shutil.which", return_value="uv"):
            with patch("app.services.tool_runner.subprocess.run", return_value=completed) as run:
                run_tool(TOOL_PROJECT, [])

        resolved_project = str(TOOL_PROJECT.resolve())
        self.assertEqual(run.call_args.args[0][3], resolved_project)
        self.assertEqual(run.call_args.kwargs["cwd"], Path(resolved_project))

    def test_run_tool_returns_nonzero_exit_code_and_output(self) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=7, stdout="partial", stderr="failed")
        with patch("app.services.tool_runner.shutil.which", return_value="uv"):
            with patch("app.services.tool_runner.subprocess.run", return_value=completed):
                result = run_tool(TOOL_PROJECT, ["--value", "x"])

        self.assertEqual(result.return_code, 7)
        self.assertEqual(result.stdout, "partial")
        self.assertEqual(result.stderr, "failed")

    def test_run_tool_raises_diagnostic_error_on_timeout(self) -> None:
        timeout = subprocess.TimeoutExpired(cmd="uv", timeout=0.25)
        with patch("app.services.tool_runner.shutil.which", return_value="uv"):
            with patch("app.services.tool_runner.subprocess.run", side_effect=timeout):
                with self.assertRaisesRegex(ToolExecutionError, "超时"):
                    run_tool(TOOL_PROJECT, [], timeout_seconds=0.25)

    def test_run_tool_fails_before_spawn_when_uv_is_not_on_path(self) -> None:
        with patch("shutil.which", return_value=None):
            with patch("app.services.tool_runner.subprocess.run") as run:
                with self.assertRaisesRegex(ToolExecutionError, "uv"):
                    run_tool(TOOL_PROJECT, [])

        run.assert_not_called()

    def test_run_tool_raises_diagnostic_error_when_uv_is_missing(self) -> None:
        with patch("app.services.tool_runner.shutil.which", return_value="uv"):
            with patch("app.services.tool_runner.subprocess.run", side_effect=FileNotFoundError("uv")):
                with self.assertRaisesRegex(ToolExecutionError, "uv"):
                    run_tool(TOOL_PROJECT, [])

    def test_run_tool_rejects_project_outside_python_tools_root(self) -> None:
        with patch("app.services.tool_runner.subprocess.run") as run:
            with self.assertRaisesRegex(ToolExecutionError, "python-tools"):
                run_tool(Path(__file__).resolve().parents[2] / "backend", [])

        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()

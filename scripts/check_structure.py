from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRECTORIES = ("frontend", "backend", "data", "python-tools")


def check_structure() -> list[str]:
    missing = [name for name in REQUIRED_DIRECTORIES if not (ROOT / name).is_dir()]
    if not (ROOT / "README.md").is_file():
        missing.append("README.md")
    ignore_file = ROOT / ".gitignore"
    if not ignore_file.is_file():
        missing.append(".gitignore")
    elif "/data/*" not in ignore_file.read_text() or "!/data/.gitkeep" not in ignore_file.read_text():
        missing.append("data ignore rules")
    return missing


if __name__ == "__main__":
    missing_items = check_structure()
    if missing_items:
        raise SystemExit(f"缺少项目结构项：{', '.join(missing_items)}")
    print("项目结构检查通过")

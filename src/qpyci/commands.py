import subprocess
import shutil
import sys
import importlib.util
from pathlib import Path

def generate_badge():
    coverage_badge_exe = shutil.which("coverage-badge")
    if coverage_badge_exe is not None:
        return subprocess.run([coverage_badge_exe, "-f", "-o", "coverage.svg"]).returncode

    if importlib.util.find_spec("coverage_badge") is not None:
        return subprocess.run(
            [sys.executable, "-m", "coverage_badge", "-f", "-o", "coverage.svg"]
        ).returncode

    return 0

def clean():
    root = Path.cwd()

    for directory in (root / "dist", root / "build",root/'__pycache__',root/'.pytest_cache/'):
        if directory.exists():
            shutil.rmtree(directory, ignore_errors=True)

    for egg_info_path in root.glob("*.egg-info"):
        if egg_info_path.is_dir():
            shutil.rmtree(egg_info_path, ignore_errors=True)
        else:
            try:
                egg_info_path.unlink()
            except FileNotFoundError:
                pass

def run_tests(cov_target: str) -> int:
    args = [
        sys.executable,
        "-m",
        "pytest",
    ]
    if importlib.util.find_spec("pytest_cov") is not None:
        args.extend(["--cov-report", "term", f"--cov={cov_target}"])
    if Path("tests").is_dir():
        args.append("tests")
    return subprocess.run(args).returncode

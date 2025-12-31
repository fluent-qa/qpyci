import subprocess
import shutil
import sys
import importlib.util
from pathlib import Path
import os
import stat
import traceback
import time
from typing import List

root = Path.cwd()
BUILD_DIRs = [root / "dist", root / "build", root / "__pycache__", root / ".pytest_cache/"]
_SKIP_WALK_DIR_NAMES = {".venv", ".git", ".hg", ".svn", ".tox", ".nox", "node_modules"}


def generate_badge():
    coverage_badge_exe = shutil.which("coverage-badge")
    if coverage_badge_exe is not None:
        return subprocess.run([coverage_badge_exe, "-f", "-o", "coverage.svg"]).returncode

    if importlib.util.find_spec("coverage_badge") is not None:
        return subprocess.run([sys.executable, "-m", "coverage_badge", "-f", "-o", "coverage.svg"]).returncode

    return 0


def _log(message: str) -> None:
    print(message)


def _find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / "pyproject.toml").exists():
            return p
    return start.resolve()


def _repo_root() -> Path:
    return _find_repo_root(Path.cwd())


def _iter_dirs(root: Path, folder_name: str) -> List[Path]:
    results: list[Path] = []
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_WALK_DIR_NAMES]
        if folder_name in dirnames:
            results.append(Path(dirpath) / folder_name)
    return results


def _iter_pycache_dirs(root: Path) -> list[Path]:
    return _iter_dirs(root, "__pycache__")


def _retry(action, *, attempts: int = 3, base_delay_s: float = 0.2) -> None:
    for i in range(attempts):
        try:
            action()
            return
        except Exception:
            if i == attempts - 1:
                raise
            time.sleep(base_delay_s * (2**i))


def _safe_unlink(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return
    except PermissionError:
        try:
            os.chmod(path, stat.S_IWRITE)
            path.unlink()
        except FileNotFoundError:
            return
        except Exception:
            _log(f"cleanup: failed to delete file: {path}")
            _log(traceback.format_exc())
    except IsADirectoryError:
        return
    except Exception:
        _log(f"cleanup: failed to delete file: {path}")
        _log(traceback.format_exc())


def _rmtree_onerror(func, path: str, exc_info) -> None:
    if isinstance(exc_info[1], PermissionError):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
            return
        except Exception:
            _log(f"cleanup: failed to delete path (permission): {path}")
            _log("".join(traceback.format_exception(*exc_info)))
            return
    _log(f"cleanup: failed to delete path: {path}")
    _log("".join(traceback.format_exception(*exc_info)))


def _trash_dir(root: Path) -> Path:
    p = root / "_trash"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _quarantine_path(path: Path, *, root: Path) -> Path | None:
    if not path.exists():
        return None
    ts = time.strftime("%Y%m%d_%H%M%S")
    target = _trash_dir(root) / f"{path.name.lstrip('.')}_{ts}"
    try:
        if target.exists():
            target = _trash_dir(root) / f"{path.name.lstrip('.')}_{ts}_{int(time.time() * 1000)}"
        path.rename(target)
        _log(f"cleanup: renamed to {target}")
        return target
    except Exception:
        _log(f"cleanup: failed to rename: {path}")
        _log(traceback.format_exc())
        return None


def _safe_rmtree(path: Path, *, root: Path) -> None:
    if not path.exists():
        return
    _log(f"cleanup: deleting {path}")
    if path.is_dir():

        def _do_rmtree() -> None:
            shutil.rmtree(path, onerror=_rmtree_onerror)

        try:
            _retry(_do_rmtree, attempts=3, base_delay_s=0.2)
        except Exception:
            _log(f"cleanup: failed to delete directory: {path}")
            _log(traceback.format_exc())
            moved = _quarantine_path(path, root=root)
            if moved is not None:
                try:
                    _retry(lambda: shutil.rmtree(moved, onerror=_rmtree_onerror), attempts=3, base_delay_s=0.2)
                except Exception:
                    _log(f"cleanup: failed to delete quarantined directory: {moved}")
                    _log(traceback.format_exc())
        return
    elif path.is_file():
        os.remove(path)
        return
    _safe_unlink(path)


def _clean_artifacts() -> None:
    root = _repo_root()
    _log("cleanup: keeping protected dirs (not deleted): " + ", ".join(sorted(_SKIP_WALK_DIR_NAMES)))

    for name in [
        "build",
        "dist",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "htmlcov",
        "allure-results",
        ".coverage",
        "coverage.xml",
    ]:
        _safe_rmtree(root / name, root=root)

    pycache_dirs = _iter_pycache_dirs(root)
    if pycache_dirs:
        _log(f"cleanup: deleting __pycache__ dirs: {len(pycache_dirs)}")
    for p in pycache_dirs:
        _safe_rmtree(p, root=root)

    still_there: list[Path] = []
    for name in [".ruff_cache", "allure-results", ".pytest_cache", ".coverage", "coverage.xml"]:
        p = root / name
        if p.exists():
            still_there.append(p)

    remaining_pycache = [p for p in _iter_pycache_dirs(root) if p.exists()]
    still_there.extend(remaining_pycache)

    if still_there:
        _log("cleanup: remaining paths (likely locked by another process):")
        for p in still_there:
            _log(f"- {p}")


def cleanup() -> None:
    _clean_artifacts()


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


def check_format() -> int:
    check_result = subprocess.run(["uvx", "ruff", "check", "--fix"])
    if check_result.returncode != 0:
        return check_result.returncode
    format_result = subprocess.run(["uvx", "ruff", "format"])
    return format_result.returncode


def ci() -> int:
    fmt_code = check_format()
    if fmt_code != 0:
        return fmt_code
    test_result = subprocess.run(["uv", "run", "pytest"])
    if test_result.returncode != 0:
        return test_result.returncode
    generate_badge()
    return 1

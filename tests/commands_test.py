from __future__ import annotations

from types import SimpleNamespace


def test_cleanup_does_not_error():
    import qpyci.commands as c

    c.cleanup()


def test_generate_badge_is_noop_without_coverage_badge(monkeypatch):
    import qpyci.commands as c

    monkeypatch.setattr(c.shutil, "which", lambda _name: None)
    monkeypatch.setattr(c.importlib.util, "find_spec", lambda _name: None)
    assert c.generate_badge() == 0


def test_run_tests_builds_pytest_command(monkeypatch):
    import qpyci.commands as c

    calls: list[list[str]] = []

    def fake_run(args, cwd=None):
        calls.append(list(args))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(c.subprocess, "run", fake_run)
    monkeypatch.setattr(c, "_read_pyproject_project_name", lambda _root: "my-project")
    monkeypatch.setattr(c.importlib.util, "find_spec", lambda _name: object())
    monkeypatch.setattr(c.Path, "is_dir", lambda _self: False)

    assert c.run_tests() == 0
    assert calls
    assert calls[0][:3] == [c.sys.executable, "-m", "pytest"]
    assert "--cov=my_project" in calls[0]


def test_ci_returns_bad_exit_code(monkeypatch):
    import qpyci.commands as c

    def fake_run(_args, cwd=None):
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(c.subprocess, "run", fake_run)
    monkeypatch.setattr(c, "generate_badge", lambda: 7)
    assert c.ci() == 7

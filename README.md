# qpyci

CI helper CLI for Python projects.

## Use in a new project

Add `qpyci` to your project (usually as a dev dependency) and call it from CI.

Install from GitHub:

```bash
python -m pip install "qpyci @ git+https://github.com/fluent-qa/qpyci.git"
```

If you use `uv`:

```bash
uv pip install "qpyci @ git+https://github.com/fluent-qa/qpyci.git"
```

Pin to a tag/commit for reproducible CI:

```bash
python -m pip install "qpyci @ git+https://github.com/fluent-qa/qpyci.git@v0.1.0"
```

Optional: add script aliases in your project’s `pyproject.toml` so CI can call stable names:

```toml
[project.scripts]
ci-clean = "qpyci.commands:cleanup"
ci-badge = "qpyci.commands:generate_badge"
ci-format = "qpyci.commands:check_format"
ci = "qpyci.commands:ci"
```

Then call them:

```bash
ci-clean
qpyci coverage your_package
```

If the GitHub repo is private, use either an SSH remote (`git+ssh://...`) or an HTTPS URL with a GitHub token (PAT) available to your CI.

## CLI

Show available commands:

```bash
qpyci --help
```

Clean build artifacts (build/, dist/, caches, __pycache__):

```bash
qpyci cleanup
```

Generate `coverage.svg` (uses `coverage-badge` if available; otherwise no-op):

```bash
qpyci badge
```

Run tests with coverage for a target (requires `pytest`; uses `pytest-cov` if installed; exits with pytest’s status code):

```bash
qpyci coverage qpyci
```

Run ruff autofix + format (requires `uv`/`uvx` and `ruff`):

```bash
qpyci check-format
```

Run format + tests + badge:

```bash
qpyci ci
```


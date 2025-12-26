# qpyci

CI helper CLI for Python projects, intended to bundle common CI/maintenance tasks behind a single, installable command (works well alongside `uv`).

## What it does

- Generates a coverage badge via `coverage-badge`
- Cleans common build artifacts (`dist/`, `build/`, `*.egg-info`)
- Runs `pytest` with coverage for a given import target

## Installation

Editable install (local development):

```bash
python -m pip install -e .
```

If you use `uv`:

```bash
uv pip install -e .
```

## Usage

Show available commands:

```bash
qpyci --help
```

Generate `coverage.svg` (requires `coverage-badge` on `PATH`):

```bash
qpyci badge
```

Clean build artifacts:

```bash
qpyci clean
```

An alias entry point is also installed:

```bash
cleanup
```

Run tests with coverage for a target (requires `pytest`; uses `pytest-cov` if installed; exits with pytest’s status code):

```bash
qpyci coverage qpyci
```


# Prompts

- what to do: create an cli application for ci scripts in different projects.
- what to use to create this application: python/uv/typer 

- Why I want to create this application:

1. when use uv to manage a python project, it doesn't config shell in tool.uv.scripts section, so I need to create a separate python file to add this config, it doesn't support following features:
  ```shell
  [tool.uv.scripts]
# Simple shell commands
clean = "rm -rf dist/ build/ *.egg-info"
badge = "coverage-badge -f -o coverage.svg"

# Multiple commands using &&
build = "rm -rf dist/ && python -m build"

# Shell scripts
setup = "sh scripts/setup.sh"

# Combining Python and shell commands
test-all = "pytest && coverage report && coverage-badge -f -o coverage.svg"

# Using environment variables
env-test = "ENV=test pytest"

# Complex shell operations
backup = "tar -czf backup.tar.gz src/ tests/"
```
2. I create a pyton file, and configure it into pyproject.toml it should work.
```python
import subprocess

def generate_badge():
    subprocess.run(['coverage-badge', '-f', '-o', 'coverage.svg'])

def clean():
    subprocess.run(['rm', '-rf', 'dist/', 'build/', '*.egg-info'])

def run_tests():
    subprocess.run(['pytest', '--cov-report', 'term', '--cov=qpyconf', 'tests/'])
```

configuraiton:
```toml
[project.scripts]
ci-badge = "fluent_ci.commands:generate_badge"
ci-clean = "fluent_ci.commands:clean"
ci-test = "fluent_ci.commands:run_tests"
```
3. So I want to create a separate python package to manage all these ci scripts.

## features of this application:

1. includes all the ci scripts in one place.
2. easy to integrate with uv.
3. use it separately though cli interface
4. easy to add script: 
   1. configurate in json file with name and shell commands, could be used in both cli and uv 
   2. configurate in yaml file with name and shell commands, could be used in both cli and uv
   4. configurate in toml file with name and shell commands, could be used in both cli and uv


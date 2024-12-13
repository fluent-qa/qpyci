import subprocess

def generate_badge():
    subprocess.run(['coverage-badge', '-f', '-o', 'coverage.svg'])

def clean():
    subprocess.run(['rm', '-rf', 'dist/', 'build/', '*.egg-info'])

def run_tests(cov_target: str):
    subprocess.run(['pytest', '--cov-report', 'term', f'--cov={cov_target}', 'tests/'])
    
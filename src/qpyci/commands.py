import subprocess

def generate_badge():
    subprocess.run(['coverage-badge', '-f', '-o', 'coverage.svg'])

def clean():
    subprocess.run(['rm', '-rf', 'dist/', 'build/', '*.egg-info'])

def run_tests(cov_target: str):
    subprocess.run(['pytest', '--cov-report', 'term', f'--cov={cov_target}', 'tests/'])


def run_commands_from_file(file_path:str):
    """Run commands from a given file."""
    with open(file_path, 'r') as file:
        commands = file.readlines()
    
    for command in commands:
        command = command.strip()
        if command:  # Ensure the command is not empty
            try:
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                print(f"Output of '{command}': {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Error while executing '{command}': {e.stderr}")
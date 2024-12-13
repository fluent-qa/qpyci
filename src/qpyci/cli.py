import typer
from qpyci.commands import generate_badge, clean, run_tests,run_commands_from_file

app = typer.Typer()

@app.command()
def badge():
    generate_badge()

@app.command()
def clean():
    clean()

@app.command()
def coverage(cov_target: str):
    """Run tests with coverage for the specified target."""
    run_tests(cov_target)

@app.command()
def run(file_path: str = typer.Option(..., help="Path to the file containing commands to run.")):
    """Run commands from the specified file."""
    run_commands_from_file(file_path)

def main():
    app()
    
if __name__ == "__main__":
    main()
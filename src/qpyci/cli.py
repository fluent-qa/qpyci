import typer
from qpyci.commands import generate_badge, clean, run_tests

app = typer.Typer()

@app.command()
def badge():
    generate_badge()

@app.command()
def clean():
    clean()

@app.command()
def test(cov_target: str):
    """Run tests with coverage for the specified target."""
    run_tests(cov_target)

def main():
    app()
    
if __name__ == "__main__":
    main()
import typer
import qpyci

app = typer.Typer()

@app.command()
def badge():
    qpyci.generate_badge()

@app.command()
def clean():
    qpyci.clean()

@app.command()
def coverage(cov_target: str):
    """Run tests with coverage for the specified target."""
    raise typer.Exit(code=qpyci.run_tests(cov_target))

def main():
    app()
    
if __name__ == "__main__":
    main()

import typer
from qpyci import commands as c

app = typer.Typer()


@app.command()
def badge():
    c.generate_badge()


@app.command()
def cleanup():
    c.cleanup()


@app.command()
def coverage():
    """Run tests with coverage for the current project."""
    raise typer.Exit(code=c.run_tests())


@app.command()
def check_format():
    """Run Check format."""
    raise typer.Exit(code=c.check_format())


@app.command()
def ci():
    """Run CI"""
    raise typer.Exit(code=c.ci())


def main():
    app()


if __name__ == "__main__":
    main()

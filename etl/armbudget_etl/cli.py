"""ArmBudget command-line interface (spec 5.2: make + typer)."""

import typer

from armbudget_etl import __version__
from armbudget_etl.seed import check_headline_facts, load_headline_facts

app = typer.Typer(
    help="ArmBudget ETL: crawl -> parse -> load -> validate -> export.",
    no_args_is_help=True,
)


def _not_implemented(stage: str, phase: str) -> None:
    # Stubs fail loudly: a silent success would look like data was produced.
    typer.echo(f"'{stage}' is not implemented yet (planned in {phase}, see PHASE_PROMPTS.md).")
    raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """Print the ETL version."""
    typer.echo(__version__)


@app.command("check-seed")
def check_seed() -> None:
    """Check structure of seed/headline_facts.json."""
    problems = check_headline_facts(load_headline_facts())
    for problem in problems:
        typer.echo(f"FAIL {problem}")
    if problems:
        raise typer.Exit(code=1)
    typer.echo("seed/headline_facts.json: OK")


@app.command()
def crawl() -> None:
    """Discover and download source documents into data/raw (phase 1)."""
    _not_implemented("crawl", "phase 1")


@app.command("ingest-manual")
def ingest_manual() -> None:
    """Ingest files placed by hand into data/manual_drop (phase 1)."""
    _not_implemented("ingest-manual", "phase 1")


@app.command()
def parse() -> None:
    """Parse data/raw into data/interim (phases 2-5)."""
    _not_implemented("parse", "phase 2")


@app.command()
def load() -> None:
    """Load data/interim into the DuckDB warehouse (phase 2)."""
    _not_implemented("load", "phase 2")


@app.command()
def validate() -> None:
    """Run identities, contracts and cross-source checks (phase 2)."""
    _not_implemented("validate", "phase 2")


@app.command()
def export() -> None:
    """Export warehouse to CSV/Parquet/XLSX/JSON (phase 7)."""
    _not_implemented("export", "phase 7")


if __name__ == "__main__":
    app()

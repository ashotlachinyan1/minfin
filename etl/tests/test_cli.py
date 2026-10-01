from typer.testing import CliRunner

from armbudget_etl import __version__
from armbudget_etl.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_stubs_fail_loudly() -> None:
    for command in ["crawl", "ingest-manual", "parse", "load", "validate", "export"]:
        result = runner.invoke(app, [command])
        assert result.exit_code == 1, command
        assert "not implemented" in result.stdout


def test_check_seed_passes() -> None:
    result = runner.invoke(app, ["check-seed"])
    assert result.exit_code == 0, result.stdout

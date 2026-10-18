import asyncio
from pathlib import Path

import typer

from .auditor import Auditor
from .models import Severity
from .parser import parse_file
from .pypi import PyPIClient
from .reporter import render_json, render_table

app = typer.Typer(help="Audit Python lockfiles for future installability.", add_completion=False)


@app.callback()
def main() -> None:
    """Entry point for the pip-repro CLI."""


@app.command(name="audit")
def audit(
    path: Path = typer.Argument(..., exists=True, dir_okay=False),
    python_version: str = typer.Option("3.12", "--python", help="Target Python version"),
    as_json: bool = typer.Option(False, "--json", help="Machine-readable output"),
) -> None:
    """Audit a requirements.txt or pyproject.toml file."""

    deps = parse_file(path)

    async def run() -> list:
        async with PyPIClient() as client:
            return await Auditor(client, python_version).audit(deps)

    findings = asyncio.run(run())

    if as_json:
        render_json(findings)
    else:
        render_table(findings)

    if any(finding.severity == Severity.CRITICAL for finding in findings):
        raise typer.Exit(code=2)
    if any(finding.severity == Severity.WARNING for finding in findings):
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()

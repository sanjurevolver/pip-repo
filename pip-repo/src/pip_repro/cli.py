import asyncio
from pathlib import Path
from typing import Annotated

import typer

from .auditor import Auditor
from .models import Finding, Severity
from .parser import parse_file
from .pypi import PyPIClient
from .reporter import render_json, render_table

app = typer.Typer(help="Audit Python lockfiles for future installability.", add_completion=False)


@app.callback()
def main() -> None:
    """Entry point for the pip-repro CLI."""


@app.command(name="audit")
def audit(
    path: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    python_version: Annotated[
        str,
        typer.Option("--python", help="Target Python version"),
    ] = "3.12",
    as_json: Annotated[bool, typer.Option("--json", help="Machine-readable output")] = False,
) -> None:
    """Audit a requirements.txt or pyproject.toml file."""

    deps = parse_file(path)

    async def run() -> list[Finding]:
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

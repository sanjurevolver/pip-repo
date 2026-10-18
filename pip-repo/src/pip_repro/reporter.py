import json

from rich.console import Console
from rich.table import Table

from .models import Finding, Severity

ICON = {Severity.OK: "OK", Severity.WARNING: "WARN", Severity.CRITICAL: "CRIT"}


def render_table(findings: list[Finding]) -> None:
    table = Table(title="pip-repro audit report")
    table.add_column("Status")
    table.add_column("Package")
    table.add_column("Version")
    table.add_column("Issue")

    for finding in findings:
        table.add_row(
            f"{ICON[finding.severity]} {finding.severity.value.upper()}",
            finding.dependency.name,
            finding.dependency.pinned_version or "—",
            finding.message,
        )

    console = Console(emoji=False)
    console.print(table)

    critical = sum(1 for finding in findings if finding.severity == Severity.CRITICAL)
    warning = sum(1 for finding in findings if finding.severity == Severity.WARNING)
    ok = sum(1 for finding in findings if finding.severity == Severity.OK)
    console.print(f"\nSummary: {critical} critical, {warning} warning, {ok} ok")


def render_json(findings: list[Finding]) -> None:
    print(
        json.dumps(
            [
                {
                    "package": finding.dependency.name,
                    "version": finding.dependency.pinned_version,
                    "severity": finding.severity.value,
                    "message": finding.message,
                }
                for finding in findings
            ],
            indent=2,
        )
    )

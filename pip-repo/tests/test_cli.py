from pathlib import Path

from typer.testing import CliRunner

from pip_repro.cli import app
from pip_repro.models import Severity

runner = CliRunner()


class DummyClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return None

    async def get_many(self, names):
        return {
            "django": {
                "releases": {
                    "4.2.1": [
                        {"yanked": False, "packagetype": "bdist_wheel", "requires_python": ">=3.8"}
                    ]
                }
            }
        }


def test_cli_ok(monkeypatch, tmp_path):
    file_path = tmp_path / "requirements.txt"
    file_path.write_text("django==4.2.1\n", encoding="utf-8")

    monkeypatch.setattr("pip_repro.cli.PyPIClient", DummyClient)

    result = runner.invoke(app, ["audit", str(file_path), "--python", "3.12"])
    assert result.exit_code == 0
    assert "Summary:" in result.stdout


def test_cli_warning_exit(monkeypatch, tmp_path):
    file_path = tmp_path / "requirements.txt"
    file_path.write_text("django==4.2.1\n", encoding="utf-8")

    class WarningClient(DummyClient):
        async def get_many(self, names):
            return {
                "django": {
                    "releases": {
                        "4.2.1": [
                            {"yanked": False, "packagetype": "sdist", "requires_python": ">=3.13"}
                        ]
                    }
                }
            }

    monkeypatch.setattr("pip_repro.cli.PyPIClient", WarningClient)
    result = runner.invoke(app, ["audit", str(file_path), "--python", "3.12"])
    assert result.exit_code == 1

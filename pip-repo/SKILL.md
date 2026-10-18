# SKILL.md — pip-repro

## Why this exists

`pip-audit` checks security. `pip-tools` resolves today. `pip-repro` checks whether a dependency set still installs in the future.

## Scope

- Parse `requirements.txt` and `pyproject.toml` dependencies.
- Query PyPI JSON data.
- Flag yanked versions, missing pins, missing wheels, and incompatible `requires_python`.
- Emit human-readable and JSON reports.
- Exit codes: `0` ok, `1` warnings, `2` critical.

## Repository layout

```text
pip-repro/
├── SKILL.md
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
├── src/
│   └── pip_repro/
│       ├── __init__.py
│       ├── cli.py
│       ├── pypi.py
│       ├── parser.py
│       ├── auditor.py
│       ├── models.py
│       └── reporter.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   ├── test_parser.py
│   ├── test_pypi.py
│   ├── test_auditor.py
│   └── test_cli.py
└── .github/workflows/ci.yml
```

## Build steps

1. Create a virtual environment.
2. Install dev dependencies.
3. Run `pytest`.
4. Run `python -m build`.
5. Publish on TestPyPI.

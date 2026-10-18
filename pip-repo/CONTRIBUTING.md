# Contributing to pip-repro

Thanks for helping improve the project.

## Local setup

```bash
git clone https://github.com/sanjurevolver/pip-repo.git
cd pip-repo
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Contribution workflow

1. Create a feature branch from `main`.
2. Add or update tests alongside the code change.
3. Run the project checks before submitting a PR.
4. Keep examples and CLI output aligned with actual runtime behavior.

## Checks

Run the following before opening a pull request:

```bash
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy --strict src
python -m pytest --cov=src --cov-fail-under=80 --cov-report=term-missing
```

## Pull request guidance

- Use a clear title and concise summary.
- Explain the bug or feature being addressed.
- Include screenshots or sample output when behavior changes.
- Keep dependency and audit logic grounded in real package metadata.

## Code expectations

- Prefer clear, explicit logic over clever shortcuts.
- Keep messages actionable and user-facing.
- Preserve the CLI contract and exit codes.
- Add tests for behavior changes.

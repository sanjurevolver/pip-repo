# pip-repro

**Audit Python lockfiles for future installability.**

`pip-audit` checks security. `pip-tools` checks today's resolution.
`pip-repro` checks whether your lockfile will *still* install in 3 years.

## The problem

PyPI allows authors to **yank** versions. Wheels get deleted. Python moves forward.
Your pinned `django==4.2.1` might install cleanly today — and silently resolve to a
different version a year from now. `pip-repro` catches this **before** it bites you.

## Install

```bash
pip install pip-repro
```

## Usage

```bash
# Audit a requirements.txt against the current Python
pip-repro audit requirements.txt

# Check for future Python compatibility
pip-repro audit requirements.txt --python 3.14

# Machine-readable output for CI
pip-repro audit requirements.txt --json | jq

# Works with pyproject.toml too
pip-repro audit pyproject.toml
```

## What it catches

| Severity | Meaning |
|---|---|
| 🔴 CRITICAL | Pinned version yanked or missing on PyPI |
| 🟡 WARNING  | No wheel for target Python; sdist-only install |
| 🟢 OK       | Healthy |

## Exit codes

- `0` — all OK (safe for CI)
- `1` — warnings present
- `2` — critical issues (CI should fail)

## Development

```bash
git clone https://github.com/you/pip-repro
cd pip-repro
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

## Status

**v0.1.0 — MVP.** Transitive audit and auto-fix are planned for v0.2.
See [SKILL.md](SKILL.md) for the full project roadmap.

## License

MIT

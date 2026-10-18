# pip-repro

[![CI](https://github.com/sanjurevolver/pip-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/sanjurevolver/pip-repo/actions/workflows/ci.yml)

Audit Python dependency files for future installability and compatibility issues.

pip-repro helps you catch dependency problems before they break installs in CI, local dev, or production. It checks for:

- yanked versions on PyPI
- missing wheels for the target Python version
- packages that are not installable on newer Python releases
- dependency metadata that is valid today but risky long term

## Why this project exists

A project may look healthy when a lockfile is first created, but PyPI changes over time. Packages get yanked, wheels disappear, and Python releases move forward. pip-repro makes these risks visible early.

## Install

```bash
pip install pip-repro
```

## Usage

```bash
# Audit a requirements.txt file
pip-repro audit requirements.txt

# Audit a pyproject.toml file
pip-repro audit pyproject.toml

# Check compatibility for a future Python version
pip-repro audit requirements.txt --python 3.14

# Emit machine-readable JSON
pip-repro audit requirements.txt --json
```

## Exit codes

- `0`: no issues found
- `1`: warnings were found
- `2`: critical issues were found

## Example output

```text
Package             Status    Reason
------------------  --------  -------------------------------
requests            OK        available and compatible
numpy               WARNING   no wheel for Python 3.14
django              CRITICAL  version is yanked on PyPI
```

## Development

```bash
git clone https://github.com/sanjurevolver/pip-repo.git
cd pip-repo
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest
```

## Project status

Current version: `0.1.0`

This repository is the project home for the pip-repro CLI tool.

See [RELEASE_NOTES_v0.1.0.md](RELEASE_NOTES_v0.1.0.md) for the initial release summary.

## License

MIT

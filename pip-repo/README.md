# pip-repro

[![CI](https://github.com/sanjurevolver/pip-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/sanjurevolver/pip-repo/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

`pip-repro` audits Python dependency files for the kinds of installability problems that often slip past a normal install check: yanked releases, missing wheels for a target runtime, and pins that look valid today but fail for future environments.

It is designed for requirements files and `pyproject.toml` declarations, helping teams catch risky dependencies before they hit CI or production.

## Why it helps

- Detects yanked or unsupported package versions
- Checks whether a wheel exists for the target Python version and platform
- Surfaces risk before a dependency lock breaks during a later install
- Produces actionable fix recommendations instead of vague warnings

## Installation

### Install from PyPI

```bash
pip install pip-repro
```

### Install from source

```bash
git clone https://github.com/sanjurevolver/pip-repo.git
cd pip-repo
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Then install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Quick usage

```bash
pip-repro audit requirements.txt
pip-repro audit pyproject.toml
pip-repro audit requirements.txt --python 3.14
pip-repro audit requirements.txt --json
```

## Example report

The CLI produces a readable summary like this for a risky dependency file. The warning is about a missing compatible wheel for the selected target environment, not necessarily a guaranteed install failure. In some cases, pip may still build from source.

```bash
pip-repro audit examples/requirements-risky.txt
```

```text
                            pip-repro audit report
+-----------------------------------------------------------------------------+
| Status       | Package  | Version | Issue              | Recommended fix    |
|--------------+----------+---------+--------------------+--------------------|
| WARN WARNING | requests | 2.26.0  | wheel exists but   | select a release   |
|              |          |         | no compatible      | of requests with a |
|              |          |         | wheel for the      | wheel compatible   |
|              |          |         | target environment | with Python 3.12   |
| WARN WARNING | django   | 4.2.1   | wheel exists but   | select a release   |
|              |          |         | no compatible      | of django with a   |
|              |          |         | wheel for the      | wheel compatible   |
|              |          |         | target environment | with Python 3.12   |
| WARN WARNING | pandas   | 1.5.0   | wheel exists but   | select a release   |
|              |          |         | no compatible      | of pandas with a   |
|              |          |         | wheel for the      | wheel compatible   |
|              |          |         | target environment | with Python 3.12   |
| WARN WARNING | urllib3  | 1.26.18 | wheel exists but   | select a release   |
|              |          |         | no compatible      | of urllib3 with a  |
|              |          |         | wheel for the      | wheel compatible   |
|              |          |         | target environment | with Python 3.12   |
+-----------------------------------------------------------------------------+

Summary: 0 critical, 4 warning, 0 ok
```

## Exit codes

- `0`: no issues found
- `1`: warnings were found
- `2`: critical issues were found

## CI and quality checks

This project runs automated quality checks in GitHub Actions:

- install and build dependencies
- Ruff linting
- Ruff format validation
- strict mypy checks
- pytest with coverage thresholds

Workflow file: `.github/workflows/ci.yml`

## Development

```bash
git clone https://github.com/sanjurevolver/pip-repo.git
cd pip-repo
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

> Note: `pip-repro` warns when a package has no compatible wheel for the chosen Python version and platform. That is a compatibility risk signal, not a promise that installation always fails.

## Release notes

See [RELEASE_NOTES_v0.1.0.md](RELEASE_NOTES_v0.1.0.md) for the initial release summary.

## License

This project is released under the [MIT License](LICENSE).

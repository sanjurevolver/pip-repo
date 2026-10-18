# pip-repro

A dependency audit CLI for Python projects that need to stay installable over time.

This repository hosts the `pip-repro` project and its supporting files. The main project source lives in the `pip-repo/` directory.

## What this project does

`pip-repro` helps you find packages that may break later even when they install today. It checks for:

- yanked package versions on PyPI
- missing wheels for the target Python version
- compatibility risks for newer Python releases
- packages that are technically pinned but likely to fail in CI or production later

## Installation

```bash
cd pip-repo
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Quick usage

```bash
# Audit a requirements file
pip-repro audit requirements.txt

# Audit a pyproject.toml file
pip-repro audit pyproject.toml

# Check future compatibility against Python 3.14
pip-repro audit requirements.txt --python 3.14

# Emit JSON for CI systems
pip-repro audit requirements.txt --json
```

## Example: before and after

### Before

```text
# requirements.txt
requests==2.26.0
django==4.2.1
pandas==1.5.0
```

```bash
pip-repro audit examples/requirements-risky.txt
```

### After

```text
Package     Status     Reason
----------  ---------  ------------------------------------------------
requests    OK         available and compatible with the current target
pandas      WARNING    no wheel for the selected Python version
django     CRITICAL   version is yanked or no longer recommended for install
```

Recommended fix:

```text
# upgrade pinned package versions before release
requests>=2.32.0
django>=4.2.14
pandas>=2.2.0
```

## Sample reports and actionable fixes

The tool reports risk levels and tells you what to change:

- `CRITICAL`: version is yanked or missing from PyPI
- `WARNING`: build is unavailable for the selected Python target
- `OK`: package appears installable and compatible

Example report:

```text
Package        Status      Reason                                          Fix
------------   ----------  ----------------------------------------------  -------------------------------
numpy          WARNING     no wheel for Python 3.14                        upgrade or test on 3.13/3.12
urllib3        CRITICAL    version is yanked on PyPI                       bump to a supported release
click          OK          available and compatible                        keep current pin
```

## Real project files

The project includes example dependency files under `pip-repo/examples/` and is validated with automated tests in `pip-repo/tests/`.

## CI and tests

This repository includes a GitHub Actions workflow for automated validation:

- `pip-repo/.github/workflows/ci.yml`

It installs the project, runs linting, strict type checks, and the test suite against multiple Python versions.

## Roadmap

- v0.1.0: initial CLI, dependency audit, JSON output, CI validation
- v0.2.0: better dependency graph awareness and more precise compatibility checks
- v0.3.0: auto-fix suggestions and richer reporting
- v1.0.0: stable CLI with curated rule packs and package policy integrations

## GitHub links

- Repository: https://github.com/sanjurevolver/pip-repo
- Main branch: https://github.com/sanjurevolver/pip-repo/tree/main

## Repository metadata

Suggested topics for GitHub:

- python
- dependency-management
- pip
- packaging
- pypi
- security
- ci
- cli

## License

MIT

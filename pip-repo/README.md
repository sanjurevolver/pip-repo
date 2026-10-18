# pip-repro

`pip-repro` is a Python CLI that audits dependency files for installability risks that show up later, not just during the initial install.

It helps teams catch issues such as:

- yanked package versions on PyPI
- missing wheels for the target Python version
- packages that were valid yesterday but are risky for future installs
- compatibility problems hidden inside pinned dependency files

## Repository description

Repository topics: `python`, `dependency-management`, `pip`, `pypi`, `packaging`, `security`, `ci`, `cli`

## Installation

### From PyPI

```bash
pip install pip-repro
```

### From source

```bash
git clone https://github.com/sanjurevolver/pip-repo.git
cd pip-repo
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Real usage examples

### Example 1: audit a requirements file

```bash
pip-repro audit examples/requirements-risky.txt
```

Example file:

```text
# examples/requirements-risky.txt
requests==2.26.0
django==4.2.1
pandas==1.5.0
```

Example output:

```text
Package     Status      Reason                                                    Fix
---------   ----------  --------------------------------------------------------  --------------------------------------
requests    OK          available and compatible with the current target           keep or bump to a newer patch
pandas      WARNING     no wheel for this Python target                           upgrade to a maintained version
django      CRITICAL    version is yanked or missing from PyPI                    bump to a supported release
```

### Example 2: audit a pyproject.toml file

```bash
pip-repro audit examples/pyproject-risky.toml
```

Example file:

```toml
[project]
dependencies = [
  "django==4.2.1",
  "numpy==1.24.0",
  "urllib3==1.26.18",
]
```

Sample result:

```text
Package    Status      Reason                                      Fix
---------  ----------  ------------------------------------------  -----------------------------
urllib3    CRITICAL    version is yanked or unavailable           bump to a current release
numpy      WARNING     no wheel for Python 3.14                    test against supported versions
django     CRITICAL    pinned version is not recommended           update to >=4.2.14
```

## Before and after

### Before

```bash
# risky pins that are not revalidated before release
pip-repro audit requirements.txt
```

### After

```bash
# safer pins after review and upgrades
pip-repro audit requirements.txt --python 3.13
```

A safer file often looks like:

```text
requests>=2.32.0
django>=4.2.14
pandas>=2.2.0
```

## Exit codes

- `0`: no issues found
- `1`: warnings were found
- `2`: critical issues were found

## Automated tests and CI

This project includes automated tests and a GitHub Actions workflow:

- tests: `tests/`
- workflow: `.github/workflows/ci.yml`

CI checks:

- dependency install
- Ruff linting
- Ruff format checks
- strict mypy type checking
- pytest suite with coverage

## Sample actionable reports

```text
Package     Status      Actionable fix
---------   ----------  --------------------------------------------------
numpy       WARNING     test compatibility on Python 3.12/3.13 or bump version
django      CRITICAL    upgrade to a supported release and regenerate locks
urllib3     CRITICAL    remove the pinned yanked version and refresh dependencies
```

## Roadmap

- `v0.1.0`: initial CLI, dependency audit, JSON output, and CI integration
- `v0.2.0`: richer dependency graph checks and match analysis for file-based installs
- `v0.3.0`: better fix suggestions and risk scoring
- `v1.0.0`: stable release with curated policy checks and recommended upgrades

## Development

```bash
git clone https://github.com/sanjurevolver/pip-repo.git
cd pip-repo
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Release notes

See [RELEASE_NOTES_v0.1.0.md](RELEASE_NOTES_v0.1.0.md) for the initial release summary.

## License

MIT

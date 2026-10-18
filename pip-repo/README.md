# pip-repro

> A Python dependency audit CLI for preventing future install breakage before it reaches CI or production.

<div align="center">

[![CI](https://github.com/sanjurevolver/pip-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/sanjurevolver/pip-repo/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/CLI-Audit%20Dependencies-4f46e5" alt="CLI audit dependencies" />
  <img src="https://img.shields.io/badge/Use-Requirements%20%26%20pyproject.toml-10b981" alt="Requirements and pyproject support" />
  <img src="https://img.shields.io/badge/Goal-Prevent%20future%20install%20breaks-f59e0b" alt="Prevent future install breaks" />
</p>

<p align="center">
  <strong>Audit Python dependency risk before it reaches CI or production.</strong>
</p>

<table>
  <tr>
    <td align="center"><strong>Problem</strong><br>Dependency issues often pass a normal install and break later in CI, upgrades, or production.</td>
    <td align="center"><strong>Solution</strong><br>pip-repro audits dependency files and highlights compatibility risk before it becomes a deployment problem.</td>
    <td align="center"><strong>Impact</strong><br>Better dependency hygiene, safer upgrades, and earlier signals for risky Python environments.</td>
  </tr>
</table>

`pip-repro` is a lightweight Python CLI for catching dependency risk before it becomes a deployment surprise. It inspects requirements files and `pyproject.toml` declarations for the kinds of issues that often slip past a normal install check: yanked releases, missing wheels for a target runtime, and pins that look safe today but fail later on newer Python or CI environments.

Built for developers and teams who want a practical pre-flight check before dependency drift turns into a production problem.

## Architecture

```text
+-------------------+      +----------------------+      +----------------------+
| Dependency file   | ---> | pip-repro parser     | ---> | Package metadata     |
| requirements.txt  |      | + validator          |      | PyPI / wheel check   |
| pyproject.toml   |      +----------------------+      +----------------------+
+-------------------+                                            |
                                                                  v
                                                       +----------------------+
                                                       | Risk analysis        |
                                                       | - yanked versions    |
                                                       | - wheel mismatch     |
                                                       | - Python target risk |
                                                       +----------+-----------+
                                                                  |
                                                                  v
                                                       +----------------------+
                                                       | Console / JSON       |
                                                       | report + guidance    |
                                                       +----------------------+
```

The flow is intentionally simple: parse input, inspect package metadata, evaluate compatibility risk, and output actionable remediation guidance.

## How it works

1. Parse dependency declarations from `requirements.txt` or `pyproject.toml`
2. Fetch package metadata and compatibility facts from PyPI
3. Check for yanked versions, unsupported Python targets, and missing wheel support
4. Surface a report with risk severity and recommended next steps

## Feature highlights

<table>
  <tr>
    <td align="center"><strong>Dependency audit</strong><br>Review dependency files before they drift into production.</td>
    <td align="center"><strong>Wheel compatibility</strong><br>Flag packages that lack support for the target runtime.</td>
    <td align="center"><strong>Actionable output</strong><br>Get clear guidance instead of vague warnings.</td>
  </tr>
</table>

## Why it matters

- catches compatibility risk before it reaches CI or production
- surfaces actionable remediation guidance instead of vague warnings
- works with common Python dependency sources and lockfile-style workflows
- gives both human-readable reports and JSON output for automation

## What it detects

- yanked or unsupported package versions
- missing wheels for the target Python version and platform
- dependency risk before a lockfile breaks in a later install
- upgrade paths with clear, actionable recommendations

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

## Quick start

```bash
pip-repro audit requirements.txt
pip-repro audit pyproject.toml
pip-repro audit requirements.txt --python 3.14
pip-repro audit requirements.txt --json
```

## Demo

The project is intentionally small, fast, and easy to run locally. It is a strong fit for portfolio work, internal tooling, and early-stage dependency governance.

```bash
pip-repro audit examples/requirements-risky.txt
```

This produces a concise report that highlights compatibility risk with clear next steps.

## Example output

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

## Quality checks

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

## Contributing

Contributions are welcome. To keep the project high quality:

1. fork the repo and create a feature branch
2. set up the project locally using the steps above
3. run the format, lint, type-check, and tests before filing a PR
4. keep CLI output and docs aligned with real behavior

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor workflow.

## Security

If you discover a vulnerability or unsafe dependency issue, please report it privately rather than opening a public issue.

See [SECURITY.md](SECURITY.md) for the disclosure process.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the release history and project updates.

## Launch note

See [PROJECT_LAUNCH.md](PROJECT_LAUNCH.md) for a short GitHub/social-ready launch summary.

## Release process

This repo includes a tag-based GitHub release workflow in [.github/workflows/release.yml](.github/workflows/release.yml).

## License

This project is released under the [MIT License](LICENSE).

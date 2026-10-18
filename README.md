# pip-repro

This repository hosts the `pip-repro` project, a Python CLI tool for auditing dependency files against future installability risks.

## Project overview

`pip-repro` checks whether dependency pins are likely to remain installable over time by detecting:

- yanked versions on PyPI
- missing wheels for target Python versions
- compatibility issues with newer Python releases
- dependency metadata that may break later in the lifecycle

## Where the project lives

The main project source and documentation are under the `pip-repo/` directory in this repository.

## Quick start

```bash
cd pip-repo
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## GitHub links

- Repository: https://github.com/sanjurevolver/pip-repo
- Main branch: https://github.com/sanjurevolver/pip-repo/tree/main

## License

MIT

# Release v0.1.0

## Highlights

- Initial release of the `pip-repro` CLI
- Audit dependency files for yanked packages and missing wheels
- Check compatibility with future Python versions
- Support for `requirements.txt` and `pyproject.toml` inputs
- JSON output for CI and automation

## What is included

This release includes:

- a CLI entry point for dependency auditing
- parsing support for common dependency file formats
- PyPI metadata lookup and compatibility checks
- rich terminal reporting and JSON output
- regression tests covering parsing, auditing, and CLI behavior

## Example usage

```bash
pip-repro audit requirements.txt
pip-repro audit pyproject.toml --json
```

## Notes

This is the first public milestone for the project and establishes the base command-line workflow for dependency safety checks.

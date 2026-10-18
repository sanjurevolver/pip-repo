# Changelog

All notable changes to pip-repro are documented in this file.

## [Unreleased]

### Added
- release workflow automation for tag-based GitHub releases
- contributor and security guidance for a more mature open-source workflow
- polished project launch and portfolio documentation

### Improved
- README positioning for a clearer product story and stronger GitHub landing page
- example-driven docs that better explain real dependency risk signals

## [0.1.0] - 2026-10-18

### Added
- initial dependency audit CLI for requirements files and `pyproject.toml`
- detection for yanked packages and unsupported dependency combinations
- Python-version and wheel compatibility checks
- JSON and table output for human-readable and machine-readable reports
- project CI workflow with linting, type checking, and test coverage
- MIT license and GitHub project metadata

### Changed
- improved risk messaging to distinguish between actual failure and compatibility warnings
- tightened CLI output and user-facing recommendations

### Fixed
- compatibility edge cases around wheel selection and target-environment checks
- parser behavior for malformed requirement lines and marker-based filtering

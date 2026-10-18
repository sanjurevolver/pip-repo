from __future__ import annotations

from pathlib import Path

from packaging.requirements import Requirement

from .models import Dependency


def parse_requirements_txt(path: Path) -> list[Dependency]:
    """Parse a requirements.txt file and ignore comments, blanks, and include directives."""
    deps: list[Dependency] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith(("-r", "-e", "--")):
            continue
        req = Requirement(line)
        pinned = None
        for spec in req.specifier:
            if spec.operator == "==":
                pinned = spec.version
                break
        deps.append(
            Dependency(name=req.name, specifier=str(req.specifier), pinned_version=pinned)
        )
    return deps


def parse_pyproject(path: Path) -> list[Dependency]:
    """Parse PEP 621 dependencies from pyproject.toml."""
    import sys

    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib  # type: ignore[no-redef]

    with path.open("rb") as fh:
        data = tomllib.load(fh)

    deps: list[Dependency] = []
    for raw in data.get("project", {}).get("dependencies", []):
        req = Requirement(raw)
        pinned = None
        for spec in req.specifier:
            if spec.operator == "==":
                pinned = spec.version
                break
        deps.append(
            Dependency(name=req.name, specifier=str(req.specifier), pinned_version=pinned)
        )
    return deps


def parse_file(path: Path) -> list[Dependency]:
    """Dispatch parser based on file name and content."""
    if path.name == "pyproject.toml" or path.name.startswith("pyproject"):
        return parse_pyproject(path)
    if path.suffix == ".toml":
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return parse_requirements_txt(path)
        if "[project]" in text:
            return parse_pyproject(path)
    return parse_requirements_txt(path)

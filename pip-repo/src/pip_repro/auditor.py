from packaging.specifiers import SpecifierSet

from .models import Dependency, Finding, Severity
from .pypi import PyPIClient


class Auditor:
    def __init__(self, client: PyPIClient, target_python: str) -> None:
        self.client = client
        self.target_python = target_python

    async def audit(self, deps: list[Dependency]) -> list[Finding]:
        names = [dep.name for dep in deps if dep.pinned_version]
        projects = await self.client.get_many(names)
        return [self._audit_one(dep, projects.get(dep.name, {})) for dep in deps]

    def _audit_one(self, dep: Dependency, project: dict) -> Finding:
        if not dep.pinned_version:
            return Finding(dep, Severity.WARNING, "no pinned version; cannot audit")

        releases = project.get("releases", {})
        files = releases.get(dep.pinned_version, [])

        if not files:
            return Finding(dep, Severity.CRITICAL, "pinned version not found on PyPI")

        if all(file_info.get("yanked", False) for file_info in files):
            return Finding(dep, Severity.CRITICAL, "pinned version is yanked")

        requires_python = None
        for file_info in files:
            value = file_info.get("requires_python")
            if value:
                requires_python = value
                break

        if requires_python and self.target_python not in SpecifierSet(requires_python):
            return Finding(
                dep,
                Severity.WARNING,
                f"requires_python {requires_python} excludes {self.target_python}",
            )

        has_wheel = any(
            file_info.get("packagetype") == "bdist_wheel" or str(file_info.get("filename", "")).endswith(".whl")
            for file_info in files
        )
        if not has_wheel:
            return Finding(dep, Severity.WARNING, "sdist only; no wheel available")

        return Finding(dep, Severity.OK, "healthy")

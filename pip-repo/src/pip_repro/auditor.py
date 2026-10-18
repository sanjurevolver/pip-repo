from packaging.markers import Marker
from packaging.specifiers import SpecifierSet
from packaging.tags import cpython_tags, generic_tags, parse_tag
from packaging.utils import parse_wheel_filename

from .models import Dependency, Finding, Severity
from .pypi import PyPIClient


class Auditor:
    def __init__(self, client: PyPIClient, target_python: str) -> None:
        self.client = client
        self.target_python = target_python

    def _marker_excludes_target(self, dep: Dependency) -> bool:
        if not dep.marker:
            return False
        try:
            marker = Marker(dep.marker)
            env = {"python_version": self.target_python, "python_full_version": self.target_python}
            return not marker.evaluate(environment=env)
        except Exception:
            return False

    def _compatible_wheel_for_target(self, files: list[dict]) -> bool:
        supported = set()
        try:
            major, minor = (int(part) for part in self.target_python.split(".")[:2])
            supported.update(cpython_tags(python_version=(major, minor)))
            supported.update(generic_tags())
        except Exception:
            return True

        for file_info in files:
            filename = str(file_info.get("filename", ""))
            if file_info.get("packagetype") == "bdist_wheel" and not filename:
                return True
            if not filename.endswith(".whl"):
                continue
            try:
                _, _, _, wheel_tags = parse_wheel_filename(filename)
            except Exception:
                continue
            if any(tag in supported for tag in wheel_tags):
                return True

        return False

    def _severity_score(self, severity: Severity) -> int:
        return {Severity.OK: 0, Severity.WARNING: 25, Severity.CRITICAL: 70}[severity]

    async def audit(self, deps: list[Dependency]) -> list[Finding]:
        names = [dep.name for dep in deps if dep.pinned_version]
        projects = await self.client.get_many(names)
        return [self._audit_one(dep, projects.get(dep.name, {})) for dep in deps]

    def _audit_one(self, dep: Dependency, project: dict) -> Finding:
        if dep.marker and self._marker_excludes_target(dep):
            return Finding(
                dep,
                Severity.OK,
                f"marker {dep.marker} does not apply to Python {self.target_python}",
                recommendation="no action needed; this dependency is excluded for the current environment",
                score=self._severity_score(Severity.OK),
                confidence="high",
            )

        if not dep.pinned_version:
            return Finding(
                dep,
                Severity.WARNING,
                "no pinned version; cannot audit",
                recommendation="pin a specific version or use a vetted dependency lockfile",
                score=self._severity_score(Severity.WARNING),
                confidence="medium",
            )

        releases = project.get("releases", {})
        files = releases.get(dep.pinned_version, [])

        if not files:
            return Finding(
                dep,
                Severity.CRITICAL,
                "pinned version not found on PyPI",
                recommendation=f"verify the package name or choose a published version of {dep.name} that supports Python {self.target_python}",
                score=self._severity_score(Severity.CRITICAL),
                confidence="high",
            )

        if all(file_info.get("yanked", False) for file_info in files):
            return Finding(
                dep,
                Severity.CRITICAL,
                "pinned version is yanked",
                recommendation=f"upgrade {dep.name} to a non-yanked release compatible with Python {self.target_python}",
                score=self._severity_score(Severity.CRITICAL),
                confidence="high",
            )

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
                recommendation=(
                    f"choose a version of {dep.name} that supports Python {self.target_python} "
                    f"or upgrade the interpreter to a version that satisfies {requires_python}"
                ),
                score=self._severity_score(Severity.WARNING),
                confidence="high",
            )

        has_wheel = any(
            file_info.get("packagetype") == "bdist_wheel" or str(file_info.get("filename", "")).endswith(".whl")
            for file_info in files
        )
        if not has_wheel:
            return Finding(
                dep,
                Severity.WARNING,
                "sdist only; no wheel available",
                recommendation=f"use a wheel-backed release for Python {self.target_python} or validate the source build in CI",
                score=self._severity_score(Severity.WARNING),
                confidence="medium",
            )

        if not self._compatible_wheel_for_target(files):
            return Finding(
                dep,
                Severity.WARNING,
                "wheel exists but no compatible wheel for the target environment",
                recommendation=f"select a release of {dep.name} with a wheel compatible with Python {self.target_python} and the current platform",
                score=self._severity_score(Severity.WARNING),
                confidence="medium",
            )

        return Finding(
            dep,
            Severity.OK,
            "healthy",
            recommendation="keep the pinned version and recheck during the next dependency refresh",
            score=self._severity_score(Severity.OK),
            confidence="high",
        )

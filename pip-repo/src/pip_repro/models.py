from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Dependency:
    """A single package declared in a dependency file."""

    name: str
    specifier: str
    pinned_version: str | None = None
    marker: str | None = None


@dataclass(frozen=True)
class Finding:
    """A single audit result."""

    dependency: Dependency
    severity: Severity
    message: str
    recommendation: str = ""
    score: int = 0
    confidence: str = "medium"

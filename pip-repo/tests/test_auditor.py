import pytest

from pip_repro.auditor import Auditor
from pip_repro.models import Dependency, Severity


class FakeClient:
    async def get_many(self, names):
        return {
            "django": {
                "releases": {
                    "4.2.1": [
                        {"yanked": True, "packagetype": "bdist_wheel", "requires_python": ">=3.8"}
                    ]
                }
            }
        }


@pytest.mark.asyncio
async def test_rule_r1_yanked():
    audit = Auditor(FakeClient(), target_python="3.12")
    findings = await audit.audit([Dependency("django", "==4.2.1", "4.2.1")])
    assert findings[0].severity == Severity.CRITICAL
    assert "yanked" in findings[0].message


@pytest.mark.asyncio
async def test_marker_excluded_dependency_is_not_flagged():
    audit = Auditor(FakeClient(), target_python="3.12")
    dep = Dependency("django", "==4.2.1", "4.2.1", marker='python_version < "3.12"')
    finding = audit._audit_one(
        dep,
        {
            "releases": {
                "4.2.1": [
                    {
                        "yanked": False,
                        "packagetype": "bdist_wheel",
                        "requires_python": ">=3.12",
                    }
                ]
            }
        },
    )
    assert finding.severity == Severity.OK
    assert "marker" in finding.message.lower()


@pytest.mark.asyncio
async def test_recommendation_is_actionable_for_unsupported_python():
    audit = Auditor(FakeClient(), target_python="3.10")
    dep = Dependency("django", "==4.2.1", "4.2.1")
    finding = audit._audit_one(
        dep,
        {
            "releases": {
                "4.2.1": [
                    {
                        "yanked": False,
                        "packagetype": "bdist_wheel",
                        "requires_python": ">=3.12",
                    }
                ]
            }
        },
    )
    assert finding.severity == Severity.WARNING
    assert "3.12" in finding.recommendation


@pytest.mark.asyncio
async def test_compatible_wheel_check_separates_sdist_from_unsupported_wheel():
    audit = Auditor(FakeClient(), target_python="3.12")
    dep = Dependency("django", "==4.2.1", "4.2.1")

    incompatible = {
        "releases": {
            "4.2.1": [
                {
                    "yanked": False,
                    "packagetype": "bdist_wheel",
                    "filename": "django-4.2.1-pp3-none-any.whl",
                    "requires_python": ">=3.8",
                }
            ]
        }
    }
    compatible = {
        "releases": {
            "4.2.1": [
                {
                    "yanked": False,
                    "packagetype": "bdist_wheel",
                    "filename": "django-4.2.1-cp312-cp312-win_amd64.whl",
                    "requires_python": ">=3.8",
                }
            ]
        }
    }

    incompatible_finding = audit._audit_one(dep, incompatible)
    compatible_finding = audit._audit_one(dep, compatible)

    assert incompatible_finding.severity == Severity.WARNING
    assert "compatible wheel" in incompatible_finding.message.lower()
    assert compatible_finding.severity == Severity.OK
    assert compatible_finding.score == 0


@pytest.mark.asyncio
async def test_warning_has_nonzero_risk_score():
    audit = Auditor(FakeClient(), target_python="3.10")
    dep = Dependency("django", "==4.2.1", "4.2.1")
    finding = audit._audit_one(
        dep,
        {
            "releases": {
                "4.2.1": [
                    {
                        "yanked": False,
                        "packagetype": "bdist_wheel",
                        "requires_python": ">=3.12",
                    }
                ]
            }
        },
    )
    assert finding.score > 0
    assert finding.confidence in {"low", "medium", "high"}

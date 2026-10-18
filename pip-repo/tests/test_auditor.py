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

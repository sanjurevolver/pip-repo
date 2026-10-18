from pathlib import Path

from pip_repro.parser import parse_file, parse_requirements_txt

FIX = Path(__file__).parent / "fixtures"


def test_parse_requirements_txt():
    deps = parse_requirements_txt(FIX / "requirements_simple.txt")
    assert len(deps) == 3
    assert deps[0].name == "django"
    assert deps[0].pinned_version == "4.2.1"
    assert deps[1].pinned_version is None


def test_parse_pyproject():
    deps = parse_file(FIX / "pyproject_simple.toml")
    assert {d.name for d in deps} == {"django", "requests"}

from pathlib import Path

from pip_repro.parser import parse_file, parse_requirements_txt

FIX = Path(__file__).parent / "fixtures"


def test_parse_requirements_txt():
    deps = parse_requirements_txt(FIX / "requirements_simple.txt")
    assert len(deps) == 3
    assert deps[0].name == "django"
    assert deps[0].pinned_version == "4.2.1"
    assert deps[1].pinned_version is None


def test_parse_requirements_txt_handles_markers_and_invalid_lines(tmp_path):
    file = tmp_path / "requirements.txt"
    file.write_text(
        'django==4.2.1; python_version >= "3.12"\n'
        'bad line without a valid requirement\n'
        'requests==2.32.0\n',
        encoding="utf-8",
    )

    deps = parse_requirements_txt(file)
    assert [dep.name for dep in deps] == ["django", "requests"]
    assert deps[0].marker == 'python_version >= "3.12"'
    assert deps[0].pinned_version == "4.2.1"


def test_parse_pyproject():
    deps = parse_file(FIX / "pyproject_simple.toml")
    assert {d.name for d in deps} == {"django", "requests"}

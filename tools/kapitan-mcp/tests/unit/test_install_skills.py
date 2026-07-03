"""Unit tests for scripts/install_skills.py: listing, copying, and error paths."""

from pathlib import Path

import install_skills
import pytest


def test_list_names_a_known_skill(capsys: pytest.CaptureFixture[str]) -> None:
    assert install_skills.main(["install_skills.py", "--list"]) == 0
    assert "kapitan-inventory-model" in capsys.readouterr().out


def test_install_all_copies_every_skill(tmp_path: Path) -> None:
    dest = tmp_path / "skills"

    assert install_skills.main(["install_skills.py", str(dest)]) == 0
    assert {p.name for p in dest.iterdir()} == set(install_skills._available())


def test_category_filter_installs_only_that_category(tmp_path: Path) -> None:
    dest = tmp_path / "skills"

    assert install_skills.main(["install_skills.py", str(dest), "--category", "core"]) == 0
    assert dest.iterdir()  # non-empty
    for skill in dest.iterdir():
        assert install_skills._available()[skill.name] == "core"


def test_unknown_skill_errors(tmp_path: Path) -> None:
    assert install_skills.main(["install_skills.py", str(tmp_path), "not-a-skill"]) == 1


def test_dest_is_required_without_list() -> None:
    with pytest.raises(SystemExit):
        install_skills.main(["install_skills.py"])

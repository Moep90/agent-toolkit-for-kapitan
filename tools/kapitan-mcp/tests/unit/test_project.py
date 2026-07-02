"""Unit tests for project-root discovery and path sandboxing."""

from pathlib import Path

import pytest

from kapitan_mcp.errors import PathOutsideProjectError, ProjectNotFoundError
from kapitan_mcp.project import find_project_root, resolve_within


def test_resolve_within__path_inside_root__returns_resolved_absolute(tmp_path: Path) -> None:
    (tmp_path / "inventory").mkdir()
    target = tmp_path / "inventory" / "targets" / "dev.yml"

    result = resolve_within(tmp_path, "inventory/targets/dev.yml")

    assert result == target.resolve()


def test_resolve_within__parent_traversal__raises(tmp_path: Path) -> None:
    with pytest.raises(PathOutsideProjectError):
        resolve_within(tmp_path, "../../etc/passwd")


def test_resolve_within__absolute_path_outside__raises(tmp_path: Path) -> None:
    with pytest.raises(PathOutsideProjectError):
        resolve_within(tmp_path, "/etc/passwd")


def test_resolve_within__symlink_escape__raises(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-secret"
    outside.mkdir(exist_ok=True)
    root = tmp_path / "project"
    root.mkdir()
    (root / "link").symlink_to(outside)

    with pytest.raises(PathOutsideProjectError):
        resolve_within(root, "link/secret.txt")


def test_find_project_root__marked_by_dot_kapitan__found_walking_up(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "inventory").mkdir(parents=True)
    (root / ".kapitan").write_text("inventory_backend: reclass\n")
    nested = root / "inventory" / "classes"
    nested.mkdir()

    assert find_project_root(nested) == root.resolve()


def test_find_project_root__marked_by_inventory_dir__found(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "inventory").mkdir(parents=True)

    assert find_project_root(root / "inventory") == root.resolve()


def test_find_project_root__no_marker__raises(tmp_path: Path) -> None:
    with pytest.raises(ProjectNotFoundError):
        find_project_root(tmp_path)

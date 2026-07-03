"""Shared test fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from kapitan_mcp.runner import CommandResult

FIXTURES = Path(__file__).parent / "fixtures"

# The stdlib helper scripts live at the repo root, outside the package. Put them on the path
# so the unit tests can import them directly.
_SCRIPTS = Path(__file__).resolve().parents[3] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


@pytest.fixture
def mini_inventory() -> Path:
    """Path to the tiny, deliberately quirky Kapitan project used across unit tests."""
    return FIXTURES / "mini-inventory"


@pytest.fixture
def stub_run():
    """Factory for a drop-in replacement of runner.run that returns canned output.

    Usage: ``run = stub_run(stdout="...")``; the returned callable records each call's
    argv/cwd on ``.calls`` for argv assertions.
    """

    def _factory(stdout: str = "", stderr: str = "", exit_code: int = 0):
        def _run(argv, *, cwd, timeout=120.0, forward_prefixes=()):  # type: ignore[no-untyped-def]
            _run.calls.append({"argv": argv, "cwd": cwd, "timeout": timeout})
            return CommandResult(exit_code=exit_code, stdout=stdout, stderr=stderr)

        _run.calls = []  # type: ignore[attr-defined]
        return _run

    return _factory

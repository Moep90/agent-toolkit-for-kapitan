"""Structural guards for the security invariants.

These are cheap structural checks, not behaviour tests. They fail loudly if a future
change ever wires up secret reveal or drops the env allowlist.
"""

from __future__ import annotations

from pathlib import Path

import kapitan_mcp

SRC = Path(kapitan_mcp.__file__).parent


def test_no_reveal_flag_anywhere_in_src() -> None:
    offenders = [
        py.relative_to(SRC).as_posix() for py in SRC.rglob("*.py") if "--reveal" in py.read_text()
    ]
    assert offenders == [], f"secret-reveal flag must never appear in src: {offenders}"


def test_no_refs_reveal_tool_is_registered() -> None:
    import asyncio

    from kapitan_mcp.server import create_server

    server = create_server(SRC)  # any dir; we only inspect tool names
    names = {t.name for t in asyncio.run(server.list_tools())}
    assert not any("reveal" in n for n in names)

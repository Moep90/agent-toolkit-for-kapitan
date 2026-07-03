"""Unit tests for the MCP server assembly."""

from __future__ import annotations

import asyncio
from pathlib import Path

from kapitan_mcp.errors import PathOutsideProjectError
from kapitan_mcp.models import TargetList
from kapitan_mcp.server import _guard, create_server


def test_create_server__registers_all_m1_tools(mini_inventory: Path) -> None:
    server = create_server(mini_inventory)

    names = {t.name for t in asyncio.run(server.list_tools())}
    assert {
        "kapitan_project_info",
        "kapitan_list_targets",
        "kapitan_list_classes",
        "kapitan_inventory_target",
        "kapitan_class_hierarchy",
        "kapitan_search_inventory",
        "kapitan_refs_list",
        "kapitan_compile",
        "kapitan_compile_diff",
        "kapitan_generator_trace",
        "kapitan_lint",
    } <= names


def test_create_server__tools_have_descriptions(mini_inventory: Path) -> None:
    server = create_server(mini_inventory)

    for tool in asyncio.run(server.list_tools()):
        assert tool.description, f"{tool.name} has no description for the agent"


def test_guard__success__returns_model_dump() -> None:
    def ok() -> TargetList:
        return TargetList(targets=[])

    result = _guard(ok)()

    assert result == {"schema_version": 1, "targets": []}


def test_guard__typed_error__returns_structured_error_contract() -> None:
    def boom() -> TargetList:
        raise PathOutsideProjectError("nope")

    result = _guard(boom)()

    assert result["error"]["code"] == "PATH_OUTSIDE_PROJECT"


def test_search_tool_end_to_end__returns_matches_dict(mini_inventory: Path) -> None:
    server = create_server(mini_inventory)

    result = asyncio.run(
        server.call_tool(
            "kapitan_search_inventory", {"query": "image", "kind": "key", "scope": "classes"}
        )
    )
    # FastMCP returns (content, structured); the structured payload is our dict.
    structured = result[1] if isinstance(result, tuple) else result
    assert "matches" in str(structured)

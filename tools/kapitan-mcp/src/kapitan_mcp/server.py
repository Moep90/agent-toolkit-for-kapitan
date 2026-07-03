"""FastMCP application: registers the read-only tools and serves them over stdio.

Design notes:
- The project root is fixed at server start (``--project-root`` or CWD auto-detect), so
  the model can never point tools at another project.
- Every tool catches :class:`KapitanMcpError` and returns the structured
  ``{error: {...}}`` contract instead of leaking a stack trace.
- Logging goes to stderr only; stdout belongs to the MCP protocol.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import structlog
from mcp.server.fastmcp import FastMCP

from kapitan_mcp.errors import KapitanMcpError, error_response
from kapitan_mcp.project import find_project_root
from kapitan_mcp.tools import compile as compile_tools
from kapitan_mcp.tools import generators, inventory, lint, refs, search

structlog.configure(
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
)
log = structlog.get_logger()


def _guard(fn: Any) -> Any:
    """Wrap a tool so typed errors become structured responses, not tracebacks."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = fn(*args, **kwargs)
        except KapitanMcpError as exc:
            log.warning("tool_error", tool=fn.__name__, code=exc.code)
            return error_response(exc)
        return result.model_dump()

    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


def create_server(project_root: Path) -> FastMCP:
    """Build a FastMCP app with every read-only tool bound to ``project_root``."""
    root = project_root.resolve()
    mcp = FastMCP("kapitan-mcp-server")

    @mcp.tool(name="kapitan_project_info")
    def kapitan_project_info() -> Any:
        """Detect the kapitan version, inventory backend, and target count for the project.
        Call this first: the backend determines interpolation syntax for other tools."""
        return _guard(inventory.project_info)(root)

    @mcp.tool(name="kapitan_list_targets")
    def kapitan_list_targets(pattern: str | None = None) -> Any:
        """List the project's targets (name + path). Optional glob ``pattern`` filters by name."""
        return _guard(inventory.list_targets)(root, pattern)

    @mcp.tool(name="kapitan_list_classes")
    def kapitan_list_classes(pattern: str | None = None) -> Any:
        """List classes, mapping dotted names to file paths. Optional glob ``pattern``."""
        return _guard(inventory.list_classes)(root, pattern)

    @mcp.tool(name="kapitan_inventory_target")
    def kapitan_inventory_target(target: str, parameter_path: str | None = None) -> Any:
        """Return the fully resolved (merged + interpolated) inventory for one target.
        Prefer this over mentally merging YAML. Pass a dotted ``parameter_path`` (e.g.
        'mysql.image') to fetch just a subtree and keep the response small."""
        return _guard(inventory.inventory_target)(root, target, parameter_path=parameter_path)

    @mcp.tool(name="kapitan_class_hierarchy")
    def kapitan_class_hierarchy(target: str) -> Any:
        """Show the ordered class include tree for a target, so you can see which class
        contributes or overrides a value (parameters merge in include order; target wins last)."""
        return _guard(inventory.class_hierarchy)(root, target)

    @mcp.tool(name="kapitan_search_inventory")
    def kapitan_search_inventory(query: str, kind: str = "key", scope: str = "all") -> Any:
        """Find where a parameter is defined or overridden across raw inventory YAML.
        ``kind``: key|value|regex. ``scope``: classes|targets|all. Confirm the resolved
        winner with kapitan_inventory_target."""
        return _guard(search.search_inventory)(root, query, kind=kind, scope=scope)

    @mcp.tool(name="kapitan_refs_list")
    def kapitan_refs_list() -> Any:
        """List secret refs in the inventory (backend, path, whether a ref file exists).
        Metadata only: this never reveals a ref value, and no reveal tool exists."""
        return _guard(refs.refs_list)(root)

    @mcp.tool(name="kapitan_compile")
    def kapitan_compile(targets: list[str], fetch: bool = False, apply: bool = True) -> Any:
        """Compile the given targets. Writes into the project's compiled/ only when apply
        is true. Remote fetch is off unless you opt in with fetch=true."""
        return _guard(compile_tools.compile_targets)(root, targets, fetch=fetch, apply=apply)

    @mcp.tool(name="kapitan_compile_diff")
    def kapitan_compile_diff(targets: list[str]) -> Any:
        """Compile the given targets into a temp dir and return a unified diff against the
        committed compiled/ output. Never writes into compiled/. Run this before finishing
        an inventory or template change to review what it produces."""
        return _guard(compile_tools.compile_diff)(root, targets)

    @mcp.tool(name="kapitan_generator_trace")
    def kapitan_generator_trace(targets: list[str] | None = None) -> Any:
        """Flag components/generators blocks that no kadet compile entry consumes: the
        silent no-op where an inventory block emits nothing with no error. Reads the resolved
        inventory (all targets if none given). Run after editing a generator block, before
        kapitan_compile_diff. Catches unwired blocks, not mistyped keys inside a block."""
        return _guard(generators.generator_trace)(root, targets)

    @mcp.tool(name="kapitan_lint")
    def kapitan_lint() -> Any:
        """Run kapitan's built-in lint (yamllint plus orphan-class checks) and return
        whether it passed, with the raw output."""
        return _guard(lint.lint)(root)

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(prog="kapitan-mcp-server")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Kapitan project root. Defaults to auto-detecting from the current directory.",
    )
    args = parser.parse_args()

    root = args.project_root if args.project_root else find_project_root(Path.cwd())
    log.info("starting", project_root=str(root.resolve()))
    create_server(root).run(transport="stdio")


if __name__ == "__main__":
    main()

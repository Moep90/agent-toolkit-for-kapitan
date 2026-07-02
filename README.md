# agent-toolkit-for-kapitan

MCP servers, agent skills, plugins, and rules files that make AI coding agents
(Claude Code, Codex, Cursor) good at working with [Kapitan](https://kapitan.dev) projects.

Agents are bad at Kapitan out of the box: the inventory is free-form YAML, parameters
deep-merge in include order and only *then* interpolate, and there are multiple backends
and input types. This toolkit gives agents tools to see the *resolved* inventory instead
of guessing, knowledge to reason about the merge model, and guardrails so they never edit
`compiled/` by hand or reveal secrets.

## Status

Early development. The MCP server implements the read-only inventory tools plus compile,
compile-diff, and ref listing, all tested against a real kapitan CLI. Agent skills,
plugins, and release automation are in progress.

## Layout

| Path | What |
|---|---|
| `tools/kapitan-mcp/` | Python MCP server (FastMCP, stdio) wrapping the Kapitan CLI |
| `skills/` | Agent Skills packages (planned) |
| `plugins/` | Claude Code plugins bundling skills and MCP config (planned) |
| `rules/` | AGENTS.md / CLAUDE.md / Cursor rules snippets (planned) |
| `docs/adr/` | Architecture Decision Records |

## MCP server quickstart

```bash
# From a checkout, run the server against your Kapitan repo:
uv --directory tools/kapitan-mcp run kapitan-mcp-server --project-root /path/to/kapitan/repo
```

Once published to PyPI it will run via `uvx kapitan-mcp-server`.

Read-only inventory tools: `kapitan_project_info`, `kapitan_list_targets`,
`kapitan_list_classes`, `kapitan_inventory_target`, `kapitan_class_hierarchy`,
`kapitan_search_inventory`, `kapitan_refs_list` (ref metadata only, never values).

Compile loop: `kapitan_compile` (writes into `compiled/` only when `apply=true`) and
`kapitan_compile_diff` (compiles to a temp dir and returns a unified diff against the
committed `compiled/`, without touching it).

## Development

```bash
make sync        # uv sync the MCP package
make lint        # ruff check + format check
make typecheck   # mypy strict
make test        # pytest (unit; 90% coverage gate on src/)
```

TDD is mandatory: write the failing test first, never commit red. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Apache-2.0](LICENSE).

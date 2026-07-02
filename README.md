# agent-toolkit-for-kapitan

MCP servers, agent skills, plugins, and rules files that make AI coding agents
(Claude Code, Codex, Cursor) good at working with [Kapitan](https://kapitan.dev) projects.

Agents are bad at Kapitan out of the box: the inventory is free-form YAML, parameters
deep-merge in include order and only *then* interpolate, and there are multiple backends
and input types. This toolkit gives agents tools to see the *resolved* inventory instead
of guessing, knowledge to reason about the merge model, and guardrails so they never edit
`compiled/` by hand or reveal secrets.

## Status

Early development, but usable. The MCP server exposes ten read-first tools, tested against a
real kapitan CLI at unit, integration, and MCP-protocol e2e levels. Seven agent skills, two
Claude Code plugins with a marketplace manifest, and rules files for the common clients are
in place.

## Layout

| Path | What |
|---|---|
| `tools/kapitan-mcp/` | Python MCP server (FastMCP, stdio) wrapping the Kapitan CLI |
| `skills/` | Agent Skills packages, portable across clients |
| `plugins/` | Claude Code plugins bundling skills and MCP config |
| `rules/` | AGENTS.md / CLAUDE.md / Cursor rules snippets |
| `docs/` | Getting started, tool reference, ADRs |
| `examples/demo-project/` | A tiny compilable Kapitan project used in docs and e2e tests |

## Install

Prerequisite: a `kapitan` CLI on PATH, or the project's `./kapitan` Docker wrapper. The MCP
server runs where the real CLI lives.

Until the package is on PyPI, `uvx kapitan-mcp-server` runs it straight from this repo:
`uvx --from git+https://github.com/Moep90/agent-toolkit-for-kapitan#subdirectory=tools/kapitan-mcp kapitan-mcp-server`.
Shortened to `uvx kapitan-mcp-server` below; swap in the `--from` form until the release lands.

### Claude Code

Install the plugin from this repo acting as a marketplace:

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` wires up the MCP server and the core skills; add `kapitan-generators` for the
generator, kadet, and scaffolding skills. Then open a Kapitan repo and ask a question like
"what image does target prod deploy?" and the agent answers through the tools.

### Cursor

Add the server to `.cursor/mcp.json` in your Kapitan repo, and copy the Cursor rule:

```json
{
  "mcpServers": {
    "kapitan": {
      "command": "uvx",
      "args": ["kapitan-mcp-server", "--project-root", "."]
    }
  }
}
```

Copy `rules/cursor/kapitan.mdc` into your repo's `.cursor/rules/`.

### Codex CLI

Add the server to `~/.codex/config.toml`:

```toml
[mcp_servers.kapitan]
command = "uvx"
args = ["kapitan-mcp-server", "--project-root", "/path/to/your/kapitan/repo"]
```

Drop `rules/AGENTS.md` into your repo so Codex follows the Kapitan guardrails.

### Any other MCP client

Point the client at the `kapitan-mcp-server` command over stdio with a `--project-root`
argument. The [tool reference](docs/mcp-server.md) lists every tool and its response shape.
For non-plugin clients, adopt the skills by copying the relevant `skills/<name>/` directories
into wherever your client loads Agent Skills, and add a rules file from `rules/`.

## Tools

Read-only inventory: `kapitan_project_info`, `kapitan_list_targets`, `kapitan_list_classes`,
`kapitan_inventory_target`, `kapitan_class_hierarchy`, `kapitan_search_inventory`,
`kapitan_refs_list` (ref metadata only, never values).

Compile loop: `kapitan_compile` (writes into `compiled/` only when `apply=true`),
`kapitan_compile_diff` (compiles to a temp dir and diffs against the committed `compiled/`
without touching it), and `kapitan_lint`.

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

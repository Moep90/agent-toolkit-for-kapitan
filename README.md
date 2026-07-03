# agent-toolkit-for-kapitan

MCP servers, agent skills, plugins, and rules files that make AI coding agents
(Claude Code, Codex, Cursor) good at working with [Kapitan](https://kapitan.dev) projects.

Agents are bad at Kapitan out of the box: the inventory is free-form YAML, parameters
deep-merge in include order and only *then* interpolate, and there are multiple backends
and input types. This toolkit gives agents tools to see the *resolved* inventory instead
of guessing, knowledge to reason about the merge model, and guardrails so they never edit
`compiled/` by hand or reveal secrets.

## Status

Early development, but usable. The MCP server exposes a dozen read-first tools, tested
against a real kapitan CLI at unit, integration, and MCP-protocol e2e levels. Agent skills
for the inventory model, generators, input types, and secrets; two plugins with per-client
marketplace manifests; and rules files for the common clients are in place.

## Layout

| Path | What |
|---|---|
| `tools/kapitan-mcp/` | Python MCP server (FastMCP, stdio) wrapping the Kapitan CLI |
| `skills/` | Agent Skills packages, portable across clients |
| `plugins/` | Plugins bundling skills and MCP config, with per-client manifests |
| `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/` | Marketplace manifests, one per client (generated) |
| `rules/` | AGENTS.md / CLAUDE.md / Cursor rules snippets |
| `docs/` | Getting started, tool reference, ADRs |
| `examples/demo-project/` | A tiny compilable Kapitan project used in docs and e2e tests |

## Install

The configs below bundle the `kapitan` CLI with `--with kapitan`, so the server works out of
the box; drop it if your project pins kapitan or uses the `./kapitan` wrapper. The package is
not on PyPI yet, so they run it from the repo with `uvx --from git+...` (see
[`server.json`](server.json) for the registry manifest).

**Pin a version.** Every push to `main` cuts a `vX.Y.Z` tag ([releases]); the examples pin
`@v0.1.0`. Bump it when you update, or drop the `@...` to track `main`.

[releases]: https://github.com/Moep90/agent-toolkit-for-kapitan/releases

### Claude Code

Install the plugin from this repo acting as a marketplace:

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` wires up the MCP server and the core skills; add `kapitan-generators` for the
generator, input, kadet, and scaffolding skills. Then open a Kapitan repo and ask a question
like "what image does target prod deploy?" and the agent answers through the tools.

### Cursor

Add this repo as a plugin marketplace (Cursor Settings → Plugins → Team Marketplaces →
`https://github.com/Moep90/agent-toolkit-for-kapitan`), then install the `kapitan-core`
plugin. The plugin carries the MCP server config, so you never paste the server URL. Copy
`rules/cursor/kapitan.mdc` into your repo's `.cursor/rules/`.

<details>
<summary>Manual config, without the marketplace</summary>

Add the server to `.cursor/mcp.json` in your Kapitan repo:

```json
{
  "mcpServers": {
    "kapitan": {
      "command": "uvx",
      "args": [
        "--with",
        "kapitan",
        "--from",
        "git+https://github.com/Moep90/agent-toolkit-for-kapitan.git@v0.1.0#subdirectory=tools/kapitan-mcp",
        "kapitan-mcp-server",
        "--project-root",
        "."
      ]
    }
  }
}
```
</details>

### Codex CLI

Add the marketplace, then install the plugin:

```
codex plugin marketplace add Moep90/agent-toolkit-for-kapitan
codex plugin install kapitan-core
```

Drop `rules/AGENTS.md` into your repo so Codex follows the Kapitan guardrails.

<details>
<summary>Manual config, without the marketplace</summary>

Add the server to `~/.codex/config.toml`:

```toml
[mcp_servers.kapitan]
command = "uvx"
args = ["--with", "kapitan", "--from", "git+https://github.com/Moep90/agent-toolkit-for-kapitan.git@v0.1.0#subdirectory=tools/kapitan-mcp", "kapitan-mcp-server", "--project-root", "/path/to/your/kapitan/repo"]
```
</details>

### Any other MCP client

Point the client at the `kapitan-mcp-server` command over stdio with a `--project-root`
argument. The [tool reference](docs/mcp-server.md) lists every tool and its response shape.
For non-plugin clients, adopt the skills with the installer (copies the packages into your
client's skills directory), then add a rules file from `rules/`:

```
python3 scripts/install_skills.py --list                 # see skills and categories
python3 scripts/install_skills.py <skills-dir>           # install all
python3 scripts/install_skills.py <skills-dir> --category core
```

## Tools

Read-only inventory: `kapitan_project_info`, `kapitan_list_targets`, `kapitan_list_classes`,
`kapitan_inventory_target`, `kapitan_class_hierarchy`, `kapitan_search_inventory`,
`kapitan_refs_list` (ref metadata only, never values).

Compile loop: `kapitan_compile` (writes into `compiled/` only when `apply=true`),
`kapitan_compile_diff` (compiles to a temp dir and diffs against the committed `compiled/`
without touching it), and `kapitan_lint`.

Generators: `kapitan_generator_trace` (flags a components/generators block that no compile
entry consumes, the silent no-op) and `kapitan_generator_schema` (the keys other blocks of
the family already use, so a mistyped field stands out).

Full reference with arguments and response shapes: [docs/mcp-server.md](docs/mcp-server.md).

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

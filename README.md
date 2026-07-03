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
| `docs/` | Install, getting started, tool reference, ADRs |
| `examples/demo-project/` | A tiny compilable Kapitan project used in docs and e2e tests |

## Install

Claude Code, from this repo acting as a marketplace (run the two commands separately):

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` wires up the MCP server and the core skills; add `kapitan-generators` for the
generator, input, kadet, and scaffolding skills. Open a Kapitan repo and ask "what image does
target prod deploy?" and the agent answers through the tools.

Cursor, Codex, other MCP clients, manual config, and version pinning:
**[docs/install.md](docs/install.md)**.

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

Setup, the `make` targets, TDD rules, and commit conventions are in
[CONTRIBUTING.md](CONTRIBUTING.md). The security model is in [SECURITY.md](SECURITY.md).

## Docs

- [docs/install.md](docs/install.md): install per client, manual config, version pinning.
- [docs/getting-started.md](docs/getting-started.md): a five-minute demo against the example
  project.
- [docs/mcp-server.md](docs/mcp-server.md): every MCP tool with arguments and response shape.
- [docs/adr/](docs/adr/): Architecture Decision Records.

## License

[Apache-2.0](LICENSE).

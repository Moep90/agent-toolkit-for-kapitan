# Getting started

This walks you from zero to an agent answering resolved-inventory questions about a Kapitan
project in a few minutes. It uses `examples/demo-project`, a tiny two-target project that
compiles with no external binaries.

## Prerequisites

- `uv` (for running the server) and a `kapitan` CLI on PATH, or the project's `./kapitan`
  Docker wrapper.

## Run the server against the demo

From a checkout:

```bash
uv --directory tools/kapitan-mcp run kapitan-mcp-server --project-root examples/demo-project
```

The server speaks MCP over stdio. Point any MCP client at it.

## Claude Code

Install the plugin from this repo acting as a marketplace:

Run these one at a time (the marketplace URL and the install are separate commands):

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
```

```
/plugin install kapitan-core
```

The `kapitan-core` plugin wires up the MCP server (via `uvx kapitan-mcp-server`) and the
core skills. Open a Kapitan repo and ask, for example, "what namespace does the dev target
resolve to?". The agent calls `kapitan_inventory_target` instead of guessing.

## Cursor / Codex / plain MCP

Add the server to your client's MCP config:

```json
{
  "mcpServers": {
    "kapitan": {
      "command": "uvx",
      "args": ["kapitan-mcp-server", "--project-root", "/path/to/your/kapitan/repo"]
    }
  }
}
```

Drop `rules/AGENTS.md` (or the Cursor rules in `rules/cursor/kapitan.mdc`) into your repo so
the agent follows the Kapitan guardrails.

## Five-minute demo

Against `examples/demo-project`, try:

- `kapitan_list_targets` to see `dev` and `prod`.
- `kapitan_inventory_target` with `target=dev`, `parameter_path=greeting` to see the
  interpolated value.
- Change `inventory/classes/common.yml`, then `kapitan_compile_diff` with
  `targets=["dev","prod"]` to review exactly what your edit produces before applying it.

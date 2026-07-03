# Getting started

This walks you from zero to an agent answering resolved-inventory questions about a Kapitan
project in a few minutes. It uses `examples/demo-project`, a tiny two-target project that
compiles with the `kapitan` CLI alone, no helm/jsonnet/terraform binaries.

## Install

Install the plugin for your client following [install.md](install.md). For Claude Code that
is two commands:

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` installs the core skills and configures the MCP server (optional, via
`uvx kapitan-mcp-server`; the skills work without it). For guardrails without a plugin, drop
in a [rules file](../rules/) instead.

## Run against the demo

From a checkout at the repo root:

```bash
uv --directory tools/kapitan-mcp run --extra kapitan kapitan-mcp-server --project-root "$PWD/examples/demo-project"
```

`--extra kapitan` installs the `kapitan` CLI into the run environment. It is an optional
dependency (some setups supply kapitan via the `./kapitan` docker wrapper instead), so without
it every tool that shells out to kapitan fails with `[Errno 2] No such file or directory:
'kapitan'`. Only `kapitan_list_targets`, which reads inventory files directly, works without it.

`--directory tools/kapitan-mcp` moves uv's working directory, so `--project-root` must be
absolute (or relative to `tools/kapitan-mcp`). Pass a path that does not exist and the server
starts anyway with zero targets.

The server speaks MCP over stdio: it reads JSON-RPC on stdin and writes JSON-RPC on stdout.
Typing a tool name into that terminal fails with `Invalid JSON` because the name is not a
JSON-RPC message. You drive it with an MCP client, not by hand.

## Test the server standalone

Two ways to exercise the server without wiring it into an agent.

### MCP Inspector (interactive)

A browser UI to list tools, fill arguments, and read responses:

```bash
npx @modelcontextprotocol/inspector \
  uv --directory tools/kapitan-mcp run --extra kapitan kapitan-mcp-server \
  --project-root "$PWD/examples/demo-project"
```

Open the printed `http://localhost:6274/...` URL, pick a tool, and run it.

### Raw JSON-RPC (no extra tooling)

Every MCP session is `initialize`, then an `initialized` notification, then calls. This pipes
that sequence in and calls `kapitan_list_targets`; the `sleep` keeps stdin open long enough for
the server to answer before EOF:

```bash
{ printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cli","version":"1"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kapitan_list_targets","arguments":{}}}'; sleep 2; } \
| uv --directory tools/kapitan-mcp run --extra kapitan kapitan-mcp-server --project-root "$PWD/examples/demo-project"
```

The `id:2` response lists `dev` and `prod`. Swap the last line for another tool, for example
`kapitan_inventory_target` with `{"target":"dev","parameter_path":"greeting"}`.

## Use it from an agent

Open the demo (or your own Kapitan repo) and ask, for example, "what namespace does the dev
target resolve to?" and the agent calls `kapitan_inventory_target` instead of guessing.

## Five-minute demo

Against `examples/demo-project`, try:

- `kapitan_list_targets` to see `dev` and `prod`.
- `kapitan_inventory_target` with `target=dev`, `parameter_path=greeting` to see the
  interpolated value.
- Change `inventory/classes/common.yml`, then `kapitan_compile_diff` with
  `targets=["dev","prod"]` to review exactly what your edit produces before applying it.

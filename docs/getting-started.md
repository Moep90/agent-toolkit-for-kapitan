# Getting started

This walks you from zero to an agent answering resolved-inventory questions about a Kapitan
project in a few minutes. It uses `examples/demo-project`, a tiny two-target project that
compiles with no external binaries.

## Install

Install the server and skills for your client following [install.md](install.md). For Claude
Code that is two commands:

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` wires up the MCP server (via `uvx kapitan-mcp-server`) and the core skills.

## Run against the demo

To try the server with no real project, from a checkout:

```bash
uv --directory tools/kapitan-mcp run kapitan-mcp-server --project-root examples/demo-project
```

The server speaks MCP over stdio; point any MCP client at it. Open the demo (or your own
Kapitan repo) and ask, for example, "what namespace does the dev target resolve to?" and the
agent calls `kapitan_inventory_target` instead of guessing.

## Five-minute demo

Against `examples/demo-project`, try:

- `kapitan_list_targets` to see `dev` and `prod`.
- `kapitan_inventory_target` with `target=dev`, `parameter_path=greeting` to see the
  interpolated value.
- Change `inventory/classes/common.yml`, then `kapitan_compile_diff` with
  `targets=["dev","prod"]` to review exactly what your edit produces before applying it.

# Plugins

Claude Code plugins that bundle skills and MCP config for one-command install. The repo
root's `.claude-plugin/marketplace.json` lists them, so the repo is itself a marketplace.

- `kapitan-core`: the MCP server (via `uvx kapitan-mcp-server`) plus the inventory-model,
  secrets-refs, and debugging-compile skills.
- `kapitan-generators`: the Kubernetes and Terraform generator skills, kadet authoring, and
  project scaffolding.

Skills live once under `skills/` and are copied into each plugin by `make sync-plugins`.
`make check-plugins` fails on drift. Do not edit the copies under `plugins/*/skills/`
directly; edit the source under `skills/` and re-sync.

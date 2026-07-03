# Install

How to run `kapitan-mcp-server` and adopt the skills, per client. This is the canonical
install reference; the README links here.

## Prerequisites

- `uv` (to run the server).
- A `kapitan` CLI on PATH, or the project's `./kapitan` Docker wrapper. The configs below
  bundle kapitan into the server's isolated environment with `--with kapitan`, so it works
  out of the box; drop `--with kapitan` if your project pins its own kapitan or uses the
  wrapper.

## Version pinning

The package is not on PyPI yet, so the configs run the server from the repo with
`uvx --from git+...`. Every push to `main` cuts a `vX.Y.Z` tag ([releases]); the examples
pin `@v0.1.0` for reproducible behaviour. Bump it when you update, or drop the `@...` to
track `main`. After a PyPI publish, the `--from` argument collapses to
`uvx --with kapitan kapitan-mcp-server` and you pin `kapitan-mcp-server==X.Y.Z` instead. The
server and its packaging are described for MCP clients in [`server.json`](../server.json)
(the Model Context Protocol registry manifest).

[releases]: https://github.com/Moep90/agent-toolkit-for-kapitan/releases

## Claude Code

Install the plugin from this repo acting as a marketplace (run the two commands separately):

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` wires up the MCP server and the core skills; add `kapitan-generators` for the
generator, input, kadet, and scaffolding skills. Then open a Kapitan repo and ask a question
like "what image does target prod deploy?" and the agent answers through the tools.

## Cursor

Add this repo as a plugin marketplace (Cursor Settings → Plugins → Team Marketplaces →
`https://github.com/Moep90/agent-toolkit-for-kapitan`), then install the `kapitan-core`
plugin. The plugin carries the MCP server config, so you never paste the server URL. Copy
[`rules/cursor/kapitan.mdc`](../rules/cursor/kapitan.mdc) into your repo's `.cursor/rules/`.

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

## Codex CLI

Add the marketplace, then install the plugin:

```
codex plugin marketplace add Moep90/agent-toolkit-for-kapitan
codex plugin install kapitan-core
```

Drop [`rules/AGENTS.md`](../rules/AGENTS.md) into your repo so Codex follows the Kapitan
guardrails.

<details>
<summary>Manual config, without the marketplace</summary>

Add the server to `~/.codex/config.toml`:

```toml
[mcp_servers.kapitan]
command = "uvx"
args = ["--with", "kapitan", "--from", "git+https://github.com/Moep90/agent-toolkit-for-kapitan.git@v0.1.0#subdirectory=tools/kapitan-mcp", "kapitan-mcp-server", "--project-root", "/path/to/your/kapitan/repo"]
```
</details>

## Any other MCP client

Point the client at the `kapitan-mcp-server` command over stdio with a `--project-root`
argument; [mcp-server.md](mcp-server.md) lists every tool and its response shape. For
non-plugin clients, adopt the skills with the installer, then add a rules file from
[`rules/`](../rules/):

```
python3 scripts/install_skills.py --list                 # see skills and categories
python3 scripts/install_skills.py <skills-dir>           # install all
python3 scripts/install_skills.py <skills-dir> --category core
```

## Try it against the demo

To run the server with no real project and walk through a few tool calls, see
[getting-started.md](getting-started.md).

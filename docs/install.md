# Install

How to run `kapitan-mcp-server` and adopt the skills, per client. This is the canonical
install reference; the README links here.

## Choose your layer

Three independent layers. Pick what you need; none requires the others.

| Layer | What you get | Needs | How |
|---|---|---|---|
| **Rules** | Guardrails any agent follows via the plain `kapitan` CLI | nothing | `curl` a file from [`rules/`](../rules/), shown per client below |
| **Skills** | Kapitan knowledge and workflows, no server | nothing to run | `install_skills.py`, or a plugin |
| **MCP server** | Structured, sandboxed tools (`kapitan_inventory_target`, `kapitan_compile_diff`, …) | `uv` (+ `kapitan`) | a plugin, or manual config |

The per-client sections below install the **plugin**, which bundles the skills and the MCP
server. For skills alone, see [Skills without a plugin](#skills-without-a-plugin); for
guardrails alone, use the `curl` in your client's section.

## Prerequisites (MCP server layer)

Only the MCP server needs these; the rules and skills layers need neither.

- `uv` (to run the server).
- A `kapitan` CLI on PATH, or the project's `./kapitan` Docker wrapper. The configs below
  bundle kapitan into the server's isolated environment with `--with kapitan`, so it works
  out of the box; drop `--with kapitan` if your project pins its own kapitan or uses the
  wrapper.

The server runs from this repo on `main`; the package is not on PyPI yet, so the configs use
`uvx --from git+...`. There are no release tags to pin. The server and its packaging are
described for MCP clients in [`server.json`](../server.json) (the Model Context Protocol
registry manifest).

## Claude Code

Install the plugin from this repo acting as a marketplace (run the two commands separately):

```
/plugin marketplace add https://github.com/Moep90/agent-toolkit-for-kapitan.git
/plugin install kapitan-core
```

`kapitan-core` wires up the MCP server and the core skills; add `kapitan-generators` for the
generator, input, kadet, and scaffolding skills. Then open a Kapitan repo and ask a question
like "what image does target prod deploy?" and the agent answers through the tools.

The skills already carry the guardrails. To also pin them into the repo's `CLAUDE.md` (handy
for contributors without the plugin):

```bash
curl -fsSL https://raw.githubusercontent.com/Moep90/agent-toolkit-for-kapitan/main/rules/CLAUDE.md >> CLAUDE.md
```

## Cursor

Add this repo as a plugin marketplace (Cursor Settings → Plugins → Team Marketplaces →
`https://github.com/Moep90/agent-toolkit-for-kapitan`), then install the `kapitan-core`
plugin. The plugin carries the MCP server config, so you never paste the server URL. Copy
[`rules/cursor/kapitan.mdc`](../rules/cursor/kapitan.mdc) into your repo's `.cursor/rules/`:

```bash
mkdir -p .cursor/rules
curl -fsSL https://raw.githubusercontent.com/Moep90/agent-toolkit-for-kapitan/main/rules/cursor/kapitan.mdc -o .cursor/rules/kapitan.mdc
```

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
        "git+https://github.com/Moep90/agent-toolkit-for-kapitan.git#subdirectory=tools/kapitan-mcp",
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
guardrails:

```bash
curl -fsSL https://raw.githubusercontent.com/Moep90/agent-toolkit-for-kapitan/main/rules/AGENTS.md >> AGENTS.md
```

<details>
<summary>Manual config, without the marketplace</summary>

Add the server to `~/.codex/config.toml`:

```toml
[mcp_servers.kapitan]
command = "uvx"
args = ["--with", "kapitan", "--from", "git+https://github.com/Moep90/agent-toolkit-for-kapitan.git#subdirectory=tools/kapitan-mcp", "kapitan-mcp-server", "--project-root", "/path/to/your/kapitan/repo"]
```
</details>

## Skills without a plugin

The skills are plain markdown — no server involved. Install them into any client that reads
Agent Skills:

```
python3 scripts/install_skills.py --list                 # see skills and categories
python3 scripts/install_skills.py <skills-dir>           # install all
python3 scripts/install_skills.py <skills-dir> --category core
```

## Any other MCP client

Point the client at the `kapitan-mcp-server` command over stdio with a `--project-root`
argument; [mcp-server.md](mcp-server.md) lists every tool and its response shape. Add
guardrails with a rules file — most agents read a generic `AGENTS.md`:

```bash
curl -fsSL https://raw.githubusercontent.com/Moep90/agent-toolkit-for-kapitan/main/rules/AGENTS.md >> AGENTS.md
```

## Updating

Everything tracks `main`; there are no versions to bump.

**Claude Code** — refresh the marketplace, then update the plugins:

```
/plugin marketplace update agent-toolkit-for-kapitan
/plugin update kapitan-core
/plugin update kapitan-generators
```

**Codex** — refresh and update:

```
codex plugin marketplace update
codex plugin update kapitan-core
```

**MCP server (any client)** — the server tracks `main`, but `uvx` caches the git build and
does not refetch on its own. After an upstream change, force a rebuild:

```bash
uvx --refresh --from git+https://github.com/Moep90/agent-toolkit-for-kapitan.git#subdirectory=tools/kapitan-mcp kapitan-mcp-server
```

or clear the uv cache with `rm -rf ~/.cache/uv`.

**Rules files** — re-run the `curl ... >> AGENTS.md` (or the `CLAUDE.md` / `.mdc` variant) to
re-pull the latest guardrails.

## Try it against the demo

To run the server with no real project and walk through a few tool calls, see
[getting-started.md](getting-started.md).

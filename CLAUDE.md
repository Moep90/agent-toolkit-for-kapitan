# CLAUDE.md

Contributor guide for Claude Code working in this repo.

## Build & test

```bash
make sync        # uv sync tools/kapitan-mcp
make lint        # ruff check + format check
make typecheck   # mypy strict
make test        # pytest, 90% coverage gate on src/
```

The MCP package lives in `tools/kapitan-mcp/`. A real `kapitan` CLI is only needed for
integration tests; unit tests mock the subprocess runner.

## Rules

- **TDD, always.** Write the failing test first, watch it fail, then minimal code. Never
  commit red. Coverage is a floor (90% on `src/`), not a goal.
- **`runner.py` is the only place a subprocess is spawned.** Route all CLI calls through it.
- **Every model-supplied path goes through `resolve_within`** (sandboxed to project root).
- **No secret reveal, ever.** There is deliberately no `refs_reveal` tool; `--reveal` must
  not appear anywhere in `src/`.
- **Commit messages: Conventional Commit subject + imperative body + DCO sign-off, nothing
  else.** No `Co-Authored-By:` trailers, no "Generated with ..." lines (`includeCoAuthoredBy`
  is off in `.claude/settings.json`).

## Architecture

Subprocess-first: we invoke the `kapitan` CLI, not its Python API. See
[docs/adr/0001-subprocess-first.md](docs/adr/0001-subprocess-first.md). Security model is
in [SECURITY.md](SECURITY.md).

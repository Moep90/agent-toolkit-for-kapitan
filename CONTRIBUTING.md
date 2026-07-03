# Contributing

## Dev setup

```bash
make sync            # uv sync the MCP package (tools/kapitan-mcp)
make lint            # ruff check + format check (src, tests, scripts)
make typecheck       # mypy strict
make test            # pytest, 90% coverage gate on src/
make test-plugin-cli # opt-in: drive real claude/codex CLIs to install from the marketplace

# Install the hooks once: ruff/mypy on commit, the full CI gate on push.
pre-commit install --hook-type pre-commit --hook-type pre-push
```

The `pre-push` hook runs `make lint typecheck check-plugins test` so a
red branch never reaches main. Bypass one push with `git push --no-verify`.

You need `uv`. A real `kapitan` CLI is only required for the integration tests
(`make test-integration`); the unit suite mocks the subprocess runner. `test-plugin-cli`
needs the `claude` and/or `codex` CLIs installed and skips whichever is absent.

## TDD is mandatory

Write the failing test first, watch it fail, then write the minimal code to pass.
Never commit on red. Coverage is a floor (90% on `src/`), not a goal: assert behaviour,
not lines. Anything touching subprocesses gets tested twice: a unit test asserting the
exact argv/cwd/env/timeout, and an integration test against the fixtures.

## Commit & PR conventions

- **Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`). Release
  automation derives versions and the changelog from these. We squash-merge, so the PR
  title becomes the commit.
- **DCO sign-off** on every commit: `git commit -s` (adds `Signed-off-by:`).
- **Authorship policy: commits are authored by the human developer only.** Do not add
  `Co-Authored-By:` trailers or "Generated with ..." lines to commits or PR descriptions.
  Reviewers reject commits containing them.

## Adding a skill

A skill earns its place by footgun density, not taxonomy coverage. Before adding one, read
the gate in [skills/README.md](skills/README.md#when-does-something-deserve-a-skill): if it
cannot name the specific mistake it prevents, it does not belong.

## Security invariants (never regress these)

- No tool ever reveals secret values; there is deliberately no `refs_reveal` tool.
- Read-only by default; only compile writes, and only inside the project's `compiled/`.
- Every model-supplied path goes through `resolve_within` (sandboxed to the project root).
- `runner.py` is the only place a subprocess is spawned.

See [SECURITY.md](SECURITY.md) for reporting and the full model.

# Rules

Drop-in guardrail snippets for Kapitan repos. They encode the same non-negotiables in each
tool's format. Keep them short: rules files are always in context, so every line costs
tokens on every turn.

- `AGENTS.md`: generic agent rules.
- `CLAUDE.md`: Claude Code flavour, prefers the `kapitan_*` MCP tools when installed.
- `cursor/kapitan.mdc`: Cursor rules with `globs` scoping them to inventory and components.

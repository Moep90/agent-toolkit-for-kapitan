# Security Policy

## Reporting a vulnerability

Report privately via GitHub Security Advisories: open a report at
https://github.com/Moep90/agent-toolkit-for-kapitan/security/advisories/new
("Report a vulnerability" on the Security tab). Do not open a public issue for security
problems. Triage SLA: 72 hours. We follow a 90-day coordinated disclosure policy.

## Supported versions

| Component | Supported |
|---|---|
| `kapitan-mcp-server` | latest minor |
| Kapitan | latest two minors (0.34+ / 0.36+) |
| Python | >=3.10,<3.15 (tracks Kapitan) |

## Security model (summary)

The LLM is an untrusted caller operating inside a trusted user's repo, and the repo
content itself may be untrusted (prompt injection via YAML comments or templates).

- **No secret reveal, structurally.** No tool shells out to `refs --reveal`; CI greps for
  the flag. `kapitan_refs_list` returns metadata only, never values.
- **Read-only by default.** Only compile writes, and only inside `compiled/` under the
  sandboxed project root.
- **Path sandboxing.** Every model-supplied path is resolved and prefix-checked against
  the project root, blocking `../` traversal and symlink escapes.
- **No network by default.** Remote fetch is opt-in per call and gated by a server start
  flag, so a prompt-injected "fetch this URL" fails closed.
- **Env scrubbing.** The subprocess runner passes an allowlist only; cloud credentials
  (`AWS_*`, `GOOGLE_*`, `VAULT_*`) require an explicit human-chosen forward flag.
- **Injection surfaces.** All tool string params are data: argv lists, never a shell.

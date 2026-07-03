# Releasing

Releases are automatic. Every push to `main` runs `.github/workflows/release.yml`, which
computes the next version from the Conventional Commit messages since the last tag, stamps
that version into the plugin manifests and README pins, commits the stamp back to `main`,
tags it, and publishes a GitHub release with generated notes. Versioning is SemVer; the
Python package version is derived from the git tag by hatch-vcs.

A release is cut only when the commits since the last tag warrant one: `fix:` bumps the
patch, `feat:` the minor, and `feat!:` or a `BREAKING CHANGE:` footer the major. Pushes that
are only `docs:`, `chore:`, or `ci:` do not cut a release.

## The stamp commit and `RELEASE_TOKEN`

The plugin manifests (`.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, and each
`plugins/*/…-plugin/plugin.json`) and the README install pins carry a literal version, so
clients can detect updates. The version lives once, as `VERSION` in
[`scripts/sync_plugins.py`](../scripts/sync_plugins.py); the release workflow rewrites that
line, regenerates the manifests, and commits the result as `chore(release): vX.Y.Z [skip ci]`
before tagging.

Because `main` is protected, the default `GITHUB_TOKEN` cannot push that commit. Create a
personal access token from a repo admin (fine-grained, `contents: read and write` on this
repo) and store it as the `RELEASE_TOKEN` repository secret
(`gh secret set RELEASE_TOKEN`). Without it the workflow skips the stamp and tags the merge
commit as-is, so releases still succeed; the manifests just keep their previous version.

## Publishing to PyPI and the MCP registry

Tagging and the GitHub release happen on every merge with no setup. Publishing to PyPI and
the Model Context Protocol registry is gated behind a repository variable so it stays off
until the one-time setup is done:

1. On [PyPI](https://pypi.org/manage/account/publishing/), register this repository as a
   Trusted Publisher for the `kapitan-mcp-server` project (workflow `release.yml`,
   environment none). No API token is stored.
2. Set the repository variable `PUBLISH_ENABLED` to `true`
   (`gh variable set PUBLISH_ENABLED --body true`).

Once enabled, each release also builds the wheel and sdist, publishes them to PyPI via
Trusted Publishing (OIDC), and publishes `server.json` to the MCP registry using GitHub OIDC
for the `io.github.Moep90/*` namespace. No long-lived secrets are involved.

## Support policy

- Latest two Kapitan minors.
- Python per Kapitan's own constraint (>=3.10,<3.15).
- Security fixes backported one minor.

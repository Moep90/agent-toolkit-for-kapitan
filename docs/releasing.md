# Releasing

Versioning is SemVer, driven by Conventional Commits. Release PRs and the changelog are
generated from commit history.

## Cutting a release

1. Merge the release PR (it bumps the version and updates `CHANGELOG.md`).
2. Publishing a GitHub Release triggers `.github/workflows/release.yml`, which builds the
   sdist and wheel and publishes to PyPI via Trusted Publishing (OIDC). No API tokens.
3. Smoke test the published artifact on a clean machine:

   ```bash
   uvx kapitan-mcp-server==<version> --help
   ```

## Support policy

- Latest two Kapitan minors.
- Python per Kapitan's own constraint (>=3.10,<3.15).
- Security fixes backported one minor.

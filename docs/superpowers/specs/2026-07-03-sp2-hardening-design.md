# SP2 Hardening: production-readiness spec

## Context

The README carries an "Early development, but usable" status. Making the project
production-ready decomposes into four workstreams: release/distribution (SP1), hardening
(SP2), and presentation (SP3). SP1 is dropped: the project stays rolling-main, with no
version tags, no PyPI publish, and no MCP-registry publish. This spec covers SP2 only. SP3
(README, badges, examples, dropping the status line) is a later, separate spec.

The trigger for SP2 is a coverage gap. The integration and e2e tests only exercise the
`reclass` backend (the `mini-inventory` fixture and `examples/demo-project` both use it).
`omegaconf` and `reclass-rs` appear only in mocked unit tests for backend detection, never
driven end to end. The tool advertises multi-backend support, but only one backend is proven.
`omegaconf` is the backend used by real projects in the wild.

## Scope

### In scope

1. Prove every inventory and compile tool against all three backends (`reclass`,
   `reclass-rs`, `omegaconf`) in CI.
2. Formalize the SECURITY.md claims into tested invariants plus a review record.
3. Prove the large-inventory guardrails (truncation and timeout) and document the limits.
4. Cover error classification for real backend error messages.

### Out of scope

- SP1: versioning, changelog, semver policy, PyPI publish, MCP-registry publish. The project
  stays rolling-main.
- SP3: README value prop, badges, worked examples, contributor onboarding, and removing the
  "Early development" status. SP2 makes those claims true; SP3 writes them.

## Approach

Parametrize the existing integration suite over a backend matrix (chosen over a separate
conformance module or a shared-helper split). The `pytestmark = pytest.mark.integration`
harness and the `mini-inventory` fixture pattern already work; a `backend` parametrize
fixture reuses them and yields per-backend proof of each tool with the smallest new surface.
CI cost is one pip extra: `kapitan[omegaconf,reclass-rs]`. `reclass-rs` ships as a pip wheel
through that extra, so no system binary is needed.

## Design

### 1. Backend matrix

Fixtures under `tools/kapitan-mcp/tests/fixtures/`:

- `reclass`: the existing `mini-inventory`.
- `reclass-rs`: reuse the `mini-inventory` content with the `.kapitan` backend set to
  `reclass-rs`. The parametrize fixture writes the backend into a temp copy so one inventory
  serves both reclass variants.
- `omegaconf`: a new `omega-inventory/` with dot-syntax classes and targets, plus a
  `resolvers.py`. The resolver is deliberate: it exercises the Python import and `.pyc` path
  that produced the earlier `kapitan lint` crash, so the fixture represents a real omegaconf
  project rather than a trivial one.

A `backend` parametrize fixture yields `(backend_name, project_root)`. The integration tests
in `test_kapitan_integration.py` and `test_compile_integration.py` run across it and assert,
per backend: `kapitan_list_targets`, `kapitan_inventory_target` (including the interpolation
syntax, colon for reclass variants and dot for omegaconf), `kapitan_class_hierarchy`, and
`kapitan_compile_diff`.

CI: the `integration` job in `.github/workflows/ci.yml` installs `kapitan[omegaconf,reclass-rs]`.
The backend extras are declared as a test dependency of the MCP package so local `make
test-integration` matches CI.

### 2. Security

Extend `tools/kapitan-mcp/tests/unit/test_security_invariants.py` so each SECURITY.md claim
maps to a test:

- Path escape: `../`, absolute paths, and symlink escapes are rejected by `resolve_within`
  across the tools that take a model-supplied path.
- No reveal: a static check that `--reveal` appears nowhere under `src/`.
- Env scrubbing: the runner passes the allowlist only; `AWS_*` / `GOOGLE_*` / `VAULT_*` do
  not reach the child.
- Network off by default: remote fetch is not enabled unless the caller opts in.
- Injection surface: tool params go through an argv list, never a shell string.

Add `SECURITY-REVIEW.md` at the repo root: a table of each claim, the test that proves it,
and its status. It records what was checked, so the security story is auditable rather than
asserted.

### 3. Performance and limits

Add a synthetic large-inventory fixture generated in a conftest helper (a few hundred
parameters, enough to exceed the 1 MB cap). Tests assert:

- `kapitan_inventory_target` on the large fixture returns `truncated: true` with the `hint`.
- A tiny configured timeout produces a typed `KapitanCliError` with the timeout remediation.

`docs/mcp-server.md` gains a "Limits" note: the `max_bytes` cap, the `timeout`, and the
guidance to switch to `reclass-rs` when resolves are slow.

### 4. Error-path coverage

Capture the real error strings the backends emit (an omegaconf interpolation failure, a
reclass class-not-found) from the fixtures, and assert `classify_kapitan_error` maps each to
the correct typed code and remediation. This closes the gap where the current tests feed
mocked strings that may not match what the backends actually print.

## Success criteria

- The `integration` CI job is green across `reclass`, `reclass-rs`, and `omegaconf`.
- Every inventory and compile tool is asserted against every backend.
- Each SECURITY.md claim has a passing invariant test, and `SECURITY-REVIEW.md` records it.
- Truncation and timeout paths are proven, and the limits are documented.
- Error classification covers the real backend messages, not only mocked ones.
- Coverage stays at or above the existing 90% floor.

## Verification

- `make test-integration` locally with `kapitan[omegaconf,reclass-rs]` installed, green across
  all three backends.
- `mise run gate` (lint, typecheck, check-plugins, unit tests) green.
- CI green on the PR, including the `integration` job, verified by explicit per-check status,
  not a scrolled watch.
- Manual spot check: drive `kapitan_inventory_target` against the omegaconf fixture through
  the stdio server and confirm dot-syntax interpolation resolves.

## Files

- Add: `tools/kapitan-mcp/tests/fixtures/omega-inventory/` (inventory + `resolvers.py`),
  large-inventory conftest helper, `SECURITY-REVIEW.md`.
- Edit: `tools/kapitan-mcp/tests/integration/test_kapitan_integration.py`,
  `test_compile_integration.py` (parametrize over backends);
  `tools/kapitan-mcp/tests/unit/test_security_invariants.py` (expand);
  `tools/kapitan-mcp/tests/unit/test_error_translation.py` (real backend messages);
  `tools/kapitan-mcp/pyproject.toml` (backend test extra);
  `.github/workflows/ci.yml` (install the extra in the integration job);
  `docs/mcp-server.md` (limits note).

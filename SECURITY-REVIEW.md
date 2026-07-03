# Security review

<!-- markdownlint-disable MD013 -- table cells carry full file::test names -->

Each claim in SECURITY.md's "Security model (summary)" mapped to the test
that proves it. Path locations are relative to `tools/kapitan-mcp/`.

| Claim | Test | Status |
|---|---|---|
| No tool shells out to `refs --reveal` | `tests/unit/test_security_invariants.py::test_no_reveal_flag_anywhere_in_src` | proven |
| No reveal tool is registered on the server | `tests/unit/test_security_invariants.py::test_no_refs_reveal_tool_is_registered` | proven |
| `kapitan_refs_list` returns metadata only, never a value | `tests/unit/test_refs.py::test_refs_list__never_returns_a_value` | proven |
| Only compile writes, and only when `apply=True` (temp dir otherwise) | `tests/unit/test_compile.py::test_compile__apply_false_writes_to_temp_not_project` | proven |
| Path sandboxing: `../` traversal is rejected | `tests/unit/test_project.py::test_resolve_within__parent_traversal__raises` | proven |
| Path sandboxing: absolute-path escape is rejected | `tests/unit/test_project.py::test_resolve_within__absolute_path_outside__raises` | proven |
| Path sandboxing: symlink escape is rejected | `tests/unit/test_project.py::test_resolve_within__symlink_escape__raises` | proven |
| Remote fetch is off unless the caller opts in per call | `tests/unit/test_compile.py::test_compile__fetch_off_by_default` | proven |
| Remote fetch opt-in adds the `--fetch` flag | `tests/unit/test_compile.py::test_compile__fetch_opt_in_adds_flag` | proven |
| Remote fetch is additionally gated by a server start flag | none | gap, see Findings |
| Env scrubbing: `AWS_*` credentials are dropped by default | `tests/unit/test_runner.py::test_scrub_env__drops_cloud_credentials_by_default` | proven |
| Env scrubbing: `GOOGLE_*` credentials are dropped unless forwarded | `tests/unit/test_runner.py::test_scrub_env__forwards_only_explicitly_allowed_prefixes` | proven |
| Env scrubbing: `VAULT_*` credentials are dropped by default | `tests/unit/test_security_invariants.py::test_scrub_env__drops_vault_token` | proven |
| Env scrubbing: allowlisted vars (`PATH`, `LANG`, `LC_ALL`, ...) still pass through | `tests/unit/test_runner.py::test_scrub_env__keeps_locale_vars` | proven |
| Injection surfaces: tool params are argv data, never a shell | `tests/unit/test_security_invariants.py::test_run__shell_metacharacters_in_argv_are_not_interpreted` | proven |

## Findings

**Fetch is not gated by a server start flag.** SECURITY.md states remote
fetch is "opt-in per call and gated by a server start flag, so a
prompt-injected 'fetch this URL' fails closed." The per-call opt-in
(`fetch=true` on `kapitan_compile`) exists and is tested. No server start
flag exists: `kapitan-mcp-server`'s only CLI argument is `--project-root`
(`src/kapitan_mcp/server.py:146-152`). Today, an untrusted prompt injection
that gets the model to call `kapitan_compile(..., fetch=True)` reaches the
network with no human-controlled gate beyond the per-call boolean the model
itself sets, so the "fails closed" claim does not hold as written. This
needs a decision: either add a start-time flag (e.g. `--allow-fetch`) that
`fetch=true` must also satisfy, or narrow the SECURITY.md wording to drop
the "gated by a server start flag" part. Left open, not fixed here, since
it is a behavior/design change outside this test-writing task's scope.

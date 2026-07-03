# Skills

Portable Agent Skills that encode Kapitan expertise. Each is a directory with a `SKILL.md`
(frontmatter plus body), optional `references/` for depth, and `evals/evals.json` with
example prompts and expected points.

| Skill | Teaches |
|---|---|
| `kapitan-input-types` | Which `input_type` to use for which job, and the compile-entry shape |
| `kapitan-inventory-model` | Targets, classes, merge order, interpolation-after-merge, backends |
| `kapitan-kubernetes-generator` | The `components:` schema for Kubernetes workloads |
| `kapitan-terraform-generator` | The Terraform generator layout and inventory schema |
| `kapitan-helm-input` | Rendering Helm charts via the native `input_type: helm` |
| `kapitan-omegaconf-resolvers` | Reusable inventory blocks via custom omegaconf resolvers |
| `kapitan-authoring-generator` | Writing a reusable generator: the kadet ABI and output-file layout |
| `kapitan-generator-wiring` | Wiring a block to a target and diagnosing the silent no-op |
| `kapitan-writing-kadet` | Kadet Python components and how to test them |
| `kapitan-secrets-refs` | Ref syntax per backend and the never-reveal rule |
| `kapitan-project-scaffolding` | Project layout, bootstrap, the `./kapitan` wrapper |
| `kapitan-debugging-compile` | Symptom-to-fix tables for compile errors |

Validate frontmatter and reference links with `make validate-skills`.

## When does something deserve a skill?

A skill earns its place by **footgun density, not taxonomy coverage.** Add one only when an
agent reliably gets something wrong *and* the fix is non-obvious and kapitan-specific. Do not
add a skill per input type, per generator, or per feature just to be complete: breadth for its
own sake is padding, and padding buries the value.

- **Add a skill** where kapitan is hostile to guessing: merge order, resolved inventory,
  secrets, the silent no-op, generator wiring, the kadet ABI.
- **Do not add a skill** for something an agent already knows (jinja2, jsonnet as languages)
  or that is trivial (copy, remove). At most, a row in an index skill like
  `kapitan-input-types`.
- **Index over enumerate.** When a family (inputs, backends) needs coverage, prefer one
  selector skill that routes to the few deep skills, over one skill per family member.

If a proposed skill cannot name the specific mistake it prevents, it does not earn its place.

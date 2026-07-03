# Skills

Portable Agent Skills that encode Kapitan expertise. Each is a directory with a `SKILL.md`
(frontmatter plus body), optional `references/` for depth, and `evals/evals.json` with
example prompts and expected points.

| Skill | Teaches |
|---|---|
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

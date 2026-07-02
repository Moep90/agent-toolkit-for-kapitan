# Working in a Kapitan repo

Rules for any AI agent editing this project. These are non-negotiable.

1. Never hand-edit anything under `compiled/`. It is generated output. Change the inventory
   or a template, then recompile.
2. After any inventory or template change, compile and diff against the committed output
   before finishing. An unexpected diff in a target you did not mean to touch is a
   regression, not noise.
3. Read the resolved inventory instead of merging classes in your head. Use
   `kapitan inventory -t <target>` (or the `kapitan_inventory_target` tool). Parameters
   deep-merge in include order and the target wins last; `${...}` resolves only after the
   full merge.
4. Never reveal secret values. Do not run `kapitan refs --reveal`, do not print ref values,
   do not commit revealed output. Refs stay as `?{backend:path}` tokens.
5. Respect the project's configured inventory backend. Do not switch backends to get past
   an error.
6. Interpolation syntax depends on the backend: colon for reclass (`${a:b}`), dot for
   omegaconf (`${a.b}`). Check `.kapitan` first.

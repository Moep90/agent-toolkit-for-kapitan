# Working in a Kapitan repo (Claude Code)

Drop this into a Kapitan project's `CLAUDE.md`. If the `kapitan-*` MCP tools are installed
(via the kapitan-core plugin), prefer them over shelling out.

1. Never hand-edit anything under `compiled/`. Change the inventory or a template, then
   recompile.
2. After any inventory or template change, run `kapitan_compile_diff` and review it before
   finishing. Treat an unexpected diff in other targets as a regression.
3. Use `kapitan_inventory_target` for resolved values instead of merging classes yourself.
   Use `kapitan_class_hierarchy` to see which class wins, and `kapitan_search_inventory` to
   find where a key is set. Parameters merge in include order, target last; `${...}`
   resolves after the merge.
4. Never reveal secret values. Use `kapitan_refs_list` for ref metadata. There is no reveal
   tool, and there should not be. Refs stay as `?{backend:path}` tokens.
5. Respect the configured inventory backend (`kapitan_project_info` reports it). Do not
   switch backends to work around an error.
6. Interpolation syntax depends on the backend: colon for reclass, dot for omegaconf.

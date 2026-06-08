# Repository Pattern

Use the current repository layout as the default pattern.

## Current Layering

1. `AGENTS.md`
- Keep stable repo-wide rules only.
- Point readers to `module_notes/`.
- Do not expand per-module runbooks here.

2. `module_notes/README.md`
- This is the single directory/index router.
- List common docs, modules, function directories, and reading order here.
- Do not create `module_notes/<module>/README.md`, `module_notes/common/README.md`, or other index-only files.

3. `module_notes/common/`
- Store shared user preferences, board access, ADB/SSH rules, SDK/kernel/rootfs/image/Buildroot commands, shared host setup, and cross-module mistakes.
- Common docs are listed from the root README, not from a common README.

4. `module_notes/<module>/<function>/`
- Each function directory owns exactly the current working files:
  - `README.md`
  - `handover.md`
  - `runbook.md`
  - `corrections.md`
- `README.md` is a useful function entrypoint, not a pure file list.
- `handover.md` is the current state.
- `runbook.md` is the reusable command path.
- `corrections.md` is the mistake/fix/future-guard record.

## Compression Pattern

When condensing a session into notes:
- keep commands that were actually used
- keep exact cwd, parameters, binary paths, board paths, and success signals
- when migrating old notes, inventory source command blocks and reconcile them into the target `runbook.md`
- if no recoverable command source exists, document that as a current gap instead of leaving an empty-looking runbook
- keep the shortest explanation that changes operator behavior
- put cross-module facts into `common/`
- update current function docs in place
- delete obsolete flat files and compatibility pointers after migration
- do not create extra evidence directories for dated runs

## Good Update Pattern

When adding or updating a function:
1. Compare the request with existing module/function directories.
2. Reuse an existing function if the target is the same.
3. Ask before creating a new function if the match is ambiguous.
4. Add or update the function directory with the four standard files.
5. Link the function from `module_notes/README.md`.
6. Extract shared rules into `module_notes/common/`.
7. Leave `AGENTS.md` unchanged unless the information is repo-wide and stable.

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
- Store only project-wide information that multiple modules/functions can use before a target function is known.
- Keep common flat and semantic:
  - `user_preferences.md`
  - `board_access.md`
  - `build.md`
  - `corrections.md`
- Common docs are listed from the root README, not from a common README.
- Reusable facts and commands stay in the topic file; cross-module problem/root-cause/fix records stay in `common/corrections.md`.

4. `module_notes/<module>/<function>/`
- Each function directory owns exactly the current working files:
  - `README.md`
  - `handover.md`
  - `runbook.md`
  - `corrections.md`
  - `constraints.md`
- `README.md` is the stable first-screen function entrypoint: scope, current goal, short current-state summary, where to start, and critical links. It is not a pure file list and must not absorb detailed implementation state, evidence matrices, risk inventories, technical-debt lists, long next-step plans, or dated run logs.
- `handover.md` is the detailed current continuation state: implementation state, verified facts, change boundaries, limitations, open risks, and next actions.
- `runbook.md` is the reusable command path.
- `corrections.md` is the solved-problem and mistake/fix/verification/regression-prevention record.
- `constraints.md` is the durable design/workflow/API boundary record.
- Multi-record `corrections.md` and `constraints.md` files include a `## 目录`, preferably a compact table; record types use bold blockquotes, record field labels stay bold on their own line, and field bodies use prose by default.

## Compression Pattern

When condensing a session into notes:
- keep commands that were actually used
- keep exact cwd, parameters, binary paths, board paths, and success signals
- when migrating old notes, inventory source command blocks and reconcile them into the target `runbook.md`
- if no recoverable command source exists, document that as a current gap instead of leaving an empty-looking runbook
- keep the shortest explanation that changes operator behavior
- keep README as the short first-screen entrypoint and move detailed current state to `handover.md`
- put cross-module facts into the narrowest semantic common file
- put cross-module solved problems into `common/corrections.md`
- update current function docs in place
- delete obsolete flat files and compatibility pointers after migration
- do not create extra evidence directories for dated runs

## Good Update Pattern

When adding or updating a function:
1. Compare the request with existing module/function directories.
2. Reuse an existing function if the target is the same.
3. Ask before creating a new function if the match is ambiguous.
4. Add or update the function directory with the five standard files.
5. Link the function from `module_notes/README.md`.
6. Extract shared rules into `module_notes/common/`.
7. Leave `AGENTS.md` unchanged unless the information is repo-wide and stable.

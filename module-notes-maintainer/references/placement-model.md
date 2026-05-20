# Placement Model

Pick the narrowest layer that future work will read before using the fact. Before restructuring, inspect the existing repo layout and follow it when it is coherent.

| Layer | Owns | Does Not Own |
| --- | --- | --- |
| `AGENTS.md` | Stable repo-wide collaboration, editing, testing, and shared environment rules. A pointer to `module_notes/` when present. | Module build/run steps, module status, plans, runbooks, handover, history, secrets. |
| `module_notes/README.md` | Top-level module router, reading order, module list, naming convention. | Procedures, handover content, runbook content, repo-wide rules already in `AGENTS.md`. |
| `module_notes/common/` | Cross-module board, host, transport, permission, cleanup, and environment checks. Safe secret references for shared workflows. | Module-specific build/deploy/runtime status, raw credentials, secret-revealing logs or commands. |
| `module_notes/<module>/README.md` | Module scope and topic router. Links to active plan, runbook, or handover when present. | Detailed commands, repeated repo philosophy, handover details beyond one-line purpose. |
| `module_notes/<module>/NN_*.md` | Focused module topic: build, deploy, test, runtime, driver notes, caveats, open questions, safe secret references. | Long history, accidental duplication, unqualified current-board observations, secret material. |
| `NN_*_runbook.md` | Canonical ordered procedure: steps, commands, expected signals, dependencies, compact recovery guidance. | Broad history, handover narrative, every rationale from deeper topic files. |
| `NN_*_plan.md` | Active multi-step plan that may be lost across long runs, board tests, subagents, multiple turns, or context compaction. | Completed stale checklists, chat chronology, flattened subplans. |
| `NN_handover.md` | Current goal, entrypoints, verified status, limitations, next steps, important caveats, open risks. | Raw chat chronology, every explored branch, trivial edits, speculative ideas as facts. |
| History directory | Milestone summaries and investigation history when the user asks for history or the repo intentionally separates it. | Current-state handover route, operational runbook content. |

Rules:
- `NN` means the repo's ordered numeric prefix, such as `01`, `02`, or `03`.
- Update the existing owner file in place when a new fact fits its purpose.
- Create a new topic only when adding the fact would blur an existing file's single purpose.
- A runbook may intentionally repeat the minimum validated command chain; make it clearly canonical.
- Apply the Secret Reference Pattern from `SKILL.md` wherever a secret is required.
- If cleanup is needed, remove stale links first, mark obsolete content second, and rename/delete only when safe and in scope.

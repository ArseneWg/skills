# Placement Model

Use this table to decide where new information belongs.

| Location | Owns | Does not own |
| --- | --- | --- |
| `AGENTS.md` | Repo-wide stable rules, reading order, pointer to `module_notes/`. | Module runbooks, per-function status, detailed commands. |
| `module_notes/README.md` | The single directory/index router: modules, functions, common docs, documentation convention. | Function runbooks, detailed status, compatibility maps. |
| `module_notes/common/` | Shared user preferences, board access, ADB/SSH, SDK/Buildroot/kernel/rootfs/image operations, cross-module mistakes. | Function-specific commands or handovers. |
| `module_notes/<module>/` | Container for function directories only. | Module-level README files used only as indexes or compatibility pointers. |
| `module_notes/<module>/<function>/README.md` | Stable first-screen function entrypoint: scope, current goal, short current-state summary, where to start, critical links. | Pure file lists, long procedures, detailed implementation state, evidence matrices, risk inventories, technical-debt lists, long next-step plans, raw dated notes. |
| `module_notes/<module>/<function>/handover.md` | Detailed current continuation state: implementation state, verified facts, change boundaries, limitations, open risks, next actions. | Chat chronology, discarded branches, reusable command procedures, raw evidence dumps. |
| `module_notes/<module>/<function>/runbook.md` | Reusable ordered procedures, exact commands, parameters, paths, success/failure signals. | Broad narrative or duplicated common commands. |
| `module_notes/<module>/<function>/corrections.md` | Concrete solved problems and user-corrected mistakes: problem, root cause, fix, verification, regression-prevention guard. | Durable design/workflow constraints that are not tied to one solved failure. |
| `module_notes/<module>/<function>/constraints.md` | Durable design rules, API boundaries, workflow rules, and "do not regress" decisions for this function. | Concrete solved failures, command procedures, current handover state. |

## Rules

- Do not create `history/` directories. Distill durable conclusions into handover/runbook/corrections and delete dated raw summaries unless the user explicitly asks to keep raw evidence outside the normal note layout.
- Keep problems and constraints separate: solved failures go to `corrections.md`; design/workflow constraints go to `constraints.md`.
- Keep README and handover separate: README tells the next operator what the function is and where to read next; handover carries the detailed current state needed to resume work.
- Use styled type labels: `corrections.md` entries use `> **类型：已解决问题**`, and `constraints.md` entries use `> **类型：设计约束**`.
- Multi-record `corrections.md` and `constraints.md` files need a `## 目录`, preferably a compact table; record fields use bold label-only lines such as `**问题：**` followed by separate evidence lines.
- Use prose as the default field body style; reserve bullet lists for true parallel items.
- Do not create module-level or common-level README files just to list files.
- If a module/function already matches the new request, update it instead of creating a duplicate.
- If the match is ambiguous, ask before creating a new function directory.

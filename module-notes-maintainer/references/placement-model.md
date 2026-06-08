# Placement Model

Use this table to decide where new information belongs.

| Location | Owns | Does not own |
| --- | --- | --- |
| `AGENTS.md` | Repo-wide stable rules, reading order, pointer to `module_notes/`. | Module runbooks, per-function status, detailed commands. |
| `module_notes/README.md` | The single directory/index router: modules, functions, common docs, documentation convention. | Function runbooks, detailed status, compatibility maps. |
| `module_notes/common/` | Shared user preferences, board access, ADB/SSH, SDK/Buildroot/kernel/rootfs/image operations, cross-module mistakes. | Function-specific commands or handovers. |
| `module_notes/<module>/` | Container for function directories only. | Module-level README files used only as indexes or compatibility pointers. |
| `module_notes/<module>/<function>/README.md` | Current function entrypoint: scope, current state, where to start, critical links. | Pure file lists, long procedures, raw dated notes. |
| `module_notes/<module>/<function>/handover.md` | Current verified state, limitations, open risks, next actions. | Chat chronology, discarded branches, raw evidence dumps. |
| `module_notes/<module>/<function>/runbook.md` | Reusable ordered procedures, exact commands, parameters, paths, success/failure signals. | Broad narrative or duplicated common commands. |
| `module_notes/<module>/<function>/corrections.md` | User-reported mistakes, root cause, fix, future guard. | General preferences that belong in `common/00_user_preferences.md`. |

## Rules

- Do not create `history/` directories. Distill durable conclusions into handover/runbook/corrections and delete dated raw summaries unless the user explicitly asks to keep raw evidence outside the normal note layout.
- Do not create module-level or common-level README files just to list files.
- If a module/function already matches the new request, update it instead of creating a duplicate.
- If the match is ambiguous, ask before creating a new function directory.

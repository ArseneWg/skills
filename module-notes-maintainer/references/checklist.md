# Module Notes Checklist

Use this before finishing a notes update.

- Did I read the routers: `AGENTS.md`, `module_notes/README.md`, then the relevant function README?
- Did I identify the module and function?
- Did I reuse an existing similar function, or ask before creating a new one?
- Are user preferences, corrections, tested commands, environment facts, recurring errors, and stable norms saved in the right place?
- Are verified facts backed by command output, files, logs, board observations, diffs, or explicit user confirmation?
- Are open questions / unverified risks separated from verified status?
- Are exact commands complete enough to rerun: cwd, env vars, binary path, board path, parameters, success signal?
- For migrations, did I inventory old command fences, executable snippets, paths, board destinations, and success/failure signals before deleting source files?
- Did every recoverable source command land in exactly one target `runbook.md`?
- If a runbook has no command fences, does its runbook or handover explicitly say why no recoverable/fixed command exists?
- Did I replace stale sample board serials with `$BOARD` and keep the current board value in `common/board_access.md`?
- Are host/board/CI/service commands separated when roles differ?
- Does the canonical command sequence live in `runbook.md` instead of being duplicated?
- Did I extract cross-module facts to `module_notes/common/`?
- Did I place common facts in the narrowest semantic file: `user_preferences.md`, `board_access.md`, `build.md`, or `corrections.md`?
- Did I keep cross-module solved problems in `common/corrections.md` instead of mixing them into device/network/build operation files?
- Is each function README still a short first-screen entrypoint, with detailed current state, evidence, risks, technical debt, and long plans moved to the appropriate handover/runbook/corrections/constraints file?
- Did I keep concrete solved problems in `corrections.md` and durable constraints in `constraints.md`?
- Do solved-problem records include `> **类型：已解决问题**`, and constraint records include `> **类型：设计约束**`?
- If a `corrections.md` or `constraints.md` has multiple records, does it have a `## 目录` with one entry per record, preferably as a compact table?
- Are record field labels bold and on their own line, with evidence and explanation split onto following lines for human review?
- Are record bodies written as readable prose by default, with bullets only where they clarify true parallel items?
- Did I update the function `handover.md` after meaningful work?
- Are new modules/functions discoverable from `module_notes/README.md`?
- Are current entrypoints concise, with durable dated-run conclusions distilled into handover/runbook instead of stored as chronology?
- Did I avoid creating README files that only list files, especially module-level, common-level, or history-level README files?
- Did I avoid numeric-prefix common files, nested common directories, and broad catch-all common files?
- Did I delete obsolete flat compatibility pointers after moving useful content?
- Did I avoid creating `history/` directories?
- Did I avoid secrets, partial secret values, secret logs/screenshots, and secret-printing commands?
- For broad migrations, did I run `python3 <skill-dir>/scripts/audit_module_notes.py module_notes` and resolve or explain every failure?

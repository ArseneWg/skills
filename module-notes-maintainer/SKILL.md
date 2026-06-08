---
name: module-notes-maintainer
description: Maintain repository module_notes organized by module/function. Use when Codex needs to create or update module/function notes, handovers, runbooks, corrections, common user preferences, tested command records, environment facts, recurring-error fixes, or current handoff/runbook records.
---

# Module Notes Maintainer

Keep the next operator unblocked. Notes are organized by module, then by function. Write only durable, verified information that changes how future work should be done.

## Core Model

Default layout:

```text
module_notes/
  README.md                  # the single directory/index router
  common/
    00_user_preferences.md
    <shared-board-build-adb-ssh-tooling>.md
  <module>/
    <function>/
      README.md              # current functional entrypoint, not a directory index
      handover.md
      runbook.md
      corrections.md
```

`module_notes/README.md` is the only place for directory records and module/function listings. Do not create `module_notes/<module>/README.md`, `history/`, `history/README.md`, or other index-only files. Existing flat notes should not be preserved as compatibility routers: distill useful facts into the function's current `README.md`, `handover.md`, `runbook.md`, or `corrections.md`, then delete obsolete files.

## Before Writing

- Read the routers first: `AGENTS.md`, then `module_notes/README.md`. Use the root README to find common docs and the target function. Then read the relevant function `README.md` if it exists.
- Identify the module and function. If a new request looks similar to an existing function, update the existing function docs instead of creating a new directory.
- If the target function is unclear or two existing functions may match, ask the user before creating a new module/function directory.
- For migrations or broad cleanups, inventory the source files before editing: command fences, shell snippets, binary paths, board paths, success/failure signals, and user corrections. Use `git show HEAD:<old-path>` when deleting tracked old notes.
- Keep `AGENTS.md` as the top documentation entry only: reading order, module/function index pointer, and "read docs first" rule. Do not put module runbooks there.

## What To Record

Record these durable items in the narrowest useful place:

- User preferences: repeated user requirements, strong corrections, preferred workflows, naming, validation style, and "do not do this again" rules.
- Corrections: user pointed out an agent mistake, the root cause, the fix, and the future guard. Put feature-specific corrections in `<function>/corrections.md`; cross-module mistakes go to `common/`.
- Tested commands: exact command, key parameters, working directory, built binary path, deployed board path, and success/failure signals.
- Environment facts: board address, host paths, device nodes, services, firmware/image state, tool versions, and known permissions.
- Recurring errors: symptom -> cause/scope -> fix/workaround -> how to verify.
- Stable norms: command order, validation gates, cleanup rules, and operating rules.
- Handover: at the end of meaningful work, update `<function>/handover.md` so a new person can continue without reading the chat.
- Open questions: keep unverified but important risks under `Open Questions` / `Unverified Risks`, not mixed into verified status.

## Placement Rules

- `module_notes/README.md` owns all directory/index records: modules, functions, common docs, and where to start. Keep this centralized unless the user explicitly chooses a different single index file such as `module_notes/modules/README.md`.
- `module_notes/common/` owns common user preferences, current board access, ADB/SSH rules, SDK/kernel/Buildroot package build commands, shared host setup, and cross-module mistakes. Do not add `common/README.md` just to index these files; list them in the root README.
- `<function>/README.md` is the current work entrypoint: scope, current goal/state, where to start, and any critical links. It must contain useful current context, not just a file list.
- `<function>/handover.md` owns current status, verified state, limitations, open risks, and next steps.
- `<function>/runbook.md` owns reusable ordered procedures and exact validated commands.
- `<function>/corrections.md` owns mistakes that must not repeat.

## Writing Rules

- Evidence first: record facts only when backed by command output, files read, logs, board observations, code diffs, or explicit user confirmation.
- Update current docs in place. Do not append chat chronology.
- Do not let an entrypoint become a流水账. If repeated dated runs contain durable value, distill the latest valid conclusion into `handover.md` or the reusable command into `runbook.md`; discard non-durable chronology.
- Extract common facts while writing. If a command or rule applies across modules, put it in `common/` and link to it from the function.
- Keep runbooks canonical: when a command sequence is stable, maintain it in `runbook.md`; other docs should link or summarize instead of duplicating the full sequence.
- Keep commands runnable. Include cwd, env vars, binary path, board destination path, and verification command when they matter.
- Split multi-host work clearly. Host, board, CI, and service commands need separate paths, permissions, and success signals.
- Separate verified facts from open questions.
- Do not write secrets, tokens, passwords, cookies, private keys, partial secret values, hashes, screenshots, logs, or commands that print/decode secrets. Record only purpose, storage location, lookup name, injection method, and access owner.
- Preserve useful facts, not obsolete structure. Distill durable evidence into the relevant current function files, and delete obsolete flat files or dated raw summaries unless the user explicitly asks to keep raw evidence outside the normal note layout.
- When migrating or compressing existing notes, inventory source command blocks, executable snippets, paths, binaries, board destinations, and success signals before deleting source files. Map them into the target function `runbook.md`; if a source has no recoverable command record, state that gap explicitly in `handover.md` or `runbook.md`.
- Keep the single root index current whenever a module/function directory is created, moved, or becomes the recommended entrypoint.
- Do not use `legacy_*.md`, `history/`, or any extra dated-evidence directory for retained notes.
- Do not create index-only files. A README is allowed only when it is the root index or a function's current work entrypoint with real operational context.

## Migration Audit

When converting flat notes or compressing noisy docs:

1. Build a source inventory before deleting anything:
   - Count and inspect source command fences: `rg -n '^```' module_notes/<old-scope>`.
   - Search for commands and paths: `rg -n 'adb|ssh|scp|push|pull|build.sh|make |cmake|ninja|python3|/userdata|/usr/bin|success|失败|成功信号|验证'`.
   - Check tracked deleted sources with `git show HEAD:<path>` if the file is already gone.
2. Map every source command record to exactly one target function `runbook.md`.
3. Normalize environment-specific values:
   - Current board serial belongs in `common/01_board_access.md`; function runbooks should use `$BOARD` unless the old serial is itself the subject.
   - Replace passwords, PSKs, tokens, and private values with placeholders such as `<wifi-psk>` and document the lookup owner/method, not the value.
4. If no recoverable command exists for a function, write that as a current gap in `handover.md` or `runbook.md`. Do not leave an empty template that looks complete.
5. Run the audit script when available:
   `python3 <skill-dir>/scripts/audit_module_notes.py module_notes`

## End-Of-Work Guard

Before finishing any module-notes update, check:

- The module/function was identified and routed correctly.
- A similar existing function was reused, or the user approved a new one when ambiguous.
- New modules/functions are linked from `module_notes/README.md`.
- Common facts were extracted to `common/`.
- Verified facts and open questions are separated.
- Tested commands include exact parameters, paths, and success signals.
- For migrations, source command blocks and runbook facts were reconciled against target `runbook.md` files, or the unrecoverable gap is explicitly documented.
- Corrections were captured when the user pointed out a mistake.
- The function `handover.md` lets a new operator continue from the current state.
- Stable command sequences live in `runbook.md`, not copied across multiple current docs.
- Entrypoints remain concise; dated logs are not kept in module notes unless their current conclusion has been distilled.
- No module-level, common-level, or history-level README exists, and no `history/` directory is created.
- No obsolete flat compatibility pointer remains after a migration.
- Broad migrations pass `scripts/audit_module_notes.py`, or any remaining failures are intentionally documented and explained.

## References

Only load these when they help the current edit:
- `references/placement-model.md`: compact ownership table.
- `references/handover-guidelines.md`: handover content shape.
- `references/repo-pattern.md`: repository-specific current layout.
- `references/checklist.md`: final guard checklist.
- `scripts/audit_module_notes.py`: deterministic module_notes layout/content audit; run after migrations and broad cleanup.

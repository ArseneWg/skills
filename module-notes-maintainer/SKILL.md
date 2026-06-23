---
name: module-notes-maintainer
description: Maintain repository module_notes as durable, verified module/function documentation. Use when Codex needs to update module notes, handovers, runbooks, common facts, tested commands, constraints, or correction records. Use solved-issue capture only when the user explicitly asks to record a resolved or bounded investigation as problem/root cause/fix/verification/regression guard.
---

# Module Notes Maintainer

Keep the next operator unblocked. Notes are organized by module, then by function. Write only durable, verified information that changes how future work should be done.

## Core Model

Default layout:

```text
module_notes/
  README.md                  # the single directory/index router
  common/
    user_preferences.md
    board_access.md
    build.md
    corrections.md
  <module>/
    <function>/
      README.md              # current functional entrypoint, not a directory index
      handover.md             # detailed current continuation state
      runbook.md
      corrections.md
      constraints.md
```

`module_notes/README.md` is the only place for directory records and module/function listings. Do not create `module_notes/<module>/README.md`, `history/`, `history/README.md`, or other index-only files. Existing flat notes should not be preserved as compatibility routers: distill useful facts into the function's current `README.md`, `handover.md`, `runbook.md`, `corrections.md`, or `constraints.md`, then delete obsolete files.

## Before Writing

- Read the routers first: `AGENTS.md`, then `module_notes/README.md`. Use the root README to find the relevant common docs and target function. Then read the relevant function `README.md` if it exists.
- Identify the module and function. If a new request looks similar to an existing function, update the existing function docs instead of creating a new directory.
- If the target function is unclear or two existing functions may match, ask the user before creating a new module/function directory.
- For migrations or broad cleanups, inventory the source files before editing: command fences, shell snippets, binary paths, board paths, success/failure signals, and user corrections. Use `git show HEAD:<old-path>` when deleting tracked old notes.
- Keep `AGENTS.md` as the top documentation entry only: reading order, module/function index pointer, and "read docs first" rule. Do not put module runbooks there.

## What To Record

Record these durable items in the narrowest useful place:

- User preferences: repeated user requirements, strong corrections, preferred workflows, naming, validation style, and "do not do this again" rules.
- Corrections and solved issues: concrete mistakes or failures, the root cause, the fix, verification, and the future guard. Put feature-specific records in `<function>/corrections.md`; cross-module mistakes that any module/function may hit go to `common/corrections.md`.
- Constraints: durable design, API, workflow, or documentation rules that should shape future edits but are not themselves a solved failure. Put feature-specific constraints in `<function>/constraints.md`; cross-module constraints go to the narrowest relevant common file.
- Tested commands: exact command, key parameters, working directory, built binary path, deployed board path, and success/failure signals.
- Environment facts: board address, host paths, device nodes, services, firmware/image state, tool versions, and known permissions.
- Recurring errors: symptom -> cause/scope -> fix/workaround -> how to verify.
- Stable norms: command order, validation gates, cleanup rules, and operating rules.
- Handover: at the end of meaningful work, update `<function>/handover.md` so a new person can continue without reading the chat.
- Open questions: keep unverified but important risks under `Open Questions` / `Unverified Risks`, not mixed into verified status.

## Solved Issue Mode

Use this as a mode inside this skill, not a separate skill. Enter this mode only when the user explicitly wants a solved or clearly bounded investigation turned into reusable notes. Do not use it for ordinary note edits, placement questions, runbook updates, handover refreshes, or current-status records.

When solved-issue mode applies, read `references/solved-issue-mode.md`, distill the learning there, then return to the placement and writing rules in this file.

## Placement Rules

- `module_notes/README.md` owns all directory/index records: modules, functions, common docs, and where to start. Keep this centralized unless the user explicitly chooses a different single index file such as `module_notes/modules/README.md`.
- `module_notes/common/` owns project-wide information that multiple modules/functions can use before a target function is known. Keep it flat and semantic: `user_preferences.md`, `board_access.md`, `build.md`, and `corrections.md`. Do not add `common/README.md`; list common files in the root README.
- `common/board_access.md` owns board access and network facts/rules: current board/host addresses, ADB/SSH entrypoints, whether `adb root` is needed, host-side ADB permission boundaries, process cleanup rules, SOCKS5 forwarding, host routes, route/MTU checks, iperf or throughput checks, network baselines, and network boundary checks.
- `common/build.md` owns SDK/kernel/rootfs/image/Buildroot package build commands, clean/rebuild rules, artifact locations, and build success signals.
- `common/corrections.md` owns cross-module solved problems that any module/function may hit, such as ADB transfer degradation, host route failures, stale build artifacts, or documentation migration mistakes. Use the same styled solved-issue record format as function `corrections.md`.
- `common/user_preferences.md` owns durable user preferences and repeated user corrections about working style.
- `<function>/README.md` is the stable first-screen entrypoint: scope, current goal, a short current-state summary, where to start, and critical links. It should answer "what is this function and where do I read next"; it must not become a detailed implementation record, evidence matrix, risk inventory, technical-debt list, long next-step plan, or dated run log.
- `<function>/handover.md` owns the detailed current continuation state: implementation state, verified facts, change boundaries, limitations, open risks, and next actions.
- `<function>/runbook.md` owns reusable ordered procedures and exact validated commands.
- `<function>/corrections.md` owns concrete solved problems, user-corrected mistakes, root cause, fix, verification, and future guard.
- `<function>/constraints.md` owns durable constraints, design rules, API boundaries, workflow rules, and "do not regress" decisions that are not tied to one solved failure.

Use explicit, readable record blocks so problems and constraints stay visually separate. If a `corrections.md` or `constraints.md` file has more than one record, add a `## 目录` section near the top. Prefer a compact table with `编号` / `记录` / `类型`; numbered links are acceptable only for tiny homogeneous files. Keep the record type in a bold blockquote, and keep bold field labels on their own line. Prefer natural paragraphs inside each field; use bullets only for genuinely parallel items such as separate commands, independent evidence points, or a short case matrix.

```markdown
## 目录

| 编号 | 记录 | 类型 |
| --- | --- | --- |
| 01 | [<specific problem or mistake>](#<anchor>) | 已解决问题 |

## <specific problem or mistake>
> **类型：已解决问题**

**问题：**
<observable behavior, exact error, path, metric, or degraded behavior>.

**根因：**
<verified cause and scope>.

**修复：**
<minimal working fix, durable change, or workaround>.

**验证：**
<commands, logs, code paths, board observations, diffs, or user-confirmed signals proving the fix>.

**防回归：**
<how to recognize or avoid recurrence>.
```

```markdown
## 目录

| 编号 | 记录 | 类型 |
| --- | --- | --- |
| 01 | [<specific durable rule>](#<anchor>) | 设计约束 |

## <specific durable rule>
> **类型：设计约束**

**约束：**
<the rule future work must preserve>.

**理由：**
<why this rule exists>.

**防回归：**
<review check or regression guard>.
```

## Handover Shape

Write `handover.md` for a capable operator who has not read the chat and does not know the module yet. Keep it concise, current, and judgment-oriented. A useful handover normally covers these six areas:

1. Scope and goal: what module/function this covers, the target board/package/artifact, and what problem the work solves.
2. Current implementation state: what is already wired up, which paths/configs own the behavior, and what the current user-facing behavior is.
3. Change boundaries and critical principles: the files or ownership layers that are in scope, files or layers that should not be changed for this problem, and any user corrections that constrain future work.
4. Verified facts: builds, deployment paths, board/runtime checks, success signals, and negative tests that have actually been observed.
5. Handoff path: where a new operator should start, which runbook sections to use first, and the shortest safe baseline to rerun before changing code.
6. Open risks and limits: what has not been validated, what varies by environment, and what should not be treated as a fixed fact.

Do not use handover as a dated execution log. Put exact reusable commands, long matrices, logs, and raw output in `runbook.md` or discard them after distilling their durable conclusion. If a handover section would duplicate runbook commands, replace it with a pointer to the runbook and the success signal.

For experiment-heavy work, compress aggressively: the first handover section should state the goal, acceptance line, current conclusion, and conclusion boundary. Keep only the current recommended state, the minimum proof signals that justify it, decisive boundary failures, and open risks. Replace older conclusions in place instead of appending dated sections. Put experiment matrices and failed-run details in a temporary plan or `runbook.md`. Label maturity explicitly, for example `experiment candidate`, `current offline recommended config`, or `product default`.

For unfinished work paused for a long time, record the checkpoint in `handover.md`, not a new file. Keep it to four fields: resume entry (first file, cwd, smallest validation command), current state (branch/commit, key paths, uncommitted-change ownership, artifact or board state), proven boundary (last trusted verification, ruled-out paths with evidence, unverified assumptions), and next action (smallest executable step and result-driven branches).

## Writing Rules

- Evidence first: record facts only when backed by command output, files read, logs, board observations, code diffs, or explicit user confirmation.
- Update current docs in place. Do not append chat chronology.
- Prefer prose for record body text. Do not turn every sentence into a `-` list item; use bullets only when the field contains multiple peer items that are easier to scan as a list. Prefer a compact table directory for multi-record corrections/constraints files; do not use dash-list directories.
- Keep function README files short and stable. If the content becomes detailed current state, evidence, risk, technical debt, or a multi-step plan, move that detail to `handover.md`, `runbook.md`, `corrections.md`, or `constraints.md` and leave only a pointer plus the current summary in README.
- Do not let an entrypoint become a流水账. If repeated dated runs contain durable value, distill the latest valid conclusion into `handover.md` or the reusable command into `runbook.md`; discard non-durable chronology.
- Runbooks are operating manuals, not experiment logs. Keep reusable commands, acceptance gates, and at most one compact "current baselines" table; update or replace rows when new evidence supersedes old evidence.
- Raw dated experiments belong in a temporary plan or scratch record. `handover.md` gets the distilled conclusion and current limits; `runbook.md` gets only the stable procedure and minimal proof signal needed to rerun it.
- Temporary plans may keep raw chronology, but any top or current-state summary must be refreshed when evidence changes; replace stale summary rows or explicitly mark them superseded before finishing.
- If a runbook edit adds multiple dated headings, repeats an existing command block, or preserves old samples only "for context", stop and compress before finishing.
- Extract common facts while writing. If a command or rule applies across modules, put it in `common/` and link to it from the function.
- Do not let common become a mixed scratch file. Common file names must describe the information function directly: preferences, device access, network, build, or cross-module corrections.
- In common files, separate operation rules from solved problems. Put reusable commands and current facts in `board_access.md` or `build.md`; put public problem/root-cause/fix records in `corrections.md`.
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
   - Current board serial belongs in `common/board_access.md`; function runbooks should use `$BOARD` unless the old serial is itself the subject.
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
- Common docs use semantic flat filenames; no numeric prefixes, broad catch-all files, or nested common directories.
- Cross-module solved problems live in `common/corrections.md`, not inside operation files such as `board_access.md` or `build.md`.
- Verified facts and open questions are separated.
- Tested commands include exact parameters, paths, and success signals.
- Solved problems live in `corrections.md`; durable constraints live in `constraints.md`; do not mix them in one file.
- `corrections.md` records use `> **类型：已解决问题**`; `constraints.md` records use `> **类型：设计约束**`.
- Multi-record `corrections.md` and `constraints.md` files include a `## 目录` section, preferably as a compact table, and bold field labels such as `**问题：**` or `**约束：**` are on their own line.
- Record bodies are readable prose by default; bullet lists are reserved for true parallel items, not used as the default sentence style.
- For migrations, source command blocks and runbook facts were reconciled against target `runbook.md` files, or the unrecoverable gap is explicitly documented.
- Corrections were captured when the user pointed out a mistake.
- The function `README.md` remains a short first-screen entrypoint; detailed continuation state lives in `handover.md`.
- The function `handover.md` lets a new operator continue from the current state, including scope, implementation state, change boundaries, verified facts, handoff path, and open risks.
- Long-pause handovers include resume entry, current state, proven boundary, and next action when the task is unfinished.
- Stable command sequences live in `runbook.md`, not copied across multiple current docs.
- Entrypoints remain concise; dated logs are not kept in module notes unless their current conclusion has been distilled.
- No module-level, common-level, or history-level README exists, and no `history/` directory is created.
- No obsolete flat compatibility pointer remains after a migration.
- Broad migrations pass `scripts/audit_module_notes.py`, or any remaining failures are intentionally documented and explained.

## References

Only load these when they help the current edit:
- `references/solved-issue-mode.md`: quality gate and exact structure for solved or bounded problem records; read only when the user asks to turn a verified investigation into reusable learning.
- `references/placement-model.md`: compact ownership table.
- `references/handover-guidelines.md`: handover content shape.
- `references/repo-pattern.md`: repository-specific current layout.
- `references/checklist.md`: final guard checklist.
- `scripts/audit_module_notes.py`: deterministic module_notes layout/content audit; run after migrations and broad cleanup.

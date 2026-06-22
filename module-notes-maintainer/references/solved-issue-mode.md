# Solved Issue Mode

Use this reference only after `module-notes-maintainer` has triggered and the user explicitly wants a solved or clearly bounded investigation turned into reusable notes.

Do not use this mode for ordinary note edits, placement questions, runbook updates, handover refreshes, or current-status records.

## Preconditions

All must be true:

- The problem is solved, or the current failure boundary is verified.
- The learning is non-trivial: a root cause, repeatable fix, recurring failure, board/runtime fact, or workflow correction.
- Evidence exists from commands, logs, code, board state, diffs, or explicit user confirmation.

If the issue is still being diagnosed, write an open risk or handover boundary instead of a solved-issue record.

## Distill First

Before writing, reduce the issue to:

- `问题`: exact observable behavior, error text, path, metric, or degraded behavior.
- `根因`: verified cause and scope; mark unverified parts as open questions or leave them out.
- `修复`: minimal working fix, durable config/code change, or workaround.
- `验证`: commands or signals proving the fix or boundary.
- `防回归`: how to recognize or avoid recurrence.

Use this compact shape when it fits the target file:

```markdown
## 目录

| 编号 | 记录 | 类型 |
| --- | --- | --- |
| 01 | [<specific problem or failure>](#<anchor>) | 已解决问题 |

## <specific problem or failure>
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

## Quality Gate

- If the root cause is still speculative, do not write a solved-issue record.
- If the fix cannot be rerun or recognized later, add the missing command, path, metric, or success signal before finishing.
- If the learning is already recorded, update that entry in place instead of adding a second version.
- If the issue only affects the current transient state and teaches no reusable action, skip solved-issue mode.
- If a file has multiple solved-issue records, include a `## 目录` section; prefer a compact table so readers can scan entry names and types before reading details.
- Do not write field content on the same line as the label. Use `**问题：**` on one line, then evidence on following lines.
- Prefer natural paragraphs inside fields. Use bullets only when the field contains multiple peer evidence points, commands, or cases that are clearer as a list.

## Placement

Apply the main `module-notes-maintainer` placement rules after distilling the issue.

- Put cross-module board, ADB, SSH, networking, SDK, kernel, Buildroot, or shared-host failures under `module_notes/common/`.
- Put feature-specific solved failures in the owning function's `corrections.md`. If the fix created a reusable procedure or exact rerun command, put that procedure in `runbook.md` and link or summarize it from the correction. Update `handover.md` only when the issue changes the current continuation state.
- If the distilled learning is a durable design or workflow rule rather than a solved failure, write it to `constraints.md`, not `corrections.md`.
- Keep shared fixes canonical in one place and add only short cross-references from related module docs.
- Do not create `docs/solutions/`, `CONCEPTS.md`, dated evidence directories, compatibility pointers, or a parallel knowledge-base structure.

## Search First

Before writing, search existing notes with `rg` using module names, error text, IPs, binary paths, command names, and root-cause terms. Read only matching files or sections, then update the narrowest matching record.

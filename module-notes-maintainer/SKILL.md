---
name: module-notes-maintainer
description: Maintain layered repository notes for multi-module work. Use when Codex needs to preserve verified durable facts, update existing module_notes, refresh handover/current-state notes, create runbooks for validated procedures, maintain active plans for long work, update indexes, or clean stale note references safely.
---

# Module Notes Maintainer

Keep notes useful for the next operator: layered, concise, evidence-backed, and safe. Prefer the smallest update that preserves durable facts.

## Core Rules

- Facts need evidence: command output, files read, logs observed, user-provided constraints, or confirmed conclusions.
- Unverified but important risks may be kept only under `Open Questions` or `Unverified Risks`.
- Route facts to the narrowest layer future work will read: repo-wide rules in `AGENTS.md`, shared environment facts in `module_notes/common/`, module details in `module_notes/<module>/`.
- Do not write secrets. Store only safe secret references using the pattern below.
- Do not delete or rename note files by default. Prefer removing stale links or marking obsolete content. Delete or rename only when cleanup is requested or the stale file is clearly in scope and harmful.
- Label current-board, current-host, and current-image observations unless there is evidence they are general rules.
- Preserve useful history when it is intentionally separated, but do not route current handover through history.
- On repeated runs, maintain the current useful state. Update existing notes in place before creating new files.

Durable facts worth preserving:
- User preferences that should steer future work.
- Environment facts such as board addresses, host paths, device nodes, binaries, services, and version constraints.
- Recurring-error fixes: symptom, cause or scope, fix or workaround, and rerun guidance.
- Stable norms: command order, validation gates, and operating rules.

## Modes

- Lightweight: small verified update. Touch the relevant note and required index link only.
- Standard: handover, runbook, module note, or active-plan update. Identify source buckets, classify durable facts, update the smallest file set, then check the result.
- Heavy: deduplication, stale-link cleanup, rename, deletion, or restructure. Use only when requested or clearly necessary inside the current scope.

Start Lightweight. Escalate only when the current mode cannot preserve the facts safely.

## Repeated Runs

When this skill runs multiple times on the same module:
- Inspect existing routers first: `module_notes/README.md` and `module_notes/<module>/README.md`.
- Update the owning note in place when the new fact fits its purpose.
- Replace superseded conclusions with the current verified state; do not append chat chronology.
- Keep reusable failures as `symptom -> cause/scope -> fix/workaround`.
- Treat a runbook as the canonical order once the flow is stable; other notes should link or summarize, not duplicate the full sequence.
- Keep handover current-state focused: goal, entrypoints, verified status, limitations, open risks, and next steps.
- Update active plan status as work changes: `Active`, `Blocked`, `Completed`, `Abandoned`, or `Superseded`.
- Create a new note only when existing notes would lose their single purpose.

## Secret Reference Pattern

When a workflow needs a secret, durable notes may record only:
- `Purpose`: what access the secret enables.
- `Storage`: secret manager, keyring, `pass`/`gopass`, Vault, CI secret store, ignored local file, or encrypted `sops` file.
- `Lookup`: secret name, key path, environment variable, or config path.
- `Injection`: env var, mounted file, keyring lookup, CI variable, or interactive retrieval.
- `Access`: who or which host/role must have permission.

Never record secret values, private keys, tokens, passwords, cookies, session material, partial values, hashes, screenshots, logs, or commands that print/decode secrets.

Example:

```md
Required secret: Board SSH password
Purpose: root login for board recovery workflows.
Storage: `pass rk/board/root-password`
Injection: operator retrieves it interactively; do not print it in logs.
Access: authorized board operators only.
```

## Decision Flow

1. Define scope: target module or directory, operation, and mode. For existing modules, inspect current routers before writing.
2. Identify sources: lightweight work needs only the fact and source; standard/heavy work needs source buckets such as chat conclusions, commands, logs, diffs, files, board observations, or user documents.
3. Classify durable facts by layer. If a workflow crosses machines, privileges, or transports, keep each side's commands, paths, permissions, and success signals explicit.
4. Choose artifacts only when justified:
- Handover: durable current state would be expensive for the next owner to reconstruct.
- Runbook: a validated ordered procedure would be risky to reconstruct from scattered notes.
- Active plan: ongoing work may span multiple turns, long runs, board tests, subagents, or context compaction.
- History: the user asked for history or the repo already has a useful separated history layer.
5. Write the smallest useful note: exact commands, paths, success/failure signals, and caveats that change operator behavior.
6. Update only necessary indexes and stale references.
7. Verify with `references/checklist.md` for standard or heavy work.

## Reference Loading

Load only what the current decision needs:
- `references/placement-model.md`: where each note belongs.
- `references/handover-guidelines.md`: handover threshold and content shape.
- `references/checklist.md`: final quality gates for material updates.

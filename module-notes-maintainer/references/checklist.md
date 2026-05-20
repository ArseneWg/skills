# Review Checklist

Use this for Standard or Heavy updates. For Lightweight updates, check only the first section.

## Always

- Facts are verified, or explicitly labeled as open questions/unverified risks.
- The note lives in the narrowest useful layer.
- Required secrets use only the Secret Reference Pattern from `SKILL.md`.
- Current-board, current-host, and current-image observations are scoped.
- No unrelated cleanup, formatting, rename, or deletion was introduced.
- Existing routers were checked before creating a new topic file.

## Material Updates

- Source buckets were considered: commands, logs, files, diffs, board observations, chat conclusions, or user documents.
- Durable facts were preserved when relevant: user preferences, environment facts, recurring-error fixes, stable norms.
- Commands are exact and include nearby success/failure signals.
- Reusable failures are captured as `symptom -> cause/scope -> fix/workaround`.
- Multi-host or multi-privilege workflows keep each side separate.
- Superseded conclusions were replaced with current state instead of appended as chronology.

## Artifact-Specific

- Handover states current goal, entrypoints, verified status, limitations, open risks, and next steps.
- Runbook is an ordered, validated procedure with dependencies and compact recovery guidance.
- Active plan has status: `Active`, `Blocked`, `Completed`, `Abandoned`, or `Superseded`.
- Stable runbooks are canonical; other notes do not duplicate the full sequence.
- Indexes link only to current useful notes; completed or superseded plans are not presented as active.
- History remains separate from current-state guidance.

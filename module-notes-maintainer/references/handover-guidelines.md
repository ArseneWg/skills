# Handover Guidelines

`<module>/<function>/handover.md` must let a new operator continue without reading the chat.

## Include

- Scope: what function this handover covers, and what it does not cover.
- Current state: the latest verified conclusion, not every step that led there.
- Verified evidence: commands, logs, diffs, board observations, or explicit user confirmations that matter for future work.
- Current artifacts: binary paths, model paths, image paths, board destinations, logs, datasets, configs, or output directories.
- Known limits: conditions where current results should not be reused.
- Next actions: short ordered list of what to do next and how to verify it.
- Open risks: clearly marked unverified assumptions.

## Exclude

- Chat transcript summaries.
- Dated append-only runs that do not change the current conclusion.
- Discarded branches unless the negative conclusion prevents repeated work.
- Generic build/ADB rules that belong in `common/`.
- Full command sequences that belong in `runbook.md`.

## Shape

Prefer this structure:

```markdown
# <Function> Handover

## Current State
- ...

## Verified Facts
- ...

## Next Steps
1. ...

## Open Risks
- ...
```

Keep it short enough to read first. If it grows because procedures are mixed in, move the procedures to `runbook.md`.

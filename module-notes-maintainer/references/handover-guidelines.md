# Handover Guidelines

Handover is a current-state note for the next owner, not a diary or history index.

## Create Or Update

Create or update handover when a module has durable state that is expensive to reconstruct from code and short runbooks alone.

Good triggers:
- architecture, layering, or protocol changes
- board-specific validation with reusable results
- active limitations, caveats, or important open risks
- a continuation path another owner must follow
- multiple rounds of work converged into one current state

Skip handover for typo fixes, one-off commands, discarded debugging branches, or information already captured by source comments or a short runbook.

## Content Shape

Use only the sections that add value:
1. Scope
2. User Goal
3. Relevant Entrypoints
4. Verified Status
5. Important Commands Or Environments
6. Known Pitfalls And Limitations
7. Open Questions Or Unverified Risks
8. Next Steps

Rules:
- Separate verified facts from open questions.
- Apply the Secret Reference Pattern from `SKILL.md`; never include secret-revealing material.
- Label current-board, current-host, and current-image observations.
- Rewrite in place. Collapse stale branches, replace superseded conclusions, and remove obsolete next steps.

## Avoid

- chat transcript residue
- append-only chronology
- pointer-only handover files
- history as the primary current-state route
- presenting unverified risks as facts
- deleting useful history during routine handover cleanup

## Multi-Host Workflows

If board, PC, CI, or service roles differ, record commands, paths, permissions, and success signals per side.

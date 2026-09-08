# Subagent orchestration policy

The root agent owns:
- understanding the user's goal;
- requirements and constraints;
- decomposition;
- architecture and cross-cutting decisions;
- integration;
- final verification;
- the final answer.

Use subagents when independent work can materially improve quality, reduce context pollution, or run useful investigation in parallel.

Prefer delegation for:
- codebase exploration;
- dependency and call-path tracing;
- independent research;
- test and failure investigation;
- review;
- bounded verification.

Do not delegate trivial or inherently serial work.

## Roles

Use `repo_explorer` for read-only investigation before implementation when code ownership or behavior is unclear.

Use `implementer` only after the write scope, intended behavior, and acceptance criteria are sufficiently clear.

Use `reviewer` after implementation for an independent cold review.

Use `verifier` to run concrete validation such as tests, lint, type checks, builds, or reproduction steps.

## Write ownership

Within one checkout, maintain a single source-code writer at a time.

Read-only agents may run in parallel.

Do not have the root and an implementer concurrently edit the same working tree.

Do not run multiple implementation agents concurrently in the same checkout unless their write scopes are explicitly disjoint and the root has determined that parallel writing is necessary.

If true parallel implementation is required across substantial changes, prefer separate Git worktrees or independent worktree chats.

## Delegation depth

Subagents should not spawn additional subagents unless the root has explicitly determined that nested delegation is necessary.

Default to one-level fan-out from the root and fan-in back to the root.

## Context policy

Give each subagent the minimum context required to complete its task.

For independent exploration, verification, and review, prefer a self-contained mission with fresh or minimal inherited conversation context.

Use broader inherited context only when the task genuinely depends on earlier conversation details that cannot be summarized reliably.

## Mission contract

Every delegated task should specify:

- Goal
- Scope
- Read scope
- Write scope, if any
- Known facts
- Constraints
- Acceptance criteria
- Evidence required
- Expected return format
- Stop condition

A subagent should return evidence and results, not silently expand its mission.

### Example mission card

```text
Goal:
Find the root cause of intermittent refresh-token failures.

Scope:
src/auth/**
src/session/**
tests/auth/**

Read scope:
Entire repository if needed for dependency tracing.

Write scope:
None.

Known facts:
- Failure happens after token refresh.
- Initial login succeeds.
- The issue is intermittent.

Constraints:
- Do not modify code.
- Do not propose database schema changes unless evidence requires it.

Acceptance criteria:
Identify the most likely root cause with code-level evidence.

Evidence required:
- relevant files;
- functions/symbols;
- call path;
- failing assumption;
- relevant test coverage.

Return format:
1. Findings
2. Evidence
3. Confidence
4. Recommended implementation boundary
5. Remaining unknowns

Stop condition:
Stop when the root cause is supported by repository evidence,
or report exactly what evidence is still missing.
```

## Completion

Agent agreement is not evidence of correctness.

Before declaring work complete, the root must:
- inspect the resulting diff;
- reconcile reviewer findings;
- inspect verifier results;
- confirm the requested acceptance criteria;
- distinguish verified facts from unresolved assumptions.

The root retains final responsibility for the result.

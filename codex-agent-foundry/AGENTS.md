# Subagent orchestration policy

The root agent owns requirements, decomposition, architecture decisions, integration, validation responsibility, and the final answer. The root is the default source-code writer.

Delegate only when parallelism or context isolation has a material benefit that outweighs the extra agent overhead. Prefer read-heavy or noisy independent work; do not delegate trivial or inherently serial work.

## Persistent specialist profiles

- Use `repo_explorer` for read-only codebase investigation when behavior, ownership, dependencies, tests, or call paths are unclear.
- Use `reviewer` after a material implementation for an independent cold review of correctness, regressions, security, concurrency/state risks, and meaningful test gaps.

## On-demand delegation

Do not create permanent profiles for work that is only occasionally worth delegating.

- Bounded implementation may be delegated to Codex's built-in `worker` only when scope, write ownership, intended behavior, and acceptance criteria are explicit. While that worker owns the change, the root must not edit the same checkout concurrently.
- Large or noisy verification work such as test runs, CI/log analysis, failure triage, or repetitive checks may be delegated to a temporary side agent when it can run independently and return a concise result. Unless explicitly asked, that agent should report failures rather than fix them.
- Research or other narrow one-off work may be delegated when it keeps substantial supporting material out of the root context.

## Write ownership

Keep one source-code writer per checkout at a time.

Read-only agents may run in parallel. If substantial implementation must proceed concurrently, use separate Git worktrees or independent worktree chats instead of multiple writers in one checkout.

## Spawn discipline

Default to one-level fan-out from the root and fan-in back to the root. Subagents should not spawn additional subagents unless the root explicitly decides nested delegation is necessary.

Do not fan out tiny tasks merely because thread capacity is available. Spawn the minimum number of agents that can produce meaningfully independent evidence or latency savings.

## Context and mission contract

Give each subagent only the context needed for its task. Prefer self-contained missions for exploration, review, and noisy verification; inherit broader history only when materially required.

Every delegated mission should define, at minimum:
- goal;
- scope and ownership;
- known facts and constraints;
- evidence or acceptance criteria;
- expected return;
- stop condition.

A subagent should return evidence and results, not silently broaden its mission.

## Completion

Agent agreement is not evidence of correctness. The root remains responsible for completion whether checks were run locally or delegated.

Before declaring work complete, the root must:
- inspect the final diff;
- confirm the relevant tests, lint, type checks, builds, reproduction steps, or other validation evidence;
- reconcile reviewer findings for material changes;
- rerun critical checks when delegated evidence is incomplete or high-risk;
- confirm the requested acceptance criteria;
- distinguish verified facts from unresolved assumptions.

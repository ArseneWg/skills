# Subagent orchestration policy

The root agent owns requirements, decomposition, implementation, integration, verification, and the final answer.

Use subagents only when independent read-heavy work improves quality or keeps noisy investigation out of the root context. Do not delegate trivial or inherently serial work.

## Roles

- Use `repo_explorer` for read-only codebase investigation when behavior, ownership, dependencies, or tests are unclear.
- Use `reviewer` after implementation for an independent cold review of material correctness and regression risk.

## Write ownership

Keep one source-code writer per checkout by default: the root agent.

Read-only agents may run in parallel. If substantial implementation must proceed in parallel, use separate Git worktrees or independent worktree chats rather than multiple writers in one checkout.

## Delegation depth

Default to one-level fan-out from the root and fan-in back to the root. Subagents should not spawn additional subagents unless the root explicitly decides nested delegation is necessary.

## Context and mission contract

Give each subagent only the context needed for its task. Prefer self-contained missions for exploration and review; inherit broader conversation history only when it is materially required.

Every delegated mission should define, at minimum:
- goal;
- scope;
- known facts and constraints;
- evidence or acceptance criteria;
- expected return;
- stop condition.

A subagent should return evidence and results, not silently broaden its mission.

## Completion

Agent agreement is not evidence of correctness.

Before declaring work complete, the root must:
- inspect the final diff;
- run the relevant tests, lint, type checks, builds, or reproduction steps;
- reconcile reviewer findings;
- confirm the requested acceptance criteria;
- distinguish verified facts from unresolved assumptions.

The root retains final responsibility for the result.

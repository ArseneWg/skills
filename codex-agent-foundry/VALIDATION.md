# Validation Notes

This template is intentionally minimal and adaptive. It keeps only the custom profiles that consistently add a distinct information or review advantage, while allowing bounded one-off workers when delegation is actually useful.

## Current Codex capabilities relied on

The template relies on these supported capabilities:

- project-scoped Codex configuration under `.codex/`;
- project custom agents under `.codex/agents/`;
- standalone agent TOML definitions with `name`, `description`, and `developer_instructions`;
- per-agent `model`, `model_reasoning_effort`, and `sandbox_mode` overrides;
- `[agents].max_concurrent_threads_per_session`;
- built-in multi-agent delegation, including general-purpose workers and custom specialist profiles;
- root-to-subagent delegation with results returned to the root;
- model availability that may differ by account, client, authentication mode, and rollout.

## Stable custom profiles

### Kept: `repo_explorer`

Reason: read-heavy exploration is one of the clearest high-value delegation boundaries. It can search large code surfaces, trace call paths, map dependencies and tests, and return evidence without modifying the checkout or filling the root context with intermediate detail.

### Kept: `reviewer`

Reason: an independent cold review provides a distinct signal after material implementation. It is read-only and optimized for correctness, regressions, security, concurrency/state risks, and meaningful test gaps.

## Roles intentionally not made permanent

### Implementation worker

The baseline does not define a permanent custom implementer. The root is the default writer in a normal single-checkout workflow.

However, bounded implementation may be delegated to Codex's built-in `worker` when scope, write ownership, intended behavior, constraints, acceptance criteria, and expected validation are explicit before the worker starts. During that delegation, the root must not edit the same checkout concurrently.

For substantial parallel implementation, use separate Git worktrees or independent worktree chats.

### Verification / tester

The baseline does not define a permanent verifier because focused tests, lint, type checks, builds, reproduction steps, and final diff inspection are normally part of the root's completion path.

Verification becomes a good temporary delegation target when the work is independently useful or noisy: large test suites, CI/compiler log analysis, flaky-test triage, repetitive checks, or other diagnostic output that would otherwise pollute the root context. The side agent should return concise evidence; the root retains final validation responsibility.

### Research and other one-off roles

Narrow research or supporting analysis may be delegated when isolation or parallelism has a clear benefit. These roles do not need permanent TOML profiles unless repeated use demonstrates stable specialization.

## Deliberate policy choices

These are workflow decisions, not Codex hard requirements:

- root remains the default source-code writer;
- prefer read-heavy delegation before write-heavy delegation;
- use the minimum number of agents that can provide materially independent evidence or latency savings;
- one source-code writer per checkout at a time;
- one-level fan-out/fan-in by default;
- fresh or minimal task context for independent exploration, review, and noisy verification when practical;
- concurrency ceiling of 4 is capacity, not a spawn target;
- specialist models are pinned only for the two stable custom profiles, while the root and one-off workers are left task/session-dependent.

## Important caveats

### Sandbox is not an absolute security boundary

Role-level `sandbox_mode = "read-only"` is a useful default, but parent runtime permissions can affect spawned agents. Do not treat the agent TOML as a hard security boundary.

### Delegation depth is behavioral

The template intentionally does not rely on legacy V1-only depth controls. `AGENTS.md` asks the root to use one-level fan-out/fan-in by default and asks subagents not to spawn additional agents unless explicitly justified.

### Context inheritance is a strategy decision

Fresh or minimal task context is preferred when it improves isolation or reduces noise, but it is not required for heterogeneous model routing. Pass broader history only when the task materially depends on it.

### One writer is a workflow default, not a ban on delegated writes

The baseline optimizes for cognitive parallelism and low coordination cost. A bounded worker may become the sole writer for a task, and multiple substantial implementations should move to separate worktrees rather than sharing one checkout.

## Preflight checklist

Before adopting the template:

1. Confirm the installed Codex version supports project custom agents and current multi-agent behavior.
2. Confirm `gpt-5.6-terra` and `gpt-5.6-sol` are available to the current account/client, or replace them with available equivalents.
3. Confirm the repository is trusted so project-scoped `.codex/` configuration loads.
4. Confirm `repo_explorer` and `reviewer` are discoverable.
5. Spawn `repo_explorer` on a disposable task and confirm it behaves read-only under current parent permissions.
6. Spawn `reviewer` against a non-trivial diff and confirm it reports findings without patching them.
7. Run a normal task end-to-end and confirm root-first implementation and validation work as expected.
8. Run one bounded implementation with the built-in worker and confirm the root does not concurrently edit the same checkout.
9. Run one noisy verification/log-analysis task through a side agent and confirm the returned summary is useful enough to justify the extra agent overhead.

## Upgrade policy

When Codex multi-agent behavior changes:

1. Prefer current official documentation and current stable release behavior over older examples.
2. Re-check configuration keys, built-in roles, and model IDs before changing the template.
3. Keep capability facts separate from workflow opinions.
4. Promote an on-demand role to a permanent custom profile only after repeated use demonstrates a stable advantage that outweighs coordination and token cost.

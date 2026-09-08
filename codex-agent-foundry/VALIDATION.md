# Validation Notes

This template is intentionally minimal. It keeps only the Codex multi-agent pieces that add a distinct information or review advantage in a normal single-checkout workflow.

## Current Codex capabilities relied on

The template relies on these supported capabilities:

- project-scoped Codex configuration under `.codex/`;
- project custom agents under `.codex/agents/`;
- standalone agent TOML definitions with `name`, `description`, and `developer_instructions`;
- per-agent `model`, `model_reasoning_effort`, and `sandbox_mode` overrides;
- `[agents].max_concurrent_threads_per_session`;
- root-to-subagent delegation with results returned to the root;
- model availability that may differ by account, client, authentication mode, and rollout.

## Ablation decisions

### Kept: `repo_explorer`

Reason: read-heavy investigation is a good isolation boundary. It can search large code surfaces, trace call paths, and return evidence without polluting the root context or modifying the checkout.

### Kept: `reviewer`

Reason: an independent cold review adds a genuinely different signal after implementation. It is intentionally read-only and optimized for material correctness, regressions, security, concurrency/state risks, and meaningful test gaps.

### Removed: `implementer`

Reason: in the default single-checkout workflow, handing implementation from the root to a write-capable subagent adds coordination, context transfer, and permission complexity without an inherent independent-information benefit. The root already owns the plan, architecture, integration, and final answer, so it remains the default writer.

Use separate Git worktrees when true parallel implementation is worth the extra coordination.

### Removed: `verifier`

Reason: tests, lint, type checks, builds, reproduction steps, and final diff inspection are part of the root's completion responsibility. A separate verifier is useful only when validation itself is large enough to justify independent parallel work; it is not necessary in the baseline.

### Removed: forced root/default model routing

Reason: project-level configuration should not unnecessarily override the user's current root model, reasoning effort, or all unspecified subagents. Only the two specialist roles pin models because their routing is part of their specialization.

### Kept: concurrency ceiling of 4

Reason: the baseline may occasionally run multiple independent read-only explorations plus a review, but available thread capacity should never be treated as a spawn target.

## Important caveats

### Sandbox is not an absolute security boundary

Role-level `sandbox_mode = "read-only"` is a useful default, but parent runtime permissions can affect spawned agents. Do not treat the agent TOML as a hard security boundary.

### Delegation depth is behavioral

The template intentionally does not rely on legacy V1-only depth controls. `AGENTS.md` asks the root to use one-level fan-out/fan-in by default and asks subagents not to spawn additional agents.

### Context inheritance is a strategy decision

Fresh or minimal task context is preferred for independent exploration and cold review when practical, but it is not required for heterogeneous model routing. Pass broader history only when the task materially depends on it.

### One writer is a workflow default

The baseline optimizes for cognitive parallelism, not concurrent source editing. For substantial independent implementations, use separate Git worktrees or independent worktree chats.

## Preflight checklist

Before adopting the template:

1. Confirm the installed Codex version supports project custom agents.
2. Confirm `gpt-5.6-terra` and `gpt-5.6-sol` are available to the current account/client, or replace them with available equivalents.
3. Confirm the repository is trusted so project-scoped `.codex/` configuration loads.
4. Confirm `repo_explorer` and `reviewer` are discoverable.
5. Spawn `repo_explorer` on a disposable task and confirm it behaves read-only under current parent permissions.
6. Spawn `reviewer` against a non-trivial diff and confirm it reports findings without patching them.
7. Run a normal task end-to-end and confirm the root remains the only writer, performs verification, and inspects the final diff.

## Upgrade policy

When Codex multi-agent behavior changes:

1. Prefer current official documentation and current stable release behavior over older examples.
2. Re-check configuration keys and model IDs before changing the template.
3. Keep capability facts separate from workflow opinions.
4. Re-add a removed role only when it demonstrates a distinct benefit that outweighs added coordination and token cost.

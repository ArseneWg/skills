# Validation Notes

Validated against current Codex documentation and the Codex CLI 0.153.4 behavior discussed during design.

## Current Codex capabilities relied on

The template relies on these supported capabilities:

- Project-scoped Codex configuration under `.codex/`.
- Custom project agents under `.codex/agents/`.
- Standalone agent TOML definitions with `name`, `description`, and `developer_instructions`.
- Per-agent `model` and `model_reasoning_effort` overrides.
- Per-agent `sandbox_mode` values including `read-only` and `workspace-write`.
- `[agents]` configuration including:
  - `enabled`;
  - `max_concurrent_threads_per_session`;
  - `default_subagent_model`;
  - `default_subagent_reasoning_effort`.
- Multi-agent workflows in which the root can delegate bounded work and later collect results.
- Model availability that can differ by account, client, authentication mode, and rollout.

## Deliberate policy choices

These are workflow decisions, not Codex hard requirements:

- Root uses `gpt-5.6-sol` at `medium` reasoning by default.
- Explorer uses Terra/medium.
- Implementer uses Terra/high.
- Reviewer uses Sol/high.
- Verifier uses Luna/medium.
- Maximum concurrent agent threads is set to 4 as a conservative ceiling.
- One source-code writer per checkout is the default.
- Read-only exploration happens before implementation when the affected area is unclear.
- Reviewer and verifier are independent of the implementer and may run in parallel after implementation.
- Delegation defaults to one level deep.
- Fresh/minimal task context is preferred for independent exploration, verification, and review.
- Mission cards are required for delegated work.

## Important caveats

### Sandbox is not an absolute security boundary

Role-level `sandbox_mode` is a useful default, but spawned agents are still affected by the parent session's effective runtime permissions. Do not rely on a role TOML alone as a security boundary, especially when parent permissions have been relaxed.

### No V1-only depth control

This template intentionally does not set `max_depth`. Depth control is expressed in `AGENTS.md` because legacy V1 depth settings should not be treated as a reliable V2 orchestration guard.

### Context inheritance is a strategy decision

Current V2 behavior can combine inherited conversation history with model/reasoning/role overrides. This template therefore does not claim that fresh context is required for heterogeneous models. Minimal context is recommended to reduce cost, stale-instruction leakage, and unnecessary context pollution.

### Verifier has workspace-write

Tests, compilers, linters, and build systems may write caches, coverage data, generated intermediates, or other artifacts. The verifier therefore uses `workspace-write`, while its behavioral instructions prohibit intentional source changes and require repository-status checks before and after validation.

### Worktrees for real write parallelism

If multiple agents must implement substantial changes concurrently, separate Git worktrees or independent worktree chats are preferred. The single-checkout workflow is optimized for cognitive parallelism, not uncontrolled write parallelism.

## Preflight checklist

Before adopting the template in a project:

1. Confirm the installed Codex version is current enough for project custom agents.
2. Confirm the model IDs in `.codex/config.toml` and agent TOMLs are available to the current account/client.
3. Confirm the repository is trusted so project-scoped Codex configuration is loaded.
4. Confirm all four custom agents are discoverable.
5. Spawn `repo_explorer` and verify it behaves as read-only under the current parent permissions.
6. Spawn `implementer` on a disposable branch and verify it can edit the workspace.
7. Spawn `verifier` and confirm relevant test/build tooling can run without intentional source edits.
8. Spawn `reviewer` and confirm it returns findings without patching them.
9. Confirm concurrent-thread ceiling behavior is acceptable for the machine and account limits.
10. Use a non-critical task first and inspect the complete diff and agent reports before broad adoption.

## Upgrade policy

When Codex changes agent configuration or multi-agent semantics:

1. Prefer current official documentation and current stable release behavior over older examples.
2. Re-check configuration keys before changing the template.
3. Keep capability facts separate from workflow opinions.
4. Avoid preserving compatibility workarounds after the underlying behavior has changed.

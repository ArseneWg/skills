# Codex Agent Foundry

A minimal Codex multi-agent baseline: the root remains the only default writer, while two read-only specialists handle exploration and independent review.

## Architecture

```text
                 Root
      plan + implement + verify
            /          \
           /            \
 repo_explorer        reviewer
 Terra / medium      Sol / high
   read-only          read-only
           \            /
            \          /
              Root
        final diff + answer
```

## Why only two subagents

The ablation keeps only roles that add a distinct capability:

- `repo_explorer` removes noisy, read-heavy investigation from the root context.
- `reviewer` provides an independent cold pass after implementation.

The root keeps implementation and verification because splitting those into separate agents adds coordination and token overhead without creating a clear independent information advantage in the default single-checkout workflow.

## Files

```text
codex-agent-foundry/
├── README.md
├── AGENTS.md
├── VALIDATION.md
└── .codex/
    ├── config.toml
    └── agents/
        ├── repo_explorer.toml
        └── reviewer.toml
```

## Install

Copy the template into a repository:

```bash
cp codex-agent-foundry/AGENTS.md /path/to/repo/AGENTS.md
mkdir -p /path/to/repo/.codex/agents
cp codex-agent-foundry/.codex/config.toml /path/to/repo/.codex/config.toml
cp codex-agent-foundry/.codex/agents/*.toml /path/to/repo/.codex/agents/
```

If the target repository already has `AGENTS.md`, merge the orchestration policy instead of replacing project-specific rules.

## Default workflow

```text
1. Root understands the task and acceptance criteria.
2. If the affected area is unclear, delegate bounded read-only exploration.
3. Root implements the smallest defensible change.
4. Root runs targeted verification.
5. For non-trivial changes, delegate an independent review.
6. Root reconciles findings, re-verifies if needed, inspects the final diff, and answers.
```

For substantial parallel implementation, use separate Git worktrees rather than multiple writers in one checkout.

## Model routing

| Role | Model | Effort | Purpose |
| --- | --- | --- | --- |
| Root | current session model | current session effort | Plan, implement, verify, integrate |
| Repo Explorer | `gpt-5.6-terra` | `medium` | Read-heavy codebase exploration |
| Reviewer | `gpt-5.6-sol` | `high` | Independent correctness/regression review |

The project config intentionally does not force the root model or a global default subagent model. Model availability can differ by account, rollout, authentication mode, and client.

## Operational boundaries

- Read-only agent sandbox settings are defaults, not absolute security boundaries; parent runtime permissions still matter.
- Delegation is one level deep by policy, not by legacy V1-only depth configuration.
- `max_concurrent_threads_per_session = 4` is a ceiling, not a target.
- Tests, builds, diffs, source, and documentation are evidence; agent agreement is not.

See [VALIDATION.md](./VALIDATION.md) for the ablation rationale and capability/policy boundary.

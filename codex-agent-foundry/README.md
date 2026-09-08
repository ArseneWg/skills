# Codex Agent Foundry

A conservative multi-agent baseline for Codex projects: strong root ownership, read-first delegation, a single source-code writer per checkout, independent review, and evidence-backed verification.

## Architecture

```text
                         Root
                  GPT-5.6 Sol / medium
                         │
             owns plan / decisions / merge
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
 Repo Explorer       Implementer        Reviewer
 Terra / medium      Terra / high       Sol / high
 read-only           workspace-write    read-only
        │                │                 │
        │                ▼                 │
        │             Verifier             │
        │          Luna / medium            │
        │         workspace-write           │
        │                │                 │
        └────────────────┴─────────────────┘
                         │
                         ▼
                       Root
               inspect diff + final decision
```

## Design rules

- Root owns requirements, decomposition, architecture, integration, final verification, and the final answer.
- Prefer subagents for exploration, research, review, and verification.
- Keep one source-code writer per checkout by default.
- Run reviewer and verifier after implementation; they may run in parallel when safe.
- Keep delegation one level deep unless the root explicitly decides otherwise.
- Give each subagent a bounded mission contract instead of a vague instruction.
- Treat tests, builds, diffs, source, and documentation as evidence; agent agreement is not evidence.
- Use separate Git worktrees for substantial parallel implementation.

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
        ├── implementer.toml
        ├── reviewer.toml
        └── verifier.toml
```

## Install into a repository

Copy the template files into the target repository root:

```bash
cp codex-agent-foundry/AGENTS.md /path/to/repo/AGENTS.md
mkdir -p /path/to/repo/.codex/agents
cp codex-agent-foundry/.codex/config.toml /path/to/repo/.codex/config.toml
cp codex-agent-foundry/.codex/agents/*.toml /path/to/repo/.codex/agents/
```

If the target repository already has an `AGENTS.md`, merge the `Subagent orchestration policy` section instead of replacing existing project rules.

## Recommended invocation

```text
Implement this task according to the repository AGENTS.md subagent orchestration policy.
Investigate first, preserve a single writer in this checkout, then independently review and verify the result.
Do not recursively delegate unless the root explicitly determines it is necessary.
```

For a complex bug:

```text
Diagnose and fix this issue.
Use repo_explorer for independent evidence gathering before implementation.
Only hand the bounded change to implementer after the root has a defensible plan.
After implementation, run verifier and reviewer independently, then let the root inspect the diff and reconcile findings.
```

## Model routing

The checked-in routing is a baseline, not a permanent rule:

| Role | Model | Effort | Purpose |
| --- | --- | --- | --- |
| Root | `gpt-5.6-sol` | `medium` | Planning, architecture, synthesis, final decision |
| Repo Explorer | `gpt-5.6-terra` | `medium` | Read-heavy codebase exploration |
| Implementer | `gpt-5.6-terra` | `high` | Bounded implementation |
| Reviewer | `gpt-5.6-sol` | `high` | Independent correctness/regression review |
| Verifier | `gpt-5.6-luna` | `medium` | Focused tests, lint, type checks, builds, repro steps |

Available models can differ by account, rollout, authentication mode, and client. Confirm your actual model availability with Codex before relying on these exact IDs.

## Operational boundaries

- `sandbox_mode = "read-only"` is a safe default for explorer/reviewer roles, but it is not an absolute security boundary. Parent runtime permission overrides can affect spawned agents.
- The verifier uses `workspace-write` because test/build tooling may write caches or artifacts; its instructions forbid intentional source edits.
- This template intentionally does not set legacy V1-only depth controls. Delegation depth is enforced behaviorally in `AGENTS.md`.
- The concurrency value is a ceiling, not a target. Do not spawn workers just because capacity exists.

See [VALIDATION.md](./VALIDATION.md) for which parts are current Codex capabilities versus opinionated workflow choices.
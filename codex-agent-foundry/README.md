# Codex Agent Foundry

A minimal adaptive Codex multi-agent baseline: keep two stable read-only specialists, and delegate write or verification work only when the task has a clear boundary and a real benefit from isolation or parallelism.

## Architecture

```text
                    Root
         plan + default write + integrate
                  /        \
                 /          \
        repo_explorer      reviewer
         Terra/medium      Sol/high
          read-only        read-only
                 \          /
                  \        /
                    Root
              final validation

Optional, on demand only:
- built-in worker for bounded implementation;
- temporary side agent for noisy tests, CI/log analysis, triage, or repetitive checks;
- narrow research agent when supporting material would pollute the root context.
```

## Design

The baseline keeps only two persistent custom profiles because they consistently add a distinct benefit:

- `repo_explorer` isolates read-heavy codebase investigation.
- `reviewer` provides an independent cold review after material changes.

Everything else is routed adaptively rather than encoded as a permanent role.

### Default path

```text
1. Root understands the task and acceptance criteria.
2. If the affected area is unclear, use repo_explorer.
3. Root implements the change by default.
4. Root runs focused validation by default.
5. For material changes, use reviewer for a cold review.
6. Root reconciles findings, inspects the final diff, and completes the task.
```

### Delegate implementation only when bounded

A built-in `worker` may own an implementation when all of these are clear before it starts:

- scope and files/ownership boundary;
- intended behavior;
- constraints;
- acceptance criteria;
- validation expected.

Keep one source-code writer per checkout at a time. For substantial parallel implementation, use separate Git worktrees or independent worktree chats.

### Delegate verification only when it is worth isolating

The root should normally run targeted tests, lint, type checks, builds, and reproduction steps directly. Delegate verification when it becomes independently useful or noisy, for example:

- large test suites;
- CI or compiler log analysis;
- flaky-test triage;
- repetitive matrix checks;
- large diagnostic output that would pollute root context.

The side agent should return concise evidence; the root still owns the final validation judgment.

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

```bash
cp codex-agent-foundry/AGENTS.md /path/to/repo/AGENTS.md
mkdir -p /path/to/repo/.codex/agents
cp codex-agent-foundry/.codex/config.toml /path/to/repo/.codex/config.toml
cp codex-agent-foundry/.codex/agents/*.toml /path/to/repo/.codex/agents/
```

If the target repository already has `AGENTS.md`, merge this orchestration policy instead of replacing project-specific rules.

## Model routing

| Role | Model | Effort | Purpose |
| --- | --- | --- | --- |
| Root | current session model | current session effort | Plan, default implementation, integration, final validation |
| Repo Explorer | `gpt-5.6-terra` | `medium` | Read-heavy codebase exploration |
| Reviewer | `gpt-5.6-sol` | `high` | Independent correctness/regression review |
| On-demand worker/tester | inherit or choose per task | task-dependent | Only when bounded delegation has material benefit |

The project config intentionally does not force the root model or a global default subagent model. Model availability can differ by account, rollout, authentication mode, and client.

## Operational boundaries

- Prefer read-heavy delegation; write-heavy delegation is conditional, not forbidden.
- Keep one writer per checkout; use worktrees for substantial parallel writes.
- Default to one-level fan-out/fan-in and minimal useful agent count.
- Read-only sandbox settings are defaults, not absolute security boundaries; parent runtime permissions still matter.
- `max_concurrent_threads_per_session = 4` is a ceiling, not a spawn target.
- Tests, builds, diffs, source, logs, and documentation are evidence; agent agreement is not.

See [VALIDATION.md](./VALIDATION.md) for the capability/policy boundary and the ablation rationale.

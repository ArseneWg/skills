# Practical Codex Skills

This repository is a small, shareable collection of custom Codex skills built from real engineering workflows. Each skill is meant to be dropped into `~/.codex/skills` and used directly, with references and helper scripts included only where they materially improve repeatability.

## Table Of Contents

- [Featured Skills](#featured-skills)
- [Detailed Skill Usage](#detailed-skill-usage)
  - [`agent-memory-maintainer`](#agent-memory-maintainer)
  - [`diagnosing-bugs-v2`](#diagnosing-bugs-v2)
  - [`minimal-sufficient-change`](#minimal-sufficient-change)
  - [`rk-gerrit`](#rk-gerrit)
  - [`pptx`](#pptx)
  - [`rk-redmine-analysis`](#rk-redmine-analysis)
  - [`slides`](#slides)
  - [`smux`](#smux)
- [Install](#install)
- [Example Prompts](#example-prompts)
- [Why This Repo Exists](#why-this-repo-exists)
- [Contributor Notes](#contributor-notes)

## Featured Skills

| Skill | What it solves | Notable details |
| --- | --- | --- |
| `agent-memory-maintainer` | Maintain compact repo-local `agent_memory/` records for future agents. | Keeps current context, long-term knowledge, commands, cases, and mature playbooks in a narrow V2 layout. |
| `diagnosing-bugs-v2` | Diagnose and fix bugs, regressions, failing tests, slowdowns, and intermittent failures. | Enforces a red/green diagnostic loop, evidence-backed hypotheses, cleanup, and final delivery gates. |
| `minimal-sufficient-change` | Keep implementation, repair, refactor, and review work scoped to the smallest sufficient semantic change. | Blocks speculative abstractions while preserving correctness, safety, readability, and verification. |
| `pptx` | Read, inspect, create, edit, split, merge, and repair `.pptx` files. | Includes Office XML helpers and PowerPoint-specific editing workflows. |
| `rk-gerrit` | Work against Rockchip internal Gerrit for login checks, connectivity tests, change lookup, review signal triage, and blocker analysis. | Keeps the key path local-only and documents the exact review and submit signals to inspect. |
| `rk-redmine-analysis` | Fetch and analyze Rockchip Redmine issues, attachments, logs, screenshots, and related repository code. | Produces evidence-backed issue analysis and reply drafts. |
| `slides` | Build and validate editable PowerPoint decks with PptxGenJS and rendering checks. | Bundles layout helpers plus render, montage, overflow, and font validation scripts. |
| `smux` | Control tmux panes and coordinate with other agents through tmux-bridge. | Enforces read-before-act and avoids polling other agent panes. |

## Detailed Skill Usage

This section explains what each checked-in custom skill outside `.system/` is for, when to use it, and what workflow it enforces.

### `agent-memory-maintainer`

Use this skill to maintain `agent_memory/`, a compact repo-local memory system for future agents. It is for durable engineering context, not chat archives.

Use it when:

- The user asks to create, update, read, route, extract, consolidate, or refresh `agent_memory/`.
- A repository needs current context, long-term knowledge, commands, cases, or mature playbooks preserved for later agents.
- Old note systems need to be migrated into the V2 `agent_memory/` layout.
- Existing memory needs to be checked before a task that depends on workspace history.

Normal workflow:

1. Read repo instructions and `agent_memory/README.md`.
2. Use `agent_memory/INDEX.md` to select the narrowest relevant scope.
3. Read context, knowledge, playbooks, commands, and cases in that scope as needed.
4. Extract only future-useful facts from verified artifacts.
5. Classify candidates as context, knowledge, command, case, or playbook.
6. Consolidate against existing records before writing.
7. Store the minimum durable record in the narrowest correct location.

Important safety rules:

- Only target `agent_memory/`; do not recreate legacy `module_notes/` unless explicitly requested.
- Do not create empty optional files.
- Do not copy raw chat logs or append chronology; distill verified facts, commands, cases, and handoff state.
- Ask before creating a new scope when module or function ownership is unclear.

### `diagnosing-bugs-v2`

Use this skill for bug diagnosis and repair: regressions, failing tests, crashes, slowdowns, intermittent failures, and user-reported bad behavior. The checked-in install path is `diagnosing-bugs`; the skill registers as `diagnosing-bugs-v2`.

Use it when:

- The user asks to diagnose, debug, find root cause, or investigate a failure.
- A test, build, command, board run, or workflow is failing.
- A performance regression or flaky behavior needs evidence-backed isolation.
- A previous attempted fix lacks a clear red/green loop.

Normal workflow:

1. Establish the shortest diagnostic loop that can turn red for the exact symptom.
2. Reproduce the issue and shrink variables until the remaining conditions matter.
3. Read enough relevant context to form falsifiable hypotheses.
4. Test one hypothesis at a time with explicit observations or temporary instrumentation.
5. Fix only after the root cause is verified.
6. Re-run the original loop, check known-good paths, clean temporary changes, and report remaining risk.

Important safety rules:

- Do not claim root cause without a diagnostic loop and evidence.
- Do not stack behavior-changing experiments; revert failed probes before trying another.
- Temporary workarounds are not final fixes.
- Final delivery must include verification, known-good coverage, cleanup status, uncovered areas, and residual risk.

### `minimal-sufficient-change`

Use this skill to keep code changes, fixes, refactors, and reviews focused on the minimum sufficient semantic change for the current request.

Use it when:

- Implementing or modifying functionality.
- Fixing a defect without expanding scope.
- Refactoring code where behavior must stay controlled.
- Reviewing whether a diff adds unnecessary abstraction, files, APIs, dependencies, or configuration.

Normal workflow:

1. State the intended observable behavior and completion criteria.
2. Read the target code, callers, tests, project rules, helpers, and existing dependencies.
3. Prefer no new code, existing project APIs, standard capabilities, then local edits before adding new abstractions.
4. Put the change at the correct ownership boundary.
5. Review the final diff for unnecessary concepts, files, public API, formatting churn, and unrelated cleanup.
6. Validate in proportion to the risk.

Important safety rules:

- Do not remove safety, validation, error handling, data integrity, concurrency protection, idempotency, or trust-boundary checks to reduce code.
- Do not add speculative features, wrappers, factories, registries, public API, TODO scaffolding, or unused configuration.
- Do not treat fewer lines as proof of correctness.

### `rk-gerrit`

Use this skill for Rockchip internal Gerrit work on `10.10.10.29:29418`. It is for checking login and SSH key setup, querying changes, reading patch set metadata, inspecting changed files, reviewing approvals and comments, and deciding what still blocks submission.

Use it when:

- The user asks whether Gerrit login works.
- SSH key permissions or connectivity need to be fixed.
- A numeric change id or full Change-Id needs to be inspected.
- Review status, labels, approvals, CI, or unresolved comments need triage.
- A submission blocker must be explained with exact Gerrit evidence.

Normal workflow:

1. Verify the local config and key path.
2. Ensure the private key is not printed and has safe permissions.
3. Test SSH connectivity to `10.10.10.29:29418`.
4. Query the requested change through the bundled scripts.
5. Read patch set metadata, changed files, labels, reviewers, comments, and CI signals.
6. Separate facts from inference: quote or summarize Gerrit evidence first, then state what action is still required.
7. If network or credentials are missing, report the exact blocker and the next concrete setup step.

Important safety rules:

- Never print private key contents.
- Treat leaked key output as a security incident and recommend rotation.
- Keep the real key local under `config/robot_verifier` with mode `600`.
- Do not copy private keys into commits, logs, notes, or final answers.
- If SSH fails due to key permissions, fix permissions before retrying.

### `pptx`

Use this skill any time a `.pptx` file is involved, whether the deck is input, output, or both. It covers reading slide content, extracting text, inspecting visuals, editing existing decks, creating new decks, working with templates, combining or splitting decks, and manipulating raw Office XML when higher-level tools are not enough.

Use it when:

- The user mentions a `.pptx` file, deck, slides, presentation, template, speaker notes, comments, or PowerPoint.
- A deck needs to be read and summarized.
- Existing slides need content edits while preserving PowerPoint compatibility.
- A deck needs to be created from scratch or from a template.
- Slide XML, layouts, relationships, or media assets need direct inspection.
- A deck needs to be split, merged, cleaned, packed, unpacked, or validated.

Normal workflow:

1. Decide whether the task is inspection, editing, creation, cleanup, or repair.
2. For text extraction, start with `python -m markitdown presentation.pptx`.
3. For visual inspection, render thumbnails with the bundled thumbnail script.
4. For structural edits, unpack the deck, modify XML or slide assets, clean, and repack.
5. Use the bundled Office helpers for merging runs, simplifying redlines, packing, unpacking, and validation.
6. Validate the final `.pptx` opens cleanly and preserves the requested editable structure.

Important safety rules:

- Use this skill whenever `.pptx` is mentioned, even if the user only wants extracted content.
- Keep output PowerPoint-compatible; do not silently flatten editable content unless the task calls for it.
- Inspect the existing template or slide structure before editing.
- Avoid hand-editing binary Office files directly; unpack, edit structured content, then repack.

### `rk-redmine-analysis`

Use this skill for Rockchip Redmine issue work that needs evidence collection and code-backed diagnosis. The expected output is more than an issue summary: it should connect Redmine fields, comments, attachments, logs, screenshots, PDFs, linked files, and repository code into a defensible analysis.

Use it when:

- The user provides a Redmine issue URL or issue id.
- Attachments, logs, PDFs, screenshots, or linked files need to be downloaded and organized.
- A Redmine reply needs technical evidence and clear next steps.
- Symptoms need to be mapped back to repository code, drivers, firmware, configuration, or logs.
- The issue text alone is insufficient and local code can constrain the diagnosis.

Normal workflow:

1. Create a topic-specific workspace under the repository's `redmine/` directory.
2. Fetch the issue and attachments with `scripts/fetch_issue.py`.
3. Read the issue report, raw JSON when available, comments, custom fields, and linked material before diagnosing.
4. Extract useful content from PDFs, archives, images, and large logs.
5. Connect the observed symptoms to relevant repository code or state the limitation if the needed component is missing.
6. Produce a concise analysis with evidence, uncertainty, likely cause, suggested verification, and a Redmine-ready reply when requested.

Important safety rules:

- Prefer `REDMINE_API_KEY` and `REDMINE_BASE_URL` from the environment or existing local credentials.
- Never write API keys into repositories, issue directories, notes, logs, or final answers.
- Keep raw issue artifacts in the issue workspace, not scattered across the repo.
- Do not claim certainty from issue text alone when code or attachments are available but uninspected.

### `slides`

Use this skill to create or edit presentation slide decks as editable `.pptx` files with PptxGenJS. It is for building decks from scratch, recreating slides from references, modifying existing presentations, adding diagrams or charts, and validating layout issues like overflow, bad cropping, or font substitution.

Use it when:

- A new slide deck needs to be authored.
- A deck must be recreated from screenshots, PDFs, sketches, or reference slides.
- Existing slides need layout or content edits while preserving editable PowerPoint objects.
- Charts, diagrams, equations, images, or code blocks need to be generated in a deck.
- The user needs visual validation of a `.pptx` before delivery.

Normal workflow:

1. Determine whether the task is new deck creation, recreation, or editing.
2. Set slide size up front, usually 16:9 unless the source requires another ratio.
3. Copy and use the bundled `pptxgenjs_helpers` instead of reimplementing layout helpers.
4. Build the deck in JavaScript with explicit theme fonts and stable spacing.
5. Render slides to PNG with `render_slides.py`.
6. Inspect rendered images, run overflow checks with `slides_test.py` when needed, and fix layout issues.
7. Deliver the `.pptx`, source `.js`, and any required generated assets.

Important safety rules:

- Do not use `python-pptx` for deck generation unless the task is inspection-only.
- Keep output editable where practical.
- Do not rely on PowerPoint defaults for typography.
- Use helper functions for image sizing, text measurement, equations, and code styling.
- Validate with rendered slides before considering a deck finished.

### `smux`

Use this skill to control tmux panes and communicate with other AI agents or shell processes through tmux. It combines high-level `tmux-bridge` workflows with raw tmux commands for cases where direct pane control is needed.

Use it when:

- The user mentions tmux panes, sessions, windows, or cross-pane communication.
- Messages need to be sent to another agent running in a tmux pane.
- A pane needs to be read before interaction.
- A long-running process in another pane needs command input or inspection.
- Agent-to-agent coordination must happen without copying context manually.

Normal workflow:

1. Use `tmux-bridge` for cross-pane communication.
2. Read a target pane before typing or sending keys; the tool enforces read-before-act.
3. Type the message, verify it landed when necessary, then press Enter.
4. Do not poll another agent pane for a response; responses appear back in the current pane.
5. Use raw tmux only for low-level session, window, pane, or process control that `tmux-bridge` does not cover.

Important safety rules:

- Do not send input to a pane before reading it.
- Do not sleep, poll, or repeatedly read another agent pane waiting for a reply.
- Be explicit about target pane names and whether the target is an agent or a plain shell/process.
- After interacting with a pane, read it again before the next action.

## Install

Install all public custom skills from this repository with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo xiaoyao888888/skills \
  --path agent-memory-maintainer diagnosing-bugs minimal-sufficient-change pptx rk-gerrit rk-redmine-analysis slides smux
```

After installation, restart Codex so the new skills are discovered.

## Example Prompts

```text
Use $agent-memory-maintainer to update this repository's agent_memory with the verified commands and current handoff.

Use $diagnosing-bugs-v2 to investigate this failing test and prove the root cause before patching.

Use $minimal-sufficient-change to review this implementation and remove unnecessary abstraction without weakening behavior.

Use $pptx to extract text and thumbnails from this presentation, then summarize slide-level issues.

Use $rk-gerrit to inspect this Gerrit change and tell me exactly what is still blocking submission.

Use $rk-redmine-analysis to fetch this Redmine issue, archive the attachments, inspect the logs, and draft an evidence-backed reply.

Use $slides to build an editable PPTX deck from this outline and validate the rendered slides.

Use $smux to read the target tmux pane and send this message to the other agent.
```

## Why This Repo Exists

- These skills are based on workflows that are easy to get mostly right and expensive to get slightly wrong.
- Each skill is intentionally narrow: one operational problem, one set of references, one place to start.
- The repository is meant to be understandable by other engineers browsing it for the first time, not just by the original author.

## Contributor Notes

- Read the target skill's `SKILL.md` first; the skills are designed to be self-contained.
- Keep repo-wide engineering and collaboration rules in [AGENTS.md](./AGENTS.md).
- Treat local-only secrets as local-only: document them clearly and keep them out of Git history.

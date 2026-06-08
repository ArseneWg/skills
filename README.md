# Practical Codex Skills

This repository is a small, shareable collection of custom Codex skills built from real engineering workflows. Each skill is meant to be dropped into `~/.codex/skills` and used directly, with references and helper scripts included only where they materially improve repeatability.

## Table Of Contents

- [Featured Skills](#featured-skills)
- [Detailed Skill Usage](#detailed-skill-usage)
  - [`git-repo-publish-sanitize`](#git-repo-publish-sanitize)
  - [`module-notes-maintainer`](#module-notes-maintainer)
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
| `git-repo-publish-sanitize` | Initialize a repo, publish it to GitHub, remove leaked secrets from history, and delete/recreate remotes when cleanup must reach GitHub. | Includes a bundled Linux `x86_64` `gh` fallback, in-place sanitization guidance, and concrete notes on sandbox, auth, and scope pitfalls. |
| `module-notes-maintainer` | Turn chat history, logs, diffs, and verified repo state into durable notes without mixing repo rules, runbooks, handover notes, and temporary debugging residue. | Useful when a codebase is growing and operational knowledge keeps getting lost in chat. |
| `pptx` | Read, inspect, create, edit, split, merge, and repair `.pptx` files. | Includes Office XML helpers and PowerPoint-specific editing workflows. |
| `rk-gerrit` | Work against Rockchip internal Gerrit for login checks, connectivity tests, change lookup, review signal triage, and blocker analysis. | Keeps the key path local-only and documents the exact review and submit signals to inspect. |
| `rk-redmine-analysis` | Fetch and analyze Rockchip Redmine issues, attachments, logs, screenshots, and related repository code. | Produces evidence-backed issue analysis and reply drafts. |
| `slides` | Build and validate editable PowerPoint decks with PptxGenJS and rendering checks. | Bundles layout helpers plus render, montage, overflow, and font validation scripts. |
| `smux` | Control tmux panes and coordinate with other agents through tmux-bridge. | Enforces read-before-act and avoids polling other agent panes. |

## Detailed Skill Usage

This section explains what each checked-in custom skill outside `.system/` is for, when to use it, and what workflow it enforces.

### `git-repo-publish-sanitize`

Use this skill for local Git and GitHub repository lifecycle work where small mistakes are expensive: initializing a repository, preparing a focused first commit, publishing to GitHub, removing accidentally tracked secrets, or deleting and recreating a remote after sensitive material has already been pushed.

Use it when:

- A directory needs to become a Git repository.
- A local repository needs a clean initial commit and GitHub remote.
- The user wants to publish the current directory without copying it through `/tmp`.
- A secret, credential, token, key, local config, or generated file was accidentally tracked.
- A remote GitHub repository must be deleted and recreated because secret history was already pushed.
- Visibility or remote setup needs to be verified instead of guessed.

Normal workflow:

1. Inspect the directory or existing repo with `git status -sb`.
2. Identify the requested scope: local init, GitHub publish, docs, ignore rules, secret cleanup, visibility, or remote recreation.
3. Keep work in the target repository in place; do not create a sanitized replacement in `/tmp`.
4. Add `.gitignore` before the first commit when local-only files must never be tracked.
5. Stage only intentional files and make focused commits.
6. Prefer authenticated system `gh`; use the bundled `gh` fallback only when needed.
7. If a secret was tracked, remove it from the index and history as required, then verify the remote does not retain the leaked object.
8. If a pushed repository cannot be safely cleaned, delete and recreate the remote only when that is the intended repair.

Important safety rules:

- Never print or commit secrets while diagnosing.
- Treat `.env`, private keys, cookies, tokens, generated credentials, and local machine paths as local-only unless the user explicitly says otherwise.
- Do not use `gh` binaries from `/tmp`.
- Keep the final answer concrete: repo path, branch, commit id, remote URL, visibility, and any cleanup still required.

### `module-notes-maintainer`

Use this skill to maintain repository notes under `module_notes/` so the next operator can continue without reading chat history. It is for preserving durable, verified engineering knowledge: commands that actually worked, board paths, build artifacts, environment facts, user preferences, recurring mistakes, and handoff state.

The core rule is: `module_notes/` is organized by module and function, not by chat session, date, or history phase.

Expected layout:

```text
module_notes/
  README.md
  common/
    00_user_preferences.md
    01_board_access.md
    02_sdk_build_operations.md
    03_notes_maintenance_corrections.md
  <module>/
    <function>/
      README.md
      handover.md
      runbook.md
      corrections.md
```

Hard rules:

- `module_notes/README.md` is the only directory index.
- Do not create `module_notes/<module>/README.md`.
- Do not create `module_notes/common/README.md`.
- Do not create `history/`, `logs/`, pure jump files, or compatibility pointers for old structures.
- A function directory should contain only `README.md`, `handover.md`, `runbook.md`, and `corrections.md`.
- Do not write append-only chat chronology. Distill current conclusions, reusable commands, corrections, and handoff state.

Standard workflow:

1. Read `AGENTS.md`, then `module_notes/README.md`.
2. Identify the target module and function.
3. Reuse an existing function directory if the request matches an existing function.
4. Ask before creating a new function directory when the match is ambiguous.
5. Read the target function `README.md`; then use `handover.md`, `runbook.md`, or `corrections.md` as needed.
6. Record only durable, verified information.
7. At the end of meaningful work, update the function handoff and any reusable commands.
8. For broad cleanup or migration, run the audit script.

File ownership:

- `module_notes/README.md`: module/function router, common-doc list, reading order, and current directory map.
- `module_notes/common/`: cross-module user preferences, board access, ADB/SSH rules, SDK/Buildroot/kernel/rootfs/image commands, shared host facts, and cross-module mistakes.
- `<function>/README.md`: current functional entrypoint with scope, state, and where to start.
- `<function>/handover.md`: current status, verified facts, limitations, open risks, and next actions.
- `<function>/runbook.md`: reusable procedures and exact commands, including cwd, parameters, artifact paths, board paths, and success/failure signals.
- `<function>/corrections.md`: user-reported mistakes, root cause, fix, and future guard.

Scenario guide:

- New module or function: compare the request against existing entries in `module_notes/README.md`; update an existing function when the target is the same, create a new directory only when it is genuinely distinct, and link it from the root README.
- Continue existing work: read the function `README.md`, then `handover.md` for current state, `runbook.md` for commands, and `corrections.md` for known traps.
- Tested command succeeds: write the runnable command to `runbook.md` with cwd, env vars, binary path, board destination path, log path, and success signal.
- User points out an error: write it to `corrections.md`; if the mistake applies across modules, write it under `common/`.
- Session or phase ends: update `handover.md` so a new operator can resume from the current state without the chat.
- Common fact appears: move it into `common/` instead of copying it into every function.
- Old notes are migrated or compressed: inventory old command fences, shell snippets, paths, artifacts, board destinations, success/failure signals, and corrections before deleting source files.
- No command can be recovered: state that gap explicitly in the target `handover.md` or `runbook.md`; do not leave an empty template that looks complete.
- Old board IP appears: normalize function runbooks to `$BOARD` and keep the current value only in `common/01_board_access.md`.
- Secret-like value appears: replace passwords, PSKs, tokens, private keys, cookies, and partial secret values with placeholders such as `<wifi-psk>` and document only lookup method or owner.
- Multi-host workflow appears: keep host, board, CI, service, Windows, and PC commands separate, each with its own cwd, paths, permissions, and success signal.

Migration audit:

```bash
python3 tools/skills/module-notes-maintainer/scripts/audit_module_notes.py module_notes
```

The audit checks for:

- Only one root index.
- No module-level README, common README, `history/`, or `logs/`.
- No stale sample board serials.
- No sample plaintext PSK.
- No placeholder wording such as `TODO` or "待补".
- Empty runbooks must explicitly explain why no fixed or recoverable command exists.

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

If you already have Codex and the built-in `skill-installer`, install the Git skill from this repo with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo xiaoyao888888/skills \
  --path git-repo-publish-sanitize
```

Install all public custom skills from this repository with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo xiaoyao888888/skills \
  --path git-repo-publish-sanitize module-notes-maintainer pptx rk-gerrit rk-redmine-analysis slides smux
```

After installation, restart Codex so the new skills are discovered.

## Example Prompts

```text
Use $git-repo-publish-sanitize to initialize this directory, audit secrets, and publish a clean GitHub repository.

Use $module-notes-maintainer to summarize verified progress on this module and move the durable facts into the right notes.

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

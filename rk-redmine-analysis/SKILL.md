---
name: rk-redmine-analysis
description: "Use when a user asks to inspect a Rockchip Redmine issue, download linked files or images, archive materials under a topic-specific redmine directory, analyze attachments or logs, connect symptoms to repository code, or draft an evidence-backed Redmine reply."
---

# RK Redmine Analysis

## Overview

Use this skill for Redmine issue work that needs local evidence collection and code-backed diagnosis. The expected output is not just an issue summary; it should connect Redmine facts, attachments, logs, images, and repository code into a defensible analysis.

Do not make conclusions from the issue text alone when relevant source code is available. If an important driver, vendor component, binary, or external repository is missing, state that limitation and analyze the available host, kernel, userspace, or configuration code that can still constrain the problem.

## Quick Start

For a Redmine URL or numeric issue id, fetch and organize the issue materials first:

```bash
python3 ~/.codex/skills/rk-redmine-analysis/scripts/fetch_issue.py <issue-url-or-id> --dir redmine
```

The helper wraps the local rk-redmine retrieval scripts when they are available, downloads attachments, renames the issue directory using the issue subject, saves raw API JSON when credentials are available, and extracts PDF text when local tools support it.

## Credentials

- Prefer `REDMINE_API_KEY` and `REDMINE_BASE_URL` from the environment, or the existing rk-redmine user credentials at `~/.rk-skills/rk-redmine/credentials.json`.
- Never write API keys into the repository, issue directories, notes, logs, or final answers.
- If credentials are missing, ask the user for a safe way to provide them or point them to the existing rk-redmine configuration flow.
- Honor existing proxy environment variables when network access fails.

## Workflow

1. Create the issue workspace under the current repository's `redmine/` directory.
   Use a topic-specific path such as `redmine/<issue_id>_<sanitized_subject>/`. Keep raw JSON, generated reports, attachments, extracted text, screenshots, and analysis in that directory.

2. Read the Redmine data before diagnosing.
   Inspect `issue_report.md`, raw JSON, comments or journals, custom fields, attachments, embedded images, logs, PDFs, and linked files. Preserve uncertainty when fields conflict or timestamps matter.

3. Extract attachment content.
   Convert PDFs to text, inspect images when they carry technical evidence, decompress archives only inside the issue workspace, and summarize large logs with exact filenames and relevant line excerpts or counters.

4. Map the issue to code.
   Identify the affected subsystem, then read the relevant repository code and any applicable `module_notes/`. Use `rg` first for searches. Cite concrete files and line numbers for non-trivial claims. Prefer existing platform, kernel, build, and configuration patterns over speculation.

5. Write `analysis.md` in the issue workspace.
   Use `references/analysis-format.md` for the expected structure. The analysis should include saved materials, issue facts, attachment evidence, code evidence, hypotheses, validation steps, and a reply draft when useful.

6. Keep Redmine mutations explicit.
   Draft replies or assignment suggestions locally first. Do not submit a Redmine reply, assign an issue, change a field, or upload material unless the user explicitly confirms the exact action and content.

## Analysis Standard

- Distinguish observed facts, code-derived facts, and hypotheses.
- Treat timing, environment differences, board configuration, kernel config, DTS, firmware, service scripts, and userspace command lines as first-class evidence when they are relevant.
- If two environments behave differently, compare the smallest concrete variables first: hardware path, firmware or driver availability, kernel config, device tree, service startup, command arguments, logs, and measured counters.
- Avoid issue-specific wording in reusable notes or skill updates. The skill is for all Redmine issues, not a single defect.


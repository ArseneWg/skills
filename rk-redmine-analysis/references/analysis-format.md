# Redmine Analysis Format

Use this structure for `analysis.md` in the issue workspace. Keep the content concise, evidence-backed, and specific to the current issue.

## Saved Materials

- Issue URL and issue id.
- Local workspace path.
- Main generated files, raw JSON, attachments, extracted text, screenshots, archives, and any derived logs.

## Issue Summary

- Current status, priority, reporter, assignee, affected product or module, and important timestamps.
- Reported symptom in one or two sentences.
- Environment details from the issue, preserving exact versions, boards, configs, commands, and test conditions when provided.

## Attachment Evidence

- For each relevant attachment, record the filename, type, and technical facts extracted from it.
- For logs, include only the lines or counters needed to support the conclusion.
- For images, describe the visible technical evidence rather than restating that an image exists.
- For PDFs or documents, cite the extracted text file if one was generated.

## Code Evidence

- List the repository paths inspected.
- Cite concrete file and line references for behavior, configuration, init order, device tree bindings, kernel config, service scripts, or command construction.
- Note missing source code or binary-only components explicitly.

## Hypotheses

Order hypotheses by how well they explain the issue evidence.

For each hypothesis:

- Evidence supporting it.
- Evidence against it or unknowns.
- What code path or configuration would make it true.
- The smallest validation step that can confirm or rule it out.

## Environment Comparison

When the issue compares two environments, use a table with these columns:

- Variable
- Environment 1
- Environment 2
- Why it matters
- Evidence source

Prefer concrete differences over broad labels.

## Validation Plan

- Host-side checks.
- Target-side checks.
- Build or config checks.
- Log commands or counters to collect.
- Expected result for each check.

## Redmine Reply Draft

Write a short reply draft only after the evidence is clear enough. The draft should state what was checked, what the current conclusion is, what remains uncertain, and what data or test is needed next.

Do not submit the reply without explicit user confirmation.


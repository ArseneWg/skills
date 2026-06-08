#!/usr/bin/env python3
"""Audit a repository's module_notes tree for the expected notes contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_FUNCTION_FILES = {"README.md", "handover.md", "runbook.md", "corrections.md"}

BANNED_PATTERNS = [
    (re.compile(r"history/"), "history path"),
    (re.compile(r"历史|归档|里程碑"), "archival/changelog wording"),
    (re.compile(r"\bTODO\b|待补|补齐|还缺|待确认"), "placeholder wording"),
    (re.compile(r"172\.16\.15\.(27|209):5555"), "stale sample board serial"),
    (re.compile(r"<old-sample-board>"), "old sample board placeholder"),
    (re.compile(r"1234abcd"), "sample Wi-Fi PSK"),
    (re.compile(r"send\s+--\s+\"xy\\r\""), "hard-coded SSH password send"),
    (re.compile(r"psk=\\?\"(?!<wifi-psk>)[^\"\n]+\\?\""), "non-placeholder Wi-Fi PSK"),
]

ZERO_COMMAND_OK = re.compile(r"没有|缺口|未找到|当前没有固定命令|未验证|不等价于已验证")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("module_notes")
    root = root.resolve()

    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        print(f"ERROR: {root} does not exist", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2

    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts
    )
    dirs = sorted(
        p for p in root.rglob("*")
        if p.is_dir() and ".git" not in p.parts
    )

    if not (root / "README.md").is_file():
        errors.append("missing root README.md")

    for path in dirs:
        if path == root:
            continue
        if path.name in {"history", "logs"}:
            errors.append(f"forbidden directory: {rel(root, path)}")

    for path in files:
        parts = path.relative_to(root).parts

        if path.name == "README.md":
            is_root_readme = len(parts) == 1
            is_function_readme = len(parts) == 3 and parts[0] != "common"
            if not (is_root_readme or is_function_readme):
                errors.append(f"forbidden README location: {rel(root, path)}")

        if len(parts) == 1:
            if parts[0] != "README.md":
                errors.append(f"unexpected root file: {rel(root, path)}")
            continue

        if parts[0] == "common":
            if len(parts) != 2:
                errors.append(f"unexpected nested common file: {rel(root, path)}")
            if path.name == "README.md":
                errors.append(f"common README is not allowed: {rel(root, path)}")
            continue

        if len(parts) == 2:
            errors.append(f"flat module file is not allowed: {rel(root, path)}")
            continue

        if len(parts) == 3:
            if parts[2] not in ALLOWED_FUNCTION_FILES:
                errors.append(f"unexpected function file: {rel(root, path)}")
            continue

        errors.append(f"unexpected nested file: {rel(root, path)}")

    for path in files:
        text = read_text(path)
        for pattern, label in BANNED_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label}: {rel(root, path)}:{line}")

    runbooks = sorted(root.glob("*/*/runbook.md"))
    print(f"files: {len(files)}")
    print("runbook fences:")
    for runbook in runbooks:
        text = read_text(runbook)
        fence_count = len(re.findall(r"^```", text, re.MULTILINE))
        print(f"  {fence_count:4d} {rel(root, runbook)}")
        if fence_count == 0:
            handover = runbook.with_name("handover.md")
            combined = text
            if handover.exists():
                combined += "\n" + read_text(handover)
            if not ZERO_COMMAND_OK.search(combined):
                errors.append(
                    "runbook has no command fences and no explicit current gap: "
                    f"{rel(root, runbook)}"
                )

    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"  WARNING: {warning}")

    if errors:
        print("errors:")
        for error in errors:
            print(f"  ERROR: {error}")
        return 1

    print("module_notes audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

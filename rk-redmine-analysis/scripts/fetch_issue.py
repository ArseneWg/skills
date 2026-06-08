#!/usr/bin/env python3
"""Fetch a Redmine issue into a topic-specific local workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://redmine.rock-chips.com"
DEFAULT_RK_REDMINE_SCRIPTS = Path(
    os.environ.get(
        "RK_REDMINE_SCRIPTS",
        "/home/xy/work/rk-skills/01-knowledge-retrieval/issue-tracker/rk-redmine/scripts",
    )
)


def parse_issue_id(value: str) -> str:
    value = value.strip()
    if value.isdigit():
        return value

    match = re.search(r"/issues/(\d+)", value)
    if match:
        return match.group(1)

    match = re.search(r"(?:^|[?&])issue(?:_id)?=(\d+)", value)
    if match:
        return match.group(1)

    raise SystemExit(f"Unable to parse a Redmine issue id from: {value}")


def run_checked(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def read_report_subject(report_path: Path) -> str:
    if not report_path.exists():
        return "issue"

    with report_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line.startswith("# "):
                continue
            if " - " in line:
                return line.split(" - ", 1)[1].strip() or "issue"
            return re.sub(r"^#\s+", "", line).strip() or "issue"

    return "issue"


def sanitize_topic(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text.strip())
    text = re.sub(r'[\\/:\*\?"<>\|\s]+', "_", text)
    text = re.sub(r"_+", "_", text).strip("._-")
    return text[:80].strip("._-") or "issue"


def choose_target(source_dir: Path, desired_dir: Path) -> Path:
    if source_dir == desired_dir or not desired_dir.exists():
        return desired_dir

    for index in range(2, 100):
        candidate = desired_dir.with_name(f"{desired_dir.name}_{index}")
        if not candidate.exists():
            return candidate

    raise SystemExit(f"Unable to choose an unused target directory for {desired_dir}")


def load_credentials() -> tuple[str | None, str]:
    env_key = os.environ.get("REDMINE_API_KEY")
    if env_key:
        return env_key, os.environ.get("REDMINE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

    credentials_path = Path.home() / ".rk-skills" / "rk-redmine" / "credentials.json"
    if credentials_path.exists():
        with credentials_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        api_key = data.get("api_key")
        base_url = data.get("base_url", DEFAULT_BASE_URL)
        if api_key:
            return api_key, base_url.rstrip("/")

    return None, DEFAULT_BASE_URL


def save_raw_json(issue_id: str, issue_dir: Path) -> None:
    api_key, base_url = load_credentials()
    if not api_key:
        print("No Redmine API key found for raw JSON fetch; skipping raw JSON.")
        return

    url = (
        f"{base_url}/issues/{issue_id}.json"
        "?include=attachments,journals,children,relations,watchers"
    )
    request = urllib.request.Request(url)
    request.add_header("X-Redmine-API-Key", api_key)
    request.add_header("User-Agent", "Codex-Redmine-Analysis/1.0")

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(request, context=context, timeout=60) as response:
            payload = response.read()
        parsed = json.loads(payload.decode("utf-8"))
    except Exception as exc:
        print(f"Raw JSON fetch failed: {exc}")
        return

    raw_path = issue_dir / f"issue_{issue_id}_raw.json"
    with raw_path.open("w", encoding="utf-8") as handle:
        json.dump(parsed, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Saved raw JSON: {raw_path}")


def extract_pdf_text(issue_dir: Path) -> None:
    pdfs = sorted(path for path in issue_dir.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf")
    if not pdfs:
        return

    pdftotext = shutil.which("pdftotext")
    ghostscript = shutil.which("gs")
    if not pdftotext and not ghostscript:
        print("No pdftotext or gs found; skipping PDF text extraction.")
        return

    for pdf in pdfs:
        output = pdf.with_name(f"{pdf.name}.txt")
        if output.exists():
            continue

        if pdftotext:
            cmd = [pdftotext, "-layout", str(pdf), str(output)]
        else:
            cmd = [
                ghostscript,
                "-q",
                "-dNOPAUSE",
                "-dBATCH",
                "-sDEVICE=txtwrite",
                f"-sOutputFile={output}",
                str(pdf),
            ]

        result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0 and output.exists():
            print(f"Extracted PDF text: {output}")
        else:
            try:
                output.unlink()
            except FileNotFoundError:
                pass
            print(f"PDF text extraction failed for: {pdf}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("issue", help="Redmine issue id or URL")
    parser.add_argument("--dir", default="redmine", help="Base directory for issue workspaces")
    parser.add_argument(
        "--rk-redmine-scripts",
        default=str(DEFAULT_RK_REDMINE_SCRIPTS),
        help="Directory containing get_issue_info.py",
    )
    parser.add_argument("--no-download", action="store_true", help="Do not download attachments")
    parser.add_argument("--no-raw-json", action="store_true", help="Do not save raw API JSON")
    parser.add_argument("--no-pdf-text", action="store_true", help="Do not extract PDF text")
    args = parser.parse_args()

    issue_id = parse_issue_id(args.issue)
    base_dir = Path(args.dir).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    scripts_dir = Path(args.rk_redmine_scripts).expanduser().resolve()
    get_issue_script = scripts_dir / "get_issue_info.py"
    if not get_issue_script.exists():
        raise SystemExit(f"Missing rk-redmine script: {get_issue_script}")

    cmd = [sys.executable, str(get_issue_script), issue_id, "--dir", str(base_dir)]
    if args.no_download:
        cmd.append("--no-download")
    run_checked(cmd)

    source_dir = base_dir / f"redmine_issue_{issue_id}"
    if not source_dir.exists():
        raise SystemExit(f"Expected issue directory was not created: {source_dir}")

    subject = read_report_subject(source_dir / "issue_report.md")
    desired_dir = base_dir / f"{issue_id}_{sanitize_topic(subject)}"
    issue_dir = choose_target(source_dir, desired_dir)
    if source_dir != issue_dir:
        shutil.move(str(source_dir), str(issue_dir))
        print(f"Renamed issue directory: {issue_dir}")

    if not args.no_raw_json:
        save_raw_json(issue_id, issue_dir)
    if not args.no_pdf_text:
        extract_pdf_text(issue_dir)

    print(f"Issue workspace: {issue_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


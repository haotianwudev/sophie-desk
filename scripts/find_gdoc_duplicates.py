#!/usr/bin/env python3
"""Find and report duplicate Google Drive research docs in gdocs/index.json.

Groups document entries by a normalized title (stripping trailing '(1)', '(2)', etc.,
collapsing whitespace, and lowercasing), filters for groups with 2+ entries,
and outputs a markdown report sorted by group size (descending) and newest-first
modification time to gdocs/duplicates.md.

Usage:
    python scripts/find_gdoc_duplicates.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX_PATH = REPO_ROOT / "gdocs" / "index.json"
DEFAULT_OUT_PATH = REPO_ROOT / "gdocs" / "duplicates.md"


def normalize_title(title: str) -> str:
    """Normalize title by removing trailing (N) suffix, collapsing whitespace, and lowercasing."""
    # Strip trailing \s*\(\d+\)$
    t = re.sub(r"\s*\(\d+\)$", "", title.strip(), flags=re.IGNORECASE)
    # Collapse whitespace
    t = re.sub(r"\s+", " ", t)
    return t.strip().lower()


def find_duplicates(gdocs: list[dict]) -> dict[str, list[dict]]:
    """Group docs by normalized title and return groups with 2+ members."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for doc in gdocs:
        key = normalize_title(doc.get("title", ""))
        if key:
            groups[key].append(doc)

    return {k: v for k, v in groups.items() if len(v) >= 2}


def escape_markdown(text: str) -> str:
    """Escape pipe characters for markdown table cells."""
    return text.replace("|", "\\|").replace("\n", " ")


def format_mtime(mtime: float | int) -> str:
    """Format epoch timestamp to human-readable date string."""
    try:
        dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return str(mtime)


def write_report(dup_groups: dict[str, list[dict]], total_docs: int, out_path: Path) -> None:
    """Write markdown duplicate docs report to out_path."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sorted_keys = sorted(dup_groups.keys(), key=lambda k: (-len(dup_groups[k]), k))
    total_dup_docs = sum(len(v) for v in dup_groups.values())

    lines: list[str] = [
        "# Duplicate Google Drive Research Docs Report",
        "",
        f"Total indexed docs: {total_docs} | Duplicate groups (2+ copies): {len(sorted_keys)} | Total documents across groups: {total_dup_docs}",
        "",
        "> [!NOTE]",
        "> These groups represent research sessions with duplicate or recurring titles (e.g. trailing `(1)`, `(2)`).",
        "> Members are sorted newest-first by file modification time.",
        "",
    ]

    for key in sorted_keys:
        members = dup_groups[key]
        members_sorted = sorted(members, key=lambda d: d.get("mtime", 0), reverse=True)

        lines.append(f"## {key} ({len(members)} entries)")
        lines.append("")
        lines.append("| Title (as saved) | Doc ID | Modified |")
        lines.append("| :--- | :--- | :--- |")

        for doc in members_sorted:
            title_str = escape_markdown(doc.get("title", ""))
            doc_id_str = escape_markdown(doc.get("doc_id", ""))
            mtime_str = format_mtime(doc.get("mtime", 0))
            lines.append(f"| {title_str} | {doc_id_str} | {mtime_str} |")

        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX_PATH,
        help=f"Path to index.json (default: {DEFAULT_INDEX_PATH})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_PATH,
        help=f"Path to output markdown report (default: {DEFAULT_OUT_PATH})",
    )

    args = parser.parse_args()

    if not args.index.exists():
        sys.exit(
            f"Error: {args.index} does not exist.\n"
            "Please run 'python scripts/sync_gdocs_index.py' first to build the index."
        )

    try:
        with open(args.index, "r", encoding="utf-8") as f:
            gdocs = json.load(f)
    except Exception as exc:
        sys.exit(f"Error reading {args.index}: {exc}")

    dup_groups = find_duplicates(gdocs)
    write_report(dup_groups, len(gdocs), args.out)

    print(f"Found {len(dup_groups)} duplicate groups across {len(gdocs)} docs -> {args.out}")


if __name__ == "__main__":
    main()

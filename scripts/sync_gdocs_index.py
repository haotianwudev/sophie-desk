#!/usr/bin/env python3
"""Scan D:\\GoogleDrive recursively for .gdoc stubs and refresh gdocs/db/gdocs.db's
gdocs_index table.

A .gdoc file in Google Drive's desktop sync folder is a small JSON stub:
{"doc_id": "...", "resource_key": "...", "email": "..."}
The filename without .gdoc is the document's title.

This script extracts titles and doc_ids to build a fast local index without
fetching actual document content. Writes directly to gdocs_db (see that
module and papers/db-schema/DATABASES.md) -- gdocs/index.json is gone as of
2026-09-06, this is the source of truth now.

Note: .gsheet and .gslides files are currently out of scope.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import gdocs_db

DEFAULT_DRIVE_DIR = Path("D:/GoogleDrive")
REPO_ROOT = Path(__file__).resolve().parent.parent


def is_personal_or_tmp_dir(dirname: str) -> bool:
    name_lower = dirname.lower()
    return name_lower == ".tmp.drivedownload" or "personal" in name_lower


def sync_index(
    drive_dir: Path = DEFAULT_DRIVE_DIR,
    db_path: Path = gdocs_db.DEFAULT_DB_PATH,
) -> tuple[int, int]:
    """Scans drive_dir for .gdoc files, full-refreshes gdocs_db's gdocs_index
    table, and returns (indexed_count, skipped_count)."""
    if not drive_dir.exists():
        raise FileNotFoundError(f"Drive directory not found: {drive_dir}")

    docs: list[dict] = []
    skipped_count = 0

    for root, dirs, files in os.walk(drive_dir):
        # Prune temporary and personal directories in-place
        dirs_to_skip = [d for d in dirs if is_personal_or_tmp_dir(d)]
        for d in dirs_to_skip:
            dirs.remove(d)
        skipped_count += len(dirs_to_skip)

        for file in files:
            if not file.endswith(".gdoc"):
                continue

            full_path = os.path.join(root, file)
            title = file[:-5]  # Strip .gdoc extension

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as exc:
                print(f"Warning: failed to read {full_path}: {exc}", file=sys.stderr)
                continue

            doc_id = data.get("doc_id", "")
            resource_key = data.get("resource_key", "")
            relpath = os.path.relpath(full_path, drive_dir).replace("\\", "/")
            mtime = os.path.getmtime(full_path)

            docs.append(
                {
                    "title": title,
                    "doc_id": doc_id,
                    "resource_key": resource_key,
                    "relpath": relpath,
                    "mtime": mtime,
                }
            )

    # Sort deterministically by title
    docs.sort(key=lambda item: item["title"])

    conn = gdocs_db.connect(db_path)
    try:
        gdocs_db.full_refresh(conn, "gdocs_index", docs)
    finally:
        conn.close()

    return len(docs), skipped_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--drive-dir",
        type=Path,
        default=DEFAULT_DRIVE_DIR,
        help=f"Path to Google Drive root (default: {DEFAULT_DRIVE_DIR})",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=gdocs_db.DEFAULT_DB_PATH,
        help=f"Path to gdocs.db (default: {gdocs_db.DEFAULT_DB_PATH})",
    )

    args = parser.parse_args()

    try:
        indexed, skipped = sync_index(drive_dir=args.drive_dir, db_path=args.db)
    except FileNotFoundError as err:
        sys.exit(f"Error: {err}")

    print(f"indexed {indexed} docs, skipped {skipped} (personal/tmp)")


if __name__ == "__main__":
    main()

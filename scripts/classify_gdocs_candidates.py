#!/usr/bin/env python3
"""Fetch matched Google Drive docs for classification -- NOT a candidate writer.

Reads matched article <-> Drive doc pairs from gdocs/db/gdocs.db's
article_gdoc_matches table (was gdocs/article-exact-matches.md before
2026-09-06 -- see gdocs_db.py and papers/db-schema/DATABASES.md),
fetches each public Google Doc page, and extracts content structure (title tag,
H1, headings, a text sample) into a batch file for an agent to actually read
and classify (research-paper / news / general-info) -- a plain script can't
make that judgment call itself. The agent then writes the classification
directly into gdocs/classified_state.json (same shape as existing entries:
category, reasoning, clean_title, thesis, tags).

IMPORTANT -- this script does NOT and must NOT write to
papers/FOLLOWUP-CANDIDATES.md. An earlier version of this script did exactly
that (added the Gemini doc itself as a "candidate research paper," which is
wrong -- it's our own AI synthesis, not a research paper). That code path has
been removed. The only thing that belongs in FOLLOWUP-CANDIDATES.md is real
papers CITED WITHIN a research-paper-classified doc -- see
scripts/extract_gdoc_citations.py, which is the corrected, actually-verified
mechanism for that (see tasks/done/gdocs-citation-candidates-v2.md).

Usage:
    python scripts/classify_gdocs_candidates.py [--limit 30] [--offset 0] [--delay 0.35]
    Writes gdocs/batch_to_classify.json for an agent to read and classify.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import gdocs_db

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTICLES_DIR = Path("F:/workspace/ai-stock-suggestion-client/src/data/articles")
DEFAULT_STATE_PATH = REPO_ROOT / "gdocs" / "classified_state.json"

MATCHED_TIERS = {"exact", "case-insensitive", "suffix-tolerant"}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def parse_articles_from_file(filepath: Path) -> list[dict]:
    """Parse article objects from a TypeScript quarter file."""
    content = filepath.read_text(encoding="utf-8")
    articles: list[dict] = []

    blocks = re.split(r"\n\s*\{", content)[1:]
    for block in blocks:
        title_match = re.search(r'\btitle:\s*["\']((?:[^"\'\\]|\\.)*)["\']', block)
        slug_match = re.search(r'\bslug:\s*["\']([^"\']*)["\']', block)
        date_match = re.search(r'\bdate:\s*["\']([^"\']*)["\']', block)
        gdoc_match = re.search(r'\bgoogleDoc:\s*["\']([^"\']*)["\']', block)

        if title_match:
            raw_title = title_match.group(1)
            title = raw_title.replace('\\"', '"').replace("\\'", "'")
            slug = slug_match.group(1) if slug_match else ""
            date_str = date_match.group(1) if date_match else ""
            google_doc = gdoc_match.group(1) if gdoc_match else None

            articles.append(
                {
                    "title": title,
                    "slug": slug,
                    "date": date_str,
                    "google_doc": google_doc,
                    "source_file": filepath.name,
                }
            )

    return articles


def load_all_articles(articles_dir: Path) -> dict[str, dict]:
    """Load all articles keyed by slug."""
    if not articles_dir.exists():
        raise FileNotFoundError(f"Articles directory not found: {articles_dir}")

    files = sorted(articles_dir.glob("*-q*.ts"))
    if not files:
        raise FileNotFoundError(f"No *-q*.ts files found in {articles_dir}")

    articles_by_slug: dict[str, dict] = {}
    for f in files:
        for a in parse_articles_from_file(f):
            if a.get("slug"):
                articles_by_slug[a["slug"]] = a

    return articles_by_slug


def load_matched_pairs(db_path: Path = gdocs_db.DEFAULT_DB_PATH) -> list[dict]:
    """Load confirmed matched pairs from gdocs_db's article_gdoc_matches table.
    'Matched' means match_tier is one of the three confident tiers -- see
    MATCHED_TIERS and papers/db-schema/article_gdoc_matches.md."""
    if not db_path.exists():
        raise FileNotFoundError(f"gdocs.db not found: {db_path}")

    conn = gdocs_db.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"SELECT * FROM article_gdoc_matches WHERE match_tier IN "
            f"({', '.join('?' for _ in MATCHED_TIERS)})",
            tuple(MATCHED_TIERS),
        ).fetchall()
    finally:
        conn.close()

    return [
        {
            "slug": r["slug"],
            "article_title": r["article_title"],
            "extracted_page_title": r["extracted_page_title"],
            "match_tier": r["match_tier"],
            "doc_id": r["matched_doc_id"],
        }
        for r in rows
    ]


def fetch_doc_content(url: str, timeout: float = 12.0) -> dict | None:
    """Fetch public Google Doc HTML and extract title, H1, headings, and text."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    # Title tag
    title_tag_match = re.search(r"<title[^>]*>([^<]*)</title>", raw_html, re.I)
    title_tag = html.unescape(title_tag_match.group(1)).strip() if title_tag_match else ""

    # Doc H1 / Title element
    h1_match = re.search(r'<p[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</p>', raw_html, re.I | re.DOTALL)
    if not h1_match:
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", raw_html, re.I | re.DOTALL)
    if not h1_match:
        h1_match = re.search(r"<h2[^>]*>(.*?)</h2>", raw_html, re.I | re.DOTALL)

    h1_text = html.unescape(re.sub(r"<[^>]+>", "", h1_match.group(1))).strip() if h1_match else ""

    # Headings
    headings = re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", raw_html, re.I | re.DOTALL)
    clean_headings = [
        html.unescape(re.sub(r"<[^>]+>", "", h)).strip()
        for h in headings
        if html.unescape(re.sub(r"<[^>]+>", "", h)).strip()
    ]

    # Clean body text
    body_html = re.sub(r"<(script|style|header|nav)[^>]*>.*?</\1>", "", raw_html, flags=re.DOTALL | re.I)
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = html.unescape(" ".join(text.split()))
    text = re.sub(r"^Published using Google Docs.*?(Report abuse|Learn more)", "", text).strip()
    text = re.sub(r"^(.*?Updated automatically every \d+ minutes\s*)", "", text).strip()

    return {
        "title_tag": title_tag,
        "doc_h1": h1_text,
        "headings": clean_headings,
        "text_sample": text[:3000],
    }


# NOTE: this file used to also contain normalize_title/format_markdown_cell
# and an append_candidate_rows() that wrote the Gemini doc itself into
# papers/FOLLOWUP-CANDIDATES.md as a "candidate research paper." That was
# wrong and has been removed -- see the module docstring. Real candidates
# come from scripts/extract_gdoc_citations.py instead.


DEFAULT_BATCH_OUT_PATH = REPO_ROOT / "gdocs" / "batch_to_classify.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--articles-dir",
        type=Path,
        default=DEFAULT_ARTICLES_DIR,
        help=f"Path to article data directory (default: {DEFAULT_ARTICLES_DIR})",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=gdocs_db.DEFAULT_DB_PATH,
        help=f"Path to gdocs.db (default: {gdocs_db.DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help=f"Path to classified_state.json (default: {DEFAULT_STATE_PATH})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_BATCH_OUT_PATH,
        help=f"Where to write the fetched batch for an agent to classify (default: {DEFAULT_BATCH_OUT_PATH})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Limit number of NOT-YET-CLASSIFIED docs to fetch (default: 30, 0 = all remaining)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.35,
        help="Polite delay between HTTP requests in seconds (default: 0.35)",
    )

    args = parser.parse_args()

    start_time = time.time()

    articles_by_slug = load_all_articles(args.articles_dir)
    matched_pairs = load_matched_pairs(args.db)

    # Load existing state if available
    state: dict[str, dict] = {}
    if args.state_file.exists():
        try:
            with open(args.state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    # Only fetch pairs not already classified
    unclassified = [p for p in matched_pairs if p["slug"] not in state]
    todo = unclassified[: args.limit] if args.limit > 0 else unclassified

    print(f"{len(matched_pairs)} matched pairs total, {len(state)} already classified, "
          f"{len(unclassified)} remaining, fetching {len(todo)} for this batch...")

    batch: list[dict] = []
    for idx, pair in enumerate(todo, 1):
        slug = pair["slug"]
        art = articles_by_slug.get(slug, {})
        url = art.get("google_doc")
        if not url:
            continue

        doc_data = fetch_doc_content(url)
        if doc_data:
            batch.append({
                "slug": slug,
                "doc_id": pair["doc_id"],
                "article_title": pair["article_title"],
                "article_date": art.get("date", ""),
                **doc_data,
            })

        if idx % 10 == 0 or idx == len(todo):
            print(f"  fetched {idx}/{len(todo)}...")
        if idx < len(todo):
            time.sleep(args.delay)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(batch)} fetched docs to {args.out} for classification.")
    print(f"Elapsed time: {time.time() - start_time:.2f}s")
    print(
        "\nNext step (not done by this script): read each entry in that file, decide "
        "research-paper / news / general-info the same way the first classification pass did, "
        "and write the result into "
        f"{args.state_file} under the doc's slug as "
        '{"category": ..., "reasoning": ..., "clean_title": ..., "thesis": ..., "tags": ...}. '
        "This script never writes to papers/FOLLOWUP-CANDIDATES.md -- see the module docstring."
    )


if __name__ == "__main__":
    main()

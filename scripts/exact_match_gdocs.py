#!/usr/bin/env python3
"""Exact-match Sophie platform articles to Google Drive research docs.

For articles with a `googleDoc` published URL:
1. Fetches the public published Google Doc page.
2. Extracts the exact <title> tag text (which reflects the source Drive title verbatim).
3. Compares against titles in gdocs_db's gdocs_index table (exact match, then
   case-insensitive fallback).
4. Full-refreshes gdocs_db's article_gdoc_matches table with the results.

Writes directly to gdocs_db (see that module and papers/db-schema/DATABASES.md)
-- gdocs/article-exact-matches.md is gone as of 2026-09-06, this is the
source of truth now. Still prints a console summary.

Usage:
    python scripts/exact_match_gdocs.py
"""

from __future__ import annotations

import argparse
import html
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
        gdoc_match = re.search(r'\bgoogleDoc:\s*["\']([^"\']*)["\']', block)

        if title_match:
            raw_title = title_match.group(1)
            title = raw_title.replace('\\"', '"').replace("\\'", "'")
            slug = slug_match.group(1) if slug_match else ""
            google_doc = gdoc_match.group(1) if gdoc_match else None

            articles.append(
                {
                    "title": title,
                    "slug": slug,
                    "google_doc": google_doc,
                    "source_file": filepath.name,
                }
            )

    return articles


def load_all_articles(articles_dir: Path, only_with_gdoc: bool = True) -> list[dict]:
    """Load all articles from {year}-q{quarter}.ts files."""
    if not articles_dir.exists():
        raise FileNotFoundError(f"Articles directory not found: {articles_dir}")

    files = sorted(articles_dir.glob("*-q*.ts"))
    if not files:
        raise FileNotFoundError(f"No *-q*.ts files found in {articles_dir}")

    all_articles: list[dict] = []
    for f in files:
        all_articles.extend(parse_articles_from_file(f))

    if only_with_gdoc:
        return [a for a in all_articles if a.get("google_doc")]
    return all_articles


def fetch_page_title(url: str, timeout: float = 10.0, max_retries: int = 1) -> str | None:
    """Fetch public Google Doc page and extract <title> tag text."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw_html = resp.read().decode("utf-8", errors="replace")

            # Extract <title> content up to next < or </title>
            match = re.search(r"<title[^>]*>([^<]*)", raw_html, re.IGNORECASE)
            if match:
                title_text = html.unescape(match.group(1)).strip()
                return title_text
            return None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            if attempt < max_retries:
                time.sleep(1.0)
                continue
            return None

    return None


def normalize_string(s: str) -> str:
    """Normalize string by collapsing whitespace and lowercasing."""
    return re.sub(r"\s+", " ", s).strip().lower()


def strip_paren_suffix(s: str) -> str:
    """Strip a trailing ' (N)' suffix (e.g. ' (1)', ' (2)').

    Google Drive Desktop's local .gdoc stub filename can lag the doc's live
    Drive title after a rename -- confirmed live: a doc whose current title is
    "2025 Financial Market Analysis" has a local stub named
    "2025 Financial Market Analysis (1).gdoc". This is not a duplicate; it's
    one document with a stale local filename. Stripping the suffix from both
    sides catches that case."""
    return re.sub(r"\s*\(\d+\)\s*$", "", s).strip()


def find_matching_doc(extracted_title: str, gdocs: list[dict]) -> tuple[str, str]:
    """Find matching doc in index.json.

    Returns:
        (match_tier, doc_id)
        match_tier is one of: 'exact', 'case-insensitive',
        'suffix-tolerant', 'ambiguous (N candidates)', 'no match in index'
    """
    cleaned_extracted = extracted_title.strip()
    norm_extracted = normalize_string(cleaned_extracted)

    # 1. Exact match
    exact_matches = [
        d for d in gdocs if d.get("title", "").strip() == cleaned_extracted
    ]
    if exact_matches:
        # Sort newest first if multiple
        exact_matches.sort(key=lambda d: d.get("mtime", 0), reverse=True)
        return "exact", exact_matches[0].get("doc_id", "")

    # 2. Case-insensitive / whitespace-collapsed fallback
    ci_matches = [
        d for d in gdocs if normalize_string(d.get("title", "")) == norm_extracted
    ]
    if ci_matches:
        ci_matches.sort(key=lambda d: d.get("mtime", 0), reverse=True)
        return "case-insensitive", ci_matches[0].get("doc_id", "")

    # 3. Suffix-tolerant: strip a trailing " (N)" from the index title (the
    # extracted title is the live Drive title, already "clean") and compare
    # case-insensitively. Multiple distinct docs can genuinely share a base
    # title (confirmed in gdocs/duplicates.md, e.g. recurring weekly research)
    # -- when stripping yields more than one candidate, don't guess which one
    # the article actually points to; flag it instead.
    norm_stripped_extracted = normalize_string(strip_paren_suffix(cleaned_extracted))
    suffix_matches = [
        d
        for d in gdocs
        if normalize_string(strip_paren_suffix(d.get("title", ""))) == norm_stripped_extracted
    ]
    if len(suffix_matches) == 1:
        return "suffix-tolerant", suffix_matches[0].get("doc_id", "")
    if len(suffix_matches) > 1:
        return f"ambiguous ({len(suffix_matches)} candidates)", ""

    return "no match in index", ""


def write_to_db(results: list[dict], db_path: Path) -> None:
    """Full-refresh gdocs_db's article_gdoc_matches table. Stores the raw,
    full-fidelity match_tier ('exact' / 'case-insensitive' / 'suffix-tolerant'
    / 'ambiguous (N candidates)' / 'no match in index' / 'fetch failed') --
    collapsing 'exact'/'case-insensitive'/'suffix-tolerant' into a single
    'matched' label was a markdown-report display convenience, not something
    to bake into storage; a query can collapse it if it wants
    (papers/db-schema/article_gdoc_matches.md has the example)."""
    rows = [
        {
            "slug": r["slug"],
            "article_title": r["title"],
            "extracted_page_title": r["extracted_title"],
            "match_tier": r["match_tier"],
            # NULL, not "" -- an empty string isn't a valid FK reference to
            # gdocs_index.doc_id and trips the FOREIGN KEY constraint (hit
            # live: every unmatched row failed the full_refresh transaction).
            "matched_doc_id": r["matched_doc_id"] or None,
        }
        for r in results
    ]
    conn = gdocs_db.connect(db_path)
    try:
        gdocs_db.full_refresh(conn, "article_gdoc_matches", rows)
    finally:
        conn.close()


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
        "--delay",
        type=float,
        default=0.35,
        help="Polite delay between HTTP requests in seconds (default: 0.35)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP request timeout in seconds (default: 10.0)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit number of articles to process (0 = all, default: 0)",
    )

    args = parser.parse_args()

    if not args.db.exists():
        sys.exit(
            f"Error: {args.db} does not exist.\n"
            "Please run 'python scripts/sync_gdocs_index.py' first to build the index."
        )

    try:
        articles = load_all_articles(args.articles_dir, only_with_gdoc=True)
    except Exception as exc:
        sys.exit(f"Error loading articles: {exc}")

    if args.limit > 0:
        articles = articles[: args.limit]

    conn = gdocs_db.connect(args.db)
    try:
        conn.row_factory = sqlite3.Row
        gdocs = [dict(row) for row in conn.execute("SELECT * FROM gdocs_index")]
    finally:
        conn.close()

    print(f"Loaded {len(articles)} articles with googleDoc, {len(gdocs)} indexed docs.")
    print(f"Beginning title extraction and matching (delay: {args.delay}s)...")

    results: list[dict] = []
    for idx, art in enumerate(articles, 1):
        gdoc_url = art["google_doc"]
        slug = art["slug"]
        title = art["title"]

        extracted_title = fetch_page_title(gdoc_url, timeout=args.timeout)

        if extracted_title is None:
            match_tier = "fetch failed"
            matched_doc_id = ""
            extracted_title_str = ""
        else:
            extracted_title_str = extracted_title
            match_tier, matched_doc_id = find_matching_doc(extracted_title, gdocs)

        results.append(
            {
                "slug": slug,
                "title": title,
                "google_doc": gdoc_url,
                "extracted_title": extracted_title_str,
                "match_tier": match_tier,
                "matched_doc_id": matched_doc_id,
            }
        )

        if idx % 20 == 0 or idx == len(articles):
            print(f"Processed {idx}/{len(articles)} articles...")

        if idx < len(articles) and args.delay > 0:
            time.sleep(args.delay)

    write_to_db(results, args.db)

    matched_tiers = {"exact", "case-insensitive", "suffix-tolerant"}
    matched_count = sum(1 for r in results if r["match_tier"] in matched_tiers)
    ambiguous_count = sum(1 for r in results if r["match_tier"].startswith("ambiguous"))
    no_match_count = sum(1 for r in results if r["match_tier"] == "no match in index")
    failed_count = sum(1 for r in results if r["match_tier"] == "fetch failed")

    print(f"\narticle_gdoc_matches refreshed in: {args.db}")
    print(
        f"Summary: {matched_count} matched, {ambiguous_count} ambiguous, "
        f"{no_match_count} no match in index, {failed_count} fetch failed (Total: {len(results)})"
    )


if __name__ == "__main__":
    main()

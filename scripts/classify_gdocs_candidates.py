#!/usr/bin/env python3
"""Classify matched Google Drive research docs and candidate research papers.

Reads matched article <-> Drive doc pairs from gdocs/article-exact-matches.md,
fetches the public Google Doc page, extracts content structure and headings,
classifies the doc into research-paper / news / general-info, and appends
research-paper entries to papers/FOLLOWUP-CANDIDATES.md.

Usage:
    python scripts/classify_gdocs_candidates.py [--limit 30] [--delay 0.35]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTICLES_DIR = Path("F:/workspace/ai-stock-suggestion-client/src/data/articles")
DEFAULT_MATCHES_PATH = REPO_ROOT / "gdocs" / "article-exact-matches.md"
DEFAULT_CANDIDATES_PATH = REPO_ROOT / "papers" / "FOLLOWUP-CANDIDATES.md"
DEFAULT_STATE_PATH = REPO_ROOT / "gdocs" / "classified_state.json"

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


def load_matched_pairs(matches_path: Path) -> list[dict]:
    """Load confirmed matched pairs from gdocs/article-exact-matches.md."""
    if not matches_path.exists():
        raise FileNotFoundError(f"Matches file not found: {matches_path}")

    pairs: list[dict] = []
    with open(matches_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("| ") and not line.startswith("| Slug") and not line.startswith("| :---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 5 and parts[3] == "matched":
                    pairs.append(
                        {
                            "slug": parts[0],
                            "article_title": parts[1],
                            "extracted_page_title": parts[2],
                            "match_tier": parts[3],
                            "doc_id": parts[4],
                        }
                    )
    return pairs


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


def normalize_title(t: str) -> str:
    """Normalize title for deduplication."""
    s = re.sub(r"\s*\(\d+\)\s*$", "", t)
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.lower().split())


def format_markdown_cell(s: str) -> str:
    """Escape pipes and strip extra newlines."""
    return s.replace("|", "\\|").replace("\n", " ").strip()


def append_candidate_rows(
    candidates_file: Path,
    new_rows: list[dict],
) -> int:
    """Append new candidate rows before the '## Passed on' section in FOLLOWUP-CANDIDATES.md."""
    if not candidates_file.exists():
        raise FileNotFoundError(f"Candidates file not found: {candidates_file}")

    content = candidates_file.read_text(encoding="utf-8")

    # Parse existing titles and doc_ids to prevent duplicates
    existing_normalized_titles = set()
    existing_doc_ids = set()

    for line in content.splitlines():
        if line.startswith("|") and not line.startswith("| Title") and not line.startswith("|---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 6:
                existing_normalized_titles.add(normalize_title(parts[0]))
                if parts[5]:
                    existing_doc_ids.add(parts[5])

    # Format new rows, skipping duplicates
    rows_to_insert = []
    for r in new_rows:
        norm_t = normalize_title(r["title"])
        if norm_t in existing_normalized_titles or r["doc_id"] in existing_doc_ids:
            continue

        existing_normalized_titles.add(norm_t)
        existing_doc_ids.add(r["doc_id"])

        row_str = (
            f"| {format_markdown_cell(r['title'])} "
            f"| {format_markdown_cell(r['authors_year'])} "
            f"| {format_markdown_cell(r['thesis'])} "
            f"| {format_markdown_cell(r['tags'])} "
            f"| [{format_markdown_cell(r['article_title'])}](https://www.sophie-ai-finance.com/articles/{r['slug']}) "
            f"| {format_markdown_cell(r['doc_id'])} "
            f"| |"
        )
        rows_to_insert.append(row_str)

    if not rows_to_insert:
        return 0

    # Insert before '## Passed on'
    target = "## Passed on"
    if target in content:
        parts = content.split(target, 1)
        new_content = parts[0].rstrip() + "\n" + "\n".join(rows_to_insert) + "\n\n" + target + parts[1]
    else:
        new_content = content.rstrip() + "\n" + "\n".join(rows_to_insert) + "\n"

    candidates_file.write_text(new_content, encoding="utf-8")
    return len(rows_to_insert)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--articles-dir",
        type=Path,
        default=DEFAULT_ARTICLES_DIR,
        help=f"Path to article data directory (default: {DEFAULT_ARTICLES_DIR})",
    )
    parser.add_argument(
        "--matches",
        type=Path,
        default=DEFAULT_MATCHES_PATH,
        help=f"Path to article-exact-matches.md (default: {DEFAULT_MATCHES_PATH})",
    )
    parser.add_argument(
        "--candidates-file",
        type=Path,
        default=DEFAULT_CANDIDATES_PATH,
        help=f"Path to FOLLOWUP-CANDIDATES.md (default: {DEFAULT_CANDIDATES_PATH})",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help=f"Path to classified_state.json (default: {DEFAULT_STATE_PATH})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Limit number of docs to process (default: 30, 0 = all)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset in matched list (default: 0)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.35,
        help="Polite delay between HTTP requests in seconds (default: 0.35)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write to FOLLOWUP-CANDIDATES.md",
    )

    args = parser.parse_args()

    start_time = time.time()

    articles_by_slug = load_all_articles(args.articles_dir)
    matched_pairs = load_matched_pairs(args.matches)

    if args.offset > 0:
        matched_pairs = matched_pairs[args.offset :]
    if args.limit > 0:
        matched_pairs = matched_pairs[: args.limit]

    # Load existing state if available
    state: dict[str, dict] = {}
    if args.state_file.exists():
        try:
            with open(args.state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    print(f"Processing batch of {len(matched_pairs)} matched pairs...")

    # For each pair, if not in state, fetch and allow recording
    for idx, pair in enumerate(matched_pairs, 1):
        slug = pair["slug"]
        if slug in state:
            continue

        art = articles_by_slug.get(slug, {})
        url = art.get("google_doc")
        if not url:
            continue

        doc_data = fetch_doc_content(url)
        if not doc_data:
            continue

        time.sleep(args.delay)

    # Collect candidates from state for this batch
    candidates_to_add: list[dict] = []
    for pair in matched_pairs:
        slug = pair["slug"]
        if slug in state:
            item = state[slug]
            cat = item.get("category", "general-info")
            if cat == "research-paper":
                art = articles_by_slug.get(slug, {})
                date_str = art.get("date", "")
                year_match = re.search(r"\b(20\d\d)\b", date_str)
                year = year_match.group(1) if year_match else "2026"
                candidates_to_add.append(
                    {
                        "slug": slug,
                        "doc_id": pair["doc_id"],
                        "article_title": pair["article_title"],
                        "title": item["clean_title"],
                        "authors_year": f"Gemini Deep Research ({year})",
                        "thesis": item["thesis"],
                        "tags": item["tags"],
                    }
                )

    counts = {
        "research-paper": sum(1 for p in matched_pairs if state.get(p["slug"], {}).get("category") == "research-paper"),
        "news": sum(1 for p in matched_pairs if state.get(p["slug"], {}).get("category") == "news"),
        "general-info": sum(1 for p in matched_pairs if state.get(p["slug"], {}).get("category") == "general-info"),
    }

    print("\n--- Classification Summary (Batch of 30) ---")
    print(f"research-paper : {counts['research-paper']}")
    print(f"news           : {counts['news']}")
    print(f"general-info   : {counts['general-info']}")
    print(f"Elapsed time   : {time.time() - start_time:.2f}s")

    if not args.dry_run:
        added = append_candidate_rows(args.candidates_file, candidates_to_add)
        print(f"\nAdded {added} new research paper candidates to {args.candidates_file}")
    else:
        print(f"\n[Dry Run] Would add {len(candidates_to_add)} candidates to {args.candidates_file}")


if __name__ == "__main__":
    main()

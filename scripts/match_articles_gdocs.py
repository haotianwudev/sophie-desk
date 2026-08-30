#!/usr/bin/env python3
"""Match Sophie platform articles to Google Drive research docs.

Parses article metadata from ai-stock-suggestion-client/src/data/articles/*.ts,
scores them against gdocs/index.json by title similarity using difflib.SequenceMatcher,
and writes a markdown report sorted by score descending to gdocs/article-matches.md.

Usage:
    python scripts/match_articles_gdocs.py
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTICLES_DIR = Path("F:/workspace/ai-stock-suggestion-client/src/data/articles")
DEFAULT_INDEX_PATH = REPO_ROOT / "gdocs" / "index.json"
DEFAULT_OUT_PATH = REPO_ROOT / "gdocs" / "article-matches.md"


def parse_articles_from_file(filepath: Path) -> list[dict]:
    """Parse article objects from a TypeScript quarter file."""
    content = filepath.read_text(encoding="utf-8")
    articles: list[dict] = []

    # In TypeScript files, articles are items inside array: [ { ... }, { ... } ]
    # Split by object delimiters or match { ... } blocks containing title
    blocks = re.split(r"\n\s*\{", content)[1:]
    for block in blocks:
        title_match = re.search(r'\btitle:\s*"((?:[^"\\]|\\.)*)"', block)
        slug_match = re.search(r'\bslug:\s*"([^"]*)"', block)
        has_gdoc = bool(re.search(r"\bgoogleDoc:\s*", block))

        if title_match:
            raw_title = title_match.group(1)
            title = raw_title.replace('\\"', '"').replace("\\'", "'")
            slug = slug_match.group(1) if slug_match else ""

            articles.append(
                {
                    "title": title,
                    "slug": slug,
                    "has_google_doc": has_gdoc,
                    "source_file": filepath.name,
                }
            )

    return articles


def load_all_articles(articles_dir: Path) -> list[dict]:
    """Load all articles from {year}-q{quarter}.ts files."""
    if not articles_dir.exists():
        raise FileNotFoundError(f"Articles directory not found: {articles_dir}")

    files = sorted(articles_dir.glob("*-q*.ts"))
    if not files:
        raise FileNotFoundError(f"No *-q*.ts files found in {articles_dir}")

    all_articles: list[dict] = []
    for f in files:
        all_articles.extend(parse_articles_from_file(f))

    return all_articles


def match_articles(
    articles: list[dict],
    gdocs: list[dict],
) -> list[dict]:
    """Score each article against all indexed gdocs and find the best match."""
    results: list[dict] = []

    for art in articles:
        title_norm = art["title"].strip().lower()
        best_score = 0.0
        best_doc: dict | None = None

        for doc in gdocs:
            doc_title = doc.get("title", "")
            doc_title_norm = doc_title.strip().lower()
            score = difflib.SequenceMatcher(None, title_norm, doc_title_norm).ratio()
            if score > best_score:
                best_score = score
                best_doc = doc

        results.append(
            {
                "score": best_score,
                "slug": art["slug"],
                "title": art["title"],
                "has_google_doc": art["has_google_doc"],
                "candidate_title": best_doc.get("title", "") if best_doc else "",
                "candidate_doc_id": best_doc.get("doc_id", "") if best_doc else "",
            }
        )

    # Sort descending by score
    results.sort(key=lambda item: item["score"], reverse=True)
    return results


def escape_markdown(text: str) -> str:
    """Escape pipe characters for markdown table cells."""
    return text.replace("|", "\\|").replace("\n", " ")


def write_report(matches: list[dict], out_path: Path) -> None:
    """Write markdown table report to out_path."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# Sophie Article to Google Drive Research Doc Matches",
        "",
        f"Total articles analyzed: {len(matches)}",
        "",
        "| Score | Article Slug | Article Title | Has googleDoc? | Best Gdoc Candidate | Candidate Doc ID |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for m in matches:
        score_str = f"{m['score']:.2f}"
        slug_str = escape_markdown(m["slug"])
        title_str = escape_markdown(m["title"])
        has_gdoc_str = "yes" if m["has_google_doc"] else "no"
        cand_title_str = escape_markdown(m["candidate_title"])
        cand_id_str = escape_markdown(m["candidate_doc_id"])

        lines.append(
            f"| {score_str} | {slug_str} | {title_str} | {has_gdoc_str} | {cand_title_str} | {cand_id_str} |"
        )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--articles-dir",
        type=Path,
        default=DEFAULT_ARTICLES_DIR,
        help=f"Path to article data directory (default: {DEFAULT_ARTICLES_DIR})",
    )
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
        articles = load_all_articles(args.articles_dir)
    except Exception as exc:
        sys.exit(f"Error loading articles: {exc}")

    try:
        with open(args.index, "r", encoding="utf-8") as f:
            gdocs = json.load(f)
    except Exception as exc:
        sys.exit(f"Error reading {args.index}: {exc}")

    matches = match_articles(articles, gdocs)
    write_report(matches, args.out)

    print(f"Matched {len(matches)} articles against {len(gdocs)} docs -> {args.out}")


if __name__ == "__main__":
    main()

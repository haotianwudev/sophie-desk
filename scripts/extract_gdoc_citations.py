#!/usr/bin/env python3
"""Extract cited research papers from research-paper-grade Gemini Google Docs.

Reads the 19 research-paper slugs from gdocs/classified_state.json, fetches the
full published Google Doc HTML, extracts citations from the 'Works cited' /
'References' section, filters for research quality (academic papers, working
papers, central banks, institutional research), deduplicates across articles,
and appends candidate rows to papers/FOLLOWUP-CANDIDATES.md.

Usage:
    python scripts/extract_gdoc_citations.py [--dry-run] [--delay 0.35]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTICLES_DIR = Path("F:/workspace/ai-stock-suggestion-client/src/data/articles")
DEFAULT_MATCHES_PATH = REPO_ROOT / "gdocs" / "article-exact-matches.md"
DEFAULT_CANDIDATES_PATH = REPO_ROOT / "papers" / "FOLLOWUP-CANDIDATES.md"
DEFAULT_STATE_PATH = REPO_ROOT / "gdocs" / "classified_state.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def load_classified_research_papers(state_path: Path) -> dict[str, dict]:
    """Load slugs classified as research-paper from gdocs/classified_state.json."""
    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    return {k: v for k, v in state.items() if v.get("category") == "research-paper"}


def load_article_metadata(articles_dir: Path, target_slugs: set[str]) -> dict[str, dict]:
    """Extract article titles and googleDoc published URLs from TypeScript quarter files."""
    if not articles_dir.exists():
        raise FileNotFoundError(f"Articles directory not found: {articles_dir}")

    files = sorted(articles_dir.glob("*-q*.ts"))
    articles_by_slug: dict[str, dict] = {}
    for filepath in files:
        content = filepath.read_text(encoding="utf-8")
        blocks = re.split(r"\n\s*\{", content)[1:]
        for block in blocks:
            slug_match = re.search(r'\bslug:\s*["\']([^"\']*)["\']', block)
            title_match = re.search(r'\btitle:\s*["\']((?:[^"\'\\]|\\.)*)["\']', block)
            gdoc_match = re.search(r'\bgoogleDoc:\s*["\']([^"\']*)["\']', block)
            if slug_match and slug_match.group(1) in target_slugs:
                slug = slug_match.group(1)
                raw_title = title_match.group(1) if title_match else slug
                title = raw_title.replace('\\"', '"').replace("\\'", "'")
                google_doc = gdoc_match.group(1) if gdoc_match else None
                articles_by_slug[slug] = {
                    "slug": slug,
                    "title": title,
                    "google_doc": google_doc,
                    "source_file": filepath.name,
                }
    return articles_by_slug


def load_doc_ids(matches_path: Path) -> dict[str, str]:
    """Load doc_id mappings for confirmed matches from gdocs/article-exact-matches.md."""
    if not matches_path.exists():
        return {}
    doc_ids: dict[str, str] = {}
    with open(matches_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("| ") and not line.startswith("| Slug") and not line.startswith("| :---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 5 and parts[3] == "matched":
                    doc_ids[parts[0]] = parts[4]
    return doc_ids


def unwrap_google_url(url: str) -> str:
    """Unwrap Google redirect link (https://www.google.com/url?q=...)."""
    if not url:
        return ""
    if "google.com/url?" in url:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if "q" in qs and qs["q"]:
            return qs["q"][0]
    return url


def fetch_published_doc_citations(url: str, timeout: float = 15.0) -> list[dict]:
    """Fetch full published Google Doc HTML and extract items from Works Cited / References."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(raw_html, "html.parser")

    # Locate heading for references section
    ref_heading = None
    for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
        text = el.get_text().strip().lower()
        if text in [
            "works cited",
            "works cited:",
            "references",
            "references:",
            "bibliography",
            "bibliography:",
            "citations",
            "citations:",
        ] or re.match(r"^(works cited|references|bibliography)\b", text):
            ref_heading = el
            break

    citations = []
    if ref_heading:
        curr = ref_heading
        while curr:
            curr = curr.find_next_sibling()
            if not curr:
                break
            if curr.name in ["h1", "h2", "h3"]:
                break

            items = []
            if curr.name in ["ol", "ul"]:
                items = curr.find_all("li")
            elif curr.name == "p":
                items = [curr]

            for item in items:
                raw_text = item.get_text().strip()
                if not raw_text:
                    continue
                a_tag = item.find("a")
                href = unwrap_google_url(a_tag.get("href", "")) if a_tag else ""
                citations.append({"raw_text": raw_text, "url": href})
    else:
        # Fallback: check if the document ends with an ordered/unordered list
        lists = soup.find_all(["ol", "ul"])
        if lists:
            last_list = lists[-1]
            for li in last_list.find_all("li"):
                raw_text = li.get_text().strip()
                if not raw_text:
                    continue
                a_tag = li.find("a")
                href = unwrap_google_url(a_tag.get("href", "")) if a_tag else ""
                citations.append({"raw_text": raw_text, "url": href})

    return citations


def is_research_quality(url: str, raw_text: str) -> tuple[bool, str]:
    """Filter citations to retain only academic/institutional research and working papers."""
    if not url:
        return False, "no_url"

    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    # 1. HARD EXCLUDES: news, blogs, social media, retail forums, courseware, framework docs
    exclude_domains = [
        "reddit.com", "youtube.com", "youtu.be", "github.com", "medium.com", "substack.com",
        "dev.to", "twitter.com", "x.com", "linkedin.com", "quora.com", "facebook.com",
        "investopedia.com", "wikipedia.org", "wikihow.com", "dummies.com", "fool.com",
        "seekingalpha.com", "nerdwallet.com", "bankrate.com", "thebalancemoney.com",
        "wallstreetprep.com", "corporatefinanceinstitute.com", "khanacademy.org",
        "coursera.org", "udemy.com", "edx.org", "learn.microsoft.com", "cloud.google.com",
        "aws.amazon.com", "hexdocs.pm", "readthedocs.io", "github.io", "testquality.com",
        "morphllm.com", "guild.ai", "langfuse.com", "kdnuggets.com", "tricentis.com",
        "stackoverflow.com", "modal.com", "prefactor.tech", "datadoghq.com", "liner.com",
        "optionalpha.com", "tastylive.com", "warriortrading.com", "optionsamurai.com",
        "strike.money", "tradefundrr.com", "fastercapital.com", "groww.in", "marketcalls.in",
        "stonex.com", "bloomberg.com", "reuters.com", "cnbc.com", "wsj.com", "ft.com",
        "marketwatch.com", "forbes.com", "barrons.com", "businessinsider.com", "fortune.com",
        "yahoo.com", "finance.yahoo.com", "thestreet.com", "nasdaq.com",
        "chase.com", "fidelity.com", "schwab.com", "etfstream.com",
        "etf.com", "b2broker.com", "etfarchitect.com", "tidalfinancialgroup.com",
        "enlightenedstocktrading.com", "crystalfunds.com", "graniteshares.com",
        "leverageshares.com", "bhseclaw.com", "theequityanalyst.files.wordpress.com",
        "prnewswire.com", "mstock.com", "dokumen.pub", "scribd.com", "convera.com",
        "codesignal.com", "streetofwalls.com", "blog.gopenai.com", "mongodb.com",
        "glaforge.dev", "sixty-north.com", "beancount.io", "sunlifeglobalinvestments.com",
        "rexshares.com", "uscfinvestments.com", "olivineresearch.com", "enerjisauretim.com.tr",
        "acaglobal.com", "eastspring.com", "mawer.com", "twse.com.tw", "hiltoncapitalmanagement.com",
        "tcw.com", "wisdomtree.com", "invesco.com", "direxion.com", "ecf.ctd.uscourts.gov",
        "pypi.org", "tradingblock.com", "quant.stackexchange.com", "hedgebook.com",
        "tencentcloud.com", "lobehub.com", "interactivebrokers.com", "ibkrguides.com",
        "zenml.io", "atlan.com", "futureagi.com", "vdf.ai", "soundcapitalsolutions.com",
        "inferloop.dev", "onixs.biz", "addonnetworks.com", "hackernoon.com", "speedbot.tech",
        "iptp.net", "ddn.com", "phoenixstrategy.group", "fxpro.com", "bookmap.com",
        "forex92.com", "crowell.com", "transacted.io", "xelera.io", "alphalayer.ai",
        "tejwin.com", "quantilia.com", "predictingalpha.com", "bajajbroking.in",
        "capitalmind.in", "moodys.com", "ionixxtech.com", "financestrategists.com",
        "analystprep.com", "orchestrade.com", "simcorp.com", "remita.net", "sdk.finance",
        "elastic.co", "datasciencedojo.com", "anthropic.com", "towardsdatascience.com",
        "galileo.ai", "openai.com", "morganstanley.com", "investing.com", "flashalpha.com",
        "salesforce.com", "cloudsecurityalliance.org", "vettafi.com", "paceretfs.com"
    ]

    for ed in exclude_domains:
        if ed in domain or (ed in f"{domain}{path}"):
            return False, f"exclude_domain:{ed}"

    if domain.startswith("docs.") or domain.startswith("help.") or domain.startswith("support.") or domain.startswith("api."):
        return False, "docs_or_help_subdomain"

    if "langchain.com" in domain or "mem0.ai" in domain:
        return False, "framework_docs"

    # 2. INCLUDES: Academic, Preprints, Journal Publishers
    academic_domains = [
        "arxiv.org", "ssrn.com", "papers.ssrn.com", "nber.org", "researchgate.net",
        "sciencedirect.com", "springer.com", "link.springer.com", "wiley.com",
        "onlinelibrary.wiley.com", "jstor.org", "tandfonline.com", "mdpi.com",
        "frontiersin.org", "ieee.org", "ieeexplore.ieee.org", "acm.org", "dl.acm.org",
        "pnas.org", "oup.com", "academic.oup.com", "cambridge.org", "semanticscholar.org",
        "repec.org", "ideas.repec.org", "pm-research.com", "worldscientific.com",
        "annualreviews.org", "iop.org", "openreview.net", "nature.com", "core.ac.uk",
        "dialnet.unirioja.es", "hal.science", "philarchive.org", "themoonlight.io",
        "aeaweb.org", "journals.plos.org", "uowoajournals.org", "unit.no"
    ]
    for ad in academic_domains:
        if ad in domain:
            return True, f"academic_domain:{ad}"

    # University domains: .edu, .ac.uk, .edu.xx, .ac.xx
    if re.search(r"\.(edu|ac\.[a-z]{2}|edu\.[a-z]{2})$", domain) or ".edu/" in domain or ".edu." in domain:
        return True, "university_domain"

    # Central Banks, Regulators, Policy & Multilateral
    central_bank_regulators = [
        "bis.org", "federalreserve.gov", "newyorkfed.org", "chicagofed.org",
        "stlouisfed.org", "philadelphiafed.org", "kansascityfed.org", "bostonfed.org",
        "atlantafed.org", "minneapolisfed.org", "dallasfed.org", "richmondfed.org",
        "clevelandfed.org", "sanfranciscofed.org", "ecb.europa.eu", "bankofengland.co.uk",
        "snb.ch", "boj.or.jp", "rba.gov.au", "bankofcanada.ca", "imf.org", "worldbank.org",
        "oecd.org", "esrb.europa.eu", "sec.gov", "cftc.gov", "finra.org", "esma.europa.eu",
        "iosco.org", "osc.ca", "brookings.edu", "bruegel.org", "cepr.org", "weforum.org",
        "idc.org", "efmaefm.org", "afme.eu", "sevenpillarsinstitute.org"
    ]
    for cbr in central_bank_regulators:
        if cbr in domain:
            return True, f"central_bank_regulator:{cbr}"

    # Institutional Research / Exchanges / Asset Managers / Quant Journals
    research_houses = [
        "aqr.com", "cboe.com", "cmegroup.com", "nyse.com", "blackrock.com",
        "twosigma.com", "man.com", "robeco.com", "vanguard.com", "msci.com",
        "spglobal.com", "cfainstitute.org", "cfapubs.org", "risk.net",
        "thehedgefundjournal.com", "factorresearch.com", "dimensional.com",
        "jpmcc-gcard.com", "optiver.com", "caia.org", "alphaarchitect.com",
        "quantresearch.org", "compatibl.com", "wellington.com"
    ]
    for rh in research_houses:
        if rh in domain:
            return True, f"research_house:{rh}"

    if "huggingface.co/papers" in f"{domain}{path}":
        return True, "academic_domain:huggingface_papers"

    if path.endswith(".pdf") or "/pdf/" in path:
        return True, "direct_pdf_link"

    return False, "unmatched_generic"


def clean_paper_title(raw_text: str) -> str | None:
    """Extract and sanitize paper title from raw citation text."""
    text = raw_text.strip()
    text = re.sub(r"^(?:\[\d+\]|\d+\.)\s*", "", text).strip()
    if not text or text.startswith("http://") or text.startswith("https://") or text.startswith("www."):
        return None

    split_match = re.split(
        r",\s*accessed\b|,\s*https?://|\s+-\s+accessed\b|\s+accessed\s+[A-Z][a-z]+\s+\d+",
        text,
        flags=re.I,
    )
    title_part = split_match[0].strip()

    # Strip leading prefixes: (PDF), [PDF], [2401.12345], etc.
    title = re.sub(
        r"^(?:\(?\s*PDF\s*\)?|\[\s*PDF\s*\]|\[\s*\d{4,5}\.\d{4,5}(?:v\d+)?\s*\])\s*",
        "",
        title_part,
        flags=re.I,
    ).strip()

    # Strip trailing ellipsis / dots
    title = re.sub(r"\s*\.\.\.\s*$", "", title).strip()

    # Clean source suffixes
    source_suffixes = [
        r"\s*-\s*ResearchGate(?:\s*\(PDF\))?$",
        r"\s*-\s*arXiv(?:\s*\(PDF\))?$",
        r"\s*-\s*SSRN(?:\s*Electronic\s*Journal)?$",
        r"\s*-\s*MDPI$",
        r"\s*-\s*ScienceDirect$",
        r"\s*-\s*SpringerLink$",
        r"\s*-\s*Wiley\s*Online\s*Library$",
        r"\s*-\s*JSTOR$",
        r"\s*-\s*IDEAS/RePEc$",
        r"\s*-\s*RePEc$",
        r"\s*-\s*NBER$",
        r"\s*-\s*AQR\s*Capital\s*Management$",
        r"\s*-\s*AQR$",
        r"\s*-\s*Cboe(?:\s*Global\s*Markets)?$",
        r"\s*-\s*CME\s*Group$",
        r"\s*\|\s*CME\s*Group$",
        r"\s*-\s*Bank\s*for\s*International\s*Settlements$",
        r"\s*-\s*Federal\s*Reserve\s*Bank.*$",
        r"\s*-\s*Columbia\s*Business\s*School$",
        r"\s*-\s*NYU\s*Tandon.*$",
        r"\s*-\s*CBS\s*Research\s*Portal$",
        r"\s*-\s*InK@SMU.*$",
        r"\s*-\s*Portfolio\s*Management\s*Research$",
        r"\s*\|\s*Portfolio\s*Management\s*Research$",
        r"\s*-\s*CORE$",
        r"\s*-\s*OpenReview$",
        r"\s*-\s*Alpha\s*Architect$",
        r"\s*-\s*PLOS$",
        r"\s*-\s*American\s*Economic\s*Association$",
        r"\s*\|\s*Request\s*PDF$",
        r"\s*\|\s*Semantic\s*Scholar$",
        r"\s*-\s*Publications\s*-\s*World\s*Economic\s*Forum.*$",
        r"\s*-\s*World\s*Economic\s*Forum.*$",
        r"\s*-\s*Hugging\s*Face$",
        r"\s*-\s*J\.?P\.?\s*Morgan$",
        r"\s*\|\s*J\.?P\.?\s*Morgan.*$",
        r"\s*-\s*Marcos\s*M\.?\s*Lopez\s*de\s*Prado$",
        r"\s*-\s*Federal\s*\.\.\.$",
        r"\s*-\s*Bayes\s*Business\s*School$",
        r"\s*-\s*UC\s*Berkeley\s*EECS$",
        r"\s*-\s*GOV\.UK$",
        r"\s*\|\s*FINRA\.org$",
        r"\s*-\s*Winter\s*Simulation\s*Conference$",
    ]
    for pattern in source_suffixes:
        title = re.sub(pattern, "", title, flags=re.I).strip()

    title = title.strip(" -–—,;:\'\"")
    if len(title) < 5 or title.lower().startswith("http") or title.lower().startswith("www."):
        return None

    lower_t = title.lower()
    if lower_t in [
        "table of contents", "references", "works cited", "introduction",
        "conclusion", "abstract", "research", "search", "publications"
    ]:
        return None
    if "client specifications" in lower_t or "interface specification" in lower_t:
        return None

    return title


def normalize_title(t: str) -> str:
    """Normalize paper title for deduplication."""
    s = re.sub(r"\s*\(\d+\)\s*$", "", t)
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.lower().split())


def format_markdown_cell(s: str) -> str:
    """Escape markdown pipes and strip newlines."""
    return s.replace("|", "\\|").replace("\n", " ").strip()


def build_why_sentence(title: str, tags: str) -> str:
    """Generate a clean, professional sentence explaining why the paper is worth getting."""
    primary_tag = tags.split(",")[0].strip().replace("-", " ") if tags else "quantitative finance"
    return f"Cited in research on {primary_tag}; investigates {title}."


def update_candidates_file(
    candidates_file: Path,
    candidates: list[dict],
    dry_run: bool = False,
) -> tuple[int, int]:
    """Update FOLLOWUP-CANDIDATES.md with new and merged candidate rows."""
    if not candidates_file.exists():
        raise FileNotFoundError(f"Candidates file not found: {candidates_file}")

    content = candidates_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Parse existing candidate rows
    existing_by_norm_title: dict[str, dict] = {}
    table_start_idx = -1
    passed_on_idx = -1

    for idx, line in enumerate(lines):
        if line.startswith("| Title (best guess)"):
            table_start_idx = idx
        elif line.startswith("## Passed on"):
            passed_on_idx = idx
        elif table_start_idx != -1 and passed_on_idx == -1 and line.startswith("|") and not line.startswith("| :---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 6:
                norm_t = normalize_title(parts[0])
                existing_by_norm_title[norm_t] = {
                    "line_idx": idx,
                    "title": parts[0],
                    "authors_year": parts[1],
                    "why": parts[2],
                    "tags": parts[3],
                    "surfaced_by": parts[4],
                    "doc_id": parts[5],
                    "status": parts[6] if len(parts) > 6 else "",
                }

    merged_count = 0
    new_rows_to_insert: list[str] = []

    for cand in candidates:
        norm_t = normalize_title(cand["title"])
        article_links_str = ", ".join(cand["surfaced_by"])
        doc_ids_str = ", ".join(cand["doc_ids"])

        if norm_t in existing_by_norm_title:
            # Merge with existing row
            ex = existing_by_norm_title[norm_t]
            line_idx = ex["line_idx"]

            # Merge surfaced_by
            existing_surfaced = [s.strip() for s in ex["surfaced_by"].split(",") if s.strip()]
            for link in cand["surfaced_by"]:
                if link not in existing_surfaced:
                    existing_surfaced.append(link)
            new_surfaced_str = ", ".join(existing_surfaced)

            # Merge doc_ids
            existing_docs = [d.strip() for d in ex["doc_id"].split(",") if d.strip()]
            for did in cand["doc_ids"]:
                if did and did not in existing_docs:
                    existing_docs.append(did)
            new_docs_str = ", ".join(existing_docs)

            # Update line in lines
            lines[line_idx] = (
                f"| {format_markdown_cell(ex['title'])} "
                f"| {format_markdown_cell(ex['authors_year'])} "
                f"| {format_markdown_cell(ex['why'])} "
                f"| {format_markdown_cell(ex['tags'] or cand['tags'])} "
                f"| {format_markdown_cell(new_surfaced_str)} "
                f"| {format_markdown_cell(new_docs_str)} "
                f"| {format_markdown_cell(ex['status'])} |"
            )
            merged_count += 1
        else:
            why_sentence = build_why_sentence(cand["title"], cand["tags"])
            row_str = (
                f"| {format_markdown_cell(cand['title'])} "
                f"| "
                f"| {format_markdown_cell(why_sentence)} "
                f"| {format_markdown_cell(cand['tags'])} "
                f"| {format_markdown_cell(article_links_str)} "
                f"| {format_markdown_cell(doc_ids_str)} "
                f"| |"
            )
            new_rows_to_insert.append(row_str)

    # Insert new rows before '## Passed on'
    if not dry_run:
        target = "## Passed on"
        current_text = "\n".join(lines)
        if target in current_text:
            parts = current_text.split(target, 1)
            new_content = (
                parts[0].rstrip()
                + "\n"
                + "\n".join(new_rows_to_insert)
                + "\n\n"
                + target
                + parts[1]
            )
        else:
            new_content = current_text.rstrip() + "\n" + "\n".join(new_rows_to_insert) + "\n"

        candidates_file.write_text(new_content, encoding="utf-8")

    return len(new_rows_to_insert), merged_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--articles-dir",
        type=Path,
        default=DEFAULT_ARTICLES_DIR,
        help=f"Path to article TS directory (default: {DEFAULT_ARTICLES_DIR})",
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
        "--delay",
        type=float,
        default=0.35,
        help="Delay in seconds between fetches (default: 0.35)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and filter without writing to FOLLOWUP-CANDIDATES.md",
    )

    args = parser.parse_args()
    start_time = time.time()

    research_papers_state = load_classified_research_papers(args.state_file)
    print(f"Loaded {len(research_papers_state)} research-paper entries from state.")

    target_slugs = set(research_papers_state.keys())
    articles_meta = load_article_metadata(args.articles_dir, target_slugs)
    doc_ids = load_doc_ids(args.matches)

    print(f"Fetching citations across {len(articles_meta)} published Google Docs...")

    raw_citations: list[dict] = []
    for idx, (slug, art_info) in enumerate(articles_meta.items(), 1):
        url = art_info.get("google_doc")
        if not url:
            print(f"[{idx}/{len(articles_meta)}] {slug}: No published URL, skipping.")
            continue

        print(f"[{idx}/{len(articles_meta)}] Fetching citations for {slug}...")
        extracted = fetch_published_doc_citations(url)
        doc_id = doc_ids.get(slug, "")
        tags = research_papers_state[slug].get("tags", "")

        for item in extracted:
            raw_citations.append(
                {
                    "slug": slug,
                    "article_title": art_info["title"],
                    "doc_id": doc_id,
                    "raw_text": item["raw_text"],
                    "url": item["url"],
                    "tags": tags,
                }
            )

        if args.delay > 0:
            time.sleep(args.delay)

    print(f"\nExtracted {len(raw_citations)} total raw citation items.")

    # Filter and deduplicate
    candidates_map: dict[str, dict] = {}
    filtered_out_count = 0

    for c in raw_citations:
        url = c.get("url", "")
        raw_text = c.get("raw_text", "")
        ok, reason = is_research_quality(url, raw_text)
        if not ok:
            filtered_out_count += 1
            continue

        title = clean_paper_title(raw_text)
        if not title:
            filtered_out_count += 1
            continue

        norm_t = normalize_title(title)
        article_link = f"[{c['article_title']}](https://www.sophie-ai-finance.com/articles/{c['slug']})"
        doc_id = c["doc_id"]

        if norm_t not in candidates_map:
            candidates_map[norm_t] = {
                "title": title,
                "url": url,
                "tags": c.get("tags", ""),
                "surfaced_by": [article_link],
                "doc_ids": [doc_id] if doc_id else [],
                "slugs": [c["slug"]],
            }
        else:
            if article_link not in candidates_map[norm_t]["surfaced_by"]:
                candidates_map[norm_t]["surfaced_by"].append(article_link)
                if doc_id and doc_id not in candidates_map[norm_t]["doc_ids"]:
                    candidates_map[norm_t]["doc_ids"].append(doc_id)
                candidates_map[norm_t]["slugs"].append(c["slug"])

    candidates_list = list(candidates_map.values())
    print(f"Passed quality filter: {len(candidates_list)} unique research paper candidates.")
    print(f"Filtered out {filtered_out_count} non-research / unparseable items.")

    multi_source = [c for c in candidates_list if len(c["surfaced_by"]) > 1]
    print(f"Multi-source candidates (cited across >1 article): {len(multi_source)}")

    if args.dry_run:
        print(f"\n[Dry Run] Would insert {len(candidates_list)} candidates to {args.candidates_file}")
    else:
        new_added, merged = update_candidates_file(args.candidates_file, candidates_list)
        print(f"\nSuccessfully added {new_added} new candidate rows and merged {merged} rows in {args.candidates_file}")

    print(f"Completed in {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()

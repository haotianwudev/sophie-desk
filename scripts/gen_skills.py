#!/usr/bin/env python3
"""Regenerate the skill catalogue from the real skill files.

Reads every SKILL.md we can find, pulls its frontmatter, and writes:
  skills/<name>.md   one card per skill (frontmatter -> Dataview in Obsidian)
  Skills.md          the classified index, relative-linked so it is clickable
                     both on the GitHub repo page and inside the vault

Re-run after adding or moving a skill. Nothing here is hand-maintained.
"""

from __future__ import annotations
import pathlib, re, datetime

VAULT = pathlib.Path(__file__).resolve().parent.parent
HOME_SKILLS = pathlib.Path.home() / ".claude" / "skills"
WORKSPACE = pathlib.Path("F:/workspace")
REPOS = [
    "sophie-pipeline",
    "ai-stock-suggestion-server",
    "ai-stock-suggestion-client",
    "sophie-option-research",
    "sophie-desk",
]

# name -> (kind, role, tier)
#   kind: guide | workflow | task | hybrid
#   role: architect quant integrator scribe ui auditor watchman librarian ops
#   tier: claude | agy | either | ollama
CLASSIFY = {
    "sophie-develop-guide":          ("guide",    "architect",  "claude"),
    "sophie-option-research-guide":  ("hybrid",   "architect",  "claude"),
    "sophie-agent-dev":              ("guide",    "architect",  "claude"),
    "sophie-desk":                    ("guide",    "architect",  "either"),

    "option-research-explain":       ("workflow", "quant",      "claude"),
    "investment-clock-analyze":      ("workflow", "quant",      "claude"),
    "investment-clock-analysis":     ("workflow", "quant",      "claude"),

    "sophie-donate-tiering-resume":  ("task",     "integrator", "claude"),
    "sophie-spx-write-conditions":   ("task",     "architect",  "claude"),
    "spx-option-backfill":           ("task",     "ops",        "claude"),

    "sophie-article":                ("workflow", "scribe",     "agy"),
    "sophie-brainstorm":             ("workflow", "scribe",     "agy"),
    "sophie-add-to-topic":           ("workflow", "scribe",     "agy"),
    "sophie-youtube-video":          ("workflow", "scribe",     "agy"),
    "investment-clock-prompt":       ("workflow", "scribe",     "agy"),
    "subtitle":                      ("workflow", "scribe",     "agy"),
    "intro-gen":                     ("workflow", "scribe",     "agy"),
    "intro-manim":                   ("workflow", "scribe",     "agy"),

    "sophie-option-strategy":        ("workflow", "ui",         "agy"),
    "sophie-article-style-audit":    ("hybrid",   "auditor",    "agy"),
    "sophie-next-article":           ("workflow", "auditor",    "agy"),
    "sophie-etl-tracker":            ("workflow", "watchman",   "agy"),
    "notebooklm":                    ("workflow", "librarian",  "agy"),

    "option-research-notebook":      ("workflow", "ops",        "either"),
    "tailscale-ssh":                 ("workflow", "ops",        "either"),
}

ROLE_ORDER = [
    ("architect",  "Architect",     "Feature design across repos; Pattern A/B calls, schema, migrations."),
    ("quant",      "Quant reviewer","The only role that may advance a study past G2."),
    ("integrator", "Integrator",    "Wiring research into the site. Highest blast radius."),
    ("librarian",  "Librarian",     "Literature in, testable hypotheses out."),
    ("scribe",     "Scribe",        "Articles, video, subtitles, social copy."),
    ("ui",         "UI builder",    "Frontend against an existing spec and design system."),
    ("auditor",    "Auditor",       "Repeatable conformance sweeps."),
    ("watchman",   "Watchman",      "Pipeline health."),
    ("ops",        "Ops",           "Machine, access, long-running jobs."),
]

KIND_NOTE = {
    "guide":    "reference — stable, read before building",
    "workflow": "does a thing — invoked repeatedly",
    "task":     "**really a task** — belongs in `tasks/`, not here",
    "hybrid":   "**mixed** — stable guide plus a rotting status block; split it",
}

FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def read_front(p: pathlib.Path) -> dict:
    m = FM.match(p.read_text(encoding="utf-8", errors="replace"))
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^[a-zA-Z_-]+:", line):
            key, _, val = line.partition(":")
            key = key.strip()
            out[key] = val.strip().strip('"').strip("'")
        elif key and line.startswith(("  ", "\t")):
            out[key] += " " + line.strip()
    return out


def discover() -> list[dict]:
    found = {}
    seen_paths = []

    for d in sorted(HOME_SKILLS.glob("*/")):
        for fn in ("SKILL.md", "skill.md"):
            f = d / fn
            if f.exists():
                seen_paths.append((d.name, f, "~/.claude/skills", None))
                break

    for repo in REPOS:
        base = WORKSPACE / repo / ".agents" / "skills"
        if not base.is_dir():
            continue
        for d in sorted(base.glob("*/")):
            for fn in ("SKILL.md", "skill.md"):
                f = d / fn
                if f.exists():
                    seen_paths.append((d.name, f, f"{repo}/.agents/skills", repo))
                    break

    for name, f, home, repo in seen_paths:
        fm = read_front(f)
        desc = fm.get("description", "").strip()
        if not desc:
            continue
        kind, role, tier = CLASSIFY.get(name, ("workflow", "ops", "either"))
        rec = found.setdefault(name, {
            "name": name, "desc": desc, "kind": kind, "role": role,
            "tier": tier, "homes": [], "lines": 0, "repo": repo,
        })
        rec["homes"].append(home)
        rec["lines"] = max(rec["lines"], len(f.read_text(encoding="utf-8", errors="replace").splitlines()))
    return sorted(found.values(), key=lambda r: r["name"])


def short(desc: str, n: int = 180) -> str:
    desc = " ".join(desc.split())
    return desc if len(desc) <= n else desc[: n - 1].rsplit(" ", 1)[0] + "…"


def write_cards(skills: list[dict]) -> None:
    out = VAULT / "skills"
    out.mkdir(exist_ok=True)
    for s in skills:
        shared = any("agents/skills" in h for h in s["homes"])
        (out / f"{s['name']}.md").write_text(
            "---\n"
            f"name: {s['name']}\n"
            f"kind: {s['kind']}\n"
            f"role: {s['role']}\n"
            f"tier: {s['tier']}\n"
            f"lines: {s['lines']}\n"
            f"shared: {'true' if shared else 'false'}\n"
            "---\n\n"
            f"# {s['name']}\n\n"
            f"{short(s['desc'], 600)}\n\n"
            f"- **Kind** — {KIND_NOTE[s['kind']]}\n"
            f"- **Role** — {s['role']}\n"
            f"- **Runs as** — {s['tier']}\n"
            f"- **Lives in** — {', '.join(f'`{h}`' for h in s['homes'])}\n"
            f"- **Size** — {s['lines']} lines\n\n"
            + ("> [!warning] Not visible to both agents\n"
               "> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's\n"
               "> `.agents/skills/` to share it.\n" if not shared else "")
            + ("\n> [!note] This is a task wearing a skill's clothing\n"
               "> Move its state to `tasks/` and leave only the reusable how-to behind.\n"
               if s["kind"] in ("task", "hybrid") else ""),
            encoding="utf-8",
        )


def write_index(skills: list[dict]) -> None:
    n = len(skills)
    shared = sum(1 for s in skills if any("agents/skills" in h for h in s["homes"]))
    tasks = [s for s in skills if s["kind"] in ("task", "hybrid")]

    L = []
    L.append("# Skills\n")
    L.append(
        "Generated by `scripts/gen_skills.py` — re-run it, don't edit this file.\n"
        "Links are relative markdown so they resolve both on the GitHub page and in the vault.\n"
    )
    L.append(
        f"**{n} skills** · {shared} shared with agy, {n - shared} Claude-only · "
        f"{len(tasks)} are really tasks\n"
    )

    L.append("\n## By role\n")
    for key, title, blurb in ROLE_ORDER:
        rows = [s for s in skills if s["role"] == key]
        if not rows:
            continue
        L.append(f"\n### {title}\n\n{blurb}\n")
        L.append("| Skill | Kind | Runs as | Shared | What it does |")
        L.append("|---|---|---|---|---|")
        for s in rows:
            sh = "yes" if any("agents/skills" in h for h in s["homes"]) else "**no**"
            kind = s["kind"] if s["kind"] not in ("task", "hybrid") else f"**{s['kind']}**"
            L.append(
                f"| [{s['name']}](skills/{s['name']}.md) | {kind} | {s['tier']} | {sh} | {short(s['desc'], 130)} |"
            )

    if tasks:
        L.append("\n## Migrate these\n")
        L.append(
            "A skill answers *how do I do X*; a task answers *where did I get to on X*. "
            "These carry live state and belong in `tasks/`.\n"
        )
        L.append("| Skill | Lines | Why |")
        L.append("|---|---|---|")
        for s in sorted(tasks, key=lambda r: -r["lines"]):
            why = "task in skill clothing" if s["kind"] == "task" else "stable guide + rotting status block"
            L.append(f"| [{s['name']}](skills/{s['name']}.md) | {s['lines']} | {why} |")

    L.append("\n## Not shared with agy\n")
    orphans = [s for s in skills if not any("agents/skills" in h for h in s["homes"])]
    L.append(
        f"{len(orphans)} skills live only in `~/.claude/skills/`, so only Claude Code can "
        "invoke them. Moving one into a repo's `.agents/skills/` puts it in git and gives both "
        "agents the same capability.\n"
    )

    L.append("\n---\n")
    L.append("## Obsidian views\n")
    L.append("<!-- these render as tables in Obsidian, and as code blocks on GitHub -->\n")
    L.append("```dataview\nTABLE WITHOUT ID link(file.link, name) AS \"Skill\", kind, tier, lines\n"
             "FROM \"skills\"\nWHERE kind = \"task\" OR kind = \"hybrid\"\nSORT lines DESC\n```\n")
    L.append("```dataview\nTABLE WITHOUT ID link(file.link, name) AS \"Skill\", role, tier\n"
             "FROM \"skills\"\nWHERE shared = false\nSORT role ASC\n```\n")
    L.append(f"\n<sub>Generated {datetime.date.today().isoformat()}</sub>\n")

    (VAULT / "Skills.md").write_text("\n".join(L), encoding="utf-8")


def sync_claude_mirror() -> None:
    """.agents/skills/sophie-desk/SKILL.md is canonical (shared with agy).
    Claude Code's own project-skill discovery reads .claude/skills/, not
    .agents/skills/ -- confirmed by the real, working example in
    ai-stock-suggestion-client, and by this skill being invisible to Claude
    Code until this mirror was added. A hard link was tried first and
    rejected: git checkout replaces a file's inode rather than editing it in
    place, silently breaking the link with no error -- worse than a plain
    copy, since a copy's staleness is at least visible in a diff. So: plain
    copy, kept in sync by re-running this script, same as everything else
    here. Never hand-edit .claude/skills/sophie-desk/SKILL.md directly."""
    src = VAULT / ".agents" / "skills" / "sophie-desk" / "SKILL.md"
    dst = VAULT / ".claude" / "skills" / "sophie-desk" / "SKILL.md"
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    content = src.read_text(encoding="utf-8")
    if not dst.exists() or dst.read_text(encoding="utf-8") != content:
        # newline="\n" forces LF on write regardless of platform -- without it,
        # Windows' default text-mode write reintroduces CRLF even though the
        # in-memory string was already normalized to \n by read_text(),
        # producing a real diff that isn't a real content difference.
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("synced .claude/skills/sophie-desk/SKILL.md from .agents/ copy")


if __name__ == "__main__":
    sk = discover()
    write_cards(sk)
    write_index(sk)
    sync_claude_mirror()
    print(f"{len(sk)} skills -> Skills.md + skills/*.md")
    for s in sk:
        if s["kind"] in ("task", "hybrid"):
            print(f"  task-like: {s['name']} ({s['lines']} lines)")

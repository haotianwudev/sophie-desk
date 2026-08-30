#!/usr/bin/env python3
"""The supervisor: a dumb, restartable loop over tasks/*.md.

Each tick it:
  1. runs every task's probe and writes the measured result straight into that
     task's own frontmatter (progress, probe_status, updated) — never the rest
     of the file
  2. writes supervisor/status.json — a small, committed summary of what needs
     you right now, so it's visible from the phone without opening every task
  3. commits and pushes, but only if something actually changed
  4. logs a WARN line the moment a task newly enters "needs you" — no real
     notification channel is wired up yet, see the README for why

It never decides anything. It never advances a gate, promotes a study, writes
to Neon/Supabase, or touches any repo but this one. If that ever looks
tempting, that judgement belongs in a gate, not in this file — see
sophie/work-model.md.

Modeled on sophie-pipeline/data/autorun_download.sh: check real state before
touching anything, never trust a printed message over the measured evidence,
and be safe to kill and relaunch at any point because nothing lives in memory
that isn't also on disk.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
TASKS_DIR = VAULT / "tasks"
STATUS_PATH = VAULT / "supervisor" / "status.json"
PID_PATH = VAULT / "supervisor" / "supervisor.pid"
LOG_PATH = VAULT / "supervisor" / "supervisor.log"

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
NEEDS_YOU_STATUSES = {"blocked", "gate"}
PROBE_TOKEN = re.compile(r"^\s*(OK|RUN|STALL|ERROR)\b\s*(.*)$")


def log(msg: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}Z  {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------- frontmatter: read + targeted in-place update ----------

def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_-]+:", line):
            key, _, val = line.partition(":")
            val = val.strip()
            # only unwrap a quote pair that wraps the WHOLE value -- a value
            # like `probe: "C:\..." arg` has a quote only around its first
            # token, and blindly .strip('"')-ing that leaves the closing
            # quote stranded mid-string, corrupting it. Symmetric check first.
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            out[key.strip()] = val
    return out


def set_frontmatter_fields(text: str, updates: dict[str, str]) -> tuple[str, bool]:
    """Replace only the named keys' values inside the frontmatter block.
    Leaves every other line -- frontmatter or body -- byte-for-byte untouched.
    Returns (new_text, changed)."""
    m = FRONTMATTER.match(text)
    if not m:
        return text, False
    block = m.group(1)
    changed = False
    for key, val in updates.items():
        # a value MUST be single-line -- the replacement below only rewrites
        # one line's worth of text, so a multi-line value (a probe's stderr
        # can legitimately span lines) would leave its later lines behind as
        # orphaned raw text in the file, permanently. Hit live: a Windows
        # error message left "operable program or batch file." stranded as
        # its own line. Collapse all whitespace, including newlines, to one.
        val = " ".join(str(val).split())
        pattern = re.compile(rf"^({re.escape(key)}:)(.*)$", re.M)
        if pattern.search(block):
            new_block, n = pattern.subn(
                lambda mo: f"{mo.group(1)} {val}", block, count=1
            )
            if new_block != block:
                block = new_block
                changed = True
        # if the key doesn't exist in this task's frontmatter, leave it alone --
        # the supervisor fills in fields the template already promised, it
        # doesn't restructure a task file it didn't author.
    if not changed:
        return text, False
    return text[: m.start(1)] + block + text[m.end(1):], True


# ---------- probes ----------

# A task's `probe:` field is plain YAML read by Dataview too, not just this
# script -- a Windows path with spaces would need quoting that either breaks
# Dataview's real YAML parser (unlike this file's own lenient regex one) or
# stays fragile. So a probe just writes `bash <script>`, and THIS script owns
# translating "bash" into the real Git Bash binary, once, here -- no task
# frontmatter ever needs to carry a quoted path.
_BASH_CANDIDATES = [
    r"C:\Program Files\Git\bin\bash.exe",
    r"C:\Program Files (x86)\Git\bin\bash.exe",
]


def resolve_bash() -> str:
    for c in _BASH_CANDIDATES:
        if Path(c).exists():
            return c
    return "bash"  # last resort -- whatever's on PATH, may be the WSL stub


def run_probe(cmd: str, timeout: int = 90) -> tuple[str, str]:
    """Run one task's probe command. Returns (status_token, measurement).
    A probe is a contract: read-only, prints one line, exits 0. The supervisor
    trusts that contract rather than sandboxing it -- see the README.

    Parsed into a real argv list and run with shell=False -- cmd.exe's own
    shell=True quoting breaks once a quoted executable path is followed by
    further arguments, a real failure hit live once this started running
    from plain PowerShell instead of Git Bash. shlex.split(posix=False)
    treats backslashes literally, which is what a Windows path needs."""
    import shlex
    try:
        argv = shlex.split(cmd, posix=False)
        # shlex leaves matched quotes in place with posix=False; strip them
        # off each token so subprocess/CreateProcess sees the real path, not
        # a literal quote character as part of it.
        argv = [a[1:-1] if len(a) >= 2 and a[0] == a[-1] == '"' else a for a in argv]
        if argv and argv[0].lower() in ("bash", "bash.exe"):
            argv[0] = resolve_bash()
        proc = subprocess.run(
            argv, shell=False, cwd=VAULT, timeout=timeout,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired:
        return "STALL", f"probe timed out after {timeout}s"
    except Exception as e:  # noqa: BLE001 -- a broken probe is data, not a crash
        return "ERROR", f"probe failed to run: {e}"

    out = (proc.stdout or "").strip().splitlines()
    line = out[-1] if out else ""
    m = PROBE_TOKEN.match(line)
    if m:
        return m.group(1), m.group(2).strip()
    if proc.returncode != 0:
        return "ERROR", (proc.stderr or "non-zero exit, no output").strip()[:200]
    return "ERROR", f"probe printed no recognizable status: {line!r}"[:200]


# ---------- pid handling (Windows-safe, no extra dependencies) ----------

def _pid_alive(pid: int) -> bool:
    if platform.system() == "Windows":
        out = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        ).stdout
        return str(pid) in out
    try:
        import os
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def claim_singleton() -> bool:
    """Refuse to run a second loop against the same vault. Returns True if
    this process now owns the pid file."""
    import os
    if PID_PATH.exists():
        try:
            existing = int(PID_PATH.read_text().strip())
        except ValueError:
            existing = None
        if existing and _pid_alive(existing):
            log(f"another supervisor is already running (pid {existing}) -- exiting")
            return False
    PID_PATH.write_text(str(os.getpid()))
    return True


def release_singleton() -> None:
    try:
        PID_PATH.unlink(missing_ok=True)
    except Exception:  # noqa: BLE001
        pass


# ---------- dispatch to agy ----------

_AGY_CLI = r"C:\Users\lswht\AppData\Local\Programs\Antigravity IDE\bin\antigravity-ide.cmd"


def dispatch_to_agy(task_id: str) -> bool:
    """Launch agy (Antigravity) with a prompt to read and work one task.
    Fire-and-forget -- confirmed live that the CLI returns in ~2s (VS-Code-
    style launcher behavior) rather than blocking for the whole agent turn,
    so this never stalls the supervisor's own tick."""
    prompt = (
        f"Read F:\\workspace\\sophie-desk\\.agents\\skills\\sophie-desk\\SKILL.md for how "
        f"tasks work in this repo. Then read and work the task at "
        f"F:\\workspace\\sophie-desk\\tasks\\{task_id}.md -- it is assigned to you and has "
        f"just been marked active. Follow its Goal/Plan, append to its Decision log as you "
        f"go, fill in Result and set status: done when finished, commit and push."
    )
    try:
        subprocess.Popen([_AGY_CLI, "chat", "-n", "-m", "agent", prompt], cwd=VAULT)
        return True
    except Exception as e:  # noqa: BLE001
        log(f"ERROR failed to launch agy for {task_id}: {e}")
        return False


# ---------- one tick ----------

def tick(dry_run: bool = False) -> dict:
    task_files = sorted(TASKS_DIR.glob("*.md"))
    today = datetime.now().date().isoformat()

    tasks_out = []
    any_frontmatter_changed = False
    dispatched = []

    for path in task_files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        title = fm.get("title", path.stem)
        status = fm.get("status", "queued")
        probe_cmd = fm.get("probe", "none")

        probe_status, progress = (None, None)
        if probe_cmd and probe_cmd != "none":
            probe_status, progress = run_probe(probe_cmd)
            new_text, changed = set_frontmatter_fields(
                text,
                {"progress": progress, "probe_status": probe_status, "updated": today},
            )
            if changed:
                if not dry_run:
                    path.write_text(new_text, encoding="utf-8")
                any_frontmatter_changed = True
                text = new_text  # keep the in-memory copy in sync for the dispatch check below

        # Auto-dispatch: only status=queued, assignee=agy, and -- defensively,
        # even though intake should already enforce this -- never a task that
        # carries a gate. A gate is a human decision by design; an unattended
        # dispatch must never be the thing that lets one slip through.
        task_id = fm.get("id", path.stem)
        if status == "queued" and fm.get("assignee") == "agy" and not fm.get("gate"):
            if dry_run:
                log(f"DRY-RUN would dispatch to agy: {task_id} (not launched)")
            else:
                claimed_text, claimed = set_frontmatter_fields(
                    text, {"status": "active", "updated": today}
                )
                if claimed:
                    path.write_text(claimed_text, encoding="utf-8")
                    any_frontmatter_changed = True
                    status = "active"
                if dispatch_to_agy(task_id):
                    dispatched.append(task_id)
                    log(f"dispatched to agy: {task_id}")

        tasks_out.append({
            "id": fm.get("id", path.stem),
            "title": title,
            "lane": fm.get("lane", ""),
            "status": status,
            "assignee": fm.get("assignee", "none"),
            "gate": fm.get("gate", ""),
            "probe_status": probe_status or fm.get("probe_status", ""),
            "progress": progress or fm.get("progress", ""),
        })

    needs_you = [t for t in tasks_out if t["status"] in NEEDS_YOU_STATUSES]
    stalled = [t for t in tasks_out if t["probe_status"] == "STALL"]

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        "task_count": len(tasks_out),
        "needs_you": [t["id"] for t in needs_you],
        "stalled_probes": [t["id"] for t in stalled],
        "tasks": tasks_out,
    }

    # transition-based log line -- only shout when the needs-you set actually grew
    prev_needs_you = set()
    if STATUS_PATH.exists():
        try:
            prev_needs_you = set(json.loads(STATUS_PATH.read_text()).get("needs_you", []))
        except (json.JSONDecodeError, OSError):
            pass
    new_needs_you = set(summary["needs_you"]) - prev_needs_you
    if new_needs_you:
        log(f"WARN needs-you grew: {sorted(new_needs_you)} -- see supervisor/README.md, "
            f"no notification channel wired up yet")

    if not dry_run:
        STATUS_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    return summary, any_frontmatter_changed


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=VAULT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )


def commit_and_push(reason: str) -> bool:
    status = git("status", "--porcelain").stdout
    if not status.strip():
        return False
    git("add", "-A")
    msg = f"supervisor: {reason}\n\nAutomated tick. No judgement calls made -- see supervisor/README.md."
    res = git("commit", "-q", "-m", msg)
    if res.returncode != 0:
        log(f"ERROR commit failed: {res.stderr.strip()}")
        return False
    push = git("push")
    if push.returncode != 0:
        log(f"ERROR push failed (committed locally, will retry next tick): {push.stderr.strip()}")
        return True
    log(f"pushed: {reason}")
    return True


def run_once(dry_run: bool = False) -> None:
    summary, changed = tick(dry_run=dry_run)
    log(f"tick: {summary['task_count']} tasks, "
        f"{len(summary['needs_you'])} need you, {len(summary['stalled_probes'])} stalled probes")
    if dry_run:
        print(json.dumps(summary, indent=2))
        return
    if changed:
        commit_and_push(f"{len(summary['needs_you'])} need you, {len(summary['stalled_probes'])} stalled")


def run_loop(interval: int) -> None:
    if not claim_singleton():
        sys.exit(1)
    log(f"supervisor loop starting, pid {PID_PATH.read_text().strip()}, interval {interval}s")
    try:
        while True:
            try:
                run_once()
            except Exception as e:  # noqa: BLE001 -- one bad tick must not kill the loop
                log(f"ERROR tick failed, will retry next interval: {e}")
            time.sleep(interval)
    except KeyboardInterrupt:
        log("supervisor loop stopped (KeyboardInterrupt)")
    finally:
        release_singleton()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--once", action="store_true", help="run a single tick and exit")
    ap.add_argument("--loop", action="store_true", help="run forever, ticking every --interval seconds")
    ap.add_argument("--interval", type=int, default=1800, help="seconds between ticks in --loop mode (default 1800 = 30 min)")
    ap.add_argument("--dry-run", action="store_true", help="print what would change; touch nothing on disk, commit nothing")
    args = ap.parse_args()

    if args.loop:
        run_loop(args.interval)
    else:
        run_once(dry_run=args.dry_run)

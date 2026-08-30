# Runbook

Exact commands for things you'll do repeatedly. Pulled from the skills that already document
each one — this file is a shortcut to the command, not a replacement for the skill's full
context. When a command changes, fix it here **and** in the source skill listed alongside it.

---

## The backfill (ThetaData download)

**Source skill:** `spx-option-backfill` · **Task:** [tasks/spx-option-backfill.md](tasks/spx-option-backfill.md)

Check first — don't relaunch blind. A "killed" notification has been wrong before; the log and
file counts are ground truth, not the notification:
```bash
bash probes/spx-option-backfill.sh
```

If nothing is actually running, relaunch the self-healing wrapper (safe to re-run any time —
it resumes from whatever's already on disk):
```bash
cd /f/workspace/sophie-pipeline
bash data/autorun_download.sh
```

Confirm the ThetaData Terminal itself is actually answering (port **25503**, not the 25510 the
public docs describe):
```bash
curl "http://localhost:25503/v3/option/history/eod?symbol=SPX&expiration=20240119&start_date=20240102&end_date=20240102"
```

If the Terminal is down, **you** relaunch it (Claude Code should never see the password) — in
its own window:
```powershell
cd C:\Users\lswht\Downloads
java -jar ThetaTerminalv3.jar --creds-file creds.txt
```

Before relaunching anything on a "stopped"/"killed" signal, verify nothing survived as a stray
process (Windows can leave a backgrounded `python.exe` running after its shell wrapper dies):
```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select ProcessId,CreationDate,CommandLine
Stop-Process -Id <id> -Force    # only if a genuine stale duplicate is found
```

---

## Sophie Agent dev servers (the chat widget)

**Source skill:** `sophie-agent-dev`

Two servers, both local-only:
```bash
# terminal 1 — AG-UI server, port 8000
cd /f/workspace/sophie-pipeline
poetry run python sophie_agent/serve.py --reload

# terminal 2 — Next.js client, port 3000
cd /f/workspace/ai-stock-suggestion-client
npm run dev
```
Needs `NEXT_PUBLIC_ENABLE_CHAT=true` and `NEXT_PUBLIC_AGENT_API_URL=http://localhost:8000` in
the client's `.env`.

Quick CLI checks without the browser:
```bash
cd /f/workspace/sophie-pipeline
poetry run python sophie_agent/run.py --list-agents         # profiles + toolkits + models
poetry run python sophie_agent/run.py --agent supervisor    # REPL against one profile
poetry run python sophie_agent/run.py --check-models        # live-probes Ollama, tool-calling support
```

---

## Remote JupyterLab for sophie-option-research (phone access)

**Source skill:** `option-research-notebook`

Token is stable across restarts, stored at `C:\Users\lswht\.claude\skills\option-research-notebook\.token`
— read it before generating a new one.
```bash
cd /f/workspace/sophie-option-research
PYTHONPATH=src ./.venv/Scripts/python.exe -m jupyter lab \
  --ServerApp.token=<TOKEN> \
  # (see the skill for the full flag set — bind address, port 8888, etc.)
  > "C:\Users\lswht\AppData\Local\Temp\claude\jupyter-option-research.log" 2>&1
```
One-time firewall rule (admin):
```powershell
New-NetFirewallRule -Name jupyterlab -DisplayName 'JupyterLab (8888)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8888
```
Link to open on the phone: `http://<tailscale-ip>:8888/lab?token=<TOKEN>`

---

## SSH from the phone (Tailscale + ConnectBot)

**Source skill:** `tailscale-ssh`

Confirm Tailscale and get the IP:
```powershell
"/c/Program Files/Tailscale/tailscale.exe" status
"/c/Program Files/Tailscale/tailscale.exe" ip -4
```
Confirm the SSH server is up:
```powershell
Get-Service sshd | Select-Object Status, StartType
Start-Service sshd    # if not Running
```
One-time firewall rule (admin):
```powershell
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```
Connect from the phone: `ssh <username>@<tailscale-hostname-or-ip>`

---

## Frontend: local vs. prod GraphQL

**Source skill:** `sophie-develop-guide`

```bash
cd /f/workspace/ai-stock-suggestion-client
npm run use:local-gql    # point at a local GraphQL server for dev
npm run use:prod-gql     # always switch back to this before pushing/deploying
```

---

## The supervisor

**Status: not built yet** — this is Phase 2 in [sophie/work-model.md](sophie/work-model.md), and
this entry is a placeholder for the day it exists. When it's built, fill in the actual relaunch
command here, following the same shape every other entry in this file has: how to check if it's
already running before you touch it, the exact relaunch command, and how to confirm it actually
came back up. Model it on the backfill wrapper above — that script *is* a supervisor, just for
one job — don't invent a different pattern.

---

## Adding to this file

One command block per operation, in the same shape: **source skill** (so drift gets caught),
**check-before-you-touch-it** if the operation can be running already, then the exact command.
If a command needs a secret or password, say who runs it (you, never the agent) instead of
writing the value here.

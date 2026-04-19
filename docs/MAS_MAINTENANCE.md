# MAS Hub — Maintenance Guide

**Maintainer:** Bob 🔧
**System:** MAS Hub v4.4.0
**Last Updated:** 2026-04-19

---

## System Overview

MAS Hub is a Bash + Python CLI orchestrating AI agents through a shared SQLite blackboard. The main script is `bin/mas` (~1500 lines). Runtime data lives at `~/.openclaw/mas-hub/` and is never part of the repo.

```
User → mas CLI (bin/mas)
         ├── SQLite blackboard (shared_context.db)
         ├── state.json (current project + domain)
         ├── config.json (agent definitions)
         └── Agent Pool (via OpenClaw gateway)
               ├── Archie  — Facilitator / Lead
               ├── Wang    — Financial Researcher
               ├── Lynch   — Auditor
               ├── Alonzo  — Tech Strategy
               └── Bootstrap — IT Maintainer (you)
```

---

## Directory Structure

```
~/.openclaw/mas-hub/
├── blackboard/
│   ├── shared_context.db       # SQLite — all exchanges, sessions, meta
│   └── .lock                   # Lock dir (mkdir-based). Auto-removed >120s
├── state.json                  # Current project, session ID, domain
├── config.json                 # Live agent config (overrides repo config.json)
├── agent-memories/             # Per-agent daily memory: {agent}_{YYYY-MM-DD}.md
├── projects/                   # Agent output files, per project
└── logs/
    ├── orchestrator.log        # Main log
    └── kimi-maintenance.log    # Automated maintenance log

~/Projects/mas-hub/             # Source repo
├── bin/mas                     # Main orchestrator
├── scripts/mas_context.py      # Context assembly (Python)
├── config/topics.*.json        # Topic keyword configs
└── templates/domain/*.md       # Stage gate templates
```

---

## Health Check

Run this first whenever something seems broken:

```bash
mas doctor          # Full diagnostics
mas ping archie     # Roundtrip agent test
mas ping wang
mas version         # Confirm version
mas status          # Current project / session state
```

---

## Common Breakage Scenarios

### 1. Stale Lock — All commands hang or "another process is running"

The lock is a directory at `~/.openclaw/mas-hub/blackboard/.lock`. It is auto-removed if older than 120 seconds, but a crash can leave a fresh one.

```bash
# Check lock age
ls -la ~/.openclaw/mas-hub/blackboard/.lock

# Remove it
rmdir ~/.openclaw/mas-hub/blackboard/.lock
```

### 2. Agent Returns Empty Response

```bash
# Step 1: Check connectivity
mas ping wang

# Step 2: Check gateway
openclaw gateway status
openclaw gateway start      # if not running

# Step 3: Switch to a working model
mas model wang set gpt-4.1-mini
mas model wang set claude-sonnet-4.6
mas ping wang               # verify after switch
```

### 3. "mas: command not found"

```bash
# Ensure ~/bin is in PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc

# Re-run installer if symlink is missing
cd ~/Projects/mas-hub && ./install.sh

# Or symlink manually
ln -sf ~/Projects/mas-hub/bin/mas ~/bin/mas
```

### 4. Context Not Being Shared Between Agents

Symptoms: agents answer as if in a fresh conversation with no prior context.

```bash
# Check current project
mas project

# Verify database has exchanges
sqlite3 ~/.openclaw/mas-hub/blackboard/shared_context.db \
  "SELECT COUNT(*) FROM exchanges WHERE mas_session_id = (SELECT current_mas_session_id FROM mas_meta LIMIT 1);"

# If 0 exchanges — check that mas_session_id in state.json is not empty
cat ~/.openclaw/mas-hub/state.json

# If state.json is corrupted, reset
mas new <project-name>
```

### 5. Context Relevance Scoring Broken (All Scores Show 0)

This means `current_message` is not being passed to `mas_context.py`. Check the call in `bin/mas`:

```bash
grep -n "get_context_for_agent" ~/Projects/mas-hub/bin/mas
```

The call should look like:
```bash
context=$(get_context_for_agent "$CURRENT_SID" "text" "$message")
```
If `"$message"` is absent, topic/entity scoring will be dead and all exchanges will score ≤ 2.

### 6. Lead Mode Exits Too Early / [DONE] Accepted at Round 2

The premature `[DONE]` guard uses `min_rounds` and `min_tasks`. Defaults are 7 rounds / 5 tasks. Check:

```bash
grep -n "min_rounds\|min_tasks" ~/Projects/mas-hub/bin/mas
```

Override per-run:
```bash
MAS_LEAD_MIN_ROUNDS=3 MAS_LEAD_MAX_ROUNDS=8 mas lead @archie "quick test"
```

### 7. Lead Mode Hangs — Watchdog Not Firing

Lead mode has two timeouts: soft (180s) and hard (480s). If a run hangs past hard timeout without escalating to Bootstrap, the watchdog process may have died.

```bash
# Check for orphaned background processes
ps aux | grep "mas lead\|openclaw"

# Kill and restart
pkill -f "mas lead"

# Tail the log to see where it stalled
tail -50 ~/.openclaw/mas-hub/logs/orchestrator.log
```

### 8. [PAUSE] Not Prompting — Run Continues Without Waiting

The `[PAUSE]` detection uses `grep -q '\[PAUSE\]'` on lead_text. If Archie's response encoding strips brackets, the pattern won't match.

```bash
# Check what the raw response looks like
tail -100 ~/.openclaw/mas-hub/logs/orchestrator.log | grep -i pause
```

If brackets are being HTML-escaped (`&#91;PAUSE&#93;`), it's an OpenClaw response encoding issue — check the gateway version.

### 9. Domain Template Not Loading / Wrong Stage Gate

```bash
# Check current domain
cat ~/.openclaw/mas-hub/state.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('domain','not set'))"

# Check template file exists
ls ~/Projects/mas-hub/templates/domain/

# Test template loading manually
python3 -c "
with open('$HOME/Projects/mas-hub/templates/domain/finance.md') as f:
    content = f.read()
parts = content.split('---')
for p in parts:
    lines = p.strip().split('\n')
    print('SECTION:', lines[0] if lines else '(empty)')
"
```

If domain is missing from state.json, it defaults to `finance`. To set it:
```bash
mas new <project> --domain default
```

### 10. Topic Keywords Not Loading (Relevance Scoring Uses Fallback Dict)

```bash
# Verify config files exist
ls ~/Projects/mas-hub/config/topics.*.json

# Test loader directly
python3 ~/Projects/mas-hub/scripts/mas_context.py \
  ~/.openclaw/mas-hub/blackboard/shared_context.db \
  <session_id> <project> text "research earnings" finance
```

If you see `HIGH`/`MEDIUM` scores on relevant exchanges, scoring is working. If everything is `LOW`, the topic files may be missing or malformed.

```bash
python3 -c "import json; print(json.load(open('$HOME/Projects/mas-hub/config/topics.finance.json')))"
```

### 11. Database Corruption / SQLite Errors

```bash
# Integrity check
sqlite3 ~/.openclaw/mas-hub/blackboard/shared_context.db "PRAGMA integrity_check;"

# If corrupt — backup and recreate
cp ~/.openclaw/mas-hub/blackboard/shared_context.db \
   ~/.openclaw/mas-hub/blackboard/shared_context.db.bak.$(date +%Y%m%d)
rm ~/.openclaw/mas-hub/blackboard/shared_context.db
mas new <project-name>   # Re-initializes the DB
```

### 12. Agent Output Files in Wrong Location

Wang (when delegated by Archie) sometimes saves to `~/.openclaw/workspace/projects/` instead of `~/.openclaw/mas-hub/projects/<project>/`.

This is an agent instruction issue, not a system bug. Fix by re-running the task and explicitly including in the message:
> "Save all output to `~/.openclaw/mas-hub/projects/<project_name>/`"

---

## Log Maintenance

```bash
# View live log
tail -f ~/.openclaw/mas-hub/logs/orchestrator.log

# Errors only
grep ERROR ~/.openclaw/mas-hub/logs/orchestrator.log | tail -30

# Rotate logs older than 7 days
find ~/.openclaw/mas-hub/logs -name "*.log" -mtime +7 -exec gzip {} \;
find ~/.openclaw/mas-hub/logs -name "*.gz" -mtime +30 -delete
```

---

## Database Maintenance

```bash
# Row counts per session
sqlite3 ~/.openclaw/mas-hub/blackboard/shared_context.db \
  "SELECT mas_session_id, COUNT(*) as exchanges FROM exchanges GROUP BY mas_session_id ORDER BY exchanges DESC;"

# Disk usage
du -sh ~/.openclaw/mas-hub/blackboard/shared_context.db

# VACUUM (reclaim space after bulk deletes)
sqlite3 ~/.openclaw/mas-hub/blackboard/shared_context.db "VACUUM;"

# Delete exchanges from old sessions (>90 days) — careful
sqlite3 ~/.openclaw/mas-hub/blackboard/shared_context.db \
  "DELETE FROM exchanges WHERE timestamp < datetime('now', '-90 days');"
```

---

## Model Switching Reference

```bash
mas model <agent> set <alias>   # Switch model
mas models                      # Show all current models
mas ping <agent>                # Verify new model responds
```

| Alias | Model |
|-------|-------|
| `claude-opus-4` | `zenmux/anthropic/claude-opus-4` |
| `claude-sonnet-4.6` | `zenmux/anthropic/claude-sonnet-4-6` |
| `gpt-4.1-mini` | `zenmux/openai/gpt-4.1-mini` |
| `qwen-3.5-plus` | `zenmux/qwen/qwen3.5-plus` |
| `kimi` | `moonshot/kimi-k2.5` |
| `minimax` | `minimax/MiniMax-M2.7` |

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MAS_LEAD_MIN_ROUNDS` | `7` | Minimum rounds before [DONE] is accepted |
| `MAS_LEAD_MIN_TASKS` | `5` | Minimum completed tasks before [DONE] |
| `MAS_LEAD_MAX_ROUNDS` | `15` | Hard ceiling on lead mode rounds |
| `MAS_TIMEOUT` | `120` | Agent response timeout (seconds) |
| `MAS_DEBUG` | `0` | Enable debug logging |
| `TUI_MODE` | `0` | Strip ANSI, wrap output in `---[Agent]---` delimiters |

---

## Session Reset

```bash
# Reset current session (keep project, start fresh conversation)
mas reset

# Clear ALL agent sessions (agents start with no prior context)
mas session clear

# Start a brand new project
mas new <project-name> [--domain finance|default]
```

---

## config.json Reference

Live config at `~/.openclaw/mas-hub/config.json`. Repo has a reference copy at `config.json`.

Key fields per agent: `name`, `role`, `strengths` (used by `build_team_description()` to generate lead briefing), `model`, `workspace`.

After editing config, no restart needed — `bin/mas` reads it fresh each invocation.

---

## Agent Roster

| Agent | Role | Default Model | Workspace |
|-------|------|---------------|-----------|
| `archie` | Facilitator / Lead | `moonshot/kimi-k2.5` | `~/.openclaw/workspace/` |
| `wang` | Financial Researcher | `zenmux/anthropic/claude-opus-4` | `~/.openclaw/workspace-wang/` |
| `lynch` | Auditor / Validator | `zenmux/openai/gpt-4.1-mini` | `~/.openclaw/workspace-lynch/` |
| `alonzo` | Tech Strategy | `minimax/MiniMax-M2.7` | `~/.openclaw/workspace-alonzo/` |
| `bootstrap` | IT Maintainer | `zenmux/qwen/qwen3.5-plus` | `~/.openclaw/workspace-bootstrap/` |

Sample workspace configs (SOUL.md, IDENTITY.md, MEMORY.md): `~/Projects/mas-hub/agents/`

---

*Maintained by Bootstrap 🔧 — update this file whenever a new failure mode is discovered.*

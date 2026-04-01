# MAS Hub — System Requirements

**Version:** 1.0.0  
**Last Updated:** 2026-04-01

---

## Core Dependencies

### 1. OpenClaw CLI (Required)

**Minimum Version:** `2026.3.12`  
**Recommended:** Latest stable release

**Installation:**
```bash
# Install via npm (if not already installed)
npm install -g openclaw

# Verify installation
openclaw --version
```

**Configuration:**
MAS Hub requires OpenClaw to be configured with:
- Gateway daemon running (`openclaw gateway status`)
- At least one agent configured in `~/.openclaw/openclaw.json`
- Valid API keys for your chosen models

**Check OpenClaw Health:**
```bash
openclaw health
```

---

### 2. Python 3 (Required)

**Minimum Version:** Python 3.8  
**Recommended:** Python 3.11+

**Verify Installation:**
```bash
python3 --version
```

**Required Modules:** (all part of Python standard library)
- `sqlite3` — Blackboard database
- `json` — Configuration and data exchange
- `datetime` — Timestamp handling
- `uuid` — Unique ID generation
- `re` — Pattern matching for task parsing
- `textwrap` — Text summarization
- `os` — Filesystem operations
- `sys` — System utilities

**No pip packages required** — MAS Hub uses only Python standard library.

---

### 3. Bash Shell (Required)

**Minimum Version:** Bash 3.2  
**Recommended:** Bash 5.0+

**Verify Installation:**
```bash
bash --version
```

**Note:** macOS ships with Bash 3.2 due to licensing. This is sufficient for MAS Hub.

---

### 4. SQLite3 (Required)

**Minimum Version:** SQLite 3.28  
**Recommended:** Latest stable

**Verify Installation:**
```bash
sqlite3 --version
```

**Note:** SQLite is included with macOS and most Linux distributions.

---

## Optional Dependencies

### Kimi Code CLI (Recommended for Maintenance)

**Version:** 1.23.0+  
**Purpose:** Automated IT maintenance, log rotation, config validation

**Installation:**
```bash
# Install via uv (Python package manager)
uv tool install kimi-cli

# Verify installation
kimi --version
```

**Documentation:** https://moonshotai.github.io/kimi-cli/

**Usage:**
```bash
# Run daily maintenance
~/Projects/mas-hub/bin/kimi-daily-maintenance.sh

# Ad-hoc maintenance task
kimi-maintenance "Rotate logs older than 7 days"
```

---

### Git (Recommended)

**Purpose:** Version control, tracking config changes, updating MAS Hub

**Installation:**
```bash
# macOS (if not already installed)
xcode-select --install

# Verify installation
git --version
```

---

## Model Requirements

MAS Hub supports any model available through OpenClaw. Recommended configurations:

| Agent | Recommended Model | Purpose |
|-------|------------------|---------|
| **Archie** (Facilitator) | `minimax/MiniMax-M2.7` or `moonshot/kimi-k2.5` | Strong reasoning, task orchestration |
| **Wang** (Researcher) | `zenmux/anthropic/claude-opus-4.6` or `minimax/MiniMax-M2.7` | Deep research, financial analysis |
| **Lynch** (Auditor) | `zenmux/z-ai/glm-5-turbo` or `zenmux/openai/gpt-4.1-mini` | Detail-oriented validation |
| **Bootstrap** (Maintainer) | `zenmux/qwen/qwen3.5-plus` | Technical troubleshooting |
| **Alonzo** (Tech Strategy) | `minimax/MiniMax-M2.7` | Strategic technical analysis |

**Model Aliases:** MAS Hub includes built-in aliases for common models:
- `claude-opus-4.6` → `zenmux/anthropic/claude-opus-4.6`
- `gpt-5.4` → `zenmux/openai/gpt-5.4`
- `qwen-3.5-plus` → `zenmux/qwen/qwen3.5-plus`
- `glm-5-turbo` → `zenmux/z-ai/glm-5-turbo`
- And 10+ more (see `mas help`)

---

## System Resources

### Disk Space

| Component | Size |
|-----------|------|
| MAS Hub source code | ~5 MB |
| SQLite blackboard (typical) | 10-50 MB |
| Agent memories (daily) | 1-5 MB/day |
| Logs (30-day retention) | 50-200 MB |
| **Total (typical)** | **~300 MB** |

### Memory

- **MAS CLI:** Negligible (bash script)
- **Python helpers:** ~50-100 MB during execution
- **SQLite operations:** ~20-50 MB

### Network

- Required for agent model API calls (via OpenClaw Gateway)
- No direct external API calls from MAS Hub itself
- All model traffic routed through OpenClaw Gateway

---

## Directory Structure

MAS Hub expects the following layout:

```
~/Projects/mas-hub/              # Project source (git repo)
  bin/
    mas                          # Main MAS CLI
    mas-tui                      # TUI wrapper
    kimi-maintenance             # Kimi Code wrapper
    kimi-daily-maintenance.sh    # Daily maintenance script
  ontology/
    mas-ontology.md              # Agent roles & protocols
  scripts/
    context_maintenance.py       # Adaptive context assembly
    mas_context.py               # Context retrieval
    read_pdf.py                  # PDF reading utility
  docs/                          # Documentation
  templates/                     # Message templates
  config.json                    # Reference configuration
  README.md                      # This file
  REQUIREMENTS.md                # System requirements
  install.sh                     # Installation script

~/.openclaw/mas-hub/             # Runtime data (auto-created)
  blackboard/shared_context.db   # SQLite blackboard
  agent-memories/                # Daily MAS memory files
  logs/                          # Orchestrator logs
  inbox/ outbox/ workflows/      # Message queues
  state.json                     # Current project/session state
  config.json                    # Live agent configuration
```

---

## Pre-Installation Checklist

Before installing MAS Hub, verify:

- [ ] OpenClaw CLI installed and configured (`openclaw --version`)
- [ ] OpenClaw Gateway running (`openclaw health`)
- [ ] At least one agent configured in OpenClaw
- [ ] Python 3.8+ available (`python3 --version`)
- [ ] Bash shell available (`bash --version`)
- [ ] SQLite3 available (`sqlite3 --version`)
- [ ] Git installed (optional, for updates) (`git --version`)
- [ ] Kimi Code CLI installed (optional, for maintenance) (`kimi --version`)

---

## Troubleshooting

### "openclaw: command not found"

**Solution:** Install OpenClaw CLI:
```bash
npm install -g openclaw
```

### "python3: command not found"

**Solution:** Install Python 3:
- **macOS:** `brew install python3`
- **Linux:** `sudo apt install python3` or `sudo dnf install python3`

### "SQLite3 not found"

**Solution:** Install SQLite3:
- **macOS:** Pre-installed
- **Linux:** `sudo apt install sqlite3` or `sudo dnf install sqlite3`

### "Gateway not responding"

**Solution:** Start OpenClaw Gateway:
```bash
openclaw gateway start
```

### Agent model unavailable

**Solution:** Check model configuration:
```bash
mas models
mas model <agent> set <alias>
```

---

## Support

- **Documentation:** `~/Projects/mas-hub/docs/`
- **Ontology:** `~/Projects/mas-hub/ontology/mas-ontology.md`
- **Incident Reports:** `~/Projects/mas-hub/docs/incident-*.md`
- **GitHub:** (TBD — release repo)
- **Discord:** https://discord.com/invite/clawd

---

*MAS Hub is designed to be lightweight and dependency-minimal. If you have OpenClaw running, you likely already meet all requirements.*

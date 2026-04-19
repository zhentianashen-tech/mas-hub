# MAS Hub — System Requirements

**Version:** 1.1.0  
**Last Updated:** 2026-04-19

---

## Core Dependencies

### 1. Hermes Agent (Required)

**Minimum Version:** `0.10.0`  
**Recommended:** Latest stable release

**Installation:**
```bash
# Install via uv (recommended)
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all]"

# Verify installation
hermes version
```

**Configuration:**
MAS Hub requires Hermes to be configured with:
- Valid API keys in `~/.hermes/.env` (e.g., `OPENROUTER_API_KEY`)
- Hermes profiles created for each agent (done automatically by `install.sh`)

**Check Hermes Health:**
```bash
hermes doctor
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

MAS Hub supports any model available through Hermes Agent (OpenRouter, Anthropic, OpenAI, Ollama, etc.). Recommended configurations:

| Agent | Recommended Model | Purpose |
|-------|------------------|---------|
| **Archie** (Facilitator) | `qwen/qwen3.6-plus` or `moonshot/kimi-k2.5` | Strong reasoning, task orchestration |
| **Wang** (Researcher) | `anthropic/claude-opus-4` or `anthropic/claude-opus-4.6` | Deep research, financial analysis |
| **Lynch** (Auditor) | `openai/gpt-4.1-mini` or `z-ai/glm-5-turbo` | Detail-oriented validation |
| **Bootstrap** (Maintainer) | `qwen/qwen3.5-plus` | Technical troubleshooting |
| **Alonzo** (Tech Strategy) | `minimax/MiniMax-M2.7` | Strategic technical analysis |

**Model Aliases:** MAS Hub includes built-in aliases for common models:
- `claude-opus-4.6` → `anthropic/claude-opus-4.6`
- `gpt-5.4` → `openai/gpt-5.4`
- `qwen-3.5-plus` → `qwen/qwen3.5-plus`
- `glm-5-turbo` → `z-ai/glm-5-turbo`
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

- Required for agent model API calls (via Hermes Agent / OpenRouter)
- No direct external API calls from MAS Hub itself
- All model traffic routed through Hermes Agent

---

## Directory Structure

MAS Hub expects the following layout:

```
~/project/mas-hub/               # Project source (git repo)
  bin/
    mas                          # Main MAS CLI
    mas-tui                      # TUI wrapper
    mas-monitor                  # Background conflict monitor
  ontology/
    mas-ontology.md              # Agent roles & protocols
  scripts/
    context_maintenance.py       # Adaptive context assembly
    mas_context.py               # Context retrieval
    read_pdf.py                  # PDF reading utility
  agents/                        # Agent template configs (SOUL.md etc.)
  docs/                          # Documentation
  templates/                     # Domain stage gate templates
  config.json                    # Reference configuration
  install.sh                     # Installation script

~/.hermes/profiles/<agent>/      # Per-agent Hermes profiles
  config.yaml                    # Agent model and settings
  SOUL.md                        # Agent personality
  sessions/                      # Agent session history

~/.hermes/mas-hub/               # Runtime data (auto-created)
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

- [ ] Hermes Agent CLI installed (`hermes version`)
- [ ] API keys configured in `~/.hermes/.env` (e.g., `OPENROUTER_API_KEY`)
- [ ] Hermes profiles will be created by installer
- [ ] Python 3.8+ available (`python3 --version`)
- [ ] Bash shell available (`bash --version`)
- [ ] SQLite3 available (`sqlite3 --version`)
- [ ] Git installed (optional, for updates) (`git --version`)
- [ ] Kimi Code CLI installed (optional, for maintenance) (`kimi --version`)

---

## Troubleshooting

### "hermes: command not found"

**Solution:** Install Hermes Agent:
```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent && uv pip install -e ".[all]"
```

### "python3: command not found"

**Solution:** Install Python 3:
- **macOS:** `brew install python3`
- **Linux:** `sudo apt install python3` or `sudo dnf install python3`

### "SQLite3 not found"

**Solution:** Install SQLite3:
- **macOS:** Pre-installed
- **Linux:** `sudo apt install sqlite3` or `sudo dnf install sqlite3`

### Agent not responding

**Solution:** Check Hermes profile and API keys:
```bash
hermes doctor
hermes -p wang chat -q "test" -Q
```

### Agent model unavailable

**Solution:** Check model configuration:
```bash
mas models
mas model <agent> set <alias>
```

---

## Support

- **Documentation:** `~/project/mas-hub/docs/`
- **Ontology:** `~/project/mas-hub/ontology/mas-ontology.md`
- **Incident Reports:** `~/project/mas-hub/docs/incident-*.md`
- **GitHub:** https://github.com/zhentianashen-tech/mas-hub

---

*MAS Hub is designed to be lightweight and dependency-minimal. If you have Hermes Agent running, you likely already meet all requirements.*

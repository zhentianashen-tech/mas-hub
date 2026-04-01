# MAS Hub — Multi-Agent System Orchestrator

**Version:** 1.0.0  
**Author:** Alan (沈桢天)  
**Created:** 2026-03-22  
**License:** MIT  
**Repository:** https://github.com/openclaw/mas-hub

## Overview

MAS Hub is a CLI-based multi-agent orchestration layer built on top of OpenClaw.
It provides:

- **Project-scoped shared context** (SQLite blackboard)
- **Per-agent private MAS sessions** (separate from direct TUI sessions)
- **Model switching** per agent
- **Structured exchange persistence** (key points, citations, artifacts)
- **Diagnostics** (ping, doctor)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   MAS Orchestrator                    │
│                                                       │
│  ┌─────────────┐   ┌──────────────┐                 │
│  │ Project Scope│   │ SQLite       │                 │
│  │ (tesla-thesis│   │ Blackboard   │                 │
│  │  china-macro │   │ (shared ctx) │                 │
│  │  default)    │   └──────────────┘                 │
│  └─────────────┘                                     │
│         │                                             │
│    ┌────┴────────────────────────────┐               │
│    │  Per-Agent MAS Sessions          │               │
│    │  mas::tesla-thesis::wang         │               │
│    │  mas::tesla-thesis::lynch        │               │
│    │  mas::tesla-thesis::archie       │               │
│    └──────────────────────────────────┘               │
│                                                       │
│  Separate from direct TUI sessions:                   │
│    ~/.openclaw/agents/{agent}/sessions/               │
└─────────────────────────────────────────────────────┘
```

## Directory Layout

```
~/Projects/mas-hub/              ← Project source (this repo)
  bin/
    mas                          ← Main MAS CLI (v4.2.1)
    mas-tui                      ← TUI wrapper
    mas-monitor                  ← Background conflict monitor
    mas-aliases.sh               ← Shell aliases for model switching
  docs/                          ← Architecture docs
  templates/                     ← Workflow/message templates
  config.json                    ← Reference copy of agent config
  README.md

~/.openclaw/mas-hub/             ← Runtime data (not in repo)
  blackboard/shared_context.db   ← SQLite blackboard
  agent-memories/                ← Per-agent daily memory files
  state.json                     ← Current project/session state
  config.json                    ← Live agent config
  logs/                          ← Orchestrator logs
  inbox/ outbox/ workflows/      ← Message queues
```

## Installation

### Quick Install (Recommended)

```bash
# One-line installer
curl -fsSL https://raw.githubusercontent.com/openclaw/mas-hub/main/install.sh | bash

# Or clone and install manually
git clone https://github.com/openclaw/mas-hub.git ~/Projects/mas-hub
cd ~/Projects/mas-hub && ./install.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/openclaw/mas-hub.git ~/Projects/mas-hub

# Run the installer
~/Projects/mas-hub/install.sh

# Or manually symlink
ln -sf ~/Projects/mas-hub/bin/mas ~/bin/mas
ln -sf ~/Projects/mas-hub/bin/mas-tui ~/bin/mas-tui
```

### Requirements

- **OpenClaw CLI** ≥ 2026.3.12
- **Python 3.8+** (standard library only)
- **Bash 3.2+**
- **SQLite3**

See [REQUIREMENTS.md](REQUIREMENTS.md) for full details.

---

## Quick Start

```bash
# Create your first project
mas new tesla-thesis

# Create a project
mas new tesla-thesis

# Send to agents
mas @wang "Research Tesla Q1 2026 earnings"
mas @lynch "Validate Wang's findings"
mas @archie "Synthesize the analysis"

# Check status
mas status
mas context
mas projects

# Switch models
mas model wang set gpt-5.4
mas models

# Diagnostics
mas doctor
mas ping wang
```

## Architecture

MAS Hub provides a multi-agent orchestration layer on top of OpenClaw:

```
┌─────────────────────────────────────────────────────┐
│                   MAS Orchestrator                    │
│                                                       │
│  ┌─────────────┐   ┌──────────────┐                 │
│  │ Project Scope│   │ SQLite       │                 │
│  │ (tesla-thesis│   │ Blackboard   │                 │
│  │  china-macro │   │ (shared ctx) │                 │
│  │  default)    │   └──────────────┘                 │
│  └─────────────┘                                     │
│         │                                             │
│    ┌────┴────────────────────────────┐               │
│    │  Per-Agent MAS Sessions          │               │
│    │  mas::tesla-thesis::wang         │               │
│    │  mas::tesla-thesis::lynch        │               │
│    │  mas::tesla-thesis::archie       │               │
│    └──────────────────────────────────┘               │
└─────────────────────────────────────────────────────┘
```

**Key Features:**
- **Project-scoped context** — Keep research organized by project
- **SQLite blackboard** — Structured storage with full response history
- **Adaptive context** — Relevance-scoring for efficient token usage
- **Stage Gate protocol** — 5-stage research workflow (External → DCF → Follow-up → Audit → Synthesis)
- **Watchdog timeouts** — Auto-escalation on agent stalls
- **Model switching** — Per-agent model configuration

---

## Commands Reference

### Project Management
| Command | Description |
|---------|-------------|
| `mas new <project>` | Create and switch to project |
| `mas use <project>` | Switch to existing project |
| `mas projects` | List all projects |
| `mas project` | Show current project (quick) |
| `mas reset` | New session within current project |

### Agent Messaging
| Command | Description |
|---------|-------------|
| `mas @wang <msg>` | Send to Wang with shared context |
| `mas @lynch <msg>` | Send to Lynch |
| `mas @archie <msg>` | Send to Archie |
| `mas @bootstrap <msg>` | Send to Bootstrap |
| `mas @all <msg>` | Broadcast to all |

### Model Switching
| Command | Description |
|---------|-------------|
| `mas model <agent>` | Interactive picker |
| `mas model <agent> current` | Show current model |
| `mas model <agent> set <alias>` | Set model |
| `mas models` | Show all agent models |

### Diagnostics
| Command | Description |
|---------|-------------|
| `mas ping <agent>` | Roundtrip health check |
| `mas doctor` | Full system diagnostics |
| `mas version` | Show version |

### Options
| Flag | Description |
|------|-------------|
| `--json` | Machine-readable JSON output |
| `--no-color` | Disable ANSI colors |
| `MAS_TIMEOUT=N` | Override agent timeout (seconds) |

## Model Aliases

| Alias | Full Model ID |
|-------|---------------|
| `claude-opus-4` | `zenmux/anthropic/claude-opus-4` |
| `claude-opus-4.6` | `zenmux/anthropic/claude-opus-4.6` |
| `claude-sonnet-4.6` | `zenmux/anthropic/claude-sonnet-4-6` |
| `gpt-4.1-mini` | `zenmux/openai/gpt-4.1-mini` |
| `gpt-5.4` | `zenmux/openai/gpt-5.4` |
| `gpt-5.3-codex` | `zenmux/openai/gpt-5.3-codex` |
| `qwen-3.5-plus` | `zenmux/qwen/qwen3.5-plus` |
| `qwen-3-max` | `zenmux/qwen/qwen3-max` |
| `glm-5-turbo` | `zenmux/z-ai/glm-5-turbo` |
| `doubao-seed` | `zenmux/volcengine/doubao-seed-2.0-pro` |
| `grok-4.2` | `zenmux/x-ai/grok-4.2-fast` |
| `kimi` | `moonshot/kimi-k2.5` |
| `minimax` | `minimax/MiniMax-M2.7` |
| `local-qwen` | `ollama/qwen3.5:9b` |
| `local-phi4` | `ollama/phi4:latest` |

---

## Configuration

MAS Hub reads agent configurations from `~/.openclaw/mas-hub/config.json`.

**Default agents:**
- `archie` — Facilitator/Lead (model: `moonshot/kimi-k2.5`)
- `wang` — Financial Researcher (model: `zenmux/anthropic/claude-opus-4`)
- `lynch` — Auditor/Validator (model: `zenmux/openai/gpt-4.1-mini`)
- `bootstrap` — IT Maintainer (model: `zenmux/qwen/qwen3.5-plus`)
- `alonzo` — Tech Strategy (model: `minimax/MiniMax-M2.7`)

**Customize models:**
```bash
mas model wang set claude-opus-4.6
mas model lynch set glm-5-turbo
mas models  # Show all current models
```

---

## Directory Structure

```
~/Projects/mas-hub/              # Source code (git repo)
  bin/
    mas                          # Main MAS CLI
    mas-tui                      # TUI wrapper
    kimi-maintenance             # Kimi Code wrapper
    install.sh                   # One-line installer
  ontology/
    mas-ontology.md              # Agent roles & protocols
  scripts/
    context_maintenance.py       # Adaptive context assembly
    mas_context.py               # Context retrieval
    read_pdf.py                  # PDF reading utility
  docs/                          # Documentation
  templates/                     # Message templates
  config.json                    # Reference configuration
  REQUIREMENTS.md                # System requirements
  README.md                      # This file

~/.openclaw/mas-hub/             # Runtime data (auto-created)
  blackboard/shared_context.db   # SQLite blackboard
  agent-memories/                # Daily MAS memory files
  logs/                          # Orchestrator logs
  state.json                     # Current project/session
```

---

## Maintenance

### Daily Maintenance (Automated)

If Kimi Code CLI is installed:

```bash
# Run daily maintenance
~/Projects/mas-hub/bin/kimi-daily-maintenance.sh

# Or ad-hoc tasks
kimi-maintenance "Rotate logs older than 7 days"
kimi-maintenance --log  # View maintenance log
```

### Manual Maintenance

```bash
# Check system health
mas doctor

# Clean old lock files
find ~/.openclaw/mas-hub/blackboard -name ".lock" -mmin +60 -delete

# View logs
tail -f ~/.openclaw/mas-hub/logs/orchestrator.log
```

---

## Troubleshooting

### Common Issues

**"mas: command not found"**
```bash
# Add ~/bin to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**"Gateway not responding"**
```bash
openclaw gateway start
```

**"Stale lock detected"**
```bash
find ~/.openclaw/mas-hub/blackboard -name ".lock" -mmin +5 -delete
```

**Agent returns empty response**
```bash
# Check model availability
mas ping wang
mas model wang current

# Switch to different model
mas model wang set gpt-4.1-mini
```

### Diagnostics

```bash
# Full system check
mas doctor

# Test agent connectivity
mas ping wang
mas ping lynch

# View system status
mas status
```

### Documentation

- [System Requirements](REQUIREMENTS.md)
- [Agent Ontology](ontology/mas-ontology.md)
- [Architecture Docs](docs/)
- [Incident Reports](docs/incident-*.md)

---

## Development

### Running from Source

```bash
cd ~/Projects/mas-hub
./bin/mas help
```

### Updating

```bash
cd ~/Projects/mas-hub
git pull
./install.sh  # Re-run installer if needed
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Test with `mas doctor` and real agent calls
4. Submit a pull request

---

## License

MIT License — see LICENSE file for details.

---

## Acknowledgments

MAS Hub is built on top of [OpenClaw](https://openclaw.ai) and designed for the OpenClaw ecosystem.

**Community:**
- OpenClaw Discord: https://discord.com/invite/clawd
- Documentation: https://docs.openclaw.ai

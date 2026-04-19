# MAS Hub — Multi-Agent System Orchestrator

**Version:** 4.4.0
**License:** MIT

MAS Hub is a CLI-based multi-agent orchestration layer built on top of [OpenClaw](https://openclaw.ai). It coordinates multiple named AI agents around a shared SQLite context, with support for autonomous multi-round research sessions, domain-aware stage gates, and structured output persistence.

---

## Features

- **Project-scoped shared context** — SQLite blackboard per project, agents share findings across turns
- **Adaptive context assembly** — Relevance scoring surfaces the right prior exchanges to each agent
- **Lead mode** — Archie autonomously orchestrates research across multiple agents and rounds
- **Domain system** — Domain-specific stage gates and topic keywords (`--domain finance`, `--domain default`)
- **Configurable depth** — `MAS_LEAD_MIN_ROUNDS`, `MAS_LEAD_MIN_TASKS`, `MAS_LEAD_MAX_ROUNDS` env vars
- **[PAUSE] mechanism** — Lead mode halts for user input at branching decision points
- **Model switching** — Per-agent model config with 15 built-in aliases
- **Agent profiles** — Sample workspace configs for all agents in `agents/`

---

## Requirements

- **OpenClaw CLI** ≥ 2026.3.12
- **Python 3.8+** (stdlib only)
- **Bash 3.2+**
- **SQLite3**

---

## Installation

```bash
git clone https://github.com/zhentianashen-tech/mas-hub.git ~/Projects/mas-hub
cd ~/Projects/mas-hub && ./install.sh
```

This symlinks `bin/mas` and `bin/mas-tui` into `~/bin/`.

---

## Quick Start

```bash
# Create a project
mas new tesla-thesis

# Create a project with a specific domain
mas new science-review --domain default

# Send tasks to agents
mas @wang "Research Tesla Q1 2026 earnings"
mas @lynch "Validate Wang's findings"
mas @archie "Synthesize the analysis"

# Autonomous multi-round lead session
mas lead @archie "Deep dive on NVDA competitive positioning"

# Diagnostics
mas doctor
mas ping wang
```

---

## Commands Reference

### Project Management

| Command | Description |
|---------|-------------|
| `mas new <project> [--domain <d>]` | Create project (domain: `finance`, `default`) |
| `mas use <project>` | Switch to existing project |
| `mas projects` | List all projects |
| `mas project` | Show current project |
| `mas reset` | New session within current project |

### Agent Messaging

| Command | Description |
|---------|-------------|
| `mas @<agent> <msg>` | Send message with shared context |
| `mas @all <msg>` | Broadcast to all agents |
| `mas lead @archie <msg>` | Start autonomous multi-round session |

### Model Management

| Command | Description |
|---------|-------------|
| `mas model <agent> set <alias>` | Set agent model |
| `mas model <agent> current` | Show current model |
| `mas models` | Show all agent models |

### Diagnostics

| Command | Description |
|---------|-------------|
| `mas ping <agent>` | Roundtrip health check |
| `mas doctor` | Full system diagnostics |
| `mas version` | Show version |
| `mas session` | View active MAS sessions |
| `mas session clear` | Reset all sessions |

---

## Model Aliases

| Alias | Model |
|-------|-------|
| `claude-opus-4` | `zenmux/anthropic/claude-opus-4` |
| `claude-opus-4.6` | `zenmux/anthropic/claude-opus-4.6` |
| `claude-sonnet-4.6` | `zenmux/anthropic/claude-sonnet-4-6` |
| `gpt-4.1-mini` | `zenmux/openai/gpt-4.1-mini` |
| `gpt-5.4` | `zenmux/openai/gpt-5.4` |
| `qwen-3.5-plus` | `zenmux/qwen/qwen3.5-plus` |
| `glm-5-turbo` | `zenmux/z-ai/glm-5-turbo` |
| `doubao-seed` | `zenmux/volcengine/doubao-seed-2.0-pro` |
| `grok-4.2` | `zenmux/x-ai/grok-4.2-fast` |
| `kimi` | `moonshot/kimi-k2.5` |
| `minimax` | `minimax/MiniMax-M2.7` |
| `local-qwen` | `ollama/qwen3.5:9b` |
| `local-phi4` | `ollama/phi4:latest` |

---

## Default Agents

| Agent | Role | Default Model |
|-------|------|---------------|
| `archie` | Facilitator / Lead | `moonshot/kimi-k2.5` |
| `wang` | Financial Researcher | `zenmux/anthropic/claude-opus-4` |
| `lynch` | Auditor / Validator | `zenmux/openai/gpt-4.1-mini` |
| `bootstrap` | IT Maintainer | `zenmux/qwen/qwen3.5-plus` |
| `alonzo` | Tech Strategy | `minimax/MiniMax-M2.7` |

Sample workspace configs for all agents are in [`agents/`](agents/). Copy them into your OpenClaw workspaces as a starting point.

---

## Lead Mode

`mas lead @archie "<goal>"` starts an autonomous research session. Archie coordinates Wang, Lynch, and Alonzo across multiple rounds, enforcing a domain-specific stage gate before concluding.

**Depth controls (env vars):**
```bash
MAS_LEAD_MIN_ROUNDS=9 MAS_LEAD_MIN_TASKS=7 mas lead @archie "Analyze CRISPR delivery"
```

**[PAUSE] — user input at branching points:**

When Archie needs a decision before proceeding, it emits `[PAUSE] <question>`. The run halts, prompts you inline, and resumes with your answer injected into the next round.

**Domain stage gates:**
- `--domain finance` — 5-stage DCF protocol (External Thesis → DCF Model → Follow-Up → Lynch Audit → Synthesis)
- `--domain default` — 4-stage generic protocol (Evidence → Analysis → Validation → Synthesis)

---

## Communication Protocol

Agents use structured markers in responses:

| Marker | Meaning |
|--------|---------|
| `[TASK:<agent>] <instruction>` | Delegate work to another agent |
| `[DONE] <conclusion>` | Conclude workflow |
| `[PAUSE] <question>` | Halt for user input |
| `[MISSING: <description>]` | Flag unavailable data |
| `[ESCALATE:<agent>] <issue>` | Request intervention |

---

## Runtime Data

All runtime data lives at `~/.openclaw/mas-hub/` (not in this repo):

```
~/.openclaw/mas-hub/
├── blackboard/shared_context.db   # SQLite — exchanges, sessions, meta
├── state.json                     # Current project, session ID, domain
├── config.json                    # Live agent config
├── agent-memories/                # Per-agent daily memory files
├── projects/<project>/            # Agent output files
└── logs/orchestrator.log
```

---

## Repository Structure

```
mas-hub/
├── bin/
│   ├── mas                        # Main orchestrator (~1500 lines, Bash)
│   ├── mas-tui                    # TUI wrapper
│   └── mas-monitor                # Background conflict monitor
├── agents/                        # Sample agent workspace configs
│   ├── archie/                    # SOUL.md, IDENTITY.md, MEMORY.md
│   ├── wang/                      # + financial analysis protocol
│   ├── lynch/                     # + ARBITRATOR.md
│   └── alonzo/                    # + tech strategy framework
├── config/
│   ├── topics.default.json        # Generic topic keywords for relevance scoring
│   └── topics.finance.json        # Finance domain overlay
├── templates/domain/
│   ├── finance.md                 # 5-stage DCF stage gate
│   └── default.md                 # 4-stage generic stage gate
├── scripts/
│   ├── mas_context.py             # Context assembly (adaptive relevance scoring)
│   ├── context_maintenance.py     # Context maintenance helper
│   └── read_pdf.py                # PDF reader for agents
├── ontology/
│   └── mas-ontology.md            # Agent roles, protocols, memory architecture
├── docs/
│   └── RESEARCH-STANDARD-v2.md   # Research quality standard (6 thesis types)
├── config.json                    # Reference agent configuration
└── install.sh
```

---

## Troubleshooting

**Agent returns empty response**
```bash
mas ping wang
mas model wang set gpt-4.1-mini
```

**Stale lock**
```bash
rmdir ~/.openclaw/mas-hub/blackboard/.lock
```

**Gateway not running**
```bash
openclaw gateway start
```

---

## License

MIT — see [LICENSE](LICENSE).

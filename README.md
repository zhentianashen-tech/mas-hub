# MAS Hub — Multi-Agent System Orchestrator

**Version:** 4.2.1  
**Author:** Alan (沈桢天)  
**Created:** 2026-03-22

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

## Quick Start

```bash
# Install (symlink into PATH)
ln -sf ~/Projects/mas-hub/bin/mas ~/.kimi/bin/mas

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
| `local-qwen` | `ollama/qwen3.5:9b` |
| `local-phi4` | `ollama/phi4:latest` |

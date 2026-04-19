# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MAS Hub is a CLI-based multi-agent orchestration layer on top of OpenClaw. The core orchestrator is `bin/mas` (a Bash script, currently v4.3.6). Runtime data lives separately at `~/.openclaw/mas-hub/` and is never committed.

## Running and Testing

```bash
# Run from source
./bin/mas help
./bin/mas doctor        # Full system diagnostics
./bin/mas ping wang     # Agent connectivity test

# Install (symlinks bin/ into ~/bin/)
./install.sh
```

There is no automated test suite. Validation is done via `mas doctor` and live `mas ping <agent>` calls against the OpenClaw gateway. Requires `openclaw gateway start` to be running.

## Architecture

### Core Files

- `bin/mas` — Main orchestrator (Bash). All project/session/agent/model/context logic is here (~1500+ lines). This is the primary file to edit.
- `bin/mas-tui` — Thin wrapper launching `mas` in TUI mode via OpenClaw
- `bin/mas-monitor` — Background conflict detection daemon
- `scripts/context_maintenance.py` — Adaptive context assembly with 3-layer relevance scoring (Python, stdlib only)
- `scripts/mas_context.py` — Context retrieval helper
- `scripts/read_pdf.py` — PDF reading utility (used by Wang and Lynch agents)
- `ontology/mas-ontology.md` — Canonical agent roles, protocols, memory architecture. Injected into agent prompts.
- `config.json` — Reference agent configuration (live config is at `~/.openclaw/mas-hub/config.json`)

### Runtime Data (`~/.openclaw/mas-hub/`, not in repo)

- `blackboard/shared_context.db` — SQLite; three tables: `exchanges`, `mas_agent_sessions`, `mas_meta`
- `state.json` — Current project name and MAS session ID
- `config.json` — Live agent config (overrides repo `config.json`)
- `agent-memories/` — Per-agent daily memory files: `{agent}_{YYYY-MM-DD}.md`
- `logs/orchestrator.log` — Main log; `logs/kimi-maintenance.log` for maintenance ops

### Key Concepts

**Projects** scope the SQLite blackboard. Each `mas new <project>` creates a new MAS session ID (`mas-<project>-<timestamp>`). `mas use <project>` resumes from the last session.

**Agent sessions** follow the naming pattern `mas::<project>::<agent>` and map to OpenClaw session IDs. These are separate from direct TUI sessions at `~/.openclaw/agents/{agent}/sessions/`.

**Context assembly** (`context_maintenance.py`) uses a 3-layer token budget: header (200 tokens) → relevant past exchanges scored ≥ 6 (1500 tokens) → recent exchanges (2000 tokens). Topic keywords drive relevance scoring.

**Locking** uses `mkdir` on `~/.openclaw/mas-hub/blackboard/.lock`. Locks older than 120s are auto-removed. Manual cleanup: `rmdir ~/.openclaw/mas-hub/blackboard/.lock`

**Lead mode** (`mas lead`) enables autonomous multi-round facilitation with watchdog timeouts: soft at 180s, hard at 480s, max 10 rounds. Escalates to `bootstrap` agent on hard timeout.

### Agent Roles and Workspaces

| Agent | Role | Default Model | Workspace |
|-------|------|---------------|-----------|
| `archie` | Facilitator/Lead | `moonshot/kimi-k2.5` | `~/.openclaw/workspace/` |
| `wang` | Financial Researcher | `zenmux/anthropic/claude-opus-4` | `~/.openclaw/workspace-wang/` |
| `lynch` | Auditor/Validator | `zenmux/openai/gpt-4.1-mini` | `~/.openclaw/workspace-lynch/` |
| `bootstrap` | IT Maintainer | `zenmux/qwen/qwen3.5-plus` | `~/.openclaw/workspace-bootstrap/` |
| `alonzo` | Tech Strategy | `minimax/MiniMax-M2.7` | — |

**Critical path rule:** All project output files must be saved to `~/.openclaw/mas-hub/projects/<project_name>/`. The wrong path (`~/.openclaw/workspace/projects/`) is Archie's native workspace — agents saving there pollutes the wrong context.

### Session Management

```bash
mas session          # View active MAS sessions
mas session clear    # Reset all sessions (agents start fresh)

# TUI mode — plain output, no ANSI colors, wrapped in ---[Agent]--- delimiters
TUI_MODE=1 mas @wang "Research Tesla"
mas-tui wang "Research Tesla"   # wrapper equivalent
```

MAS sessions are named `mas::<project>::<agent>` and persist within a project. Native OpenClaw sessions live at `~/.openclaw/agents/{agent}/sessions/` and are separate.

**Mid-run input injection:** From a second terminal, `mas @archie "redirect message"` injects into the running lead session. Documented in `docs/HOWTO-inject-input-mid-run.md`.

### Communication Protocol Markers

Agents use structured markers in responses:
- `[TASK:<agent>] <instruction>` — Delegate work
- `[DONE] <conclusion>` — Conclude workflow
- `[MISSING: <description>]` — Flag unavailable data
- `[ESCALATE:<agent>] <issue>` — Request intervention
- `[STATUS: <state>] <details>` — Progress report

## Maintenance

```bash
# Kimi Code CLI integration (automated IT maintenance)
kimi-maintenance "Rotate logs older than 7 days"
kimi-maintenance --log   # View maintenance log

# Manual
tail -f ~/.openclaw/mas-hub/logs/orchestrator.log
find ~/.openclaw/mas-hub/blackboard -name ".lock" -mmin +60 -delete
```

## Research Quality Standard

Use `docs/RESEARCH-STANDARD-v2.md` (v2.0, current). `docs/RESEARCH-STANDARD.md` (v1.0) is superseded — it wrongly treated a commodity/supply-chain example as a universal checklist.

v2.0 defines 6 thesis types (Commodity/Supply Chain, Deep Value, Event-Driven, Macro/Geopolitical, Technology/Disruption, Financials/Credit), each with different depth requirements. Universal requirements across all types: specificity, quantification, timing, source diversity, actionability, and explicit gap markers (`[MISSING:]`).

Lynch audit checklist: tradeable (specific tickers/entry/exit/sizing), geography/timing precise, all thesis-appropriate layers addressed, multiple independent sources, liquidity/execution confirmed.

## Known Pitfalls

- **Wrong project file path:** Agents (especially Wang when delegated by Archie) sometimes save to `~/.openclaw/workspace/projects/` instead of `~/.openclaw/mas-hub/projects/<project>/`. This is agent instruction error, not a system bug.
- **Premature [DONE]:** v4.3.6 added code-level enforcement rejecting `[DONE]` before round 5 or fewer than 3 completed tasks.
- **Stale lock:** `~/.openclaw/mas-hub/blackboard/.lock` older than 120s is auto-removed, but manual cleanup: `rmdir ~/.openclaw/mas-hub/blackboard/.lock`
- **Empty agent response:** Check model availability with `mas ping <agent>`, switch with `mas model <agent> set <alias>`.

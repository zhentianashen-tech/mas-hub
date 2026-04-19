# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MAS Hub is a CLI-based multi-agent orchestration layer backed by Hermes Agent. The core orchestrator is `bin/mas` (a Bash script, v4.4.0). Each agent runs as an isolated Hermes profile (`~/.hermes/profiles/<agent>/`). Runtime data lives at `~/.hermes/mas-hub/` and is never committed.

## Running and Testing

```bash
# Run from source
./bin/mas help
./bin/mas doctor        # Full system diagnostics
./bin/mas ping wang     # Agent connectivity test

# Install (symlinks bin/ into ~/bin/)
./install.sh
```

There is no automated test suite. Validation is done via `mas doctor` and live `mas ping <agent>` calls against Hermes profiles. Requires Hermes Agent CLI to be installed and API keys configured in `~/.hermes/.env`.

## Architecture

### Core Files

- `bin/mas` — Main orchestrator (Bash, ~1600 lines). All project/session/agent/model/context logic. This is the primary file to edit.
- `bin/mas-tui` — Thin wrapper launching `mas` in TUI mode
- `bin/mas-monitor` — Background conflict detection daemon
- `scripts/mas_context.py` — Context assembly with adaptive relevance scoring (Python, stdlib only)
- `scripts/context_maintenance.py` — Context maintenance helper
- `scripts/read_pdf.py` — PDF reading utility for agents
- `ontology/mas-ontology.md` — Canonical agent roles, protocols, memory architecture. Injected into agent prompts.
- `config.json` — Reference agent configuration (live config at `~/.hermes/mas-hub/config.json`)

### Hermes Agent Backend

Agents are Hermes profiles, called via: `hermes -p <profile> chat -q "message" -Q`

The `-Q` (quiet) flag outputs plain text on stdout and `session_id: <id>` on stderr. The `hermes_agent_call()` function in `bin/mas` wraps this, handles session continuity via `-r <session_id>`, and stores session IDs in SQLite.

Model management uses `hermes -p <agent> config set model.default <model>` and reads from `~/.hermes/profiles/<agent>/config.yaml`.

### Runtime Data (`~/.hermes/mas-hub/`, not in repo)

- `blackboard/shared_context.db` — SQLite; tables: `exchanges`, `mas_agent_sessions`, `mas_meta`
- `state.json` — Current project name and MAS session ID
- `config.json` — Live agent config (overrides repo `config.json`)
- `agent-memories/` — Per-agent daily memory files: `{agent}_{YYYY-MM-DD}.md`
- `logs/orchestrator.log` — Main log

### Key Concepts

**Projects** scope the SQLite blackboard. `mas new <project>` creates a new MAS session ID. `mas use <project>` resumes.

**Agent sessions** follow `mas::<project>::<agent>` naming. Each also tracks a `hermes_session_id` for Hermes session continuity.

**Context assembly** (`mas_context.py`) uses a 3-layer token budget: header (200 tokens) -> relevant past exchanges scored >= 6 (4000 tokens) -> recent exchanges (3000 tokens). Topic keywords drive relevance scoring.

**Locking** uses `mkdir` on `~/.hermes/mas-hub/blackboard/.lock`. Locks older than 120s are auto-removed.

**Lead mode** (`mas lead`) enables autonomous multi-round facilitation with watchdog timeouts: soft at 300s, hard at 900s, max 15 rounds. Escalates to `bootstrap` agent on hard timeout.

### Agent Roles and Profiles

| Agent | Role | Default Model | Hermes Profile |
|-------|------|---------------|----------------|
| `archie` | Facilitator/Lead | `qwen/qwen3.6-plus` | `~/.hermes/profiles/archie/` |
| `wang` | Financial Researcher | `anthropic/claude-opus-4` | `~/.hermes/profiles/wang/` |
| `lynch` | Auditor/Validator | `openai/gpt-4.1-mini` | `~/.hermes/profiles/lynch/` |
| `bootstrap` | IT Maintainer | `qwen/qwen3.5-plus` | `~/.hermes/profiles/bootstrap/` |
| `alonzo` | Tech Strategy | `minimax/minimax-m2.7` | `~/.hermes/profiles/alonzo/` |

Agent template configs (SOUL.md, IDENTITY.md, MEMORY.md) live in `agents/` and are copied into Hermes profiles during install.

**Critical path rule:** All project output files must be saved to `~/.hermes/mas-hub/projects/<project_name>/`.

### Communication Protocol Markers

Agents use structured markers in responses:
- `[TASK:<agent>] <instruction>` — Delegate work
- `[DONE] <conclusion>` — Conclude workflow
- `[PAUSE] <question>` — Halt for user input
- `[MISSING: <description>]` — Flag unavailable data
- `[ESCALATE:<agent>] <issue>` — Request intervention

### Response Parsing

`extract_structured_response()` handles both Hermes plain text and legacy OpenClaw JSON payloads. For Hermes, it takes the raw text directly and extracts summary, key points, open questions, citations, and artifacts.

### Model Aliases

Aliases resolve to OpenRouter format by default. Zenmux-prefixed model strings are passed through for future use.

## Research Quality Standard

Use `docs/RESEARCH-STANDARD-v2.md` (v2.0, current). Defines 6 thesis types with different depth requirements. Universal requirements: specificity, quantification, timing, source diversity, actionability, explicit `[MISSING:]` gap markers.

## Known Pitfalls

- **Wrong project file path:** Agents sometimes save to wrong directory instead of `~/.hermes/mas-hub/projects/<project>/`.
- **Premature [DONE]:** v4.3.6+ added code-level enforcement rejecting `[DONE]` before min rounds/tasks.
- **Stale lock:** `~/.hermes/mas-hub/blackboard/.lock` older than 120s is auto-removed. Manual: `rmdir ~/.hermes/mas-hub/blackboard/.lock`
- **Empty agent response:** Check model availability with `mas ping <agent>`, switch with `mas model <agent> set <alias>`.
- **Hermes session drift:** If an agent's Hermes session gets out of sync, use `mas reset` to start fresh MAS sessions.

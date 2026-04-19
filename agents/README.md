# Sample Agent Configurations

This directory contains sample workspace configuration files for the three default MAS Hub agents. Copy these into your OpenClaw agent workspaces to replicate the setup.

## Agents

| Agent | Role | Emoji | Workspace Path |
|-------|------|-------|---------------|
| **Archie** | General facilitator / researcher | 🐙 | `~/.openclaw/workspace/` |
| **Wang** | Financial research analyst | 🦉 | `~/.openclaw/workspace-wang/` |
| **Lynch** | Auditor / arbitrator | ⚖️ | `~/.openclaw/workspace-lynch/` |
| **Alonzo** | Tech strategy researcher | 🎯 | `~/.openclaw/workspace-alonzo/` |

## Files Included

| File | Purpose | All Agents |
|------|---------|------------|
| `SOUL.md` | Behavioral principles and stance | ✅ |
| `IDENTITY.md` | Name, role, capabilities | ✅ |
| `MEMORY.md` | Memory architecture + protocols | ✅ |
| `ARBITRATOR.md` | Conflict resolution protocol | Lynch only |

## Setup

1. Copy the agent folder contents into the corresponding OpenClaw workspace:
   ```bash
   cp agents/archie/* ~/.openclaw/workspace/
   cp agents/wang/* ~/.openclaw/workspace-wang/
   cp agents/lynch/* ~/.openclaw/workspace-lynch/
   cp agents/alonzo/* ~/.openclaw/workspace-alonzo/
   ```

2. Edit `IDENTITY.md` for each agent to set your preferred name/vibe.

3. For Wang, create `~/.openclaw/workspace-wang/.env.local` with your API keys:
   ```
   ALPHA_VANTAGE_API_KEY=...
   FMP_API_KEY=...
   FINNHUB_API_KEY=...
   FRED_API_KEY=...
   ```

4. Create the `memory/` subdirectory in each workspace for daily session logs:
   ```bash
   mkdir -p ~/.openclaw/workspace/memory
   mkdir -p ~/.openclaw/workspace-wang/memory
   mkdir -p ~/.openclaw/workspace-lynch/memory
   ```

## Notes

- `SOUL.md` files are loaded by OpenClaw as the agent's behavioral grounding
- `MEMORY.md` files are auto-loaded each session — update them as the agent learns
- Wang's domain is finance (equity + fixed income) — for other domains, create a new agent with a domain-appropriate `SOUL.md`
- Lynch is domain-agnostic as an auditor, but the `ARBITRATOR.md` protocol is finance-aware

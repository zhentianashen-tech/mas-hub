# Sample Agent Configurations

This directory contains template configuration files for the MAS Hub agents. These are copied into Hermes profiles during `install.sh` setup.

## Agents

| Agent | Role | Emoji | Hermes Profile |
|-------|------|-------|----------------|
| **Archie** | General facilitator / researcher | 🐙 | `~/.hermes/profiles/archie/` |
| **Wang** | Financial research analyst | 🦉 | `~/.hermes/profiles/wang/` |
| **Lynch** | Auditor / arbitrator | ⚖️ | `~/.hermes/profiles/lynch/` |
| **Alonzo** | Tech strategy researcher | 🎯 | `~/.hermes/profiles/alonzo/` |

## Files Included

| File | Purpose | All Agents |
|------|---------|------------|
| `SOUL.md` | Behavioral principles and stance | Yes |
| `IDENTITY.md` | Name, role, capabilities | Yes |
| `MEMORY.md` | Memory architecture + protocols | Yes |
| `ARBITRATOR.md` | Conflict resolution protocol | Lynch only |

## Setup

The installer (`install.sh`) handles this automatically, but for manual setup:

1. Create Hermes profiles for each agent:
   ```bash
   hermes profile create archie --clone
   hermes profile create wang --clone
   hermes profile create lynch --clone
   hermes profile create alonzo --clone
   ```

2. Copy SOUL.md into each profile:
   ```bash
   cp agents/archie/SOUL.md ~/.hermes/profiles/archie/SOUL.md
   cp agents/wang/SOUL.md ~/.hermes/profiles/wang/SOUL.md
   cp agents/lynch/SOUL.md ~/.hermes/profiles/lynch/SOUL.md
   cp agents/alonzo/SOUL.md ~/.hermes/profiles/alonzo/SOUL.md
   ```

3. Set models for each profile:
   ```bash
   hermes -p wang config set model.default "anthropic/claude-opus-4"
   hermes -p lynch config set model.default "openai/gpt-4.1-mini"
   ```

## Notes

- `SOUL.md` files are loaded by Hermes as the agent's behavioral grounding
- `MEMORY.md` files describe the memory architecture for reference — Hermes profiles have their own persistent memory
- Wang's domain is finance (equity + fixed income) — for other domains, create a new agent with a domain-appropriate `SOUL.md`
- Lynch is domain-agnostic as an auditor, but the `ARBITRATOR.md` protocol is finance-aware

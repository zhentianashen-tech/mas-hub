# MAS Hub Agent Memory Access

**Version:** 1.0  
**Date:** 2026-03-23  
**Purpose:** Enable agents to access their MAS Hub memory files

---

## Overview

Each MAS agent has a daily memory file that stores their MAS Hub session work:

```
~/.openclaw/mas-hub/agent-memories/{agent}_{YYYY-MM-DD}.md
```

## Agent Memory Files

| Agent | Memory File Pattern |
|-------|-------------------|
| Archie | `archie_{date}.md` |
| Wang | `wang_{date}.md` |
| Lynch | `lynch_{date}.md` |
| Bootstrap | `bootstrap_{date}.md` |

## Workspace Bootstrap Files

Each agent workspace contains a `MAS_HUB_MEMORY.md` file that:

1. Tells them where their MAS memory is located
2. Provides commands to read it
3. Explains when to check it
4. Distinguishes MAS memory from workspace memory

## File Locations

```
~/.openclaw/
├── mas-hub/
│   └── agent-memories/
│       ├── archie_2026-03-23.md
│       ├── wang_2026-03-23.md
│       ├── lynch_2026-03-23.md
│       └── bootstrap_2026-03-23.md
├── workspace-main/        # Archie
│   └── MAS_HUB_MEMORY.md
├── workspace-wang/         # Wang
│   └── MAS_HUB_MEMORY.md
├── workspace-lynch/        # Lynch
│   └── MAS_HUB_MEMORY.md
└── workspace-bootstrap/    # Bootstrap
    └── MAS_HUB_MEMORY.md
```

## Usage

When asked "do you remember...?" or "what did you research in MAS...?", agents should:

1. Read their MAS Hub memory file
2. Extract relevant context
3. Incorporate into current session

## Example Prompt to Agent

```
Do you remember any companies or topics you researched 
in recent MAS Hub sessions? Check your MAS Hub memory 
file and tell me what you find.
```

## Distinction

| Memory Type | Location | Contents |
|-------------|----------|----------|
| **MAS Hub Memory** | `~/.openclaw/mas-hub/agent-memories/` | MAS session work only |
| **Workspace Memory** | `~/.openclaw/workspace-{agent}/MEMORY.md` | All interactions |

---

*Bob maintains the MAS Hub infrastructure*

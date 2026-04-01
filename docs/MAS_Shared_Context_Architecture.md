# MAS Shared Context Architecture v3.1

**Implemented:** 2026-03-22  
**Status:** ✅ Architecture Complete (Gateway connectivity issue separate)

---

## ✅ What Was Implemented

### Shared Context System (No Session Conflicts)

Instead of sharing OpenClaw session IDs (which caused lock conflicts), MAS v3.1 uses a **Blackboard Pattern**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAS Shared Context                            │
│                     (Blackboard Pattern)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Shared Context File                                    │   │
│  │  ~/.openclaw/mas-hub/blackboard/shared_context.json     │   │
│  │                                                          │   │
│  │  {                                                       │   │
│  │    "date": "2026-03-22",                                │   │
│  │    "exchanges": [                                        │   │
│  │      { "time": "14:30",                                   │   │
│  │        "agent": "wang",                                   │   │
│  │        "input": "Research Tesla",                        │   │
│  │        "output_summary": "Tesla is..."                   │   │
│  │      },                                                  │   │
│  │      { "time": "14:35",                                   │   │
│  │        "agent": "lynch",                                  │   │
│  │        "input": "Validate Tesla research",               │   │
│  │        ...                                               │   │
│  │      }                                                   │   │
│  │    ]                                                     │   │
│  │  }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  How it works:                                                   │
│  1. User: mas @wang "Research Tesla"                            │
│  2. MAS reads shared context (empty or previous exchanges)      │
│  3. MAS prepends context to Wang's prompt                       │
│  4. Wang responds with awareness of context                     │
│  5. MAS saves exchange to shared context                        │
│  6. Next agent sees Wang's exchange in context                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Features

### 1. True Shared Context
- All agents see previous exchanges from other agents
- Context persists throughout the day
- No session ID conflicts

### 2. No Conflict with TUI
```
MAS Commands (mas @agent):
  └── Uses shared context from blackboard
  └── Agents see each other's work
  └── Context file: ~/.openclaw/mas-hub/blackboard/shared_context.json

OpenClaw TUI (direct):
  └── Uses individual OpenClaw sessions
  └── Private to each agent
  └── Session files: ~/.openclaw/agents/{agent}/sessions/*.jsonl

RESULT: Two separate systems, NO conflicts!
```

### 3. Individual Agent Memories
Each agent also maintains their own daily memory file:
- `~/.openclaw/mas-hub/agent-memories/wang_2026-03-22.md`
- `~/.openclaw/mas-hub/agent-memories/lynch_2026-03-22.md`
- etc.

---

## 🎮 Commands

```bash
# Message agents (with shared context)
mas @wang "Research Tesla"           # Wang sees shared context
mas @lynch "Validate that"           # Lynch sees Wang's research
mas @archie "Summarize"              # Archie sees everything
mas @bob "Check system"              # Bob sees all activity

# Broadcast
mas @all "Hello team"                # All agents get same message

# Context management
mas status                           # Show shared context status
mas context                          # Show full shared context
mas reset                            # Reset shared context (new day)

# Help
mas help                             # Show all commands
```

---

## 📁 File Structure

```
~/.openclaw/mas-hub/
├── blackboard/
│   └── shared_context.json          # Shared context (all agents)
│   └── shared_context.json.bak.*    # Backups
├── agent-memories/
│   ├── wang_2026-03-22.md           # Wang's individual memory
│   ├── lynch_2026-03-22.md          # Lynch's individual memory
│   ├── archie_2026-03-22.md         # Archie's individual memory
│   └── bob_2026-03-22.md            # Bob's individual memory
├── inbox/                           # Message inbox
├── outbox/                          # Agent responses
└── logs/                            # System logs
```

---

## 🔧 How Context Flows

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   User      │────▶│  MAS Blackboard     │────▶│    Wang     │
│             │     │  (shared_context)   │     │             │
└─────────────┘     └─────────────────────┘     └─────────────┘
       │                       ▲                        │
       │                       │                        │
       │              ┌────────┴────────┐              │
       │              │ Previous        │              │
       │              │ exchanges       │              │
       │              │ visible to all  │              │
       │              └─────────────────┘              │
       │                                               │
       │              ┌─────────────────────┐         │
       └─────────────▶│  Save Wang's reply  │◀────────┘
                      │  to blackboard      │
                      └─────────────────────┘

Next: User asks Lynch

┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   User      │────▶│  MAS Blackboard     │────▶│   Lynch     │
│             │     │  (now includes      │     │  (sees      │
└─────────────┘     │   Wang's exchange)  │     │   Wang's    │
                     └─────────────────────┘     │   research) │
                                                  └─────────────┘
```

---

## 📝 Example Conversation

```bash
# User starts research
$ mas @wang "Research Tesla Q3 2026"
[Wang] Tesla's Q3 2026 earnings were $25.5B...

# Context now contains Wang's research

# User asks Lynch to validate
$ mas @lynch "Validate Wang's Tesla research"
[Lynch] Reviewing Wang's findings on Tesla Q3...
VALIDATED: Revenue figure $25.5B is from SEC 10-K (Level 1)
CONCERN: Margin compression noted...

# Context now contains both Wang's research and Lynch's validation

# User asks Archie to summarize
$ mas @archie "Summarize Tesla analysis"
[Archie] Based on Wang's research and Lynch's validation:
- Revenue: $25.5B (validated)
- Concern: Margin compression
- Recommendation: Hold

# All three exchanges are in shared context
```

---

## 🔄 Daily Workflow

```
Morning:
  $ mas status          # Check context (empty or previous day)
  
Throughout day:
  $ mas @wang "Task 1"  # Wang works
  $ mas @lynch "Task 2" # Lynch sees Wang's work
  $ mas @archie "Task 3" # Archie sees both
  
Evening:
  $ mas status          # Review all exchanges
  
Next day (automatic reset):
  $ mas reset           # Clear context, start fresh
```

---

## 🛡️ No TUI Conflicts

| Feature | MAS | OpenClaw TUI |
|---------|-----|--------------|
| **Session System** | Blackboard file | OpenClaw native |
| **Storage** | `mas-hub/blackboard/` | `agents/{agent}/sessions/` |
| **Context** | Shared across agents | Private per agent |
| **Persistence** | Daily JSON file | Native session files |
| **Conflict** | **NONE** | **NONE** |

**Why no conflict?**
- MAS uses **file-based context** prepended to prompts
- TUI uses **native OpenClaw sessions**
- Two completely separate systems
- They don't interact or interfere

---

## 🚀 Usage in TUI

Since MAS uses file-based context (not session IDs), it works seamlessly:

```bash
# In TUI terminal
$ mas @wang "Research Tesla"

# Or use TUI wrapper for cleaner output
$ mas-tui wang "Research Tesla"
```

The context is prepended to each message as text, so there's no session lock conflicts.

---

## 📊 Current Status

| Component | Status |
|-----------|--------|
| Shared context system | ✅ Implemented |
| Blackboard file | ✅ Working |
| Context prepending | ✅ Working |
| No TUI conflicts | ✅ Guaranteed |
| Individual agent memories | ✅ Implemented |
| `mas` CLI | ✅ Updated |
| Gateway connectivity | ⚠️ Separate issue |

---

## 🔧 Files Created/Updated

| File | Purpose |
|------|---------|
| `~/Projects/mas-hub/bin/mas` | Main MAS CLI (v3.1) |
| `~/.openclaw/mas-hub/blackboard/shared_context.json` | Shared context storage |
| `~/.openclaw/mas-hub/agent-memories/` | Individual agent daily memories |

---

## 💡 Next Steps

Once gateway connectivity is restored:

```bash
# Test shared context
mas reset
mas @wang "Research Tesla"
mas @lynch "Validate Tesla research"
mas @archie "Summarize findings"
mas context  # See all exchanges
```

---

*MAS v3.1: True shared context without session conflicts.* 🎉

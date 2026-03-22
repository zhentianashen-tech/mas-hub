# MAS Session Management Guide

**Agent:** Bob 🔧  
**System:** Multi-Agent System (MAS)  
**Version:** 2.0  

---

## 📋 Overview

MAS v2.0 introduces proper session management for all agents. Each agent now maintains persistent conversation context within a session, rather than starting fresh each time.

---

## 🗂️ Session Types

### 1. MAS Sessions (Daily)

**Location:** `~/.openclaw/mas-hub/.sessions/`

MAS uses **daily sessions** by default. Each agent gets one session per day:
- `wang:20250322` → Wang's session for March 22, 2026
- `lynch:20250322` → Lynch's session for March 22, 2026
- etc.

**Benefits:**
- Context persists throughout the day
- Agents remember previous exchanges
- Automatic cleanup (new session each day)

### 2. OpenClaw Sessions (Native)

**Location:** `~/.openclaw/agents/{agent}/sessions/`

OpenClaw's native session storage. Each conversation gets a unique session ID.

---

## 🎮 Session Commands

### View Active Sessions

```bash
mas session
```

### Clear MAS Sessions

Reset all MAS sessions (agents will start fresh):

```bash
mas session clear
```

---

## 🖥️ TUI Integration

### Using MAS in TUI

The TUI mode provides simplified output:

```bash
# Enable TUI mode
export TUI_MODE=1
mas @wang "Research Tesla"

# Or use the TUI wrapper
mas-tui wang "Research Tesla"
```

**TUI Output Format:**
```
---
[Wang]
Tesla's Q3 2026 earnings show...
---
```

---

## 🚀 Quick Reference

```bash
# View sessions
mas session

# Clear all MAS sessions
mas session clear

# TUI mode (plain output)
TUI_MODE=1 mas @wang "Research Tesla"

# TUI wrapper
mas-tui wang "Research Tesla"
```

---

*Session management keeps your agents contextually aware.* 🧠

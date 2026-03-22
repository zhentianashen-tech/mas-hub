# Multi-Agent System (MAS) Unified Interface Proposal

## Overview
A three-layer architecture enabling seamless collaboration between Archie, Wang, and Lynch.

---

## 🎯 Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 1: UNIFIED INTERFACE (User-facing)                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Command Types:                                               │  │
│  │  • Direct: "@archie analyze this"                             │  │
│  │  • Broadcast: "@all review this document"                     │  │
│  │  • Workflow: "@wang research → @lynch validate → @archie sum" │  │
│  │  • Debate: "@wang vs @archie on thesis X"                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 2: ORCHESTRATION HUB (Coordination Layer)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │  Message Router │  │  Workflow       │  │  Conflict       │     │
│  │  (Blackboard)   │  │  Engine         │  │  Detector       │     │
│  │                 │  │                 │  │                 │     │
│  │  • Agent Inbox  │  │  • Sequential   │  │  • Variance     │     │
│  │  • Broadcast    │  │  • Parallel     │  │  • Contradiction│     │
│  │  • Direct Msg   │  │  • Debate Loop  │  │  • Auto-trigger │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: AGENT POOL (Execution Layer)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   🦉 ARCHIE  │  │   🦉 WANG    │  │   ⚖️ LYNCH   │              │
│  │              │  │              │  │              │              │
│  │  General     │  │  Financial   │  │  Arbitrator  │              │
│  │  Intelligence│  │  Research    │  │  Conflicts   │              │
│  │              │  │              │  │              │              │
│  │  • Broad     │  │  • Deep      │  │  • Validate  │              │
│  │  • Creative  │  │  • Analysis  │  │  • Resolve   │              │
│  │  • Summarize │  │  • Models    │  │  • Audit     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
│  Shared: ~/.openclaw/mas-hub/ (Blackboard + Logs)                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Implementation Options

### Option A: File-Based Blackboard (Recommended)

**How it works:**
- Shared directory `~/.openclaw/mas-hub/` acts as message board
- Agents "post" by writing files
- Orchestrator monitors and routes

**Pros:**
- Simple, no additional services
- Persistent, auditable
- Works with existing OpenClaw

**Cons:**
- Polling-based (not real-time)
- File I/O overhead

### Option B: SQLite Message Queue

**How it works:**
- SQLite database as message broker
- Tables: messages, agent_inboxes, workflows
- Trigger-based notifications

**Pros:**
- Structured, queryable
- ACID transactions
- Fast

**Cons:**
- More complex setup
- Requires SQLite knowledge

### Option C: Wrapper Scripts (Simplest)

**How it works:**
- Shell scripts chain agent calls
- Output capture and forwarding
- No persistent state

**Pros:**
- Extremely simple
- No state management
- Easy to debug

**Cons:**
- No async capabilities
- Limited inter-agent chatter

---

## 📋 Recommended Implementation: Hybrid Approach

I'll build **Option A + C Hybrid** with these components:

### 1. Shared Communication Hub
```
~/.openclaw/mas-hub/
├── inbox/              # Incoming messages for each agent
│   ├── archie/
│   ├── wang/
│   └── lynch/
├── outbox/             # Agent responses
├── blackboard/         # Shared state & context
├── workflows/          # Active workflow tracking
└── logs/               # Audit trail
```

### 2. Message Protocol

```json
{
  "message_id": "uuid",
  "timestamp": "ISO8601",
  "from": "user|archie|wang|lynch",
  "to": "archie|wang|lynch|broadcast",
  "type": "direct|broadcast|workflow_step|conflict_alert",
  "content": "...",
  "context": {
    "workflow_id": "...",
    "step_number": 1,
    "dependencies": []
  }
}
```

### 3. Unified CLI Commands

```bash
# Direct messaging
mas @archie "Analyze this document"
mas @wang "Research AAPL fundamentals"
mas @lynch "Validate this thesis"

# Broadcast to all
mas @all "Review Q3 earnings strategy"

# Sequential workflow
mas workflow "research→validate→summarize" "Tesla investment thesis"

# Parallel workflow  
mas parallel "@archie analyze sentiment; @wang analyze fundamentals"

# Debate mode
mas debate "@wang bull vs @archie bear" "Is NVDA overvalued?"

# Auto-conflict detection
mas smart "Analyze AAPL"  # Runs research, auto-sends conflicts to Lynch
```

### 4. Auto-Conflict Detection

Lynch monitors all agent outputs:
- Detects numerical variance > 5%
- Flags narrative contradictions
- Auto-triggers arbitration
- Logs to blackboard

### 5. Workflow Templates

```yaml
# research-validate.yaml
name: Research with Validation
steps:
  - agent: wang
    action: deep_research
    output: research_report
  
  - agent: lynch
    action: validate_facts
    input: research_report
    condition: auto_detect_conflicts
  
  - agent: archie
    action: synthesize
    input: [research_report, validation_report]
    output: final_summary
```

---

## 🚀 Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Unified CLI** | Single command interface | No context switching |
| **Inter-agent Chat** | Agents message each other | Collaborative reasoning |
| **Auto-Arbitration** | Lynch monitors & intervenes | Guaranteed consistency |
| **Workflow Engine** | Sequential/parallel execution | Complex pipelines |
| **Audit Trail** | Complete conversation logs | Full transparency |
| **Context Sharing** | Shared blackboard | No information loss |

---

## 📊 Communication Patterns

### Pattern 1: Sequential (Assembly Line)
```
User → Wang (Research) → Lynch (Validate) → Archie (Summarize) → User
```

### Pattern 2: Parallel (Committee)
```
User → [Wang + Archie] → Lynch (Resolve conflicts) → User
```

### Pattern 3: Debate (Adversarial)
```
User → Wang (Pro) + Archie (Con) → Lynch (Judge) → User
```

### Pattern 4: Broadcast (All Hands)
```
User → @all → [Individual responses] → Lynch (Synthesize) → User
```

---

## 🔧 Technical Implementation Plan

### Phase 1: Core Infrastructure (1-2 hours)
1. Create MAS hub directory structure
2. Build message protocol (JSON)
3. Create orchestrator script (`mas`)

### Phase 2: Basic Communication (1 hour)
1. Direct messaging between agents
2. Broadcast capability
3. Message inbox system

### Phase 3: Workflow Engine (2 hours)
1. Sequential workflows
2. Parallel execution
3. Workflow templates

### Phase 4: Conflict Integration (1 hour)
1. Lynch auto-monitoring
2. Conflict detection
3. Auto-trigger arbitration

### Phase 5: Polish (1 hour)
1. Unified CLI interface
2. Logging & audit trail
3. Documentation

**Total: ~6 hours** for full implementation

---

## 💡 Usage Examples (Post-Implementation)

```bash
# Simple research with validation
mas workflow research "Tesla Q3 2026"
# → Wang researches → Lynch validates → Returns clean report

# Investment thesis with debate
mas debate "bull vs bear" "Apple at $200"
# → Wang argues bull case → Archie argues bear case → Lynch judges

# Portfolio review
mas @all "Review my portfolio: AAPL 50%, TSLA 30%, NVDA 20%"
# → All three agents analyze → Lynch resolves conflicts → Unified view

# Automated fact-checking
mas smart "Is Tesla's revenue $25B or $30B?"
# → Wang checks sources → Lynch validates → Returns authoritative answer
```

---

## ✅ Next Steps

Shall I proceed with **Phase 1** implementation?

1. Create the MAS hub infrastructure
2. Build the unified `mas` CLI
3. Set up inter-agent messaging
4. Configure Lynch as the conflict monitor

**Reply with:**
- "**Build it**" — Start full implementation
- "**Simplify**" — Start with basic wrapper scripts only
- "**Modify**" — Change architecture (specify what)

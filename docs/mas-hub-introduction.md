# MAS Hub: Multi-Agent System for Collaborative Research

**Version:** 4.3.4  
**Last Updated:** 2026-03-23  
**Location:** `~/Projects/mas-hub/`

---

## 1. Purpose & Vision

MAS Hub is a collaborative multi-agent system designed for complex research workflows requiring diverse expertise, quality assurance, and systematic validation. It enables multiple AI agents with specialized roles to work together on projects while maintaining strict memory separation and context sharing protocols.

### Core Objectives

- **Collaborative Intelligence**: Combine specialized agents (research, audit, strategy) into unified workflows
- **Quality Assurance**: Built-in validation layers prevent errors from propagating
- **Memory Hygiene**: Strict separation between MAS Hub sessions and native agent workspaces
- **Context Efficiency**: Smart context management prevents token overflow while preserving relevance
- **Auditability**: Full traceability of decisions, conflicts, and resolutions

---

## 2. Architecture Overview

### 2.1 Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        MAS HUB ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   MAS CLI   │◄──►│  Blackboard │◄──►│   Agents    │         │
│  │   (bin/mas) │    │ (SQLite DB) │    │ (5 agents)  │         │
│  └──────┬──────┘    └─────────────┘    └──────┬──────┘         │
│         │                                       │                │
│         ▼                                       ▼                │
│  ┌─────────────┐                        ┌─────────────┐         │
│  │   Ontology  │                        │   Memory    │         │
│  │   (Docs)    │                        │   (Tiered)  │         │
│  └─────────────┘                        └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Details

| Component | Purpose | Location |
|-----------|---------|----------|
| **MAS CLI** | Command-line interface for orchestration | `bin/mas` |
| **Blackboard** | Shared SQLite database for cross-agent context | `blackboard/shared_context.db` |
| **Ontology** | Agent roles, protocols, communication standards | `ontology/mas-ontology.md` |
| **Agent Memories** | Daily MAS session logs per agent | `agent-memories/{agent}_{date}.md` |
| **Scripts** | Utilities (PDF reader, context maintenance) | `scripts/` |
| **Projects** | Per-project state and memory files | `projects/{project}/` |

---

## 3. The Five Agents

### 3.1 Agent Roster

| Agent | Role ID | Emoji | Primary Function | Model |
|-------|---------|-------|------------------|-------|
| **Archie** | `agent_facilitator_01` | 🦉 | Project leadership, synthesis | moonshot/kimi-k2.5 |
| **Wang** | `agent_researcher_01` | 🦉 | Deep research, financial analysis | minimax/MiniMax-M2.7 |
| **Lynch** | `agent_auditor_01` | ⚖️ | Validation, conflict resolution | zenmux/z-ai/glm-5-turbo |
| **Alonzo** | `agent_tech_strat_01` | 🎯 | Tech strategy, competitive intel | zenmux/anthropic/claude-opus-4.6 |
| **Bootstrap (Bob)** | `agent_maintainer_01` | 🔧 | System maintenance, diagnostics | zenmux/qwen/qwen3.5-plus |

### 3.2 Agent Specialties

#### Archie — General Manager / Facilitator
- Issues `[TASK:<agent>]` blocks for work delegation
- Writes `[DONE]` with final conclusions
- Detects conflicts and coordinates resolution
- **Authority**: Lead agent in `mas lead` workflows
- **Escalation**: None (top of chain)

#### Wang — Researcher / Analyst
- Deep financial research and DCF modeling
- SEC EDGAR data extraction
- External thesis triangulation (Protocol v2.0)
- **PDF Access**: `python3 scripts/read_pdf.py <path>`
- **Authority**: Execution (receives tasks from Archie)

#### Lynch — Auditor / Validator
- Systematic verification against authoritative sources
- Catches material discrepancies and methodological errors
- Structured audit checklists (7-point protocol)
- **Verdicts**: PASS / CONDITIONAL PASS / FAIL
- **Authority**: Quality gate (can block progression)

#### Alonzo — Tech Strategy Research
- Bridge between technical feasibility and economic viability
- Strategic frameworks: Wardley Mapping, Jevons Paradox, OODA Loop
- Competitive intelligence and second-order thinking
- **Memory**: 5-layer architecture (L1-L5)
- **Collaboration**: Wang (capital constraints), Archie (cross-domain)

#### Bootstrap (Bob) — IT / System Maintainer
- Infrastructure monitoring and technical diagnostics
- Context propagation issue resolution
- Watchdog escalation handling
- **Fixes Applied**: Context overflow, session locks, memory reorganization
- **Authority**: Technical overrides on system issues

---

## 4. Solving Context Bloating: Tiered Smart Compacting

### 4.1 The Problem

Early MAS Hub sessions suffered from **context bloating**:
- Naive approach: Show all exchanges → token overflow at ~10 exchanges
- Initial fix: Show 2 recent + summaries → still bloated over time
- Real issue: Agents couldn't see actual content from previous exchanges

### 4.2 The Solution: Hybrid Relevance System

Implemented **3-layer context architecture** with adaptive relevance scoring:

```
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT INJECTION LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: MOST RECENT (Always Shown)                       │
│  ├─ Last 2 exchanges: FULL content (1000 char limit)       │
│  └─ Token budget: ~1000 tokens                             │
│                                                             │
│  Layer 2: ADAPTIVE RELEVANCE (Scored)                      │
│  ├─ HIGH (score ≥6): Full content (800 char limit)         │
│  ├─ MEDIUM (score 3-5): Summary only                       │
│  └─ LOW (score <3): Excluded (timestamp only)              │
│                                                             │
│  Layer 3: PROJECT HEADER (Always)                          │
│  └─ Topics, entities, current state (~200 tokens)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Relevance Scoring Algorithm

```python
score = min(topic_overlap * 2, 4)      # Max 4 pts
      + min(entity_overlap * 2, 4)     # Max 4 pts  
      + temporal_proximity               # Max 2 pts
      # Total: 0-10 scale
```

| Factor | Weight | Criteria |
|--------|--------|----------|
| Topic overlap | +2 per match | semiconductors, AI, financial, etc. |
| Entity overlap | +2 per match | Companies, tickers (NVDA, AMD, etc.) |
| Temporal | +2 if <5min | Recent exchanges get bonus |

### 4.4 Token Budgets

| Layer | Min | Max | Typical |
|-------|-----|-----|---------|
| Project Header | 100 | 200 | 150 |
| Adaptive Relevance | 300 | 1000 | 600 |
| Recency (2 full) | 400 | 2000 | 1000 |
| **Total** | **900** | **3200** | **1750** |

**Result**: 50-turn research sessions stay under ~2000 tokens vs. 150,000+ before.

---

## 5. Case Study: 3-Company Cross Comparison

### 5.1 Project Overview

**Project:** `3_cross_comparison`  
**Date:** March 23, 2026  
**Companies:** GOOGL, AMZN, MSFT  
**Outcome:** Discovered critical price errors, implemented Protocol v2.1

### 5.2 Agent Contributions

#### Archie — Facilitation
- Initiated project with 5-stage protocol
- Tasked Wang with external thesis map
- Synthesized final investment recommendations
- **Critical moment**: Stopped prematurely → Bob implemented Stage Gate reminders

#### Wang — Research
- Compiled 3-company comparison framework
- Extracted FCF, margins, P/E ratios from SEC filings
- **Error**: Used stale price data (GOOGL ~$185 vs actual ~$298)
- **Resolution**: Re-verified all prices with 3-source cross-check

#### Lynch — Audit
- Executed 7-point audit checklist
- **Caught**: FY timing discrepancy (MSFT Jun 30 vs others Dec 31)
- **Caught**: Cloud thesis overlap across all three companies
- **Critical**: Identified 62% price error in GOOGL data
- **Verdict**: CONDITIONAL PASS → PASS after corrections

#### Alonzo — Strategic Analysis (via TUI)
- Provided tech strategy perspective through independent TUI window
- Analyzed competitive positioning
- Contributed Wardley Mapping insights
- Validated strategic moats (MSFT AI, GOOGL Search, AMZN Logistics)

#### Bootstrap (Bob) — System Fixes
- **Fixed**: Context overflow bug (reduced full responses 2000→1000 chars)
- **Fixed**: Session lock issues for Alonzo
- **Fixed**: Context propagation to Lynch (reversed list bug)
- **Implemented**: Stage Gate protocol to prevent premature [DONE]
- **Reorganized**: All 5 agent memory structures for consistency

### 5.3 Key Learnings

| Issue | Solution | Status |
|-------|----------|--------|
| Stale price data | Protocol v2.1: Real-time verification with timestamps | ✅ Implemented |
| Premature completion | Stage Gate: 5 mandatory stages before [DONE] | ✅ Implemented |
| Context overflow | Tiered compacting: 3-layer architecture | ✅ Implemented |
| Memory duplication | Consolidated to `memory/` directory | ✅ Fixed |

---

## 6. Communication Protocols

### 6.1 Standard Tags

| Tag | Usage | Example |
|-----|-------|---------|
| `[TASK:<agent>]` | Delegate work | `[TASK:wang] Extract revenue data` |
| `[DONE]` | Signal completion | `[DONE] Analysis complete` |
| `[MISSING:]` | Flag knowledge gaps | `[MISSING: Q1 2026 guidance]` |
| `[ESCALATE:<agent>]` | Request intervention | `[ESCALATE:bootstrap] Timeout error` |
| `[STATUS:]` | Progress update | `[STATUS: blocked] Waiting for data` |

### 6.2 5-Stage Research Protocol (v2.1)

```
Stage 1: Fact Table
  └─ Filing-grounded numbers only
  
Stage 2: External Assumption Map  
  └─ 2+ sources BEFORE model building
  
Stage 3: Multiple Architectures
  └─ DCF + SOTP + segment decomposition
  
Stage 4: Divergence Memo
  └─ Document if >20% from consensus
  
Stage 5: Enhanced Audit
  └─ Lynch audit with 7-point checklist
```

---

## 7. Future Development Directions

### 7.1 Near-Term (v4.4.x)

- **Project Memory Files**: Persistent `projects/{project}/memory.md` for long-running work
- **Adaptive Relevance v2**: ML-based scoring instead of rule-based
- **Agent Self-Selection**: Allow agents to request specific context expansions
- **Workflow Templates**: Pre-defined patterns for common research types

### 7.2 Mid-Term (v5.x)

- **Cross-Project Context**: Share insights across related projects
- **Automated Maintenance**: Bob runs context pruning autonomously
- **Conflict Prediction**: Detect potential disagreements before they occur
- **Ontology Evolution**: Auto-expand entity graph based on research

### 7.3 Long-Term (v6.x)

- **Meta-Learning**: Agents learn optimal collaboration patterns per project type
- **External Tool Integration**: Direct API access for real-time data
- **Visual Workflows**: Graph-based project state visualization
- **Human-in-the-Loop**: Seamless handoffs for complex decisions

---

## 8. File Organization

```
~/Projects/mas-hub/
├── bin/
│   ├── mas                    # Main CLI (v4.3.4)
│   └── mas-tui               # TUI wrapper
├── ontology/
│   └── mas-ontology.md       # Agent roles & protocols
├── scripts/
│   ├── read_pdf.py           # PDF utility
│   ├── context_maintenance.py # Bob's maintenance service
│   └── mas_context.py        # Adaptive context assembly
├── docs/
│   ├── context-maintenance-design.md
│   └── mas-hub-introduction.md  # This file
├── blackboard/
│   └── shared_context.db     # Cross-agent exchanges
└── projects/                 # Per-project state

~/.openclaw/
├── mas-hub/
│   ├── agent-memories/       # Daily MAS logs
│   ├── config.json          # Agent registry
│   └── projects/            # Active project state
├── agents/{agent}/           # Runtime config only
└── workspace-{agent}/        # Personal memory + files
```

---

## 9. Key Metrics

| Metric | Value |
|--------|-------|
| **Version** | v4.3.4 |
| **Agents** | 5 (Archie, Wang, Lynch, Alonzo, Bootstrap) |
| **Projects Completed** | 5+ (GOOGL, AMZN, MSFT, 3-cross, work_review) |
| **Context Efficiency** | ~2000 tokens per message (was ~150,000) |
| **Audit Pass Rate** | 100% (all projects audited) |
| **Bugs Fixed** | 15+ (context, memory, propagation) |

---

## 10. Credits

**Created by:** Alan (沈桢天)  
**System Maintainer:** Bootstrap (Bob) — `agent_mas_maintainer_01`  
**Architecture:** Context Maintenance System v1.0  
**Protocol:** MAS Research Protocol v2.1

---

*Last updated: March 23, 2026*  
*For updates, check: ~/Projects/mas-hub/docs/*

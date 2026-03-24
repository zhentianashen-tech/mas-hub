# Memory Systems in MAS Hub

**Version:** 1.0  
**Date:** 2026-03-23  
**Purpose:** Explain the different memory architectures used by MAS Hub agents

---

## Overview

MAS Hub agents use **two different memory architectures**:

| Architecture | Agents | Use Case |
|--------------|--------|----------|
| **5-Layer System** | Alonzo | Complex strategic analysis with structured knowledge |
| **Standard System** | Archie, Wang, Lynch, Bootstrap | Daily logs + long-term MEMORY.md |

---

## 1. Alonzo's 5-Layer Memory System

Alonzo uses a sophisticated 5-layer architecture designed for **tech strategy research** requiring structured knowledge management.

### Directory Structure

```
workspace-alonzo/
├── alonzo_memory/                 # 5-layer memory system
│   ├── L1_bootstrap/             # Self-configuration
│   │   └── self_config.md        # Core competencies, projects, collaboration matrix
│   ├── L2_daily_logs/            # Activity stream
│   │   └── YYYY-MM-DD.md         # Daily technical audits, competitive alerts
│   ├── L3_sessions/              # Conversation history
│   │   └── {session_id}.md       # Session summaries
│   ├── L4_knowledge_base/        # Structured intelligence
│   │   ├── tech_strat_frameworks.md  # Wardley Mapping, Jevons Paradox, etc.
│   │   └── [additional domains]  # As research expands
│   └── L5_ontology/              # Entity graph
│       └── graph.jsonl           # Agent, TechnologyTrend, Competitor entities
│
├── memory/                        # Standard daily logs (canonical)
│   └── 2026-03-23.md
└── MEMORY.md                      # Memory overview document
```

### Layer Descriptions

#### L1: Bootstrap (Self-Configuration)
**Location:** `L1_bootstrap/self_config.md`

Contains Alonzo's foundational configuration:
- Core competencies (AI/ML infrastructure, distributed systems)
- Active projects and research focus areas
- Collaboration matrix with other agents
- Response patterns and operating modes

**Updated:** On configuration changes, role updates

#### L2: Daily Logs (Activity Stream)
**Location:** `L2_daily_logs/YYYY-MM-DD.md`

Structured daily activity logs:
- Technical audits performed
- Competitive intelligence gathered
- Strategic findings with implications
- Timestamps for temporal awareness

**Note:** Duplicated with `memory/YYYY-MM-DD.md` (canonical location). **L2 should be consolidated to `memory/`.**

**Updated:** Daily or per significant activity

#### L3: Sessions (Conversation History)
**Location:** `L3_sessions/`

Session-by-session summaries:
- User interaction patterns
- Decision rationale
- Context from multi-turn conversations

**Updated:** Per session

#### L4: Knowledge Base (Structured Intelligence)
**Location:** `L4_knowledge_base/`

Curated strategic frameworks and domain knowledge:
- `tech_strat_frameworks.md` — Wardley Mapping, Jevons Paradox, Value Chain Analysis, OODA Loop
- Additional files as research domains expand

**Updated:** When new frameworks or domains are added

#### L5: Ontology (Entity Graph)
**Location:** `L5_ontology/graph.jsonl`

Machine-readable entity relationships:
- Entity types: Agent, TechnologyTrend, Competitor, StrategicRecommendation, Relationship
- Cross-references with Archie/Wang ontology
- Queryable for context assembly

**Updated:** When new entities or relationships discovered

### Memory Operations

#### Write Pattern
1. Technical research → L2 daily log (and canonical `memory/`)
2. Strategic frameworks → L4 knowledge base
3. Competitive entities → L5 ontology
4. Cross-references → Unified graph

#### Read Pattern
1. **Startup:** L1 (load self-configuration)
2. **Analysis:** L4 (reference frameworks)
3. **Context:** L5 (query related entities)
4. **Continuity:** L2/`memory/` (review recent findings)

---

## 2. Standard Memory System (Archie, Wang, Lynch, Bootstrap)

Other agents use a simpler, flat memory structure:

### Directory Structure

```
workspace-{agent}/
├── memory/                        # Daily logs only
│   ├── 2026-03-22.md
│   ├── 2026-03-23.md
│   └── ...
│
├── MEMORY.md                      # Long-term curated memory
└── MAS_HUB_MEMORY.md              # MAS Hub access instructions
```

### Components

#### Daily Logs (`memory/YYYY-MM-DD.md`)
- Date-stamped session summaries
- Key decisions and findings
- Tasks and pending items
- Lessons learned

**Example from Wang:**
```markdown
# Daily Log — 2026-03-23

## Session Start
- **Time:** 10:30 CST
- **Type:** MAS Hub (3_cross_comparison)
- **Project:** 3-company comparison (GOOGL, AMZN, MSFT)

## Tasks
- [x] Extract FCF data for all 3 companies
- [x] Build comparison framework
- [x] Price verification (caught errors!)

## Key Decisions
- MSFT: BUY, $500 target
- AMZN: BUY, $280 target  
- GOOGL: HOLD, $340 target

## Lessons Learned
- Always verify prices <15 min old (Protocol v2.1)
```

#### Long-Term Memory (`MEMORY.md`)
Curated long-term knowledge:
- Architecture decisions
- Important lessons
- Agent relationships
- Current state

**Example from Bootstrap:**
- MAS Hub version
- Key architecture decisions
- Current projects
- Maintenance patterns

---

## 3. Comparison: 5-Layer vs Standard

| Aspect | 5-Layer (Alonzo) | Standard (Others) |
|--------|------------------|-------------------|
| **Complexity** | High | Low |
| **Use Case** | Strategic research | General research/audit |
| **Knowledge Structure** | Structured (L1-L5) | Flat (daily logs) |
| **Ontology** | Machine-readable graph | Implicit in text |
| **Frameworks** | Explicit (L4) | Implicit in MEMORY.md |
| **Queryability** | High (L5 graph) | Low (text search) |
| **Maintenance** | Higher | Lower |
| **Best For** | Competitive intel, strategy | Financial research, audit |

---

## 4. MAS Hub Memory (All Agents)

**Separate from workspace memory** — only for MAS Hub sessions:

```
~/.openclaw/mas-hub/agent-memories/
├── archie_2026-03-23.md         # MAS session work only
├── wang_2026-03-23.md
├── lynch_2026-03-23.md
├── alonzo_2026-03-23.md
└── bootstrap_2026-03-23.md
```

### Strict Separation Rule

| Memory Type | Location | Access |
|-------------|----------|--------|
| **Workspace Memory** | `workspace-{agent}/` | Native sessions only |
| **MAS Hub Memory** | `mas-hub/agent-memories/` | MAS Hub sessions only |

**Never cross-pollinate.** Agents maintain dual awareness:
- Native workspace context for direct TUI chats
- MAS Hub context for collaborative projects

---

## 5. Recommendations

### For Alonzo (5-Layer)

**Consolidate L2:** The `L2_daily_logs/` duplicates `memory/`. After Alonzo reorganizes:
- Canonical daily logs: `workspace-alonzo/memory/`
- Delete `alonzo_memory/L2_daily_logs/`

**Keep L1, L3, L4, L5:** These provide unique structured value.

### For Archie/Wang/Lynch/Bootstrap (Standard)

**No changes needed.** The standard system is sufficient for:
- Financial research (Wang)
- Facilitation/synthesis (Archie)
- Audit/validation (Lynch)
- System maintenance (Bootstrap)

### Future Considerations

If other agents need structured knowledge:
1. **Option A:** Adopt 5-layer (high overhead)
2. **Option B:** Enhance standard with `knowledge_base/` subdirectory
3. **Option C:** Use shared ontology in MAS Hub blackboard

**Recommendation:** Keep Alonzo as the only 5-layer agent. Others benefit from simplicity.

---

## 6. File Locations Summary

| Agent | Memory System | Canonical Daily Logs | Long-Term |
|-------|---------------|---------------------|-----------|
| **Alonzo** | 5-Layer | `workspace-alonzo/memory/` | `alonzo_memory/L1-L5` |
| **Archie** | Standard | `workspace/memory/` | `workspace/MEMORY.md` |
| **Wang** | Standard | `workspace-wang/memory/` | `workspace-wang/MEMORY.md` |
| **Lynch** | Standard | `workspace-lynch/memory/` | `workspace-lynch/MEMORY.md` |
| **Bootstrap** | Standard | `workspace-bootstrap/memory/` | `workspace-bootstrap/MEMORY.md` |

---

## 7. Quick Reference

### Access Alonzo's 5-Layer Memory

```bash
# L1: Self-config
cat ~/.openclaw/workspace-alonzo/alonzo_memory/L1_bootstrap/self_config.md

# L4: Knowledge base
cat ~/.openclaw/workspace-alonzo/alonzo_memory/L4_knowledge_base/tech_strat_frameworks.md

# L5: Ontology graph
cat ~/.openclaw/workspace-alonzo/alonzo_memory/L5_ontology/graph.jsonl
```

### Access Standard Agent Memory

```bash
# Daily log
cat ~/.openclaw/workspace-wang/memory/2026-03-23.md

# Long-term memory
cat ~/.openclaw/workspace-wang/MEMORY.md

# MAS Hub memory
cat ~/.openclaw/mas-hub/agent-memories/wang_2026-03-23.md
```

---

*Document created: 2026-03-23*  
*Maintainer: Bootstrap (Bob)*

# MAS Hub Ontology v1.0

**Version:** 1.0  
**Created:** 2026-03-22  
**Location:** `~/Projects/mas-hub/ontology/mas-ontology.md`

---

## 1. Agent Roles & Responsibilities

### Archie (General Manager / Facilitator)
- **Role ID:** `agent_facilitator_01`
- **Primary Function:** Project leadership, task orchestration, final synthesis
- **Capabilities:**
  - Issues `[TASK:<agent>]` blocks for work delegation
  - Writes `[DONE]` with final conclusions
  - Detects conflicts and coordinates resolution
  - Manages research workflow progression
  - Makes strategic decisions on task reassignment
- **Authority Level:** Lead agent in `mas lead` workflows
- **Escalation Target:** None (top of chain)
- **Model Profile:** Primary model with strong reasoning capabilities

### Wang (Researcher / Analyst)
- **Role ID:** `agent_researcher_01`
- **Primary Function:** Deep financial research, data extraction, DCF modeling
- **Capabilities:**
  - Provides detailed numerical analysis with methodology
  - Accesses external data sources (SEC EDGAR, financial APIs, PDFs)
  - **PDF Reading:** Use `python3 ~/Projects/mas-hub/scripts/read_pdf.py <path>` for any PDF
  - Delivers framework responses when precise data unavailable
  - Corrects errors rapidly when flagged by Lynch
  - Performs sensitivity analysis and scenario modeling
- **Authority Level:** Execution (receives tasks from Archie)
- **Escalation Target:** Bootstrap (technical), Archie (task scope)
- **Model Profile:** Research-optimized with data analysis capabilities

### Lynch (Auditor / Validator)
- **Role ID:** `agent_auditor_01`
- **Primary Function:** Fact validation, conflict resolution, quality assurance
- **Capabilities:**
  - Systematic verification against authoritative sources
  - **PDF Reading:** Use `python3 ~/Projects/mas-hub/scripts/read_pdf.py <path>` for any PDF
  - Catches material discrepancies and methodological errors
  - Provides structured audit checklists
  - Maintains high evidentiary standards
  - Rates confidence levels on claims
- **Authority Level:** Quality gate (can block progression)
- **Escalation Target:** Bootstrap (technical), Archie (priority conflicts)
- **Model Profile:** Validation-focused with attention to detail

### Bootstrap (IT / System Maintainer)
- **Role ID:** `agent_maintainer_01`
- **Primary Function:** Infrastructure monitoring, technical issue diagnosis, escalation handling
- **Capabilities:**
  - Monitors agent health and system performance
  - Diagnoses technical failures (empty payloads, timeouts, context issues)
  - Provides data access solutions when needed
  - Handles watchdog escalations automatically
  - Maintains MAS hub infrastructure
- **Authority Level:** Technical authority (overrides on system issues)
- **Escalation Target:** Human operator (Alan)
- **Model Profile:** Technical troubleshooting with system awareness

## Kimi Code CLI Integration (IT Maintenance Tool)

**Tool ID:** `tool_it_maint_01`  
**Type:** External CLI Tool (not an OpenClaw agent)  
**Location:** `kimi` command (installed via uv)  
**Version:** 1.23.0+  
**Documentation:** https://moonshotai.github.io/kimi-cli/

### Purpose
Kimi Code CLI serves as the default IT maintenance automation tool for MAS Hub. It handles:
- Routine maintenance tasks (log rotation, config validation, dependency updates)
- Code fixes and refactoring in MAS Hub scripts
- System health monitoring and preventive actions
- Technical documentation updates
- Git operations (commits, branches, PRs for maintenance changes)

### Integration Pattern
```
Agent (Bootstrap/Archie) → MAS CLI → Kimi Code CLI → Execute Maintenance Task
```

### Usage Examples
```bash
# Interactive maintenance session
kimi "Rotate logs older than 7 days in ~/.openclaw/mas-hub/logs/"

# Non-interactive task execution
kimi --print "Validate MAS Hub config.json and fix any JSON syntax errors"

# Git maintenance operations
kimi "Check git status in ~/Projects/mas-hub/, commit any config changes with message 'Maintenance: updated config'"
```

### Safety Constraints
- **Non-destructive by default:** Uses `trash` over `rm`, creates backups before modifications
- **Scope-limited:** Only operates within MAS Hub directories (`~/Projects/mas-hub/`, `~/.openclaw/mas-hub/`)
- **Escalation:** Complex issues escalate to Bootstrap (human maintainer Bob)
- **Logging:** All Kimi Code operations logged to `~/.openclaw/mas-hub/logs/kimi-maintenance.log`

### Escalation Target
Kimi Code escalates to **Bootstrap (Bob)** when:
- Maintenance task requires human approval (destructive operations)
- System-wide changes needed (OpenClaw config, agent models)
- Unrecoverable errors detected (database corruption, missing critical files)

### Alonzo (Tech Strategy Research)
- **Role ID:** `agent_tech_strat_01`
- **Primary Function:** Technical strategy analysis, competitive intelligence, deep-tech research
- **Capabilities:**
  - Bridge between technical feasibility and economic viability
  - Deep-tech stack audits (AI/ML infrastructure, distributed systems)
  - Competitive situational awareness and second-order thinking
  - Strategic frameworks: Wardley Mapping, Jevons Paradox, Value Chain Analysis, OODA Loop
  - Collaborates with Wang on capital constraints for Build/Buy decisions
  - Collaborates with Archie on cross-domain research
  - **Strict Memory Control:** MAS Hub memory separate from 5-layer workspace memory
- **Authority Level:** Strategic advisor (provides technical perspective)
- **Escalation Target:** Archie (strategic conflicts), Bootstrap (data access)
- **Model Profile:** Strategic analysis with technical depth
- **Memory Architecture:** 5-layer system (L1 bootstrap, L2 daily logs, L3 sessions, L4 knowledge base, L5 ontology)

---

## 2. Communication Protocols

### Task Delegation
```
[TASK:<agent>] <instruction>
```
- **Usage:** Delegate work to specific agent
- **Example:** `[TASK:wang] Extract revenue figures from the 10-K filing`
- **Response Expected:** Agent completes task or reports blocker

### Completion Signal
```
[DONE] <final synthesis/conclusion>
```
- **Usage:** Conclude research with final answer
- **Example:** `[DONE] GOOGL is a BUY with $110 price target based on...`
- **Response Expected:** Workflow terminates, results archived

### Knowledge Gap Marker
```
[MISSING: <description>]
```
- **Usage:** Mark unavailable data or unresolved questions
- **Example:** `[MISSING: Q1 2026 guidance not yet released by company]`
- **Response Expected:** Lead decides to proceed or wait

### Escalation Request
```
[ESCALATE:<agent>] <issue description>
```
- **Usage:** Request intervention from specialist agent
- **Example:** `[ESCALATE:bootstrap] Wang experiencing repeated timeout errors`
- **Response Expected:** Escalated agent diagnoses and resolves

### Status Report
```
[STATUS: <state>] <details>
```
- **Usage:** Report current progress or blockers
- **Example:** `[STATUS: blocked] Waiting for SEC filing access`
- **Response Expected:** Lead provides guidance or reassigns

---

## 3. Memory Architecture

### MAS Hub Memory (Project-Scoped)
- **Location:** `~/.openclaw/mas-hub/agent-memories/{agent}_{YYYY-MM-DD}.md`
- **Purpose:** Daily memory for MAS Hub interactions only
- **Scope:** Project-specific tasks, findings, collaborations
- **Retention:** Daily files, archived by project context
- **Access:** Only during MAS Hub operations (`mas` commands)

### Native Workspace Memory (Agent-Scoped)
- **Location:** `~/.openclaw/workspace/memory/{YYYY-MM-DD}.md`
- **Purpose:** Agent's personal continuity across all interactions
- **Scope:** Direct TUI sessions, personal learnings, identity
- **Retention:** Daily files, curated into long-term memory
- **Access:** All agent interactions (MAS and non-MAS)

### Shared Blackboard (Project-Wide)
- **Location:** `~/.openclaw/mas-hub/blackboard/shared_context.db`
- **Purpose:** Cross-agent coordination and context sharing
- **Scope:** All exchanges within a MAS project session
- **Structure:** SQLite with structured fields (agent, request, summary, key_points, etc.)
- **Access:** All agents during MAS Hub operations

### Critical Separation Rule
> **MAS Hub memories must NEVER reference or pollute native workspace memories.**  
> Agents maintain dual awareness: MAS context during `mas` commands, native context otherwise.

---

## 4. Project Lifecycle

### Phase 1: Briefing
- **Trigger:** `mas new <project>` or `mas lead @<agent> "<brief>"`
- **Activities:**
  - Project scope definition
  - Team assembly
  - Initial task assignment
- **Output:** Project initialized, agents briefed

### Phase 2: Research
- **Lead:** Wang (researcher)
- **Activities:**
  - Data extraction from sources (SEC filings, reports, APIs)
  - Quantitative analysis (DCF, comparables, sensitivity)
  - Framework development
- **Output:** Research deliverables with citations

### Phase 3: Audit
- **Lead:** Lynch (auditor)
- **Activities:**
  - Fact validation against primary sources
  - Methodology review
  - Conflict detection
  - Confidence rating
- **Output:** Audit report with pass/fail/conditional verdict

### Phase 4: Synthesis
- **Lead:** Archie (facilitator)
- **Activities:**
  - Integrate research and audit findings
  - Resolve conflicts
  - Formulate final recommendation
- **Output:** `[DONE]` with investment thesis

### Phase 5: Verification (Optional)
- **Trigger:** Audit identifies gaps or errors
- **Activities:**
  - Corrective research
  - Re-audit
  - Final validation
- **Output:** Verified conclusion or `[MISSING:]` markers

---

## 5. Escalation Chain

```
Agent Technical Failure
    ↓
Kimi Code CLI (Automated Maintenance & Fixes)
    ↓
If unresolved → Bootstrap (Diagnosis & Remediation)
    ↓
If unresolved → Human Operator (Alan)
    ↓
If systemic → MAS Hub Maintenance (Bob)
```

### Escalation Triggers
- **Empty Payload Errors:** Agent returns no usable content
- **Hard Timeout:** No response after 8 minutes (configurable)
- **Context Corruption:** Agent loses project awareness
- **Data Access Failure:** Cannot retrieve required sources
- **Model Unavailability:** Assigned model offline or rate-limited

### Escalation Protocol
1. **Detection:** Watchdog or agent self-report
2. **Logging:** Error details recorded in blackboard
3. **Dispatch:** `[ESCALATE:bootstrap]` with full context
4. **Diagnosis:** Bootstrap investigates (model, session, data access)
5. **Resolution:** Fix, reassign, or escalate to human
6. **Documentation:** Incident logged for future reference

---

## 6. Watchdog Parameters

### Timeout Configuration
| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAS_LEAD_MAX_ROUNDS` | 10 | Maximum facilitation rounds |
| `MAS_LEAD_SOFT_TIMEOUT` | 180s | Warning threshold (slow response) |
| `MAS_LEAD_HARD_TIMEOUT` | 480s | Escalation threshold (no response) |
| `MAS_LEAD_ESCALATE_AGENT` | bootstrap | Agent for technical escalations |
| `MAS_LEAD_STALL_ACTION` | partial | Action on total stall (partial|abort) |

### Task Ledger Fields
- `round`: Facilitation round number
- `agent`: Target agent ID
- `instruction`: Task description
- `issued_at`: Unix timestamp of dispatch
- `soft_due`: `issued_at + MAS_LEAD_SOFT_TIMEOUT`
- `hard_due`: `issued_at + MAS_LEAD_HARD_TIMEOUT`
- `status`: `dispatched` → `completed` | `failed` | `timeout` | `escalated`
- `completed_at`: Unix timestamp of completion
- `duration_ms`: Execution time in milliseconds
- `error`: Error message if failed/timeout

### Run Summary Format
```
Rounds: {n} | Tasks: {dispatched} dispatched, {completed} completed, {failed} failed, {timeout} timeout | Escalations: {n}
```

---

## 7. Directory Structure

```
~/Projects/mas-hub/              # Project source (git repo)
  bin/
    mas                          # Main MAS CLI (v4.2.2+)
    mas-tui                      # TUI wrapper
    mas-monitor                  # Background monitor
  ontology/
    mas-ontology.md              # THIS FILE - Central ontology
  scripts/
    read_pdf.py                  # PDF reading utility for agents
  docs/                          # Architecture documentation
  templates/                     # Workflow templates
  config.json                    # Agent configuration reference

~/.openclaw/mas-hub/             # Runtime data
  blackboard/
    shared_context.db            # SQLite blackboard
  agent-memories/                # Daily MAS memory files
  logs/                          # Orchestrator logs
  workflows/                     # Completed workflow archives
  state.json                     # Current project/session state
  config.json                    # Live agent configuration

~/.openclaw/agents/{agent}/      # Individual agent workspaces
  sessions/                      # Native session history
  agent/
    system.md                    # Core system prompt
  memory/                        # Native workspace memory
```

---

## 8. Glossary

| Term | Definition |
|------|------------|
| **Blackboard** | Shared SQLite database for cross-agent context |
| **Lead Agent** | Agent facilitating autonomous workflow (usually Archie) |
| **MAS Session** | Project-scoped interaction sequence with unique ID |
| **Task Ledger** | Runtime tracking of dispatched tasks and status |
| **Watchdog** | Timeout monitoring and auto-escalation system |
| **Stall-Safe Synthesis** | Partial conclusion when agents fail to respond |
| **Context Injection** | MAS awareness prepended to agent prompts |
| **Native Workspace** | Agent's personal OpenClaw context (separate from MAS) |

---

## 9. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-22 | Initial ontology release |

---

*This ontology is machine-readable and injected into all MAS Hub interactions. Agents reference this for role awareness, protocol compliance, and memory management.*

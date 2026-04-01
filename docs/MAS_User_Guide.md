# MAS (Multi-Agent System) User Guide

**Version:** 1.0.0  
**Created:** 2026-03-22  
**Agents:** Archie 🦉, Wang 🦉, Lynch ⚖️

---

## 🚀 Quick Start

```bash
# 1. Test individual agents
mas @wang "Research Tesla stock"
mas @archie "Summarize this report"
mas @lynch "Validate this thesis"

# 2. Run workflows
mas workflow research "Apple investment analysis"

# 3. Debate mode
mas debate "Is Bitcoin a good investment?"

# 4. Smart mode (auto-conflict detection)
mas smart "Should I buy NVIDIA stock?"

# 5. Check status
mas status
```

---

## 📋 Command Reference

### Direct Messaging

Send a message to a specific agent.

```bash
mas @<agent> "<message>"

# Examples
mas @wang "Research Tesla Q3 2026 earnings"
mas @archie "Summarize the key points"
mas @lynch "Validate these claims"
```

**Agents:**
- `@archie` — General intelligence, synthesis, summaries
- `@wang` — Financial research, deep analysis
- `@lynch` — Conflict resolution, validation, arbitration

### Broadcast

Send the same message to all agents simultaneously.

```bash
mas @all "<message>"

# Example
mas @all "Review this investment thesis for errors"
```

### Workflow Mode

Run predefined multi-step workflows.

```bash
mas workflow <name> "<context>"

# Available workflows:
mas workflow research "<topic>"     # Research → Validate → Synthesize
```

**Research Workflow Steps:**
1. **Wang** conducts comprehensive research
2. **Lynch** validates facts and flags conflicts
3. **Archie** synthesizes final report

### Debate Mode

Run an adversarial debate between agents with Lynch as judge.

```bash
mas debate "<topic>"

# Example
mas debate "Is the tech bubble going to burst?"
```

**Debate Structure:**
- **Round 1:** Wang (Pro) opening vs Archie (Con) opening
- **Round 2:** Lynch judges arguments
- **Round 3:** Rebuttals from both sides
- **Round 4:** Lynch delivers final judgment

### Smart Mode

Automatically detects conflicts between agents and arbitrates.

```bash
mas smart "<query>"

# Example
mas smart "What's the outlook for Tesla stock?"
```

**Smart Mode Flow:**
1. Both Wang and Archie analyze independently
2. Lynch checks for conflicts/contradictions
3. If conflicts found → Lynch arbitrates
4. Archie synthesizes unified answer

### Status

Check system and agent status.

```bash
mas status
```

Shows:
- Agent availability
- Message inbox counts
- Active workflows

---

## 🏗️ Architecture

### Directory Structure

```
~/.openclaw/mas-hub/
├── config.json           # System configuration
├── inbox/               # Agent mailboxes
│   ├── archie/         # Messages for Archie
│   ├── wang/           # Messages for Wang
│   └── lynch/          # Messages for Lynch
├── outbox/             # Agent responses
├── blackboard/         # Shared context/state
├── workflows/          # Active workflow instances
├── logs/               # System logs
│   ├── orchestrator.log
│   └── monitor.log
└── templates/          # Workflow templates
    ├── workflow.yaml
    └── debate.yaml
```

### Communication Flow

```
User
  │
  ▼
┌─────────────┐
│   mas CLI   │
└──────┬──────┘
       │
       ├───────────────┬───────────────┐
       ▼               ▼               ▼
  ┌─────────┐    ┌─────────┐    ┌─────────┐
  │  Archie │    │  Wang   │    │  Lynch  │
  │  🦉     │    │  🦉     │    │  ⚖️     │
  └────┬────┘    └────┬────┘    └────┬────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
                       ▼
              ┌─────────────┐
              │   Blackboard │
              │  (Shared     │
              │   State)     │
              └─────────────┘
```

---

## 🎯 Agent Roles & Strengths

### 🦉 Archie (Main Agent)

| Property | Value |
|----------|-------|
| **Role** | General Intelligence |
| **Model** | Moonshot Kimi K2.5 |
| **Strengths** | Synthesis, summarization, creative thinking |
| **Best For** | Final reports, executive summaries, brainstorming |

**Use When:**
- Need a comprehensive summary
- Want creative problem-solving
- Final output needs polish

### 🦉 Wang (Financial Research)

| Property | Value |
|----------|-------|
| **Role** | Financial Research Analyst |
| **Model** | Claude Opus 4 (via ZenMux) |
| **Strengths** | Deep research, financial analysis, data extraction |
| **Best For** | Investment research, due diligence, market analysis |

**Use When:**
- Need deep financial research
- Analyzing earnings reports
- Building investment theses

### ⚖️ Lynch (The Arbitrator)

| Property | Value |
|----------|-------|
| **Role** | Conflict Resolution Agent |
| **Model** | GPT-4.1 Mini (via ZenMux) |
| **Strengths** | Fact validation, evidence weighing, conflict detection |
| **Best For** | Validating claims, resolving contradictions, arbitration |

**Use When:**
- Two agents disagree
- Need fact-checking
- Require objective judgment

---

## 🔧 Advanced Usage

### Custom Workflows

Create custom workflows in `~/.openclaw/mas-hub/templates/`:

```yaml
# my-workflow.yaml
name: my-custom-flow
steps:
  - agent: wang
    action: analyze
    input: "{{USER_QUERY}}"
  
  - agent: lynch
    action: validate
    input: "{{previous.output}}"
```

Run with:
```bash
mas workflow my-custom-flow "Analyze this"
```

### Monitoring (Background)

Start the auto-conflict monitor:

```bash
# Start in background
mas-monitor &

# Or with custom check interval (seconds)
MAS_CHECK_INTERVAL=60 mas-monitor &

# Stop
kill %1  # or find PID and kill
```

The monitor:
- Checks agent outputs every 30 seconds
- Detects numerical conflicts (>5% variance)
- Automatically alerts Lynch
- Logs to `~/.openclaw/mas-hub/logs/monitor.log`

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAS_HUB` | MAS hub directory | `~/.openclaw/mas-hub` |
| `MAS_DEBUG` | Enable debug logging | `0` |
| `MAS_CHECK_INTERVAL` | Monitor check interval (seconds) | `30` |

---

## 📊 Workflow Examples

### Example 1: Research Workflow

```bash
$ mas workflow research "Tesla Q3 2026 investment thesis"

╔═══════════════════════════════════════════════════════════════╗
║           WORKFLOW: Research → Validate → Synthesize         ║
╚═══════════════════════════════════════════════════════════════╝

[Step 1/3] Wang conducting research...
✓ Research complete (1,247 words)

[Step 2/3] Lynch validating facts...
✓ Validation complete

[Step 3/3] Archie synthesizing final report...
✓ Synthesis complete

═══════════════════════════════════════════════════════════════
FINAL REPORT
═══════════════════════════════════════════════════════════════
[Final synthesized report appears here]
```

### Example 2: Debate Mode

```bash
$ mas debate "Is AI overvalued in 2026?"

╔═══════════════════════════════════════════════════════════════╗
║              DEBATE MODE: Wang vs Archie                      ║
║                      Judged by Lynch                          ║
╚═══════════════════════════════════════════════════════════════╝

Topic: Is AI overvalued in 2026?

[Round 1/4] Opening Statements

🦉 Wang (Pro):
AI sector fundamentals remain strong with revenue...

🦉 Archie (Con):
Valuation metrics suggest significant overextension...

[Round 2/4] Arbitration by Lynch

⚖️ Lynch (Judge):
Evaluating evidence quality using Source Authority...

[Round 3/4] Rebuttals
...

[Round 4/4] Final Analysis

⚖️ Lynch (Final Judgment):
Based on evidence quality, [winner] presents...
```

### Example 3: Smart Mode with Conflict

```bash
$ mas smart "What's Tesla's Q3 revenue?"

╔═══════════════════════════════════════════════════════════════╗
║                    SMART MODE (Auto-Detect)                  ║
╚═══════════════════════════════════════════════════════════════╝

[Phase 1] Gathering analysis from Wang and Archie...

[Phase 2] Checking for conflicts...
⚠️ Conflicts detected! Lynch is arbitrating...

⚖️ Lynch:
DISCREPANCY DETECTED:
- Wang reports: $25.5B (from 10-K filing, L1)
- Archie reports: $24.8B (from news article, L4)

Resolution: Level 1 source overrides. Correct value: $25.5B

[Phase 3] Synthesizing final answer...

═══════════════════════════════════════════════════════════════
FINAL ANSWER
═══════════════════════════════════════════════════════════════
Tesla's Q3 2026 revenue is $25.5B (validated from SEC 10-K filing)...
```

---

## 🐛 Troubleshooting

### Command Not Found

```bash
# Ensure ~/Projects/mas-hub/bin is in PATH
export PATH="$HOME/Projects/mas-hub/bin:$PATH"

# Or source your zshrc
source ~/.zshrc
```

### Agent Not Responding

```bash
# Check if agent exists
openclaw agents list

# Validate config
openclaw config validate

# Check gateway (optional)
openclaw health
```

### Workflow Fails

```bash
# Check logs
tail -f ~/.openclaw/mas-hub/logs/orchestrator.log

# Check workflow directory
ls -la ~/.openclaw/mas-hub/workflows/
```

### Conflict Detection Not Working

```bash
# Check if monitor is running
ps aux | grep mas-monitor

# Start manually with debug
MAS_DEBUG=1 mas-monitor

# Check monitor logs
tail -f ~/.openclaw/mas-hub/logs/monitor.log
```

---

## 🔗 Related Documentation

- **Wang Setup:** `~/Alan_Memory/OpenClaw_Wang_Agent_Setup.md`
- **Lynch Setup:** `~/Alan_Memory/OpenClaw_Lynch_Arbitrator_Setup.md`
- **MAS Architecture:** `~/Alan_Memory/MAS_Architecture_Proposal.md`

---

## 📝 Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-22 | Initial release with research workflow, debate mode, smart mode |

---

*MAS: Where agents collaborate, conflicts resolve, and insights multiply.* 🚀

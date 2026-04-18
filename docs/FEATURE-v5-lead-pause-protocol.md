# Feature Request: Lead Mode Pause Protocol

**Version Target:** MAS Hub v5.0.0  
**Priority:** Medium  
**Status:** Proposed  
**Created:** 2026-04-19  
**Reporter:** Alan (沈桢天)

---

## Problem Statement

**Current behavior:** When a lead agent (Archie) needs user input mid-run, it uses `[DONE]` to pause, which **incorrectly terminates the research session**.

**Example from `new_ideas_20260418` session:**
```
Round 4 / 10

Archie: I'm waiting for your decision on the three options I presented.
- Option A: Accept 2 signals, close project
- Option B: Search for more non-obvious ideas
- Option C: Deep-dive further

═══ Archie concluded the research ═══  ← WRONG: Session ended prematurely
```

**Issue:** Archie had no way to pause for user input without ending the session.

---

## Current Protocol Limitations

| Token | Purpose | Limitation |
|-------|---------|------------|
| `[TASK:agent]` | Dispatch work | Can't pause for user |
| `[DONE]` | Conclude research | Terminates session |
| `[MISSING:description]` | Flag gaps | Doesn't pause |
| `[ESCALATE:agent]` | Request help | For technical issues only |

**Missing:** No token for "pause and wait for user decision."

---

## Design Gap

### PROJECT LIFECYCLE Rules (Current)

```markdown
- Projects are NEVER complete until the USER explicitly closes them
- NEVER claim a project is "done" or "complete" based on your own assessment
- NEVER say 'nothing left to do' - always ask the user before wrapping up
- The USER, not you, decides when a project is finished
- [DONE] is reserved for when the user explicitly asks for final synthesis
```

**Conflict:** Rules say "ask the user," but there's no mechanism to pause for input.

---

## Proposed Solution

### New Token: `[PAUSE]`

```markdown
[PAUSE] Waiting for user decision on: <options>

Usage:
- Present options clearly
- Specify timeout (default: 5 minutes, configurable)
- User can respond via: mas @archie "proceed with Option A"
- After timeout: proceed with default or escalate
```

### Behavior

**When lead agent outputs `[PAUSE]`:**

1. **Don't exit** — keep session alive
2. **Print user instructions:**
   ```
   ⏸ Lead paused for your decision
   
   Options:
   - Option A: Accept 2 signals, close project
   - Option B: Search for more non-obvious ideas
   - Option C: Deep-dive further on these 2
   
   Respond with: mas @archie "proceed with Option A"
   
   Timeout: 5 minutes (will proceed with Option A by default)
   ```
3. **Wait for user input** — check blackboard for user message
4. **Resume or timeout** — continue lead loop after input or timeout

---

## Implementation Options

### Option A: Simple Polling (Recommended for v5)

```python
# In cmd_lead(), detect [PAUSE]
if '[PAUSE]' in lead_text:
    print("⏸ Lead paused for your decision")
    print("Respond with: mas @archie 'your decision'")
    
    # Wait for user input (poll blackboard)
    for i in range(timeout_seconds // 5):
        sleep(5)
        # Check if user sent message to lead agent
        if user_input_received():
            lead_message = f"User decided: {get_user_input()}"
            continue_loop = True
            break
    
    if not user_input_received():
        lead_message = "User did not respond. Proceeding with default: Option A"
        continue_loop = True
```

**Pros:**
- Simple to implement
- No new infrastructure
- Works with existing `mas @agent` mechanism

**Cons:**
- Polling required
- User must know to use `mas @archie` (not just `mas lead`)

---

### Option B: Interactive Prompt

```python
if '[PAUSE]' in lead_text:
    print("⏸ Lead paused. Choose an option:")
    print("  1) Option A")
    print("  2) Option B")
    print("  3) Option C")
    
    choice = input("Enter choice (1-3) or press Enter for default: ")
    
    if choice == "1":
        lead_message = "User chose Option A"
    # ... etc
```

**Pros:**
- Truly interactive
- No polling needed

**Cons:**
- Breaks non-interactive mode
- User must be watching terminal
- Can't run in background

---

### Option C: Hybrid (Best UX)

```python
if '[PAUSE]' in lead_text:
    # Start background watcher for user input
    print("⏸ Lead paused. Options:")
    print("  - Respond now: mas @archie 'proceed with Option A'")
    print("  - Or wait 5 minutes for default action")
    
    # Poll for input while showing progress
    start_time = time.time()
    while time.time() - start_time < timeout:
        if user_input_received():
            break
        print(f"⏳ Waiting... {int(timeout - (time.time() - start_time))}s remaining")
        sleep(10)
```

**Pros:**
- Works in both interactive and background mode
- Clear user feedback
- Timeout prevents indefinite pause

**Cons:**
- More complex
- Still requires polling

---

## User Experience Flow

### Before (Current)

```
$ mas lead @archie "Find 10 investment ideas"
Round 1 → Round 2 → Round 3 → Round 4
Archie: I need your decision...
═══ Archie concluded the research ═══  ← Session ends

$ mas lead @archie "continue with Option B"  ← Manual restart
```

### After (Proposed)

```
$ mas lead @archie "Find 10 investment ideas"
Round 1 → Round 2 → Round 3 → Round 4
Archie: [PAUSE] Waiting for your decision...

⏸ Lead paused for your decision
Options:
  A) Accept 2 signals, close project
  B) Search for more non-obvious ideas
  C) Deep-dive further

Respond with: mas @archie "proceed with Option A"
Timeout: 5 minutes (will proceed with Option A)

[User opens new terminal]
$ mas @archie "proceed with Option B"

[Original terminal resumes]
✓ User chose: Option B
Round 5 → Round 6 → ... → Round 8
═══ Archie concluded the research ═══  ← Natural conclusion
```

---

## Configuration

Add to `config.json`:

```json
{
  "lead_mode": {
    "pause_timeout_seconds": 300,
    "pause_default_action": "proceed_with_option_a",
    "pause_enabled": true
  }
}
```

Environment variables:
- `MAS_PAUSE_TIMEOUT=300` — seconds to wait for user input
- `MAS_PAUSE_DEFAULT=proceed` — action if timeout

---

## Alternative: Remove Need for Pause

**Instead of pausing, teach lead agents to:**

1. **Make autonomous decisions** — "Based on research goals, I'll proceed with Option B"
2. **Never ask for input mid-run** — Present options only at the END
3. **Use Bootstrap for guidance** — `[TASK:bootstrap] "What should I do?"` (escalate internally)

This avoids the need for a pause mechanism entirely.

---

## Recommendation

**For v5.0:**

1. **Implement Option A (Simple Polling)** — works with existing `mas @agent` mechanism
2. **Add `[PAUSE]` token** to lead agent protocol
3. **Update lead prompt** with clear pause instructions
4. **Add timeout** to prevent indefinite hangs
5. **Document in ontology** — "When to pause vs. autonomous decision"

**Quick fix for v4.x:**

Update lead prompt to say:
```
CRITICAL: NEVER use [DONE] to pause. Either:
1. Make autonomous decisions based on research goals
2. Continue working and present options at the END
3. Use [TASK:bootstrap] for internal guidance
```

---

## Testing Checklist

- [ ] Lead agent pauses on `[PAUSE]` token
- [ ] User can respond via `mas @archie "decision"`
- [ ] Session resumes after user input
- [ ] Timeout works (doesn't hang forever)
- [ ] Default action proceeds after timeout
- [ ] Works in background mode
- [ ] Works in TUI mode
- [ ] Logs pause/resume events

---

## Related Issues

- None yet (first report of this behavior)

---

## Version History

| Version | Changes |
|---------|---------|
| v4.3.x | No pause mechanism (current) |
| v5.0.0 | [PAUSE] protocol proposed |

---

*Feature request created: 2026-04-19*

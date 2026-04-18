# MAS Hub v5.0.0 Roadmap

**Target Release:** Q3 2026 (tentative)  
**Status:** Planning  
**Last Updated:** 2026-04-19

---

## v5.0.0 Goals

1. **Improved lead mode UX** — Better handling of user input mid-run
2. **Enhanced project management** — More robust file handling and path resolution
3. **Better error recovery** — Graceful handling of agent failures

---

## Planned Features

### 1. Lead Mode Pause Protocol ✨ NEW

**Issue:** Lead agents cannot pause for user input without ending session.

**Solution:** Add `[PAUSE]` token with timeout and user input injection.

**Status:** 📋 Proposed — See `FEATURE-v5-lead-pause-protocol.md`

**Priority:** Medium

---

### 2. Automatic Project Path Resolution

**Issue:** Agents save files to wrong locations (workspace vs. MAS Hub).

**Solution:** 
- Add `PROJECT_DIR` environment variable injection
- Create `mas-save` helper tool
- Add post-hook validation

**Status:** 📋 Proposed

**Priority:** High

---

### 3. Better Agent Failure Recovery

**Issue:** When agents fail, lead mode can stall indefinitely.

**Solution:**
- Better stall detection (no progress for N rounds)
- Auto-escalation with context
- Partial synthesis on total failure

**Status:** ✅ Partially implemented (stall-safe synthesis in v4.3)

**Priority:** Medium

---

### 4. Cross-Agent File Sharing Protocol

**Issue:** Agents can't reliably find each other's files.

**Solution:**
- Central project directory (already exists)
- File manifest in blackboard
- `mas-list-files` command

**Status:** 📋 Proposed

**Priority:** Low

---

### 5. Session Persistence & Resum

**Issue:** Lead sessions can't be resumed after crash/interruption.

**Solution:**
- Save task ledger to disk after each round
- `mas lead --resume` command
- Checkpoint state for recovery

**Status:** 📋 Proposed

**Priority:** Medium

---

## Backlog

- [ ] Web UI for project monitoring
- [ ] Docker container option
- [ ] PostgreSQL backend (alternative to SQLite)
- [ ] Plugin system for custom agents
- [ ] Multi-machine sync

---

## Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| v4.3.5 | 2026-04-18 | Fixed mas_context.py path bug |
| v4.3.4 | 2026-03-24 | Parser fix, Kimi Code integration |
| v4.3.0 | 2026-03-23 | Stage Gate protocol, watchdog timeouts |
| v4.2.0 | 2026-03-22 | Project-scoped sessions |
| **v5.0.0** | **Q3 2026** | **Pause protocol, path resolution, recovery** |

---

*Last updated: 2026-04-19*

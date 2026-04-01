# Changelog

All notable changes to MAS Hub will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-04-01

### Added
- **First stable release** of MAS Hub
- One-line installer (`install.sh`) with dependency checking
- Comprehensive [REQUIREMENTS.md](REQUIREMENTS.md) documentation
- Updated README with installation, configuration, and troubleshooting sections
- CHANGELOG for version tracking

### Core Features (v4.3.4 orchestrator)
- Project-scoped shared context with SQLite blackboard
- Per-agent MAS sessions (separate from native OpenClaw sessions)
- Adaptive context assembly with relevance scoring
- 5-stage research protocol (External → DCF → Follow-up → Audit → Synthesis)
- Lead mode with watchdog timeouts and auto-escalation
- Model switching per agent with 15+ model aliases
- Full response persistence (not just summaries)
- Kimi Code CLI integration for automated maintenance
- PDF reading utility for agents
- Stale lock detection and cleanup
- Comprehensive diagnostics (`mas doctor`, `mas ping`)

### Agents
- **Archie** — Facilitator/Lead agent
- **Wang** — Financial researcher
- **Lynch** — Auditor/validator
- **Bootstrap** — IT maintainer
- **Alonzo** — Tech strategy analyst

### Documentation
- Agent ontology (`ontology/mas-ontology.md`)
- Architecture docs (`docs/`)
- Incident reports (`docs/incident-*.md`)
- Maintenance guides (`docs/MAS_MAINTENANCE.md`)

### Changed
- Versioning scheme: Internal orchestrator version (4.x) → Release version (1.x)
- README restructured for first-time users
- Config format standardized

### Fixed
- OpenClaw JSON format change compatibility (dual parser support)
- Bash syntax errors in heredocs
- Context overflow issues (adaptive relevance scoring)
- Stale lock file blocking issues
- Agent session ID tracking

---

## [Unreleased] — Pre-1.0 Development

### v4.3.4 (2026-03-24)
- Parser fix for OpenClaw JSON format change
- Kimi Code IT maintenance integration
- Feishu removed from config

### v4.3.3 (2026-03-24)
- Added Alonzo (tech strategy agent)
- Context maintenance system v1.0

### v4.3.2 (2026-03-23)
- Stage Gate protocol implementation
- Watchdog timeouts with auto-escalation
- Stall-safe synthesis

### v4.2.x (2026-03-22)
- Initial MAS Hub implementation
- SQLite blackboard
- Project-scoped sessions
- Per-agent memory files

---

## Versioning Notes

**Internal Version:** The `mas` CLI reports internal version (e.g., 4.3.4) for debugging.

**Release Version:** GitHub releases use semantic versioning (e.g., 1.0.0).

**Mapping:**
- Release 1.0.0 → Internal v4.3.4
- Future releases will increment release version while internal version continues independently

---

## Upgrade Path

### From Pre-1.0 to 1.0.0

```bash
# Backup your runtime data
cp -r ~/.openclaw/mas-hub ~/.openclaw/mas-hub.backup

# Update source code
cd ~/Projects/mas-hub
git pull

# Re-run installer
./install.sh

# Verify
mas doctor
```

Your existing projects, agent memories, and blackboard data are preserved.

---

## Support

- **Issues:** GitHub Issues (TBD)
- **Discussions:** GitHub Discussions (TBD)
- **Discord:** https://discord.com/invite/clawd
- **Documentation:** `docs/` folder

# MAS Hub Release Checklist

**Version:** 1.0.0  
**Release Date:** 2026-04-01  
**Release Manager:** Alan (沈桢天)

---

## Pre-Release

### Code Quality
- [x] All backup files removed (`*.bak`, `*.broken`)
- [x] No debug print statements in production code
- [x] Bash scripts pass `bash -n` syntax check
- [x] Python scripts have no syntax errors
- [ ] All TODO/FIXME comments resolved or documented

### Documentation
- [x] README.md updated with installation instructions
- [x] REQUIREMENTS.md lists all dependencies
- [x] CHANGELOG.md documents all changes
- [x] LICENSE file added
- [x] Ontology version matches release version
- [x] Inline code comments are accurate

### Versioning
- [x] `MAS_VERSION` in `bin/mas` updated
- [x] `config.json` version field updated
- [x] `ontology/mas-ontology.md` version updated
- [x] CHANGELOG.md has release date
- [x] Git tag prepared: `v1.0.0`

### Testing
- [ ] Fresh install test on clean machine
- [ ] `mas doctor` passes all checks
- [ ] `mas new test-project` creates project
- [ ] `mas @wang "test message"` returns response
- [ ] `mas lead @archie "test briefing"` completes workflow
- [ ] Model switching works: `mas model wang set gpt-4.1-mini`
- [ ] Context persistence verified across sessions
- [ ] Watchdog timeout tested (optional, time-consuming)

### Compatibility
- [x] OpenClaw 2026.3.12+ compatibility verified
- [x] Python 3.8+ syntax only (no 3.10+ features)
- [x] macOS Bash 3.2 compatibility (no Bash 5+ features)
- [x] SQLite 3.28+ features only

### Security
- [x] No hardcoded API keys or secrets
- [x] No exfiltration of user data
- [x] Destructive operations use `trash` not `rm` (in Kimi Code wrapper)
- [x] Config backups created before modifications

---

## Release Process

### 1. Final Git Checks
```bash
cd ~/Projects/mas-hub
git status
git diff main
```

### 2. Run Full Test Suite
```bash
# Syntax checks
bash -n bin/mas
bash -n bin/mas-tui
bash -n bin/kimi-maintenance
python3 -m py_compile scripts/context_maintenance.py
python3 -m py_compile scripts/mas_context.py

# Functional tests
mas doctor
mas version
mas new release-test-$(date +%Y%m%d)
mas @wang "This is a release validation test. Reply 'TEST OK'."
mas status
mas projects
```

### 3. Create Git Tag
```bash
git add -A
git commit -m "Release v1.0.0 — Initial stable release"
git tag -a v1.0.0 -m "MAS Hub 1.0.0 — Initial stable release"
```

### 4. Push to GitHub
```bash
git push origin main
git push origin v1.0.0
```

### 5. Create GitHub Release
- Go to: https://github.com/openclaw/mas-hub/releases
- Click "Create a new release"
- Tag: `v1.0.0`
- Title: "MAS Hub 1.0.0 — Initial Stable Release"
- Description: Copy from CHANGELOG.md
- Attach: None (source code only)

### 6. Update Documentation
- [ ] Update https://openclaw.ai docs if applicable
- [ ] Announce on OpenClaw Discord
- [ ] Update any internal references to MAS Hub version

---

## Post-Release

### Verification
- [ ] GitHub release published and visible
- [ ] Git tag pushed successfully
- [ ] Install script works: `curl -fsSL ... | bash`
- [ ] Fresh install completes without errors

### Monitoring
- [ ] Watch GitHub Issues for bug reports
- [ ] Monitor Discord for user questions
- [ ] Track installation success rate

### Follow-up Tasks
- [ ] Create v1.0.1 patch release for any critical bugs
- [ ] Plan v1.1.0 feature release
- [ ] Gather user feedback for roadmap

---

## Rollback Plan

If critical bug found post-release:

1. **Immediately** pin the release as "pre-release" on GitHub
2. Post announcement on Discord about known issue
3. Fix bug in `main` branch
4. Release v1.0.1 with fix
5. Document in CHANGELOG.md under "Fixed"

---

## Release Notes Template

```markdown
## MAS Hub 1.0.0 — Initial Stable Release

**Release Date:** 2026-04-01  
**OpenClaw Compatibility:** 2026.3.12+  
**Python Requirement:** 3.8+

### What's New

MAS Hub provides multi-agent orchestration for OpenClaw with:
- Project-scoped shared context
- SQLite blackboard for structured persistence
- Adaptive context assembly with relevance scoring
- 5-stage research protocol with Stage Gate
- Lead mode with watchdog timeouts
- Per-agent model switching
- Automated maintenance via Kimi Code CLI

### Installation

```bash
curl -fsSL https://raw.githubusercontent.com/openclaw/mas-hub/main/install.sh | bash
```

### Quick Start

```bash
mas new my-project
mas @wang "Research topic..."
mas status
```

### Documentation

- [README](https://github.com/openclaw/mas-hub/blob/main/README.md)
- [Requirements](https://github.com/openclaw/mas-hub/blob/main/REQUIREMENTS.md)
- [Ontology](https://github.com/openclaw/mas-hub/blob/main/ontology/mas-ontology.md)

### Contributors

- Alan (沈桢天) — Initial work

---

**Full Changelog:** https://github.com/openclaw/mas-hub/compare/v0.0.0...v1.0.0
```

---

## Sign-Off

**Release Manager:** _________________  
**Date:** _________________  
**QA Sign-Off:** _________________  

---

*This checklist ensures MAS Hub releases are consistent, tested, and well-documented.*

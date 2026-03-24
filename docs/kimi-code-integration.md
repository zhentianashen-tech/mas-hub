# Kimi Code Integration Guide

**Version:** 1.0  
**Date:** 2026-03-24  
**Author:** Bob (MAS Hub Maintainer)

---

## Overview

Kimi Code CLI is now the default IT maintenance automation tool for MAS Hub. This guide covers installation, configuration, usage, and best practices.

## What is Kimi Code CLI?

Kimi Code CLI is an AI-powered coding agent from Moonshot AI that runs in your terminal. It can:
- Read and edit code files
- Execute shell commands
- Search and fetch web content
- Plan and execute multi-step tasks autonomously

**Documentation:** https://moonshotai.github.io/kimi-cli/  
**GitHub:** https://github.com/MoonshotAI/kimi-cli

---

## Installation

Kimi Code CLI is already installed on this system (v1.23.0).

### Verify Installation

```bash
kimi --version
# Output: kimi, version 1.23.0
```

### Reinstall if Needed

```bash
# Install via uv (recommended)
uv tool install kimi-cli

# Or via install script
curl -LsSf https://code.kimi.com/install.sh | bash
```

### Upgrade

```bash
uv tool upgrade kimi-cli --no-cache
```

---

## MAS Hub Integration

### Wrapper Scripts

Two wrapper scripts are provided for easy integration:

#### 1. `kimi-maintenance` - Ad-hoc Tasks

Execute single maintenance tasks with proper logging and safety constraints.

**Location:** `~/Projects/mas-hub/bin/kimi-maintenance`

**Usage:**

```bash
# Basic task execution
kimi-maintenance "Rotate logs older than 7 days"

# Dry run (preview without executing)
kimi-maintenance --dry-run "Clean up old workflow archives"

# Verbose output
kimi-maintenance --verbose "Validate all JSON config files"

# View recent maintenance logs
kimi-maintenance --log
```

**Options:**
- `-h, --help` - Show help message
- `-d, --dry-run` - Preview without executing
- `-v, --verbose` - Enable verbose output
- `-l, --log` - Show last 20 lines of maintenance log

#### 2. `kimi-daily-maintenance.sh` - Automated Routine

Runs a complete daily maintenance routine.

**Location:** `~/Projects/mas-hub/bin/kimi-daily-maintenance.sh`

**Usage:**

```bash
# Run full daily maintenance
~/Projects/mas-hub/bin/kimi-daily-maintenance.sh
```

**Tasks Performed:**
1. System health check (disk usage, log sizes)
2. Log rotation (compress logs >7 days old)
3. Config validation (JSON syntax check)
4. Workflow archival (move completed >30 days)
5. Git maintenance (commit config changes)
6. Inbox cleanup (remove messages >48h old)

---

## Common Maintenance Tasks

### Log Management

```bash
# Rotate old logs
kimi-maintenance "Compress log files older than 7 days in ~/.openclaw/mas-hub/logs/ using gzip"

# Analyze log sizes
kimi-maintenance "Report the 10 largest log files in MAS Hub directories"

# Clean empty log files
kimi-maintenance "Remove empty log files from ~/.openclaw/mas-hub/logs/"
```

### Configuration Management

```bash
# Validate and fix configs
kimi-maintenance "Validate JSON syntax of all config files and fix errors"

# Backup configs
kimi-maintenance "Create timestamped backups of all .json config files"

# Compare configs
kimi-maintenance "Show diff between current config and last backup"
```

### Git Operations

```bash
# Check and commit changes
kimi-maintenance "Check git status, commit any config changes with descriptive message"

# Create maintenance branch
kimi-maintenance "Create git branch 'maintenance/YYYY-MM-DD' for today's changes"

# Review recent commits
kimi-maintenance "Show last 10 commits in MAS Hub repository"
```

### Cleanup Tasks

```bash
# Archive old workflows
kimi-maintenance "Move completed workflow folders older than 30 days to archive"

# Clean inbox
kimi-maintenance "Remove processed messages older than 48 hours from inbox/"

# Remove temporary files
kimi-maintenance "Delete .tmp and .bak files older than 7 days"
```

### System Audits

```bash
# Disk usage audit
kimi-maintenance "Analyze disk usage in MAS Hub directories, identify files >100MB"

# Security audit
kimi-maintenance "Check for any world-readable config files containing sensitive data"

# Dependency audit
kimi-maintenance "List all Python dependencies and check for outdated packages"
```

---

## Safety Features

### Non-Destructive Defaults

- Uses `trash` command instead of `rm` for deletions
- Creates backups before modifying config files
- Requires confirmation for destructive operations

### Scope Limitation

Kimi Code is constrained to operate only within:
- `~/Projects/mas-hub/` (source code)
- `~/.openclaw/mas-hub/` (runtime data)

### Logging

All maintenance operations are logged to:
- `~/.openclaw/mas-hub/logs/kimi-maintenance.log` (individual tasks)
- `~/.openclaw/mas-hub/logs/daily-maintenance.log` (daily routines)

### Escalation

Kimi Code escalates to **Bootstrap (Bob)** when:
- Destructive operations are required
- System-wide changes needed
- Unrecoverable errors detected
- Database corruption found

---

## Scheduling

### Manual Execution

```bash
# Run daily maintenance manually
~/Projects/mas-hub/bin/kimi-daily-maintenance.sh

# Run specific task
kimi-maintenance "Validate and fix all configuration files"
```

### Cron Integration

Add to crontab (`crontab -e`):

```bash
# Daily maintenance at 6:00 AM
0 6 * * * ~/Projects/mas-hub/bin/kimi-daily-maintenance.sh >> ~/.openclaw/mas-hub/logs/cron-daily.log 2>&1

# Weekly full audit on Sundays at 2:00 AM
0 2 * * 0 kimi-maintenance "Perform full system audit and generate report" >> ~/.openclaw/mas-hub/logs/cron-weekly.log 2>&1
```

### OpenClaw Heartbeat

Add to `HEARTBEAT.md` in your workspace:

```markdown
# Daily Maintenance Check
- [ ] Run kimi-daily-maintenance.sh
- [ ] Review kimi-maintenance.log for errors
- [ ] Check disk usage < 80%
```

---

## Troubleshooting

### Kimi Code Not Found

```bash
# Check if installed
which kimi

# If not found, reinstall
uv tool install kimi-cli
```

### Task Fails Silently

```bash
# Run with verbose output
kimi-maintenance --verbose "your task"

# Check logs
tail -50 ~/.openclaw/mas-hub/logs/kimi-maintenance.log
```

### Permission Errors

```bash
# Ensure scripts are executable
chmod +x ~/Projects/mas-hub/bin/kimi-maintenance
chmod +x ~/Projects/mas-hub/bin/kimi-daily-maintenance.sh
```

### Kimi Code Authentication

```bash
# Login to Kimi Code
kimi /login

# Follow OAuth flow in browser
```

---

## Best Practices

### 1. Use Dry Run First

Always preview what Kimi Code will do:

```bash
kimi-maintenance --dry-run "Your task description"
```

### 2. Be Specific in Task Descriptions

❌ Bad: "Clean up logs"  
✅ Good: "Compress log files older than 7 days, keep last 3 days uncompressed"

### 3. Review Logs Regularly

```bash
# Check recent maintenance activity
kimi-maintenance --log

# Search for errors
grep ERROR ~/.openclaw/mas-hub/logs/kimi-maintenance.log | tail -10
```

### 4. Backup Before Major Changes

```bash
# Create full backup
kimi-maintenance "Create timestamped backup of entire ~/.openclaw/mas-hub/ directory"
```

### 5. Escalate When Unsure

If Kimi Code reports uncertainty or asks for confirmation on critical operations, escalate to Bootstrap:

```bash
mas @bootstrap "Kimi Code flagged this task as requiring human approval: [task description]"
```

---

## Integration with MAS Agents

### Bootstrap (Bob)

Bob can invoke Kimi Code for routine maintenance:

```bash
# From MAS CLI
mas @bootstrap "Run daily maintenance via Kimi Code"
```

### Archie (Facilitator)

Archie can delegate maintenance tasks during workflows:

```
[TASK:bootstrap] Please rotate logs and clean inbox using Kimi Code
```

### Custom Agent Integration

Add to agent system prompts:

```markdown
## Maintenance Tools

For IT maintenance tasks, use Kimi Code CLI:

```bash
kimi-maintenance "task description"
```

Common tasks:
- Log rotation
- Config validation
- Git operations
- Cleanup operations
```

---

## Configuration

### MAS Hub Config

Kimi Code settings in `~/.openclaw/mas-hub/config.json`:

```json
{
  "maintenance": {
    "tool": "kimi-code",
    "tool_version": "1.23.0+",
    "wrapper_script": "~/Projects/mas-hub/bin/kimi-maintenance",
    "daily_script": "~/Projects/mas-hub/bin/kimi-daily-maintenance.sh",
    "log_file": "~/.openclaw/mas-hub/logs/kimi-maintenance.log",
    "schedule": {
      "daily": "06:00",
      "weekly": "Sunday 02:00"
    }
  }
}
```

### Kimi Code Config

Kimi Code's own config: `~/.config/kimi-cli/config.toml`

```toml
[provider]
name = "kimi-code"

[defaults]
print_mode = true
auto_approve = false
```

---

## Monitoring

### Health Checks

```bash
# Check Kimi Code availability
kimi --version

# Test execution
kimi-maintenance --dry-run "Test task"

# Verify log writing
ls -lh ~/.openclaw/mas-hub/logs/kimi-maintenance.log
```

### Metrics to Track

- **Task Success Rate:** `(successful tasks / total tasks) * 100`
- **Average Task Duration:** Track execution times
- **Disk Space Saved:** From log rotation and cleanup
- **Escalation Frequency:** How often human intervention needed

### Alerting

Set up alerts for:
- Maintenance task failures (>3 consecutive)
- Disk usage >80%
- Log file size >100MB
- No maintenance activity in 48h

---

## Appendix: Example Maintenance Sessions

### Example 1: Log Rotation

```bash
$ kimi-maintenance "Rotate logs older than 7 days"

🔧 Kimi Code Maintenance
Task: Rotate logs older than 7 days

I'll compress log files older than 7 days in ~/.openclaw/mas-hub/logs/

Found 15 log files older than 7 days:
- orchestrator.log.2026-03-15 (2.3MB)
- monitor.log.2026-03-14 (1.1MB)
...

Compressing with gzip...
✓ orchestrator.log.2026-03-15.gz (340KB, 85% reduction)
✓ monitor.log.2026-03-14.gz (156KB, 86% reduction)
...

Summary:
- Processed: 15 files
- Total size before: 45.2MB
- Total size after: 6.8MB
- Space saved: 38.4MB (85%)

✓ Maintenance task completed
```

### Example 2: Config Validation

```bash
$ kimi-maintenance "Validate all JSON configs and fix syntax errors"

🔧 Kimi Code Maintenance
Task: Validate all JSON configs and fix syntax errors

Checking JSON syntax in MAS Hub config files...

✓ ~/.openclaw/mas-hub/config.json - Valid
✗ ~/Projects/mas-hub/config.json - Invalid (missing comma on line 23)

Fixing ~/Projects/mas-hub/config.json...
- Added missing comma after "timeout" on line 23
- Created backup: config.json.bak.20260324

Validating fix...
✓ config.json now valid

Summary:
- Checked: 2 files
- Valid: 1
- Fixed: 1
- Backups created: 1

✓ Maintenance task completed
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-24 | Initial integration guide |

---

## Support

- **Kimi Code Docs:** https://moonshotai.github.io/kimi-cli/
- **GitHub Issues:** https://github.com/MoonshotAI/kimi-cli/issues
- **MAS Hub Ontology:** `~/Projects/mas-hub/ontology/mas-ontology.md`
- **Bootstrap (Bob):** `mas @bootstrap "Help with Kimi Code integration"`

---

*This guide is maintained by Bob, MAS Hub Maintainer. Last updated: 2026-03-24*

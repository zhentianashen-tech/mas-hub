# MAS Hub — Setup & Maintenance Guide

**Maintainer:** Bob 🔧  
**System:** Multi-Agent System (MAS) Hub  
**Version:** 1.0.0  
**Last Updated:** 2026-03-22

---

## 1. System Overview

The MAS Hub enables AI agents (Archie, Wang, Lynch, Bootstrap) to collaborate through message passing, shared state, and workflow orchestration.

### Architecture

```
User → mas CLI → Agent Pool
                  ├── Archie (General)
                  ├── Wang (Financial)
                  ├── Lynch (Arbitrator)
                  └── Bootstrap (Maintainer)
```

---

## 2. Directory Structure

```
~/.openclaw/mas-hub/
├── config.json              # System configuration
├── inbox/                   # Agent mailboxes
│   ├── archie/
│   ├── wang/
│   ├── lynch/
│   └── bootstrap/
├── outbox/                  # Agent responses
├── blackboard/              # Shared context
├── workflows/               # Active workflows
├── logs/                    # System logs
└── templates/               # Workflow templates
```

---

## 3. Installation & Setup

### Prerequisites
- OpenClaw CLI installed
- Python 3 for JSON parsing
- zsh/bash shell

### Setup Commands

```bash
# Create directory structure
mkdir -p ~/.openclaw/mas-hub/{inbox/{archie,wang,lynch,bootstrap},outbox,blackboard,workflows,logs,templates}

# Make scripts executable
chmod +x ~/Projects/mas-hub/bin/mas
chmod +x ~/Projects/mas-hub/bin/mas-monitor

# Verify installation
mas help
mas status
```

---

## 4. Daily Maintenance Tasks

### Morning Health Check

```bash
#!/bin/bash
# Run: ./daily-check.sh

echo "=== MAS Hub Daily Check ==="

# 1. Agent status
mas status | head -15

# 2. Disk usage
du -sh ~/.openclaw/mas-hub/* | sort -hr

# 3. Monitor status
mas-monitor-status

# 4. Recent errors
tail -20 ~/.openclaw/mas-hub/logs/orchestrator.log | grep ERROR || echo "No errors"

echo "=== Check Complete ==="
```

### Log Rotation

```bash
#!/bin/bash
# Run daily: ./rotate-logs.sh

LOG_DIR="$HOME/.openclaw/mas-hub/logs"
DATE=$(date +%Y%m%d)

# Compress old logs
find "$LOG_DIR" -name "*.log" -mtime +0 -exec gzip {} \;

# Move to archive
mkdir -p "$LOG_DIR/archive/$DATE"
find "$LOG_DIR" -name "*.gz" -exec mv {} "$LOG_DIR/archive/$DATE/" \;

# Delete archives older than 30 days
find "$LOG_DIR/archive" -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null

echo "Logs rotated: $DATE"
```

### Inbox Cleanup

```bash
#!/bin/bash
# Remove messages older than 7 days

for agent in archie wang lynch bootstrap; do
    find ~/.openclaw/mas-hub/inbox/$agent -name "*.json" -mtime +7 -delete
done
```

---

## 5. Weekly Maintenance

### Full System Check

```bash
#!/bin/bash
# Run weekly: ./weekly-maintenance.sh

echo "=== Weekly Maintenance ==="

# 1. Archive old workflows (14+ days)
find ~/.openclaw/mas-hub/workflows -maxdepth 1 -type d -mtime +14 \
    -exec mv {} ~/.openclaw/mas-hub/archive/workflows/ \;

# 2. Clean outbox (7+ days)
find ~/.openclaw/mas-hub/outbox -name "*.json" -mtime +7 -delete

# 3. Validate configs
openclaw config validate

# 4. Test all agents
for agent in wang lynch bootstrap; do
    echo -n "Testing $agent... "
    openclaw agent --agent "$agent" --message "ping" --json >/dev/null 2>&1 && echo "OK" || echo "FAIL"
done

# 5. Backup configs
BACKUP_DIR="$HOME/.openclaw/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp ~/.openclaw/mas-hub/config.json "$BACKUP_DIR/"

echo "Backup saved: $BACKUP_DIR"
echo "=== Maintenance Complete ==="
```

---

## 6. Troubleshooting

### Agent Not Responding

```bash
# Check agent exists
openclaw agents list | grep <agent>

# Validate config
openclaw config validate

# Test directly
openclaw agent --agent <id> --message "test" --json
```

### MAS CLI Not Found

```bash
# Add to PATH
export PATH="$HOME/Projects/mas-hub/bin:$PATH"
source ~/.zshrc
```

### Monitor Issues

```bash
# Check if running
pgrep -f mas-monitor

# View logs
tail -50 ~/.openclaw/mas-hub/logs/monitor.log

# Restart
mas-monitor-stop
mas-monitor-start
```

### Disk Space Full

```bash
# Check usage
du -sh ~/.openclaw/mas-hub/* | sort -hr

# Clean old files
find ~/.openclaw/mas-hub/logs -name "*.gz" -delete
find ~/.openclaw/mas-hub/outbox -name "*.json" -mtime +3 -delete
```

---

## 7. Configuration Reference

### MAS Hub Config

Location: `~/.openclaw/mas-hub/config.json`

Key settings:
- Agent definitions (4 agents)
- Conflict detection interval: 30 seconds
- Variance threshold: 5%
- Log retention: 30 days

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MAS_HUB | ~/.openclaw/mas-hub | Hub directory |
| MAS_DEBUG | 0 | Debug logging |
| MAS_CHECK_INTERVAL | 30 | Monitor interval (sec) |

---

## 8. Agent Reference

| Agent | Role | Model | Workspace |
|-------|------|-------|-----------|
| Archie | General | moonshot/kimi-k2.5 | workspace/ |
| Wang | Financial | zenmux/claude-opus-4 | workspace-wang/ |
| Lynch | Arbitrator | zenmux/gpt-4.1-mini | workspace-lynch/ |
| Bootstrap | Maintainer | zenmux/claude-opus-4.6 | workspace-bootstrap/ |

---

## 9. Quick Commands

```bash
# Message agents
mas @archie "Hello"
mas @wang "Research Tesla"
mas @lynch "Validate this"
mas @all "Broadcast"

# Workflows
mas workflow research "Topic"
mas debate "Topic"
mas smart "Query"

# Maintenance
mas status
mas-monitor-start
mas-monitor-stop
```

---

## 10. Maintenance Checklist

### Daily
- [ ] Check agent status
- [ ] Verify monitor running
- [ ] Review error logs
- [ ] Check disk usage

### Weekly
- [ ] Archive old workflows
- [ ] Rotate logs
- [ ] Clean inbox
- [ ] Backup configs
- [ ] Test all agents

### Monthly
- [ ] Update documentation
- [ ] Clean old archives
- [ ] Test disaster recovery

---

*Maintained by Bootstrap 🔧 | Last updated: 2026-03-22*

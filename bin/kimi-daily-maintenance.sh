#!/bin/bash
# MAS Hub Daily Maintenance Script
# Uses Kimi Code CLI for automated maintenance tasks
#
# Usage: ~/Projects/mas-hub/bin/kimi-daily-maintenance.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAS_HUB="${HOME}/.openclaw/mas-hub"
LOG_FILE="${MAS_HUB}/logs/daily-maintenance.log"

echo "🔧 MAS Hub Daily Maintenance"
echo "============================"
echo ""

# Ensure log directory exists
mkdir -p "${MAS_HUB}/logs"

log_task() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

run_kimi_task() {
    local task="$1"
    local description="$2"
    
    echo "→ $description"
    log_task "START: $description"
    
    if "${SCRIPT_DIR}/kimi-maintenance" "$task" >> "$LOG_FILE" 2>&1; then
        echo "  ✓ Completed"
        log_task "DONE: $description"
    else
        echo "  ✗ Failed"
        log_task "FAIL: $description"
        return 1
    fi
    echo ""
}

# Task 1: Check system health
run_kimi_task "Check MAS Hub disk usage, log file sizes, and report any concerns" \
               "System health check"

# Task 2: Rotate old logs
run_kimi_task "Compress log files older than 7 days in ~/.openclaw/mas-hub/logs/ using gzip, keep last 3 days uncompressed" \
               "Log rotation"

# Task 3: Validate configurations
run_kimi_task "Validate JSON syntax of ~/.openclaw/mas-hub/config.json and ~/Projects/mas-hub/config.json, fix any errors" \
               "Config validation"

# Task 4: Clean up old workflows
run_kimi_task "Archive completed workflow folders older than 30 days from ~/.openclaw/mas-hub/workflows/ to ~/.openclaw/mas-hub/workflows-archive/" \
               "Workflow archival"

# Task 5: Check git status
run_kimi_task "Check git status in ~/Projects/mas-hub/, if there are uncommitted config changes, create a backup and commit them with message 'Maintenance: auto-commit config changes'" \
               "Git maintenance"

# Task 6: Clean inbox
run_kimi_task "Remove message files older than 48 hours from ~/.openclaw/mas-hub/inbox/" \
               "Inbox cleanup"

echo "============================"
echo "Daily maintenance complete!"
echo ""
echo "Log file: $LOG_FILE"
echo ""

# Show summary
echo "📊 Summary:"
tail -20 "$LOG_FILE" | grep -E "(START|DONE|FAIL)" | tail -10

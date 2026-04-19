#!/bin/bash
# MAS Hub Installer v1.0
# One-line installation script for MAS Hub
#
# Usage: curl -fsSL <url> | bash
#    or: ./install.sh [--dry-run] [--uninstall]

set -e

MAS_HUB_SRC="$HOME/project/mas-hub"
MAS_HUB_BIN="$MAS_HUB_SRC/bin"
HERMES_MAS_HUB="$HOME/.hermes/mas-hub"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

DRY_RUN=0
UNINSTALL=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=1; shift ;;
        --uninstall) UNINSTALL=1; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

log_info() { echo -e "${BLUE}ℹ${NC} $*"; }
log_success() { echo -e "${GREEN}✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $*"; }
log_error() { echo -e "${RED}✗${NC} $*"; }

check_prereq() {
    local cmd="$1" name="$2" install_url="$3"
    if command -v "$cmd" >/dev/null 2>&1; then
        log_success "$name found: $($cmd --version 2>&1 | head -1)"
        return 0
    else
        log_error "$name not found"
        if [[ -n "$install_url" ]]; then
            echo -e "  ${DIM}Install from: $install_url${NC}"
        fi
        return 1
    fi
}

check_prereqs() {
    echo -e "${BOLD}${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║        MAS Hub Installer — Prerequisite Check (Hermes)         ║${NC}"
    echo -e "${BOLD}${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    local failed=0

    check_prereq "hermes" "Hermes Agent" "https://github.com/NousResearch/hermes-agent" || failed=1
    check_prereq "python3" "Python 3" "https://python.org" || failed=1
    check_prereq "bash" "Bash" "" || failed=1
    check_prereq "sqlite3" "SQLite3" "" || failed=1

    echo ""
    
    # Optional deps
    if command -v "git" >/dev/null 2>&1; then
        log_success "Git found (optional): $(git --version)"
    else
        log_warn "Git not found (optional, recommended for updates)"
    fi

    if command -v "kimi" >/dev/null 2>&1; then
        log_success "Kimi Code CLI found (optional): $(kimi --version 2>&1 | head -1)"
    else
        log_warn "Kimi Code CLI not found (optional, for automated maintenance)"
    fi

    echo ""
    if [[ $failed -eq 1 ]]; then
        log_error "Missing required dependencies. Please install them and re-run."
        exit 1
    else
        log_success "All required dependencies met!"
    fi
    echo ""
}

check_hermes_health() {
    log_info "Checking Hermes Agent health..."
    if hermes version >/dev/null 2>&1; then
        log_success "Hermes Agent: $(hermes version 2>/dev/null | head -1)"
    else
        log_warn "Hermes Agent: not responding"
        echo -e "  ${DIM}Check with: hermes doctor${NC}"
        echo -e "  ${DIM}Continuing anyway — you can fix this later${NC}"
    fi
}

setup_hermes_profiles() {
    log_info "Setting up Hermes agent profiles..."
    local agents=(archie wang lynch bootstrap alonzo)
    for agent in "${agents[@]}"; do
        if [[ -d "$HOME/.hermes/profiles/$agent" ]]; then
            log_success "Profile '$agent' already exists"
        else
            if [[ $DRY_RUN -eq 1 ]]; then
                echo "  [DRY RUN] Would create Hermes profile: $agent"
            else
                hermes profile create "$agent" --clone >/dev/null 2>&1
                # Copy SOUL.md if agent template exists
                if [[ -f "$MAS_HUB_SRC/agents/$agent/SOUL.md" ]]; then
                    cp "$MAS_HUB_SRC/agents/$agent/SOUL.md" "$HOME/.hermes/profiles/$agent/SOUL.md"
                fi
                log_success "Created profile '$agent'"
            fi
        fi
    done
}

create_runtime_dirs() {
    log_info "Creating runtime directories..."
    
    if [[ $DRY_RUN -eq 1 ]]; then
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB"
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB/blackboard"
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB/agent-memories"
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB/logs"
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB/inbox"
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB/outbox"
        echo "  [DRY RUN] Would create: $HERMES_MAS_HUB/workflows"
        return 0
    fi

    mkdir -p "$HERMES_MAS_HUB"/{blackboard,agent-memories,logs,inbox,outbox,workflows}
    log_success "Runtime directories created at $HERMES_MAS_HUB"
}

setup_symlinks() {
    log_info "Setting up symlinks..."

    if [[ $DRY_RUN -eq 1 ]]; then
        echo "  [DRY RUN] Would symlink: $MAS_HUB_BIN/mas → ~/bin/mas"
        echo "  [DRY RUN] Would symlink: $MAS_HUB_BIN/mas-tui → ~/bin/mas-tui"
        return 0
    fi

    # Create ~/bin if it doesn't exist
    mkdir -p "$HOME/bin"

    # Symlink mas CLI
    if [[ -L "$HOME/bin/mas" ]]; then
        rm "$HOME/bin/mas"
    fi
    ln -sf "$MAS_HUB_BIN/mas" "$HOME/bin/mas"
    log_success "Symlinked: ~/bin/mas → $MAS_HUB_BIN/mas"

    # Symlink mas-tui
    if [[ -L "$HOME/bin/mas-tui" ]]; then
        rm "$HOME/bin/mas-tui"
    fi
    ln -sf "$MAS_HUB_BIN/mas-tui" "$HOME/bin/mas-tui"
    log_success "Symlinked: ~/bin/mas-tui → $MAS_HUB_BIN/mas-tui"

    # Symlink mas-maintenance
    if [[ -L "$HOME/bin/mas-maintenance" ]]; then
        rm "$HOME/bin/mas-maintenance"
    fi
    ln -sf "$MAS_HUB_BIN/mas-maintenance" "$HOME/bin/mas-maintenance"
    log_success "Symlinked: ~/bin/mas-maintenance → $MAS_HUB_BIN/mas-maintenance"
}

add_to_path() {
    log_info "Checking PATH configuration..."

    if echo "$PATH" | grep -q "$HOME/bin"; then
        log_success "~/bin already in PATH"
        return 0
    fi

    echo ""
    log_warn "~/bin not in PATH"
    echo ""
    echo "Add this to your ~/.zshrc or ~/.bashrc:"
    echo ""
    echo -e "  ${CYAN}export PATH=\"\$HOME/bin:\$PATH\"${NC}"
    echo ""
    echo -e "${DIM}Or run:${NC}"
    echo -e "  ${CYAN}echo 'export PATH=\"\$HOME/bin:\$PATH\"' >> ~/.zshrc${NC}"
    echo ""
}

copy_config() {
    log_info "Setting up configuration..."

    if [[ $DRY_RUN -eq 1 ]]; then
        echo "  [DRY RUN] Would copy: $MAS_HUB_SRC/config.json → $HERMES_MAS_HUB/config.json"
        return 0
    fi

    if [[ ! -f "$HERMES_MAS_HUB/config.json" ]]; then
        cp "$MAS_HUB_SRC/config.json" "$HERMES_MAS_HUB/config.json"
        log_success "Created default config at $HERMES_MAS_HUB/config.json"
    else
        log_warn "Config already exists at $HERMES_MAS_HUB/config.json (skipping)"
    fi
}

verify_installation() {
    echo ""
    echo -e "${BOLD}${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║                  Installation Verification                    ║${NC}"
    echo -e "${BOLD}${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    if command -v mas >/dev/null 2>&1; then
        log_success "MAS CLI installed: $(mas version)"
    else
        log_error "MAS CLI not found in PATH"
        echo -e "  ${DIM}Make sure ~/bin is in your PATH${NC}"
        return 1
    fi

    if [[ -f "$HERMES_MAS_HUB/config.json" ]]; then
        log_success "Config file exists"
    else
        log_warn "Config file not found (will auto-create on first use)"
    fi

    echo ""
    log_info "Running MAS doctor..."
    echo ""
    mas doctor

    echo ""
    log_success "Installation complete!"
    echo ""
    echo -e "${BOLD}Quick Start:${NC}"
    echo ""
    echo "  1. Create your first project:"
    echo -e "     ${CYAN}mas new my-first-project${NC}"
    echo ""
    echo "  2. Send a message to an agent:"
    echo -e "     ${CYAN}mas @wang 'Research Tesla Q1 2026 earnings'${NC}"
    echo ""
    echo "  3. Check status:"
    echo -e "     ${CYAN}mas status${NC}"
    echo ""
    echo -e "For more help: ${CYAN}mas help${NC}"
    echo ""
}

uninstall() {
    echo -e "${BOLD}${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${RED}║                    MAS Hub Uninstaller                        ║${NC}"
    echo -e "${BOLD}${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    log_warn "This will remove:"
    echo "  - Symlinks: ~/bin/mas, ~/bin/mas-tui"
    echo "  - Runtime data: $HERMES_MAS_HUB"
    echo ""
    echo -e "${RED}Your MAS projects, agent memories, and blackboard data will be lost!${NC}"
    echo ""
    read -p "Are you sure? Type 'yes' to confirm: " confirm
    if [[ "$confirm" != "yes" ]]; then
        log_info "Uninstall cancelled"
        exit 0
    fi

    log_info "Removing symlinks..."
    rm -f "$HOME/bin/mas" "$HOME/bin/mas-tui"
    log_success "Symlinks removed"

    log_info "Removing runtime directory..."
    rm -rf "$HERMES_MAS_HUB"
    log_success "Runtime directory removed"

    echo ""
    log_success "Uninstall complete!"
    echo ""
    echo -e "${DIM}Note: $MAS_HUB_SRC (source code) was not removed.${NC}"
    echo -e "${DIM}Delete it manually if desired: rm -rf $MAS_HUB_SRC${NC}"
}

# Main
if [[ $UNINSTALL -eq 1 ]]; then
    uninstall
    exit 0
fi

echo -e "${BOLD}${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║              MAS Hub Installer v1.0                           ║${NC}"
echo -e "${BOLD}${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [[ $DRY_RUN -eq 1 ]]; then
    log_info "Running in DRY RUN mode — no changes will be made"
    echo ""
fi

check_prereqs
check_hermes_health
setup_hermes_profiles
create_runtime_dirs
copy_config
setup_symlinks
add_to_path
verify_installation

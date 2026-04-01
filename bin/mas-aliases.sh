#!/bin/sh
# MAS Model Switcher Aliases
# Source this file: source ~/Projects/mas-hub/bin/mas-aliases.sh

# Wang model switcher
wang-model() { openclaw config get agents.list[2].model.primary; }
alias wang-claude='wang-set-model claude-opus-4.6'
alias wang-gpt='wang-set-model gpt-4.1-mini'
alias wang-gpt54='wang-set-model gpt-5.4'
alias wang-codex='wang-set-model gpt-5.3-codex'
alias wang-qwen='wang-set-model qwen-3.5-plus'
alias wang-grok='wang-set-model grok-4.2'
alias wang-kimi='wang-set-model kimi'

# Lynch model switcher
lynch-model() { openclaw config get agents.list[3].model.primary; }
alias lynch-gpt='lynch-set-model gpt-4.1-mini'
alias lynch-claude='lynch-set-model claude-opus-4.6'

# Bootstrap model switcher  
bootstrap-model() { openclaw config get agents.list[4].model.primary; }
alias bootstrap-gpt='bootstrap-set-model gpt-4.1-mini'
alias bootstrap-claude='bootstrap-set-model claude-opus-4.6'

echo "MAS aliases loaded. Available:"
echo "  wang-model, wang-claude, wang-gpt, wang-gpt54, wang-codex, wang-qwen, wang-grok, wang-kimi"
echo "  lynch-model, lynch-gpt, lynch-claude"
echo "  bootstrap-model, bootstrap-gpt, bootstrap-claude"

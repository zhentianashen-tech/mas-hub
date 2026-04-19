#!/usr/bin/env python3
"""
MAS Hub Context Maintenance Service

Bob's background service for managing MAS Hub context.

Features:
- Project memory file management
- Rule-based relevance scoring
- Context assembly (3-layer system)
- Agent self-selection protocol support

Usage:
    python3 context_maintenance.py <command> [args]

Commands:
    init <project> <session_id>     Initialize project memory
    update <project>                Update project from latest exchange
    score <project> <message>       Score relevance of past exchanges
    assemble <project> <message>     Assemble full context for message
    expand <project> <exchange_id>  Get full content of specific exchange
    maintain <project>              Run periodic maintenance
"""

import sqlite3
import json
import os
import re
import textwrap
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ─── Configuration ────────────────────────────────────────────────────────────

MAS_HUB_ROOT = Path.home() / ".hermes" / "mas-hub"
DB_FILE = MAS_HUB_ROOT / "blackboard" / "shared_context.db"
PROJECTS_DIR = MAS_HUB_ROOT / "projects"

# Token budgets per layer
TOKEN_BUDGET_HEADER = 200
TOKEN_BUDGET_RELEVANT = 1500
TOKEN_BUDGET_RECENCY = 2000

# Relevance thresholds
SCORE_HIGH = 6  # Include full content
SCORE_MEDIUM = 3  # Include summary only
SCORE_LOW = 0  # Exclude (but show timestamp)

# ─── Topic Keywords ────────────────────────────────────────────────────────────

TOPIC_KEYWORDS = {
    'semiconductors': {'chip', 'semiconductor', 'gpu', 'cpu', 'fabrication', 'tsmc', 'foundry', ' wafer', 'nm node'},
    'ai': {'ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'neural', 'deep learning'},
    'financial': {'valuation', 'dcf', 'revenue', 'earnings', 'eps', 'pe ratio', 'margin', 'cash flow', 'ebitda'},
    'research': {'analyze', 'research', 'study', 'investigate', 'deep dive', 'report', 'analysis'},
    'audit': {'verify', 'validate', 'check', 'audit', 'confirm', 'fact', 'source', 'citation'},
    'portfolio': {'portfolio', 'diversify', 'allocation', 'position', 'weight', 'basket', 'combine'},
    'risk': {'risk', 'volatility', 'downside', 'threat', 'concern', 'uncertainty', 'hedge'},
    'competitive': {'competitive', 'competition', 'market share', 'rival', 'versus', 'vs', 'competitor'},
    'growth': {'growth', 'cagr', 'expansion', 'scaling', 'increase', 'moat', 'advantage'},
    'equity': {'equity', 'stock', 'share', 'invest', 'return', 'dividend', 'buy', 'sell', 'hold'},
}

# ─── Known Entities ────────────────────────────────────────────────────────────

KNOWN_COMPANIES = {
    'nvidia': 'NVDA', 'amd': 'AMD', 'intel': 'INTC', 'qualcomm': 'QCOM',
    'broadcom': 'AVGO', 'alphabet': 'GOOGL', 'google': 'GOOGL', 'meta': 'META',
    'facebook': 'META', 'apple': 'AAPL', 'microsoft': 'MSFT', 'amazon': 'AMZN',
    'tesla': 'TSLA', 'tsmc': 'TSM', 'samsung': '005930.KS', 'netflix': 'NFLX',
    'jpmorgan': 'JPM', 'goldman': 'GS', 'morgan stanley': 'MS', 'ubs': 'UBS',
    'alibaba': 'BABA', 'tencent': '0700.HK', 'byd': '002594.SZ',
}

KNOWN_TICKERS = {
    'NVDA', 'AMD', 'INTC', 'QCOM', 'AVGO', 'GOOGL', 'GOOG', 'META', 'AAPL',
    'MSFT', 'AMZN', 'TSLA', 'TSM', 'NFLX', 'JPM', 'GS', 'MS', 'BABA',
}


# ─── Topic Extraction ─────────────────────────────────────────────────────────

def extract_topics(message: str) -> set:
    """Extract semantic topics from message."""
    message_lower = message.lower()
    topics = set()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in message_lower for kw in keywords):
            topics.add(topic)
    return topics


def extract_entities(message: str) -> set:
    """Extract company names and tickers from message."""
    entities = set()
    message_upper = message.upper()
    message_lower = message.lower()
    
    # Ticker patterns (e.g., NVDA, AMD, TSM, 688008.SS)
    ticker_pattern = r'\b([A-Z]{2,5})\b'
    tickers = re.findall(ticker_pattern, message_upper)
    for t in tickers:
        if t in KNOWN_TICKERS or len(t) >= 3:
            entities.add(t)
    
    # Known company names
    for company, ticker in KNOWN_COMPANIES.items():
        if company in message_lower:
            entities.add(ticker)
    
    return entities


# ─── Relevance Scoring ────────────────────────────────────────────────────────

def score_exchange(current_message: str, exchange: dict) -> int:
    """
    Score how relevant an exchange is to the current message.
    
    Returns 0-10:
    - 0-2: Exclude (LOW)
    - 3-5: Summary only (MEDIUM)  
    - 6+: Full content (HIGH)
    """
    score = 0
    
    # Factor 1: Topic Overlap (max 4 pts)
    current_topics = extract_topics(current_message)
    exchange_topics = set(exchange.get('topics', []) or [])
    topic_matches = current_topics & exchange_topics
    score += min(len(topic_matches) * 2, 4)
    
    # Factor 2: Entity Overlap (max 4 pts)
    current_entities = extract_entities(current_message)
    exchange_entities = set(exchange.get('entities', []) or [])
    entity_matches = current_entities & exchange_entities
    score += min(len(entity_matches) * 2, 4)
    
    # Factor 3: Temporal Proximity (max 2 pts)
    exchange_time = exchange.get('timestamp', '')
    if exchange_time:
        try:
            # Parse timestamp (format: "2026-03-23 16:13:45")
            exc_time = datetime.strptime(exchange_time[:19], "%Y-%m-%d %H:%M:%S")
            diff_minutes = (datetime.now() - exc_time).total_seconds() / 60
            if diff_minutes < 5:
                score += 2
            elif diff_minutes < 15:
                score += 1
        except:
            pass
    
    return min(score, 10)


def score_all_exchanges(current_message: str, exchanges: list) -> list:
    """Score all exchanges and annotate with relevance."""
    scored = []
    for ex in exchanges:
        score = score_exchange(current_message, ex)
        scored.append({
            **ex,
            'relevance_score': score,
            'relevance_level': 'HIGH' if score >= SCORE_HIGH else 'MEDIUM' if score >= SCORE_MEDIUM else 'LOW'
        })
    return scored


# ─── Project Memory File ──────────────────────────────────────────────────────

def get_project_memory_path(project: str) -> Path:
    """Get path to project memory file."""
    return PROJECTS_DIR / project / "memory.md"


def init_project_memory(project: str, session_id: str) -> dict:
    """Initialize project memory file."""
    project_dir = PROJECTS_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)
    
    memory_path = get_project_memory_path(project)
    
    # Extract initial topics from session ID
    session_topics = extract_session_topics(session_id)
    
    memory = {
        'metadata': {
            'project': project,
            'session_id': session_id,
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'exchange_count': 0,
        },
        'topics': list(session_topics),
        'entities': {'companies': [], 'tickers': []},
        'state': {
            'phase': 'init',
            'last_agent': None,
            'open_questions': [],
        },
        'decisions': [],
        'summarized_exchanges': []
    }
    
    # Write initial memory file
    write_memory_file(memory_path, memory)
    
    return memory


def extract_session_topics(session_id: str) -> set:
    """Extract potential topics from session ID."""
    topics = set()
    session_lower = session_id.lower()
    
    # Common project keywords
    if 'portfolio' in session_lower:
        topics.add('portfolio')
    if 'research' in session_lower:
        topics.add('research')
    if 'audit' in session_lower:
        topics.add('audit')
    if 'equity' in session_lower:
        topics.add('equity')
    
    return topics


def read_memory_file(memory_path: Path) -> Optional[dict]:
    """Read project memory file."""
    if not memory_path.exists():
        return None
    
    try:
        with open(memory_path, 'r') as f:
            content = f.read()
        
        # Try to extract JSON from markdown code block
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            memory = json.loads(json_match.group(1).strip())
        else:
            # Fallback: try parsing entire file as JSON
            try:
                memory = json.loads(content)
            except:
                return None
        
        return memory
    except Exception as e:
        print(f"Error reading memory file: {e}", file=__import__('sys').stderr)
        return None


def write_memory_file(memory_path: Path, memory: dict):
    """Write project memory file."""
    # Create directory if needed
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Update last_updated
    memory['metadata']['last_updated'] = datetime.now().isoformat()
    
    # Write as JSON for easy parsing (embedded in markdown for readability)
    content = f"""# Project: {memory['metadata']['project']}

## Metadata
- Session: {memory['metadata']['session_id']}
- Created: {memory['metadata']['created']}
- Updated: {memory['metadata']['last_updated']}
- Exchanges: {memory['metadata']['exchange_count']}

## Topics Discussed
{', '.join(memory['topics']) if memory['topics'] else 'None yet'}

## Key Entities
- Companies: {', '.join(memory['entities']['companies']) if memory['entities']['companies'] else 'None yet'}
- Tickers: {', '.join(memory['entities']['tickers']) if memory['entities']['tickers'] else 'None yet'}

## Current State
- Phase: {memory['state']['phase']}
- Last Agent: {memory['state']['last_agent'] or 'None'}
- Open Questions: {len(memory['state']['open_questions'])} pending

## Decisions Log
{chr(10).join(f"- [{d['timestamp']}] {d['agent']}: {d['decision']}" for d in memory['decisions']) if memory['decisions'] else 'No decisions yet'}

---

## Raw Data (JSON)

```json
{json.dumps(memory, indent=2)}
```
"""
    
    with open(memory_path, 'w') as f:
        f.write(content)


def update_from_exchange(project: str, exchange: dict):
    """Update project memory from a new exchange."""
    memory_path = get_project_memory_path(project)
    
    if not memory_path.exists():
        # Auto-init if missing
        memory = init_project_memory(project, exchange.get('mas_session_id', project))
    else:
        memory = read_memory_file(memory_path)
        if not memory:
            memory = init_project_memory(project, exchange.get('mas_session_id', project))
    
    # Extract topics from exchange
    req = exchange.get('user_request', '')
    resp = exchange.get('response_text', '')
    resp_summary = exchange.get('response_summary', '')
    
    topics = extract_topics(req + ' ' + resp)
    entities = extract_entities(req + ' ' + resp)
    
    # Update topics
    for t in topics:
        if t not in memory['topics']:
            memory['topics'].append(t)
    
    # Update entities
    for e in entities:
        if e in KNOWN_TICKERS or e.endswith('.SS') or e.endswith('.HK'):
            if e not in memory['entities']['tickers']:
                memory['entities']['tickers'].append(e)
        else:
            if e not in memory['entities']['companies']:
                memory['entities']['companies'].append(e)
    
    # Update state
    memory['state']['last_agent'] = exchange.get('agent')
    
    # Log decision if [DONE] signal
    if '[DONE]' in resp:
        decision = extract_decision(resp)
        if decision:
            memory['decisions'].append({
                'timestamp': exchange.get('timestamp', datetime.now().isoformat()),
                'agent': exchange.get('agent'),
                'decision': decision
            })
    
    # Update exchange count
    memory['metadata']['exchange_count'] = memory['metadata'].get('exchange_count', 0) + 1
    
    # Write updated memory
    write_memory_file(memory_path, memory)


def extract_decision(response: str) -> Optional[str]:
    """Extract key decision from [DONE] response."""
    # Look for key sentences
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 20:
            # Return first substantive line after [DONE]
            if line.startswith('**') or line.startswith('-') or line.startswith('1.'):
                return line[:200]
    return response[:200]


# ─── Context Assembly ─────────────────────────────────────────────────────────

def assemble_context(project: str, mas_session_id: str, current_message: str, max_tokens: int = 3000) -> str:
    """
    Assemble 3-layer context for current message.
    
    Returns formatted context string ready for injection.
    """
    # Get project memory (Layer 1)
    memory_path = get_project_memory_path(project)
    memory = read_memory_file(memory_path) if memory_path.exists() else None
    
    # Get recent exchanges
    exchanges = get_recent_exchanges(mas_session_id, limit=20)
    
    # Score exchanges for relevance
    scored = score_all_exchanges(current_message, exchanges)
    
    # Build Layer 1: Project Header
    layer1 = build_project_header(memory, project, mas_session_id)
    
    # Build Layer 2: Adaptive Relevance
    layer2 = build_relevance_layer(scored, current_message)
    
    # Build Layer 3: Recency Layer (last 2 always shown)
    layer3 = build_recency_layer(scored)
    
    # Combine with budget awareness
    context = f"""
{layer1}

{layer2}

{layer3}
"""
    
    return context.strip()


def build_project_header(memory: dict, project: str, session_id: str) -> str:
    """Build Layer 1: Project Header."""
    if not memory:
        return f"""═══ PROJECT CONTEXT ═══
Project: {project}
Session: {session_id}
[No prior context in this session]"""

    topics = memory.get('topics', [])
    tickers = memory.get('entities', {}).get('tickers', [])
    phase = memory.get('state', {}).get('phase', 'unknown')
    last_agent = memory.get('state', {}).get('last_agent', 'unknown')
    decisions_count = len(memory.get('decisions', []))
    
    topics_str = ', '.join(topics[:5]) if topics else 'Not yet determined'
    tickers_str = ', '.join(tickers[:10]) if tickers else 'None identified yet'
    
    return f"""═══ PROJECT CONTEXT ═══
Project: {project} | Phase: {phase} | Last: {last_agent}
Topics: {topics_str}
Companies/Tickers: {tickers_str}
Decisions: {decisions_count} logged

{len(memory.get('decisions', [])) > 0 and format_recent_decisions(memory['decisions']) or ''}"""


def format_recent_decisions(decisions: list, limit: int = 3) -> str:
    """Format recent decisions for header."""
    recent = decisions[-limit:]
    lines = ['Recent Decisions:']
    for d in recent:
        ts = d.get('timestamp', '')[:16]
        agent = d.get('agent', '')
        decision = d.get('decision', '')[:80]
        lines.append(f"  [{ts}] {agent}: {decision}")
    return '\n'.join(lines)


def build_relevance_layer(scored: list, current_message: str) -> str:
    """Build Layer 2: Adaptive Relevance (full/summary/excluded)."""
    if not scored:
        return "═══ RELEVANT CONTEXT ═══\n[No prior exchanges in this session]"
    
    lines = ['═══ RELEVANT TO CURRENT REQUEST ═══', '']
    
    # Sort by relevance (highest first)
    sorted_exchanges = sorted(scored, key=lambda x: x['relevance_score'], reverse=True)
    
    # Track token budget
    tokens_used = 0
    shown_full = 0
    shown_summary = 0
    excluded = 0
    
    for ex in sorted_exchanges:
        score = ex['relevance_score']
        agent = ex.get('agent', 'unknown')
        ts = ex.get('timestamp', '')[:16]
        resp_text = ex.get('response_text', '') or ex.get('response_summary', '') or ''
        summary = ex.get('response_summary', '')[:200]
        
        # Layer 3 override: always show last 2
        if shown_full < 2 and not ex.get('_is_recency_override'):
            # Force full for recency
            tokens = len(resp_text) // 4  # rough token estimate
            if tokens_used + tokens < TOKEN_BUDGET_RELEVANT:
                lines.append(f"[RECENT - {ts}] {agent}")
                lines.append(f"  FULL RESPONSE:\n{textwrap.fill(resp_text[:2000], width=100, subsequent_indent='  ')}")
                lines.append('')
                tokens_used += tokens
                shown_full += 1
            continue
        
        # High relevance: full content
        if score >= SCORE_HIGH and shown_full < 4:
            tokens = len(resp_text) // 4
            if tokens_used + tokens < TOKEN_BUDGET_RELEVANT:
                lines.append(f"[HIGH - Score:{score}] {agent} ({ts})")
                lines.append(f"  FULL:\n{textwrap.fill(resp_text[:1500], width=100, subsequent_indent='  ')}")
                lines.append('')
                tokens_used += tokens
                shown_full += 1
            else:
                # Budget exceeded, show summary instead
                lines.append(f"[HIGH - Score:{score}] {agent} ({ts})")
                lines.append(f"  SUMMARY: {summary[:200]}")
                lines.append('')
                shown_summary += 1
        
        # Medium relevance: summary only
        elif score >= SCORE_MEDIUM and shown_summary < 5:
            lines.append(f"[MEDIUM - Score:{score}] {agent} ({ts})")
            lines.append(f"  SUMMARY: {summary[:200]}")
            lines.append('')
            shown_summary += 1
        
        # Low relevance: timestamp only (max 5)
        elif excluded < 5:
            excluded += 1
        # Beyond 5 excluded, skip entirely
    
    # Add note about excluded
    remaining = len(scored) - shown_full - shown_summary - excluded
    if remaining > 0:
        lines.append(f"[{remaining} older exchanges omitted]")
    
    return '\n'.join(lines)


def build_recency_layer(scored: list) -> str:
    """Build Layer 3: Recency Layer (last 2 exchanges always full)."""
    if len(scored) <= 2:
        return ""  # Already shown in Layer 2
    
    lines = ['═══ MOST RECENT (Always Shown) ═══', '']
    
    # Get last 2 (oldest in the scored list, which is reversed chronological)
    recent = list(reversed(scored))[:2]
    
    for ex in recent:
        # Mark as recency override so Layer 2 doesn't duplicate
        ex['_is_recency_override'] = True
        
        agent = ex.get('agent', 'unknown')
        ts = ex.get('timestamp', '')[:16]
        resp_text = ex.get('response_text', '') or ''
        
        if resp_text:
            lines.append(f"[{ts}] {agent}:")
            lines.append(textwrap.fill(resp_text[:1500], width=100, subsequent_indent='  '))
            lines.append('')
    
    return '\n'.join(lines)


def get_recent_exchanges(mas_session_id: str, limit: int = 20) -> list:
    """Get recent exchanges from blackboard."""
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    
    cur.execute("""
        SELECT timestamp, agent, user_request, response_text, response_summary,
               key_points_json, open_questions_json, citations_json, status,
               key_points_json
        FROM exchanges 
        WHERE mas_session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (mas_session_id, limit))
    
    rows = cur.fetchall()
    conn.close()
    
    exchanges = []
    for row in rows:
        (timestamp, agent, req, resp_text, summary, kp_json, oq_json, 
         cites_json, status, kp_raw) = row
        
        # Parse key_points for topic/entity hints
        topics = []
        entities = []
        try:
            kp = json.loads(kp_json or '[]')
            # Extract any entities from key points
            for pt in kp:
                topics.extend(extract_topics(pt))
                entities.extend(extract_entities(pt))
        except:
            pass
        
        exchanges.append({
            'timestamp': timestamp,
            'agent': agent,
            'user_request': req,
            'response_text': resp_text,
            'response_summary': summary,
            'topics': list(set(topics)),
            'entities': list(set(entities)),
            'status': status
        })
    
    return exchanges


def expand_exchange(project: str, mas_session_id: str, exchange_timestamp: str) -> str:
    """Get full content of specific exchange."""
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    
    cur.execute("""
        SELECT timestamp, agent, user_request, response_text, response_summary
        FROM exchanges 
        WHERE mas_session_id = ? AND timestamp LIKE ?
        ORDER BY id DESC
        LIMIT 1
    """, (mas_session_id, f"{exchange_timestamp[:13]}%"))
    
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return f"Exchange not found: {exchange_timestamp}"
    
    ts, agent, req, resp_text, summary = row
    
    return f"""═══ EXPANDED EXCHANGE ═══
Agent: {agent}
Time: {ts}
Request: {req}

FULL RESPONSE:
{resp_text or summary}
"""


# ─── Maintenance ───────────────────────────────────────────────────────────────

def run_maintenance(project: str):
    """Run periodic maintenance on project."""
    memory_path = get_project_memory_path(project)
    
    if not memory_path.exists():
        print(f"No project memory found for: {project}")
        return
    
    memory = read_memory_file(memory_path)
    if not memory:
        return
    
    # Update exchange count from DB
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    
    # Get projects from session_id prefix
    session_prefix = f"mas-{project}-"
    cur.execute("""
        SELECT COUNT(*) FROM exchanges 
        WHERE mas_session_id LIKE ?
    """, (f"{session_prefix}%",))
    
    count = cur.fetchone()[0]
    conn.close()
    
    memory['metadata']['exchange_count'] = count
    
    # Check for stale exchanges (older than 1 hour)
    stale_threshold = datetime.now() - timedelta(hours=1)
    
    # Write updated memory
    write_memory_file(memory_path, memory)
    
    print(f"Maintenance complete for {project}")
    print(f"  Exchanges: {count}")
    print(f"  Topics: {len(memory['topics'])}")
    print(f"  Decisions: {len(memory['decisions'])}")


# ─── CLI Interface ────────────────────────────────────────────────────────────

def main():
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'init':
        if len(sys.argv) < 4:
            print("Usage: context_maintenance.py init <project> <session_id>")
            sys.exit(1)
        project, session_id = sys.argv[2], sys.argv[3]
        memory = init_project_memory(project, session_id)
        print(f"Initialized project memory: {project}")
        print(json.dumps(memory, indent=2))
    
    elif cmd == 'update':
        if len(sys.argv) < 3:
            print("Usage: context_maintenance.py update <project>")
            sys.exit(1)
        project = sys.argv[2]
        
        # Get latest exchange from blackboard
        conn = sqlite3.connect(str(DB_FILE))
        cur = conn.cursor()
        cur.execute("""
            SELECT mas_session_id, timestamp, agent, user_request, response_text,
                   response_summary, key_points_json
            FROM exchanges ORDER BY id DESC LIMIT 1
        """)
        row = cur.fetchone()
        conn.close()
        
        if row:
            exchange = {
                'mas_session_id': row[0],
                'timestamp': row[1],
                'agent': row[2],
                'user_request': row[3],
                'response_text': row[4],
                'response_summary': row[5],
                'key_points_json': row[6]
            }
            update_from_exchange(project, exchange)
            print(f"Updated memory from latest exchange by {exchange['agent']}")
        else:
            print("No exchanges found")
    
    elif cmd == 'score':
        if len(sys.argv) < 4:
            print("Usage: context_maintenance.py score <project> <message>")
            sys.exit(1)
        project, message = sys.argv[2], sys.argv[3]
        
        # Get session from memory
        memory_path = get_project_memory_path(project)
        memory = read_memory_file(memory_path) if memory_path.exists() else None
        session_id = memory['metadata']['session_id'] if memory else f"mas-{project}"
        
        exchanges = get_recent_exchanges(session_id)
        scored = score_all_exchanges(message, exchanges)
        
        print(f"Scored {len(scored)} exchanges:")
        for s in scored:
            print(f"  [{s['relevance_score']:2d}] {s['relevance_level']:6s} {s['agent']:8s} {s.get('timestamp', '')[:16]}")
    
    elif cmd == 'assemble':
        if len(sys.argv) < 4:
            print("Usage: context_maintenance.py assemble <project> <message>")
            sys.exit(1)
        project, message = sys.argv[2], ' '.join(sys.argv[3:])
        
        # Get session from memory
        memory_path = get_project_memory_path(project)
        memory = read_memory_file(memory_path) if memory_path.exists() else None
        session_id = memory['metadata']['session_id'] if memory else f"mas-{project}"
        
        context = assemble_context(project, session_id, message)
        print(context)
    
    elif cmd == 'expand':
        if len(sys.argv) < 4:
            print("Usage: context_maintenance.py expand <project> <exchange_timestamp>")
            sys.exit(1)
        project, timestamp = sys.argv[2], sys.argv[3]
        
        memory_path = get_project_memory_path(project)
        memory = read_memory_file(memory_path) if memory_path.exists() else None
        session_id = memory['metadata']['session_id'] if memory else f"mas-{project}"
        
        result = expand_exchange(project, session_id, timestamp)
        print(result)
    
    elif cmd == 'maintain':
        if len(sys.argv) < 3:
            print("Usage: context_maintenance.py maintain <project>")
            sys.exit(1)
        project = sys.argv[2]
        run_maintenance(project)
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()

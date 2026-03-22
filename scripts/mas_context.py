#!/usr/bin/env python3
"""
Context assembly wrapper for MAS CLI.

Integrates with the context maintenance system to provide
adaptive relevance-based context assembly.

Usage:
    python3 mas_context.py <db_file> <mas_session_id> <project> <mode> [current_message]
"""

import sqlite3
import json
import os
import re
import textwrap
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ─── Configuration ────────────────────────────────────────────────────────────

TOKEN_BUDGET_HEADER = 200
TOKEN_BUDGET_RELEVANT = 1500
TOKEN_BUDGET_RECENCY = 2000
SCORE_HIGH = 6
SCORE_MEDIUM = 3

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

# ─── Helper Functions ─────────────────────────────────────────────────────────

def extract_topics(message: str) -> set:
    message_lower = message.lower()
    topics = set()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in message_lower for kw in keywords):
            topics.add(topic)
    return topics

def extract_entities(message: str) -> set:
    entities = set()
    message_upper = message.upper()
    message_lower = message.lower()
    
    ticker_pattern = r'\b([A-Z]{2,5})\b'
    tickers = re.findall(ticker_pattern, message_upper)
    for t in tickers:
        if t in KNOWN_TICKERS or len(t) >= 3:
            entities.add(t)
    
    for company, ticker in KNOWN_COMPANIES.items():
        if company in message_lower:
            entities.add(ticker)
    
    return entities

def score_exchange(current_message: str, exchange: dict) -> int:
    score = 0
    
    current_topics = extract_topics(current_message)
    exchange_topics = set(exchange.get('topics', []) or [])
    topic_matches = current_topics & exchange_topics
    score += min(len(topic_matches) * 2, 4)
    
    current_entities = extract_entities(current_message)
    exchange_entities = set(exchange.get('entities', []) or [])
    entity_matches = current_entities & exchange_entities
    score += min(len(entity_matches) * 2, 4)
    
    exchange_time = exchange.get('timestamp', '')
    if exchange_time:
        try:
            exc_time = datetime.strptime(exchange_time[:19], "%Y-%m-%d %H:%M:%S")
            diff_minutes = (datetime.now() - exc_time).total_seconds() / 60
            if diff_minutes < 5:
                score += 2
            elif diff_minutes < 15:
                score += 1
        except:
            pass
    
    return min(score, 10)

def get_recent_exchanges(db_file: str, mas_session_id: str, limit: int = 20) -> list:
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT timestamp, agent, user_request, response_text, response_summary,
               key_points_json, open_questions_json, citations_json, status
        FROM exchanges 
        WHERE mas_session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (mas_session_id, limit))
    
    rows = cur.fetchall()
    conn.close()
    
    exchanges = []
    for row in rows:
        timestamp, agent, req, resp_text, summary = row[0], row[1], row[2], row[3], row[4]
        
        topics = []
        entities = []
        try:
            kp = json.loads(row[5] or '[]')
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
            'status': row[8]
        })
    
    return exchanges

# ─── Context Assembly ────────────────────────────────────────────────────────

def build_context(db_file: str, mas_session_id: str, project: str, current_message: str, mode: str = 'text') -> str:
    """Build adaptive context for current message."""
    
    exchanges = get_recent_exchanges(db_file, mas_session_id)
    
    if not exchanges:
        return f"""═══ SHARED MAS CONTEXT ═══
Project: {project} | Session: {mas_session_id} | Exchanges: 0

[No previous shared context in this MAS session]"""
    
    # Score all exchanges
    scored = []
    for ex in exchanges:
        score = score_exchange(current_message, ex)
        scored.append({
            **ex,
            'relevance_score': score,
            'relevance_level': 'HIGH' if score >= SCORE_HIGH else 'MEDIUM' if score >= SCORE_MEDIUM else 'LOW'
        })
    
    # Build output
    lines = []
    lines.append('═══ SHARED MAS CONTEXT ═══')
    lines.append(f"Project: {project} | Session: {mas_session_id} | Exchanges: {len(exchanges)}")
    lines.append('')
    
    # Layer 1: Most recent 2 (always full)
    lines.append('═══ MOST RECENT (Always Shown) ═══')
    lines.append('')
    
    recent = list(reversed(scored))[:2]
    for ex in recent:
        ts = ex.get('timestamp', '')[:16]
        agent = ex.get('agent', 'unknown')
        req = ex.get('user_request', '')[:100]
        resp = ex.get('response_text', '') or ex.get('response_summary', '') or ''
        
        lines.append(f"[{ts}] {agent}")
        lines.append(f"  request: {req}...")
        if resp:
            wrapped = textwrap.fill(resp[:2000], width=100, subsequent_indent='  ')
            lines.append(f"  FULL:\n{wrapped}")
        lines.append('')
    
    # Layer 2: Other exchanges (relevance-based)
    lines.append('═══ RELEVANT CONTEXT ═══')
    lines.append('')
    
    sorted_ex = sorted(scored[2:], key=lambda x: x['relevance_score'], reverse=True)
    
    tokens_used = 0
    shown_full = 0
    shown_summary = 0
    
    for ex in sorted_ex:
        score = ex['relevance_score']
        ts = ex.get('timestamp', '')[:16]
        agent = ex.get('agent', 'unknown')
        resp_text = ex.get('response_text', '') or ''
        summary = ex.get('response_summary', '')[:280]
        
        if score >= SCORE_HIGH and shown_full < 3:
            tokens = len(resp_text) // 4
            if tokens_used + tokens < TOKEN_BUDGET_RELEVANT:
                lines.append(f"[HIGH - Score:{score}] {agent} ({ts})")
                wrapped = textwrap.fill(resp_text[:1500], width=100, subsequent_indent='  ')
                lines.append(f"  FULL:\n{wrapped}")
                lines.append('')
                tokens_used += tokens
                shown_full += 1
            else:
                lines.append(f"[HIGH - Score:{score}] {agent} ({ts})")
                lines.append(f"  SUMMARY: {summary}")
                lines.append('')
                shown_summary += 1
        
        elif score >= SCORE_MEDIUM and shown_summary < 4:
            lines.append(f"[MEDIUM - Score:{score}] {agent} ({ts})")
            lines.append(f"  SUMMARY: {summary}")
            lines.append('')
            shown_summary += 1
        
        elif score < SCORE_MEDIUM:
            # Show timestamp only for low relevance
            if len(lines) < 50:  # Cap total lines
                lines.append(f"[LOW - Score:{score}] {agent} ({ts}) - {summary[:80]}...")
                lines.append('')
    
    lines.append('═══════════════════════════')
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 5:
        print("Usage: mas_context.py <db_file> <mas_session_id> <project> <mode> [current_message]")
        sys.exit(1)
    
    db_file = sys.argv[1]
    mas_session_id = sys.argv[2]
    project = sys.argv[3]
    mode = sys.argv[4]
    current_message = sys.argv[5] if len(sys.argv) > 5 else ""
    
    context = build_context(db_file, mas_session_id, project, current_message, mode)
    print(context)

if __name__ == '__main__':
    main()

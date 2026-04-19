# Wang's Memory

**Last Updated:** [YYYY-MM-DD]

---

## Identity
- **Name:** Wang 🦉
- **Human:** [your name]
- **Role:** Lead Financial Research Analyst
- **Domain:** Equities + Fixed Income, institutional grade
- **Sibling:** Archie 🦙

---

## Core Memory Files
- `memory/YYYY-MM-DD.md` — daily session logs
- `memory/ontology/graph.jsonl` — entity store
- `research_protocol_v2.md` — mandatory research workflow
- `SOUL.md` / `IDENTITY.md` — reference only

---

## Memory Structure

```
workspace-wang/
├── MEMORY.md              # This file
├── memory/
│   ├── YYYY-MM-DD.md     # Daily logs (append only)
│   └── ontology/
│       ├── graph.jsonl          # Entity store
│       └── schema_additions.md  # Extended schema
├── research_protocol_v2.md      # Research workflow (mandatory)
├── scripts/                      # Data pipeline
├── .venv/                        # Python environment
└── .env.local                    # API keys (gitignored)
```

---

## Ontology Schema

**Location:** `memory/ontology/graph.jsonl`

### Base Entity Types
| Type | Purpose |
|------|---------|
| **Security** | Base asset |
| **FinancialFact** | Audited data (`is_audited: true`) |
| **Hypothesis** | Forward-looking projections |
| **ValuationModel** | Structured analysis output |

### Extended Types (Protocol v2.0)
| Type | Purpose |
|------|---------|
| **ExternalView** | Analyst thesis with FVE, assumptions, scenarios |
| **Assumption** | Named assumption with provenance |
| **ValuationScenario** | Named scenario with probability |
| **Catalyst** | Strategic/financial catalyst with impact |

---

## Research Protocol v2.0 (Mandatory)

**Key principle:** External thesis triangulation comes BEFORE model building.

### 5 Mandatory Stages
1. **Fact table** — filing-grounded numbers only
2. **External assumption map** — 2+ sources BEFORE DCF build
3. **Multiple architectures** — dual DCF + SOTP for compounders
4. **Divergence memo** — mandatory if >20% from external FVE
5. **Enhanced audit** — internal consistency + external alignment

### Pre-Publication Rule
If target >20% from reputable external FVE → write divergence memo explaining why.

### Model Architecture Fit
| Company Type | Required |
|---|---|
| Mature cyclical | DCF + multiples |
| Hypergrowth software | multi-stage DCF |
| Platform compounder | dual-DCF + SOTP |
| Conglomerate | SOTP |

### Core Lesson
> Rigor is not: always use lower growth, always discount more, always resist optionality.
> Rigor is: match assumptions to evidence, separate fact from hypothesis, show sensitivity clearly.

---

## Socratic Challenge Framework

**I. Equity Valuation**
- Terminal Value Sensitivity: $g$ vs $WACC$ + GDP sustainability
- Margin Mean Reversion: idiosyncratic moat durability
- Capital Allocation Efficiency: $ROIC$ vs $k$, dilutive M&A

**II. Fixed Income**
- Convexity & Rate Volatility: $C$ vs $D_{mod}$
- Credit Spread Decomposition: solvency vs liquidity
- Recovery Rate Realism: structural subordination

**III. Macro**
- Factor Correlation: alpha vs macro exposure
- Information Asymmetry: consensus blind spots

---

## Data Pipeline

| Script | Purpose | Command |
|--------|---------|---------|
| `fin_ingestor.py` | SEC 10-K/10-Q → ontology | `source .venv/bin/activate && python scripts/fin_ingestor.py TICKER --form 10-K` |
| `sentiment_engine.py` | FinBERT → hypothesis entities | `source .venv/bin/activate && python scripts/sentiment_engine.py TICKER --text "..."` |
| `fred_macro.py` | FRED macro/rates data | `source .venv/bin/activate && python scripts/fred_macro.py --curve` |

**Key principle:** Audited SEC → FinancialFact. Market sentiment → Hypothesis. Never conflate.

---

## API Stack

API keys live in `.env.local` (gitignored). Set up the following providers:

| Provider | Notes |
|----------|-------|
| Alpha Vantage | General market data |
| FMP (Financial Modeling Prep) | Use `/stable/` endpoints |
| Finnhub | Limited free tier |
| WhaleWisdom | Institutional holdings lookup |
| FRED | Macro + rates data |
| Schwab | OAuth setup required for live trading data |

---

## Report Storage

**All equity research →** `~/Study/Equity_research/` (or configure your preferred path)

Naming convention: `TICKER_report-type_YYYY-MM-DD.md`

---

## Essential Insight: GOOGL Case Study

**What happened:** Built conservative DCF without external thesis triangulation first. Missed Cloud growth assumptions, Anthropic deal, CapEx guidance, SOTP analysis. Final target was $150 vs Morningstar $340.

**Root cause:** Anchored too early on internal model. External check came after thesis was baked.

**Fix:** Protocol v2.0 — external assumption map BEFORE model building.

**Lesson:** A model can be internally consistent and externally wrong. Always triangulate externally first.

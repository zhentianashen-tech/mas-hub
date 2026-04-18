# Research Quality Standard — MAS Hub v2

**Version:** 2.0  
**Created:** 2026-04-19  
**Correction:** Example was illustrative, not exhaustive. Framework must support diverse thesis types.

---

## Core Principle

> Professional investment analysis requires **both comprehensive macro and micro depth**. The specific questions depend on the thesis type — there is no one-size-fits-all checklist.

Your example (fertilizers → crops → water → irrigation → liquidity) demonstrated **granularity** for a **commodity supply shock thesis**. Other theses require entirely different depths.

---

## Thesis-Type Specific Requirements

### Type 1: Commodity/Supply Chain Shocks
**Example:** Drought + Iran conflict → agriculture squeeze

**Macro Level:**
- Global supply/demand balances
- Trade flows and disruptions
- Inventory levels (days of supply)
- Price elasticity curves

**Micro Level:**
- Specific product grades/types affected
- County-level production data
- Infrastructure constraints (irrigation, storage, transport)
- Farm-level financial stress (debt, working capital)
- Timing precision (planting windows, harvest dates)

**Key Question:** *Where exactly does the constraint bind, and who can't adapt?*

---

### Type 2: Company-Specific Deep Value
**Example:** Baidu SOTP undervaluation

**Macro Level:**
- Sector TAM and growth rates
- Competitive dynamics and market share
- Regulatory environment
- Technology disruption risks

**Micro Level:**
- Segment-level financials (revenue, margin, capex)
- Balance sheet details (cash, debt, off-balance-sheet)
- Management incentives and capital allocation
- Sum-of-parts valuation by business unit
- Real options (AI, cloud, spinoffs)
- Management guidance vs. consensus
- Insider ownership and transactions

**Key Question:** *What does the market miss about the sum of the parts?*

---

### Type 3: Event-Driven/Special Situations
**Example:** M&A, spinoffs, restructuring

**Macro Level:**
- Regulatory approval probabilities
- Industry consolidation trends
- Comparable transactions
- Market sentiment and timing

**Micro Level:**
- Deal terms and conditions
- Break fees and downside protection
- Shareholder base and voting requirements
- Timeline and catalyst path
- Financing commitments
- Management incentives post-close
- Tax implications
- Antitrust specifics (market definition, HHI)

**Key Question:** *What is the probability-weighted outcome, and where is the market mispricing it?*

---

### Type 4: Macro/Geopolitical Themes
**Example:** Iran structural energy premium

**Macro Level:**
- Global energy balances and spare capacity
- Geopolitical risk scenarios
- OPEC+ dynamics and compliance
- Demand elasticity (short vs. long term)
- Currency and inflation impacts
- Policy responses (SPR releases, sanctions)

**Micro Level:**
- Specific crude grades affected
- Refinery configurations and alternatives
- Shipping routes and insurance costs
- Inventory levels by region
- Physical delivery mechanisms
- Trader positioning and futures curves
- Infrastructure bottlenecks (pipelines, ports)

**Key Question:** *What is the structural change, and who is positioned for/against it?*

---

### Type 5: Technology/Disruption
**Example:** AI capex cycle, semiconductor recovery

**Macro Level:**
- Adoption curves and TAM expansion
- Competitive landscape shifts
- Regulatory risks (export controls, antitrust)
- Capital cycle dynamics (capex → supply → price)

**Micro Level:**
- Customer concentration and pipeline
- Product roadmaps and timing
- Manufacturing yields and capacity
- Design win specifics
- ASP trends and mix shift
- Gross margin bridges (fixed cost leverage)
- R&D efficiency and output
- Talent and IP moats

**Key Question:** *What is the durable competitive advantage, and when does it show in numbers?*

---

### Type 6: Financials/Credit
**Example:** Bank stress, insurance cycle

**Macro Level:**
- Interest rate environment and curve
- Credit cycle position
- Regulatory capital requirements
- Systemic risk factors

**Micro Level:**
- Loan/deposit composition and pricing
- NIM sensitivity by bucket
- Credit quality trends (NPLs, provisions)
- Capital ratios and buffers
- Book value adjustments (HTM securities)
- Funding mix and costs
- Management guidance on net interest income
- Stress test results

**Key Question:** *Where exactly does the balance sheet break or benefit from the macro shift?*

---

## Universal Requirements (All Thesis Types)

Regardless of thesis type, every analysis needs:

### 1. Specificity
- ❌ "China is slowing"  
- ✅ "Property completions down 23% YoY in tier-3 cities, cement demand -15%"

### 2. Quantification
- ❌ "Prices are up"  
- ✅ "Urea spot $380/ton → $530/ton, +40% YoY, 2-year high"

### 3. Timing
- ❌ "Coming quarters"  
- ✅ "Q2 2026 guidance: June 15-30 critical planting window"

### 4. Source Diversity
- Minimum 2 independent sources for critical claims
- Mix of primary (filings, management) and secondary (research, data)

### 5. Actionability
- Specific tickers/instruments
- Entry/exit levels or triggers
- Position sizing rationale
- Risk management (stops, hedges)

### 6. Honest Gaps
- Explicit `[MISSING: data description]` flags
- What would change the thesis
- Key uncertainties

---

## Red Flags (Auto-Reject)

Lynch should reject research with:

- [ ] **Vague geography** — No specific regions/counties/markets
- [ ] **No quantification** — Qualitative claims without numbers
- [ ] **Single source** — Critical claims from one origin
- [ ] **Missing micro** — Macro story without granular validation
- [ ] **Missing macro** — Company-specific without context
- [ ] **No timing** — "Eventually" instead of specific dates
- [ ] **Not actionable** — No specific trade or entry/exit

---

## Task Dispatch Template

Archie should adapt the prompt to the thesis type:

```
[TASK:wang]

**Thesis Type:** [Commodity Shock / Deep Value / Event-Driven / Macro / Tech / Credit]

**Analysis Required:**

For [THESIS TYPE], provide:

**Macro Level:**
- [Specific macro questions for this type]
- Global/regional context
- Market dynamics

**Micro Level:**
- [Specific micro questions for this type]
- Granular data
- Entity-specific details

**Quantification:**
- All claims with numbers
- Sensitivity ranges
- Source citations

**Timing:**
- Critical dates/windows
- Catalyst calendar

**Actionability:**
- Specific instruments
- Entry/exit criteria
- Position sizing logic

**Gaps:**
- [MISSING:] for any unavailable data
- What would change the thesis
```

---

## Audit Checklist (Lynch)

- [ ] Thesis type appropriate for the signal?
- [ ] Macro context complete?
- [ ] Micro granularity sufficient?
- [ ] Quantified throughout?
- [ ] Specific timing?
- [ ] Multiple sources?
- [ ] Actionable trade?
- [ ] Honest about gaps?

**If any fail:** Return to Wang with specific type-appropriate gaps.

---

## Example: Your Fertilizer Prompt (Revised)

Your example showed depth for a **commodity supply shock** thesis:

> *"Which kind of fertilizers are being impacted right now, what kind of crops up and down the chain are negatively influenced by that squeeze, where are they grown, when do they need water the most (down to weeks, even days), which areas, how are the irrigation infra, what kind of liquidity levels are available in those areas..."*

**This is MICRO-LEVEL GRANULARITY for a MACRO SUPPLY SHOCK.**

For a **different thesis type**, the equivalent depth would be entirely different questions.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-19 | Initial (too narrow — based on one example) |
| 2.0 | 2026-04-19 | **Corrected:** Thesis-type specific, macro + micro, flexible framework |

---

*This document establishes the professional research standard for MAS Hub. Depth must match the thesis type.*

# Research Thoroughness Standard — MAS Hub

**Version:** 1.0  
**Created:** 2026-04-19  
**Source:** User requirement from `new_ideas_20260418` session

---

## The Standard

When analyzing an investment signal, agents must answer:

> *"Which kind of fertilizers are being impacted right now, what kind of crops up and down the chain are negatively influenced by that squeeze, where are they grown, when do they need water the most (down to weeks, even days), which areas, how are the irrigation infra, what kind of liquidity levels are available in those areas... these are real questions that influence investment decisions."*

---

## Required Depth by Layer

### Layer 1: Direct Impact
- **What:** Specific commodities/products affected
- **Which:** Exact types, grades, specifications
- **How much:** Quantified impact (%, volume, price)

### Layer 2: Supply Chain Mapping
- **Upstream:** Raw materials, inputs, precursors
- **Midstream:** Processing, logistics, bottlenecks
- **Downstream:** End products, substitutes, demand elasticity

### Layer 3: Geographic Granularity
- **Regions:** Countries, states, provinces
- **Localities:** Counties, districts, specific farms
- **Timing:** Seasonality down to weeks/days
- **Infrastructure:** Irrigation, storage, transport

### Layer 4: Financial/Liquidity
- **Credit availability:** Working capital, farm debt
- **Market depth:** Futures liquidity, bid-ask spreads
- **Hedging:** Tools available, basis risk
- **Insurance:** Coverage levels, payout triggers

### Layer 5: Second-Order Effects
- **Substitution:** What replaces what, at what cost
- **Competition:** Who benefits from others' pain
- **Policy:** Government response, subsidies, trade
- **Long-term:** Structural shifts, permanent changes

---

## Example: Fertilizer/Drought Thesis

| Layer | Questions | Sources | Output |
|-------|-----------|---------|--------|
| **Direct** | Which N-P-K fertilizers? Spot vs contract prices? | CRU, Fertilizer Institute, USDA | Fertilizer type breakdown with price moves |
| **Supply Chain** | Natural gas → ammonia → urea/DAP/MAP. Who makes what? Where? | Company filings, trade data, EIA | Flow diagram with key producers |
| **Geographic** | Corn belt drought severity by county. Planting windows. | USDA drought monitor, state ag depts | County-level risk map with timing |
| **Infrastructure** | Irrigation coverage by region. Groundwater levels. | USGS, state water boards, NASS | Infrastructure vulnerability score |
| **Financial** | Farm debt levels. Crop insurance coverage. Working capital. | Farm Credit, RMA, USDA ERS | Liquidity stress indicators |
| **Second-Order** | Who benefits? Seed companies? Equipment? Alternative crops? | Industry reports, trade pubs | Winners/losers matrix |

---

## Red Flags: When Research is Incomplete

Agents must flag these explicitly with `[MISSING: description]`:

- [ ] **Vague geography** — "the Midwest" instead of counties/states
- [ ] **Missing timing** — No planting/harvest windows specified
- [ ] **No quantification** — "prices are up" without % or $/ton
- [ ] **Single source** — Only one data point for critical claims
- [ ] **No infrastructure** — Physical constraints ignored
- [ ] **Financial gaps** — Liquidity, credit, hedging not analyzed
- [ ] **No second-order** — First-order only, no downstream effects

---

## Task Template for Deep Research

When dispatching research tasks, use this format:

```
[TASK:wang]

**Deep-dive required on [TOPIC]:**

Layer 1 - Direct Impact:
- What specific [products/types] are affected?
- Current prices/availability vs baseline?

Layer 2 - Supply Chain:
- Map upstream → midstream → downstream
- Identify bottlenecks and single points of failure

Layer 3 - Geography & Timing:
- Specific regions/counties affected
- Critical timing windows (down to weeks if possible)
- Seasonal factors

Layer 4 - Infrastructure & Financial:
- Physical infrastructure state (irrigation, storage, transport)
- Credit/liquidity conditions in affected areas
- Insurance coverage and payouts

Layer 5 - Second-Order:
- Substitution effects
- Competitive dynamics (who benefits?)
- Policy responses

**Output:**
- Structured analysis by layer
- Quantified data with sources
- Maps/timelines where relevant
- [MISSING:] flags for gaps
- Investment implications
```

---

## Audit Checklist (Lynch)

Before approving research:

- [ ] **Specificity test:** Can I trade on this? (Specific tickers, entry/exit, sizing)
- [ ] **Granularity test:** Geography/timing precise enough?
- [ ] **Completeness test:** All 5 layers addressed?
- [ ] **Source test:** Multiple independent sources?
- [ ] **Financial test:** Liquidity, execution feasibility confirmed?

**If any check fails:** Return to Wang with specific gaps.

---

## Examples of Insufficient vs. Sufficient

### ❌ Insufficient
> "Fertilizer prices are up due to drought, which could hurt corn yields."

**Problems:**
- Which fertilizers? By how much?
- Which corn regions? Which counties?
- When is the critical period?
- What are yields vs normal?
- Can I trade this?

### ✅ Sufficient
> "Urea prices up 40% YoY ($380→$530/ton) due to:
> - Natural gas feedstock costs (CF Industries, Yara earnings)
> - Iran/Ukraine supply disruptions (CRU data)
> 
> Impact on corn:
> - Corn belt: 61% in drought (USDA D4 monitor, April 18)
> - Critical period: May 15-June 30 (V6-V12 growth stage)
> - Iowa/Illinois most exposed (52% of US corn acres)
> - Irrigation: Only 15% coverage in affected counties
> 
> Financial stress:
> - Farm debt/liquidity: Farm Credit reports Q1 2026
> - Crop insurance: 85% coverage, but revenue protection varies
> 
> **Trade:** Long CORN (Teucrium) June-July. Target $28. Stop $24."

---

## Implementation

### For Archie (Lead)
Include in task dispatch:
```
Use 5-layer analysis. Be specific on geography, timing, and quantification.
Flag any [MISSING:] data explicitly.
```

### For Wang (Research)
Follow the 5-layer template. Start with Layer 1, expand to Layer 5.

### For Lynch (Audit)
Use the 5-check audit. Reject if insufficient depth.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-19 | Initial standard based on user feedback |

---

*This document sets the research quality bar for MAS Hub investment analysis.*

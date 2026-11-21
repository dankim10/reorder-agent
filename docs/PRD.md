# PRD: Reorder Agent (v0)

**Owner:** Dan Kim · **Status:** Draft · **Last updated:** 22 Nov 2026

## Problem
Buyers at cannabis dispensaries reorder hundreds of SKUs weekly, mostly from spreadsheets and memory. Two costly failures result:
- **Stockouts** on fast movers: lost sales and customers who switch stores
- **Overstock** on slow movers: cash tied up, plus expiry and write-offs

## User and job to be done
**Primary user:** the store buyer or inventory manager at a single- or multi-location dispensary.
**Job:** "Each week, tell me what to reorder and how much, and why, so I can approve it in 10 minutes instead of 2 hours."

## Success metrics
| Metric | Target (v1) | Why |
| --- | --- | --- |
| Eval pass rate (golden set) | ≥ 85% | Quality bar before any real user |
| Buyer override rate (lines changed) | ≤ 20% | Trust signal |
| Time to approve a weekly order | ≤ 10 min | The core value |
| Projected stockout days (simulated) | −30% vs naive reorder | Outcome |
| Cost per order run | < US$0.10 | Unit economics |

## Scope
**In:** weekly reorder suggestions per SKU, with a reason; flags for judgement calls; JSON plus readable output.
**Not in v0:** placing orders with vendors, pricing, multi-vendor optimisation, live POS integrations.

## Design principles
1. **Math in code, judgement in the model.** Velocity and days of cover are computed deterministically; the LLM explains, flags and handles exceptions.
2. **A human approves every order.** The agent drafts; it never submits.
3. **Every line has a reason** a buyer can check in 5 seconds.
4. **Say "I'm not sure".** Low-confidence lines are flagged, never guessed.

## Risks and failure modes
| Risk | Mitigation |
| --- | --- |
| Hallucinated quantities | Quantities come from code; the model can only adjust them with a stated reason |
| Promo or seasonal spikes misread as trends | Eval scenarios cover promos; flag spikes over 2x baseline |
| Bad or missing data | Validate inputs; refuse to recommend on missing data |
| Over-trust by buyers | Show confidence; track override rate |
| Compliance limits (possession and purchase caps vary by market) | Out of scope for v0; documented as a known gap |

## Open questions
- Which markets should v1 assume (US state rules differ)?
- Is the buyer persona single-store or multi-location first?

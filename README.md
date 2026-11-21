# reorder-agent

An AI agent that helps cannabis retail buyers decide **what to reorder and how much**. It reads sales velocity and stock on hand, then drafts a purchase order with a reason for every line. A human approves every order.

Built by [Dan Kim](https://github.com/dankim10) with Claude Code, as a public AI product case study: PRD first, evals from day one, and an honest build log.

## Why this problem
Cannabis retailers juggle hundreds of SKUs with short shelf lives, compliance limits and cash tied up in stock. Buyers often reorder by gut feel, so best-sellers stock out and slow movers expire. A good reorder assistant should cut both.

## How it works (v0 plan)
1. **Inputs:** sales history (`data/sample_sales.csv`) and current inventory (`data/sample_inventory.csv`)
2. **Compute:** sales velocity, days of cover and reorder points (deterministic code, not the LLM)
3. **Reason:** the LLM drafts the order and explains each line, flagging judgement calls (promos, new products, expiry risk)
4. **Output:** structured JSON plus a human-readable order for the buyer to approve or edit
5. **Measure:** every change runs against the golden eval set in `evals/`

## Project map
| Path | What |
| --- | --- |
| `docs/PRD.md` | Problem, user, success metrics, risks |
| `docs/decision-log.md` | Why things are the way they are |
| `BUILD_LOG.md` | Weekly progress, including what broke |
| `evals/golden_set.jsonl` | Scenarios with expected behaviour |
| `data/` | Synthetic sample data (no real customer data, ever) |
| `CLAUDE.md` | Instructions for Claude Code when working in this repo |

## Status
v0 deterministic core built. **Eval pass rate: 5/5 (100%)** after a deliberate policy decision on stock cover (see the decision log).

Run it: `python3 src/reorder.py` · Test it: `python3 evals/run_evals.py`

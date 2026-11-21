# Build Log

Honest weekly notes: what shipped, what I learned, what broke.

## 2026-11-22: Week 0, kickoff
- Created the repo, PRD, eval scaffold and synthetic sample data.
- Decision: compute quantities in code, and use the LLM only for reasons and exceptions (see the decision log).
- Learned: starting with evals forces you to define "good" before building.
- Eval pass rate: not yet measured (no agent yet).
- Next: v0 velocity and days-of-cover calculator, then the first eval run.

## 2026-11-22: v0 core calculator + first eval run
- Built `src/reorder.py`: velocity, days of cover, reorder point, quantity. Handles promo spikes (plans on the median, not the spike), stockouts (ignores zero weeks caused by empty shelves) and missing data (refuses to guess).
- Built `evals/run_evals.py`, which runs the golden set and prints a pass rate.
- **First eval run: 4/5 (80%).**
- **First real failure (E001):** for a steady seller (~40/week, 20 on hand, 7-day lead time) v0 orders 141 units; the eval expects 50-90. Cause: v0 targets ~4 weeks of stock (lead time + 1 week safety + 2 weeks). For cannabis flower (short shelf life, cash tied up) that's probably too much.
- This is a **product decision, not a bug**. Options: (A) target less cover, which saves cash but raises stockout risk; (B) keep 4 weeks and change the eval. Decision pending (Dan).
- Learned: writing the eval first exposed a hidden policy choice (how much stock to hold) that would otherwise have been buried in code.

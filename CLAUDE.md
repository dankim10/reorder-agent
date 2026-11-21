# Instructions for Claude Code in this repo

Dan is a product leader learning to build. He had never programmed before November 2026. When working here:
- Explain what you're doing in plain language before significant changes, and teach one concept per session.
- Keep the stack simple: Python 3, standard library plus pandas where it helps. Avoid frameworks until needed.
- **Math in code, judgement in the model.** Velocity, days of cover and reorder points are deterministic Python.
- Every change that affects recommendations must be run against `evals/golden_set.jsonl`; report the pass rate before and after.
- Never commit real customer data or secrets. `data/` holds synthetic data only.
- After each session, append a dated entry to `BUILD_LOG.md`: what changed, what was learned, what broke, and the eval pass rate.
- Record meaningful choices in `docs/decision-log.md` (decision, options considered, why).
- Work on a branch and open a pull request; never push directly to main.

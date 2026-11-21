# Decision Log

| Date | Decision | Options considered | Why |
| --- | --- | --- | --- |
| 2026-11-22 | Quantities computed in code; the LLM explains and flags | LLM does everything; code only; hybrid | LLMs are unreliable at arithmetic. Code is testable; the model adds value on judgement and explanation |
| 2026-11-22 | A human approves every order (no auto-submit) | Auto-submit under a threshold | Trust has to be earned with data first; revisit when the override rate stays under 10% |
| 2026-11-22 | Synthetic data only in the public repo | Anonymised real data | No privacy or compliance risk in a public portfolio |
| 2026-11-22 | Hold ~4 weeks of cover on fast movers (Option B) | A: ~2 weeks (less cash, more stockout risk); B: ~4 weeks (fewer stockouts) | A stockout on a best-seller can cost customer loyalty, which outweighs the cash tied up. Revisit for short-shelf-life SKUs and slow movers |

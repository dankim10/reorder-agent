"""Run the golden eval set and print a pass rate.

Usage (from the repo root): python3 evals/run_evals.py

Each scenario in golden_set.jsonl describes a SKU situation and the expected
behaviour. A scenario passes only if every expectation holds.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from reorder import recommend  # noqa: E402


def check(result, expect):
    problems = []
    if "reorder" in expect and result["reorder"] != expect["reorder"]:
        problems.append(f"reorder={result['reorder']} (expected {expect['reorder']})")
    if "qty_min" in expect and result["qty"] < expect["qty_min"]:
        problems.append(f"qty {result['qty']} < min {expect['qty_min']}")
    if "qty_max" in expect and result["qty"] > expect["qty_max"]:
        problems.append(f"qty {result['qty']} > max {expect['qty_max']}")
    for flag in expect.get("flags", []):
        if flag not in result["flags"]:
            problems.append(f"missing flag '{flag}'")
    return problems


def main():
    path = os.path.join(os.path.dirname(__file__), "golden_set.jsonl")
    passed, total = 0, 0
    for line in open(path):
        if not line.strip():
            continue
        case = json.loads(line)
        total += 1
        result = recommend(case["sku"], case["weekly_sales"], case["on_hand"], case["lead_time_days"])
        problems = check(result, case["expect"])
        status = "PASS" if not problems else "FAIL"
        passed += not problems
        print(f"{status}  {case['id']} {case['name']}: qty={result['qty']} flags={result['flags']}"
              + (f"  <- {'; '.join(problems)}" if problems else ""))
    rate = 100 * passed / total if total else 0
    print(f"\nPass rate: {passed}/{total} ({rate:.0f}%)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

"""Reorder agent v0: the deterministic core.

"Math in code, judgement in the model." This module does the arithmetic
(velocity, days of cover, reorder quantity) and raises flags for the
judgement calls the LLM layer will explain later.

Plain-English glossary:
- velocity: average units sold per week
- days of cover: how many days current stock lasts at that velocity
- lead time: days between placing an order and receiving it
- safety stock: extra buffer so a busy week doesn't cause a stockout
"""

import csv
import json
import sys
from statistics import median

SAFETY_WEEKS = 1.0      # buffer on top of lead-time demand
TARGET_WEEKS = 2.0      # stock to have on hand after the order lands
SPIKE_RATIO = 2.0       # a week above 2x the usual is treated as a spike


def estimate_velocity(weekly_sales, on_hand):
    """Return (units_per_week, flags). Handles spikes, stockouts and missing data."""
    flags = []
    sales = list(weekly_sales)
    if len(sales) < 2:
        return None, ["insufficient_data"]

    # Stockout: stock is zero and recent weeks show zero sales after real sales.
    # The zeros reflect empty shelves, not zero demand, so ignore them.
    if on_hand == 0 and sales[-1] == 0 and any(s > 0 for s in sales):
        while sales and sales[-1] == 0:
            sales.pop()
        flags.append("stockout_suppressed_demand")

    if len(sales) >= 3:
        baseline = median(sales[:-1])
        if baseline > 0 and sales[-1] > SPIKE_RATIO * baseline:
            # The latest week looks like a promo or one-off spike: plan on the baseline.
            flags.append("promo_or_spike")
            return float(baseline), flags

    return sum(sales) / len(sales), flags


def recommend(sku, weekly_sales, on_hand, lead_time_days):
    """Recommend whether to reorder one SKU, and how much."""
    velocity, flags = estimate_velocity(weekly_sales, on_hand)
    if velocity is None:
        return {"sku": sku, "reorder": None, "qty": 0, "flags": flags,
                "reason": "Not enough sales history to recommend. Buyer to decide."}

    daily = velocity / 7
    days_of_cover = on_hand / daily if daily > 0 else float("inf")
    lead_weeks = lead_time_days / 7
    reorder_point = velocity * (lead_weeks + SAFETY_WEEKS)

    if on_hand > reorder_point:
        return {"sku": sku, "reorder": False, "qty": 0, "flags": flags,
                "days_of_cover": round(days_of_cover, 1),
                "reason": f"{days_of_cover:.0f} days of cover is above the reorder point."}

    target = velocity * (lead_weeks + SAFETY_WEEKS + TARGET_WEEKS)
    qty = max(0, round(target - on_hand))
    return {"sku": sku, "reorder": True, "qty": qty, "flags": flags,
            "days_of_cover": round(days_of_cover, 1) if days_of_cover != float("inf") else None,
            "reason": (f"Selling ~{velocity:.0f}/week with {on_hand} on hand "
                       f"and a {lead_time_days}-day lead time. Order {qty} to cover "
                       f"lead time + {SAFETY_WEEKS:.0f} week buffer + {TARGET_WEEKS:.0f} weeks.")}


def load_weekly_sales(path):
    sales = {}
    with open(path, newline="") as f:
        for row in sorted(csv.DictReader(f), key=lambda r: r["week_start"]):
            sales.setdefault(row["sku"], []).append(int(row["units_sold"]))
    return sales


def run(sales_path="data/sample_sales.csv", inventory_path="data/sample_inventory.csv"):
    sales = load_weekly_sales(sales_path)
    results = []
    with open(inventory_path, newline="") as f:
        for item in csv.DictReader(f):
            results.append(recommend(item["sku"], sales.get(item["sku"], []),
                                     int(item["on_hand"]), int(item["lead_time_days"])))
    return results


if __name__ == "__main__":
    print(json.dumps(run(*sys.argv[1:3]), indent=2))

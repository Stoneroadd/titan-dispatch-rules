"""Deterministic allocation demo for synthetic mining equipment."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def assign(scenario: dict) -> dict:
    trucks = scenario.get("trucks")
    loaders = scenario.get("loaders")
    if not isinstance(trucks, list) or not isinstance(loaders, list):
        raise ValueError("trucks and loaders must be arrays")
    if any(not isinstance(item, dict) for item in trucks + loaders):
        raise ValueError("Every equipment item must be an object")
    ids = [item.get("id") for item in trucks + loaders]
    if any(not isinstance(item, str) or not item.strip() for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("Equipment IDs must be nonempty and unique")
    for truck in trucks:
        if truck.get("status") not in ("available", "unavailable") or not _positive(truck.get("capacity_t")):
            raise ValueError(f"Invalid truck: {truck['id']}")
    for loader in loaders:
        slots = loader.get("max_trucks")
        if (loader.get("status") not in ("available", "unavailable")
                or not _positive(loader.get("min_capacity_t"))
                or type(slots) is not int or slots < 1):
            raise ValueError(f"Invalid loader: {loader['id']}")
    counts = {loader["id"]: 0 for loader in loaders}
    assigned = []
    unassigned = []
    for truck in sorted(trucks, key=lambda item: item["id"]):
        if truck["status"] != "available":
            unassigned.append({"truck_id": truck["id"], "reason": "truck_unavailable"})
            continue
        eligible = [loader for loader in loaders
                    if loader["status"] == "available"
                    and truck["capacity_t"] >= loader["min_capacity_t"]
                    and counts[loader["id"]] < loader["max_trucks"]]
        if not eligible:
            unassigned.append({"truck_id": truck["id"], "reason": "no_eligible_loader_or_slot"})
            continue
        loader = min(eligible, key=lambda item: (counts[item["id"]], item["id"]))
        counts[loader["id"]] += 1
        assigned.append({"truck_id": truck["id"], "loader_id": loader["id"],
                         "reason": "available_capacity_and_least_assigned"})
    return {"data_kind": "synthetic_rule_demo", "assignments": assigned,
            "unassigned": unassigned, "loader_counts": counts}


def _positive(value: object) -> bool:
    return type(value) in (int, float) and value > 0 and value != float("inf")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python dispatch.py scenario.json")
    try:
        scenario = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = assign(scenario)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

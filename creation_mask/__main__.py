"""Bounded supplied-record JSON; no host mode or mask lookup/change."""

import argparse
import json
import sys

from .core import MAX_INPUT_BYTES, analyze_json, evaluate, serialize_report
from .fixtures import case, observed, oracles, request


def main() -> int:
    parser = argparse.ArgumentParser(description="Invented creation-mode arithmetic; actual outcomes unverified")
    parser.add_argument("command", choices=("analyze", "demo"))
    args = parser.parse_args()
    try:
        if args.command == "analyze":
            report = analyze_json(sys.stdin.buffer.read(MAX_INPUT_BYTES + 1))
        else:
            results = []
            for index, (requested, mask, derived, removed, rows) in enumerate(oracles()):
                decision = evaluate(request(case(requested, mask, case_id=f"Case{index}")))
                actual = observed(decision["results"][0]) if decision["complete"] else None
                results.append({"report": decision, "expected": (derived, removed, rows),
                                "passed": actual == (derived, removed, rows)})
            report = {"mode": "invented_creation_arithmetic", "actual_creation": "unverified",
                      "actual_mode": "unverified", "actual_access": "unverified",
                      "cases": results, "passed": all(item["passed"] for item in results)}
        payload = serialize_report(report)
        emitted = json.loads(payload)
        if sys.stdout.buffer.write(payload) != len(payload):
            raise OSError("short output write")
        sys.stdout.buffer.flush()
    except OSError:
        sys.stdout = None
        try:
            print('{"error":"input_or_output_failure"}', file=sys.stderr)
        except OSError:
            pass
        return 3
    if emitted.get("status") == "over_limit":
        return 2
    if args.command == "demo":
        return 0 if report["passed"] else 1
    return 0 if report["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

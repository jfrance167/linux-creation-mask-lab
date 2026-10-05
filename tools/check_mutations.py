"""Require assertion failures for two injected faults, then restored passes.

Usage: python tools/check_mutations.py
No source edits/external commands/network. A test error does not count as a caught
mutation. JSON evidence reports assertions/errors separately. Not a coverage score.
"""

from io import StringIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from creation_mask import core
from test_core import CoreTests


def run_case(name: str) -> dict:
    result = unittest.TextTestRunner(stream=StringIO()).run(unittest.TestSuite([CoreTests(name)]))
    return {"passed": result.wasSuccessful(), "assertion_failures": len(result.failures),
            "errors": len(result.errors), "tests_run": result.testsRun}


def main() -> int:
    mutations = []
    pairs = (("subtraction", lambda requested, mask: requested-mask, "test_subtraction_regression"),
             ("missing_requested_intersection", lambda requested, mask: ~mask & 0o777,
              "test_no_requested_intersection_regression"))
    for name, fault, test in pairs:
        with patch.object(core, "_retained", fault):
            result = run_case(test)
        mutations.append({"mutation": name, **result,
                          "detected": result["assertion_failures"] > 0 and result["errors"] == 0})
    restored = [run_case(test) for _, _, test in pairs]
    print(json.dumps({"mutations": mutations, "restored": restored,
                      "scope": "two in-memory logic faults; no source mutation"}, indent=2))
    return 0 if all(item["detected"] for item in mutations) and all(item["passed"] for item in restored) else 1


if __name__ == "__main__":
    raise SystemExit(main())

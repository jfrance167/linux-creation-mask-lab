"""Independent fixed/bit-set oracles and bounded fail-closed input checks."""

import builtins
from contextlib import ExitStack
from copy import deepcopy
import json
import os
from pathlib import Path
import socket
import subprocess
import unittest
from unittest.mock import patch

from creation_mask import core
from creation_mask.fixtures import case, observed, oracles, request


class CoreTests(unittest.TestCase):
    def incomplete(self, value, status="rejected"):
        report = core.evaluate(value)
        self.assertEqual(report["status"], status)
        self.assertFalse(report["complete"])
        for field in ("actual_creation", "actual_mode", "actual_access"):
            self.assertEqual(report[field], "unverified")
        self.assertNotIn("results", report)
        self.assertNotIn("formula", report)
        return report

    def test_fixed_oracles(self):
        self.assertEqual(len(oracles()), 10)
        for requested, mask, derived, removed, rows in oracles():
            for kind in ("regular", "directory"):
                with self.subTest(requested=requested, mask=mask, kind=kind):
                    report = core.evaluate(request(case(requested, mask, kind=kind)))
                    self.assertTrue(report["complete"])
                    self.assertEqual(observed(report["results"][0]), (derived, removed, rows))
                    self.assertEqual([row["class"] for row in report["results"][0]["triplets"]],
                                     ["owner", "group", "other"])

    def test_no_requested_intersection_regression(self):
        result = core.evaluate(request(case("0400", "0000")))["results"][0]
        self.assertEqual(result["derived_mode"], "0400")
        self.assertEqual(result["removed_bits"], "0000")

    def test_subtraction_regression(self):
        result = core.evaluate(request(case("0666", "0001")))["results"][0]
        self.assertEqual(result["derived_mode"], "0666")
        self.assertEqual(result["triplets"][2]["retained"], 6)

    def test_independent_bit_set_properties(self):
        def positions(value):
            # Parse positional binary digits, independently of production bitwise logic.
            return {index for index, digit in enumerate(f"{value:09b}") if digit == "1"}
        requested_values = (0, 1, 2, 4, 7, 0o222, 0o444, 0o777)
        mask_values = (0, 1, 7, 0o22, 0o77, 0o222, 0o400, 0o777)
        corpus = [(value, mask) for value in requested_values for mask in range(512)]
        corpus += [(value, mask) for value in range(512) for mask in mask_values]
        checked = 0
        for offset in range(0, len(corpus), 16):
            batch = corpus[offset:offset+16]
            records = [case(f"{value:04o}", f"{mask:04o}", case_id=f"C{index}")
                       for index, (value, mask) in enumerate(batch)]
            report = core.evaluate(request(*records))
            self.assertTrue(report["complete"])
            self.assertEqual(len(report["results"]), len(batch))
            for (value, mask), result in zip(batch, report["results"]):
                wanted, blocked = positions(value), positions(mask)
                retained = positions(int(result["derived_mode"], 8))
                removed = positions(int(result["removed_bits"], 8))
                self.assertEqual(retained, wanted - blocked)
                self.assertEqual(removed, wanted.intersection(blocked))
                self.assertLessEqual(retained, wanted)
                self.assertFalse(retained.intersection(blocked))
                self.assertFalse(retained.intersection(removed))
                self.assertEqual(retained.union(removed), wanted)
                checked += 1
        self.assertEqual(checked, 8192)  # Includes intentional repeated pairs.

    def test_zero_is_complete(self):
        for requested, mask in (("0000", "0000"), ("0777", "0777")):
            report = core.evaluate(request(case(requested, mask)))
            self.assertEqual(report["status"], "model_complete")
            self.assertEqual(report["results"][0]["derived_mode"], "0000")

    def test_required_context_and_all_known_exclusions(self):
        for field, values in core.CONTEXT.items():
            for excluded in values[1:]:
                record = case(); record["context"][field] = excluded
                report = self.incomplete(request(record), "unsupported")
                self.assertEqual(report["unsupported_reasons"],
                                 [{"case_id": "Example", "reason": f"{field}_{excluded}"}])
            for invalid in ("anything", 0, None, True, "absent\n"):
                record = case(); record["context"][field] = invalid
                self.incomplete(request(record))
            record = case(); record["context"].pop(field); self.incomplete(request(record))
        record = case(); record["context"]["extra"] = "absent"; self.incomplete(request(record))

    def test_high_operands_are_unsupported(self):
        for requested, mask, reason in (("4755", "0022", "high_requested_bits"),
                                        ("0666", "1000", "high_mask_bits"),
                                        ("0666", "7777", "high_mask_bits")):
            report = self.incomplete(request(case(requested, mask)), "unsupported")
            self.assertEqual(report["unsupported_reasons"][0]["reason"], reason)

    def test_no_partial_results_for_unsupported_batch(self):
        other = case(case_id="Other"); other["context"]["default_acl"] = "unknown"
        self.incomplete(request(case(), other), "unsupported")

    def test_all_common_records_validate_before_exclusions(self):
        earlier = case("0000", "0000", case_id="Earlier")
        for exclusion in ("none", "version", "profile", "context", "high_mask", "high_request"):
            for later_invalid in ("mode", "context", "missing", "duplicate"):
                fixture = request(deepcopy(earlier), case(case_id="Later"))
                if exclusion == "version": fixture["version"] = 2
                elif exclusion == "profile": fixture["profile"] = "Other"
                elif exclusion == "context": fixture["cases"][0]["context"]["default_acl"] = "present"
                elif exclusion == "high_mask": fixture["cases"][0]["mask"] = "1000"
                elif exclusion == "high_request": fixture["cases"][0]["requested_mode"] = "4755"
                if later_invalid == "mode": fixture["cases"][1]["mask"] = "0088"
                elif later_invalid == "context": fixture["cases"][1]["context"]["object_state"] = True
                elif later_invalid == "missing": fixture["cases"][1].pop("requested_mode")
                else: fixture["cases"][1]["id"] = "Earlier"
                self.incomplete(fixture)
        for field, value in (("version", 0), ("version", 999_999_999), ("profile", "Other")):
            fixture = request(); fixture[field] = value
            self.incomplete(fixture, "unsupported")
            fixture["cases"] = []
            self.incomplete(fixture)

    def test_unsupported_reasons_are_stable(self):
        z = case("4755", "1000", case_id="Z"); z["context"]["default_acl"] = "present"
        a = case(case_id="A"); a["context"]["application_mode"] = "later_change"
        fixture = request(z, a); fixture.update(version=2, profile="Other")
        report = self.incomplete(fixture, "unsupported")
        self.assertEqual(report["unsupported_reasons"], [
            {"case_id": None, "reason": "profile"}, {"case_id": None, "reason": "version"},
            {"case_id": "A", "reason": "application_mode_later_change"},
            {"case_id": "Z", "reason": "default_acl_present"},
            {"case_id": "Z", "reason": "high_mask_bits"}, {"case_id": "Z", "reason": "high_requested_bits"}])

    def test_no_coercion_subclasses_or_custom_keys(self):
        class Hostile:
            def __str__(self): raise AssertionError("coercion")
            def __int__(self): raise AssertionError("coercion")
        class DictSubclass(dict):
            def __iter__(self): raise AssertionError("custom iteration")
        class ListSubclass(list):
            def __iter__(self): raise AssertionError("custom iteration")
        class StrSubclass(str): pass
        self.incomplete(DictSubclass(request()))
        for value in (None, True, 0o666, Hostile(), StrSubclass("0666")):
            record = case(); record["requested_mode"] = value; self.incomplete(request(record))
        fixture = request(); fixture["cases"] = ListSubclass([case()]); self.incomplete(fixture)
        fixture = request(DictSubclass(case())); self.incomplete(fixture)
        record = case(); record["context"] = DictSubclass(record["context"]); self.incomplete(request(record))
        class Key:
            def __hash__(self): return 1
            def __eq__(self, other): raise AssertionError("key equality")
        fixture = request(); fixture.pop("version"); fixture[Key()] = 1; self.incomplete(fixture)

    def test_shapes_grammar_and_case_bounds(self):
        for field in request():
            fixture = request(); fixture.pop(field); self.incomplete(fixture)
        for field in case():
            record = case(); record.pop(field); self.incomplete(request(record))
        for value in (True, "1", 1.0, -1, 1_000_000_000):
            fixture = request(); fixture["version"] = value; self.incomplete(fixture)
        for text in ("", "../x", "A/B", "A\\B", "A\x00", "A\n", "é", "A" * 33, "\ud800"):
            record = case(case_id=text); self.incomplete(request(record))
        for text in ("666", "0o666", "0666\n", "0088", "-001", "06666", "x" * 100_000):
            self.incomplete(request(case(text)))
            self.incomplete(request(case(mask=text)))
        self.incomplete(request(case(kind="symlink")))
        fixture = request(); fixture["extra"] = 1; self.incomplete(fixture)
        fixture = request(); fixture["cases"] = []; self.incomplete(fixture)
        fixture["cases"] = (); self.incomplete(fixture)
        fixture = request(*[case(case_id=f"C{i}") for i in range(17)])
        self.incomplete(fixture, "over_limit")
        fixture["cases"].pop()
        fixture["cases"][0]["id"] = "A" * 32
        self.assertTrue(core.evaluate(fixture)["complete"])

    def test_json_boundaries(self):
        raw = json.dumps(request()).encode()
        self.assertTrue(core.analyze_json(raw)["complete"])
        self.assertTrue(core.analyze_json(raw+b" " * (core.MAX_INPUT_BYTES-len(raw)))["complete"])
        for data, status in ((bytearray(raw), "rejected"), (b"\xff", "rejected"),
                             (b"x" * (core.MAX_INPUT_BYTES+1), "over_limit"),
                             (b"[" * 7 + b"]" * 7, "over_limit"), (b"[" * 6 + b"]" * 6, "rejected"),
                             (b'{"x":12345678901}', "over_limit"), (b'{"x":1234567890}', "rejected"),
                             (b'{"x":1.0}', "rejected"), (b'{"x":NaN}', "rejected"),
                             (b'{"x":Infinity}', "rejected"), (b'{"x":1e12345678901}', "over_limit"),
                             (b'{"version":1,"version":1}', "rejected"),
                             (raw+b"{}", "rejected"), (b"{", "rejected")):
            report = core.analyze_json(data)
            self.assertEqual(report["status"], status)
            self.assertNotIn("results", report)
        nested_duplicate = raw.replace(b'"mask": "0022"', b'"mask":"0022","mask":"0000"')
        self.assertEqual(core.analyze_json(nested_duplicate)["reason"], "duplicate_key")
        with self.assertRaises(core._Invalid) as error:
            core._depth('[' * 7 + ']' * 7)
        self.assertEqual(error.exception.reason, "depth_limit")
        # Scanner seam: delimiters and escaped quotes inside JSON strings aren't structural.
        core._depth(json.dumps('[' * 100 + '\\"' + ']' * 100))

    def test_no_mutation_json_equivalence_and_fixed_claims(self):
        for requested, mask, _, _, _ in oracles():
            fixture = request(case(requested, mask))
            before = deepcopy(fixture)
            direct = core.evaluate(fixture)
            self.assertEqual(fixture, before)
            self.assertEqual(core.analyze_json(json.dumps(fixture).encode()), direct)
            for field in ("actual_creation", "actual_mode", "actual_access"):
                self.assertEqual(direct[field], "unverified")

    def test_internal_output_boundary_and_escaping(self):
        output = core.serialize_report({"text": "\n\x1b\ud800"})
        self.assertEqual(output.count(b"\n"), 1)
        self.assertNotIn(b"\x1b", output)
        self.assertEqual(json.loads(output)["text"], "\n\x1b\ud800")
        # Trusted formatter seam, unreachable by the bounded accepted schema.
        self.assertEqual(len(core.serialize_report({"x": "x" * (core.MAX_OUTPUT_BYTES-9)})), core.MAX_OUTPUT_BYTES)
        report = json.loads(core.serialize_report({"x": "x" * (core.MAX_OUTPUT_BYTES-8)}))
        self.assertEqual(report["status"], "over_limit")
        self.assertFalse(report["complete"])
        self.assertNotIn("results", report)

    def test_no_host_capabilities(self):
        def forbidden(*args, **kwargs): raise AssertionError("host capability called")
        # Trusted imports/mocks/fixture construction precede guarding the model.
        guards = [(builtins, name) for name in ("open", "eval", "exec")]
        guards += [(os, name) for name in ("umask", "stat", "lstat", "access", "chmod", "chown", "walk",
                                           "getuid", "geteuid", "getgid", "getegid", "getgroups") if hasattr(os, name)]
        guards += [(Path, "resolve"), (socket, "socket"), (socket, "create_connection"), (subprocess, "Popen")]
        fixture = request(); raw = json.dumps(fixture).encode()
        contexts = [patch.object(obj, name, forbidden) for obj, name in guards]
        with ExitStack() as stack:
            for context in contexts: stack.enter_context(context)
            self.assertTrue(core.evaluate(fixture)["complete"])
            self.assertTrue(core.analyze_json(raw)["complete"])
            self.assertEqual(core.evaluate({})["status"], "rejected")
            self.assertTrue(core.serialize_report(core.evaluate(fixture)))


if __name__ == "__main__":
    unittest.main()

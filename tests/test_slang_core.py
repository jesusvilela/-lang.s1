import json
from pathlib import Path
import unittest

from slang_core import CoreRuntimeError, CoreSyntaxError, run_source
from slang_core.conformance import DEFAULT_MANIFEST, run_conformance


class SlangCoreTests(unittest.TestCase):
    def test_arithmetic_and_binding(self):
        result = run_source(
            """
§let x = 7
§let y = mul(x, 6)
§emit y
§assert y == 42
"""
        )
        self.assertEqual("PASS", result["status"])
        self.assertEqual([42], result["emissions"])
        self.assertEqual(42, result["bindings"]["y"])

    def test_failed_assertion_is_program_fail(self):
        result = run_source("§assert add(20, 22) == 41")
        self.assertEqual("FAIL", result["status"])
        self.assertFalse(result["assertions"][0]["pass"])

    def test_no_assertions_is_not_tested(self):
        result = run_source('§emit "hello"')
        self.assertEqual("NOT_TESTED", result["status"])
        self.assertEqual(["hello"], result["emissions"])

    def test_evidence_is_metadata_not_validation(self):
        result = run_source(
            '§evidence X-1 [P] "This tag is preserved but not independently proved."'
        )
        self.assertEqual("NOT_TESTED", result["status"])
        self.assertEqual(
            [{"id": "X-1", "tag": "P", "text": "This tag is preserved but not independently proved."}],
            result["evidence"],
        )

    def test_unknown_operator_fails_at_runtime(self):
        with self.assertRaises(CoreRuntimeError):
            run_source("§emit Mostow(1)")

    def test_historical_surface_is_not_silently_parsed(self):
        with self.assertRaises(CoreSyntaxError):
            run_source("§|LANG|SOURCE{ bind.version = v5 }")

    def test_unbound_name_fails(self):
        with self.assertRaises(CoreRuntimeError):
            run_source("§emit x")

    def test_conformance_manifest_has_four_statuses(self):
        report = run_conformance(DEFAULT_MANIFEST)
        self.assertEqual("PASS", report["status"])
        counts = report["case_status_counts"]
        self.assertGreater(counts["PASS"], 0)
        self.assertEqual(0, counts["FAIL"])
        self.assertGreater(counts["NOT_APPLICABLE"], 0)
        self.assertGreater(counts["NOT_TESTED"], 0)

    def test_conformance_negative_program_is_expected_case_pass(self):
        report = run_conformance(DEFAULT_MANIFEST)
        case = next(c for c in report["cases"] if c["id"] == "negative-assertion")
        self.assertEqual("PASS", case["status"])
        self.assertEqual("FAIL", case["observed_program_status"])


if __name__ == "__main__":
    unittest.main()

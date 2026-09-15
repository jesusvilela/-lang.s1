from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate_typecast.py"
spec = importlib.util.spec_from_file_location("validate_typecast", MODULE_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class ValidateTypecastTests(unittest.TestCase):
    def write_source(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".lang", delete=False, encoding="utf-8")
        handle.write(text)
        handle.close()
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return Path(handle.name)

    PACK_NAME = "MHRR_PM_Hypercomplex_Orthogonal"

    def pack_source(self, extra: str = "") -> Path:
        return self.write_source(f"§PACK {self.PACK_NAME}\n§VERSION 1\n{extra}")

    def test_empty_sections_are_not_reported_as_pass(self) -> None:
        source = self.pack_source()
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["checks"]["section_vectors_dimension_8"], validator.NOT_APPLICABLE)
        self.assertEqual(report["checks"]["section_norm_below_0_999"], validator.NOT_APPLICABLE)
        self.assertEqual(report["checks"]["salience_positive"], validator.NOT_APPLICABLE)

    def test_unknown_profile_fails_explicitly(self) -> None:
        source = self.pack_source()
        report = validator.validate_source(source, "unknown-profile")
        self.assertEqual(report["checks"]["declared_profile_known"], validator.FAIL)
        self.assertFalse(validator.report_passes(report))

    def test_pack_requires_explicit_pack_and_version_headers(self) -> None:
        source = self.write_source(f"§PACK {self.PACK_NAME}\n")
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["checks"]["surface_recognized"], validator.FAIL)

    def test_pack_recognition_is_independent_of_filename(self) -> None:
        source = self.pack_source()
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["checks"]["surface_recognized"], validator.PASS)

    def test_valid_section_is_checked(self) -> None:
        source = self.pack_source(
            "§S{label=a, x=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], sal=1.0}\n"
        )
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["checks"]["section_vectors_dimension_8"], validator.PASS)
        self.assertEqual(report["checks"]["section_norm_below_0_999"], validator.PASS)
        self.assertEqual(report["checks"]["salience_positive"], validator.PASS)

    def test_pack_identity_must_match_declared_profile(self) -> None:
        """A well-formed pack surface is not enough: it must be the declared pack."""
        source = self.write_source("§PACK Some_Other_Pack\n§VERSION 1\n")
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["checks"]["surface_recognized"], validator.PASS)
        self.assertEqual(report["checks"]["pack_identity_matches_profile"], validator.FAIL)
        self.assertFalse(validator.report_passes(report))

    def test_matching_pack_identity_passes(self) -> None:
        source = self.pack_source()
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["checks"]["pack_identity_matches_profile"], validator.PASS)

    def test_legacy_block_profile_has_no_pack_identity_check(self) -> None:
        source = self.write_source("§|LANG|DIALECT_TREE{\n§|LANG|DIALECT_RULES{\n§|LANG|DIALECT_NOTES{\n")
        report = validator.validate_source(source, "dialects")
        self.assertEqual(report["checks"]["pack_identity_matches_profile"], validator.NOT_APPLICABLE)
        self.assertEqual(report["checks"]["block_headers_present"], validator.PASS)

    def test_theorem_declarations_are_counted_but_never_a_check(self) -> None:
        """Counting a §THEOREM line must not create proof authority."""
        source = self.pack_source(
            "§THEOREM_A: §GAUGE(x) ⊢ COMMIT\n§THEOREM_B: §GAUGE(y) ⊢ COMMIT\n§AXIOM_1: z\n"
        )
        report = validator.validate_source(source, "mhrr_pack_v1")
        self.assertEqual(report["declarations"]["theorem_declarations"], 2)
        self.assertEqual(report["declarations"]["commit_markers"], 2)
        self.assertEqual(report["declarations"]["axiom_declarations"], 1)
        self.assertEqual(report["checks"]["mathematical_claims"], validator.NOT_TESTED)
        self.assertNotIn("theorem_declarations", report["checks"])


if __name__ == "__main__":
    unittest.main()

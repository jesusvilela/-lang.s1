from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sheaf = _load("sheaf_coherence")


def section(cosmos: int, depth: int, prime: int, berry: float | None = None, hq: float | None = None) -> dict:
    return {
        "cosmos": cosmos,
        "depth": depth,
        "prime": prime,
        "coordinates": {} if berry is None else {"berry": berry},
        "hamiltonian_hq": hq,
    }


class GluingTests(unittest.TestCase):
    def test_disjoint_cover_is_vacuous_not_a_pass(self) -> None:
        """A sheaf over a pairwise-disjoint cover glues trivially."""
        sections = [section(1, 1, 3), section(1, 2, 5), section(2, 1, 7), section(2, 2, 11)]
        # Force both readings disjoint by giving each stratum distinct depths.
        sections[2]["depth"], sections[3]["depth"] = 3, 4
        result = sheaf.h1_gluing(sections)
        self.assertTrue(result["by_prime"]["cover_is_pairwise_disjoint"])
        self.assertEqual(result["verdict"], "VACUOUS")

    def test_overlapping_cover_glues(self) -> None:
        sections = [section(1, 1, 3), section(1, 2, 5), section(2, 1, 3), section(2, 2, 5)]
        result = sheaf.h1_gluing(sections)
        self.assertEqual(result["verdict"], "GLUES")

    def test_readings_that_disagree_report_undetermined(self) -> None:
        """Distinct primes but shared depths: the two covers give opposite answers."""
        sections = [section(1, 1, 3), section(1, 2, 5), section(2, 1, 7), section(2, 2, 11)]
        result = sheaf.h1_gluing(sections)
        self.assertTrue(result["by_prime"]["cover_is_pairwise_disjoint"])
        self.assertFalse(result["by_depth"]["cover_is_pairwise_disjoint"])
        self.assertTrue(result["readings_disagree"])
        self.assertEqual(result["verdict"], "UNDETERMINED_COVER")


class AdiabaticTests(unittest.TestCase):
    def test_monotone_series_is_retired_not_promoted(self) -> None:
        """A perfectly smooth ramp beats a shuffle but never beats sorted."""
        sections = [section(1, d, d, hq=0.001 * d) for d in range(1, 11)]
        result = sheaf.h2_adiabatic(sections)
        self.assertEqual(result["verdict"], "RETIRED_MONOTONICITY")
        self.assertEqual(result["strata_beating_sorted_null"], 0)

    def test_multiplicity_correction_is_reported(self) -> None:
        sections = [section(c, d, d, hq=0.001 * d) for c in (1, 2, 3) for d in range(1, 11)]
        result = sheaf.h2_adiabatic(sections)
        self.assertEqual(result["strata_tested"], 3)
        self.assertAlmostEqual(result["alpha_bonferroni"], 0.05 / 3, places=6)
        self.assertIn("strata_smoother_uncorrected", result)
        self.assertIn("strata_smoother_bonferroni", result)

    def test_absent_hamiltonian_is_not_applicable(self) -> None:
        sections = [section(1, d, d) for d in range(1, 5)]
        self.assertEqual(sheaf.h2_adiabatic(sections)["verdict"], "NOT_APPLICABLE")


class BerryTests(unittest.TestCase):
    def test_deviation_beyond_stated_precision_is_approximate_only(self) -> None:
        sections = [section(1, 1, 3, berry=1.5741)]
        result = sheaf.h3_berry(sections)
        self.assertEqual(result["verdict"], "APPROXIMATE_ONLY")
        self.assertFalse(result["within_stated_precision"])

    def test_exact_value_passes(self) -> None:
        sections = [section(1, 1, 3, berry=sheaf.BERRY_TARGET)]
        self.assertEqual(sheaf.h3_berry(sections)["verdict"], "EQUALS_AS_WRITTEN")


class RhoStarTests(unittest.TestCase):
    def test_real_pack_value_is_consistent_but_stability_unsupported(self) -> None:
        result = sheaf.h4_rho_star(Path("MHRR_PM_Hypercomplex_Orthogonal.lang"))
        self.assertEqual(result["verdict_value"], "CONSISTENT")
        self.assertEqual(result["verdict_substrate_stability"], "UNSUPPORTED")
        self.assertEqual(result["substrate_axes_varied"], 0)
        self.assertFalse(result["estimator_declared"])


if __name__ == "__main__":
    unittest.main()

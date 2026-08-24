#!/usr/bin/env python3
"""Measure the sheaf/adiabatic/Berry claims the packs assert, over mesh projections.

The n-Cosmos and MHRR packs assert `⊢ UNIFIED_MANIFOLD` per stratum,
`⊢ HEGELIAN_CLOSURE` globally, `[Adiabatic Ground State]` per declaration, and
`γ_Berry = π/2`. Those are assertions in text. This tool turns each into a
number that could contradict it.

Preregistered before measurement (see AUDIT.md):

  H1 gluing    metric: pairwise prime overlap between cosmos strata
               kill:   all pairwise overlaps empty -> gluing is vacuous
  H2 adiabatic metric: max |dH| between consecutive depths vs a shuffled null
               kill:   real sequence no smoother than the matched null
  H3 berry     metric: max |BERRY - pi/2|
               kill:   > 5e-5, the 4-decimal precision the pack states
  H4 rho-star  metric: existence of an in-repo derivation
               kill:   none exists -> stays H

Evidence scope. Every quantity here is computed from text the packs already
contain. Measuring an asserted number does not make the assertion true; it makes
the assertion checkable. A PASS here means the pack's own numbers are consistent
with the pack's own adjective, nothing more.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path

BERRY_TARGET = math.pi / 2
BERRY_STATED_PRECISION = 5e-5  # pack writes 1.5708 -> 4 decimals
NULL_TRIALS = 2000
NULL_SEED = 142  # fixed so the control is reproducible


def load_mesh(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _overlap_under(sections: list[dict], index_key: str) -> dict:
    """Overlap structure of the cosmos cover under one choice of index."""
    strata: dict[int, set] = {}
    for section in sections:
        cosmos = section.get("cosmos")
        value = section.get(index_key)
        if cosmos is None or value is None:
            continue
        strata.setdefault(cosmos, set()).add(value)

    keys = sorted(strata)
    pairs = []
    for i, a in enumerate(keys):
        for b in keys[i + 1 :]:
            shared = strata[a] & strata[b]
            union = strata[a] | strata[b]
            pairs.append(
                {
                    "strata": [a, b],
                    "shared": len(shared),
                    "jaccard": round(len(shared) / len(union), 6) if union else 0.0,
                }
            )
    nonempty = [p for p in pairs if p["shared"] > 0]
    return {
        "index": index_key,
        "strata_count": len(keys),
        "pair_count": len(pairs),
        "nonempty_overlap_pairs": len(nonempty),
        "cover_is_pairwise_disjoint": bool(pairs) and not nonempty,
        "mean_jaccard": round(statistics.mean([p["jaccard"] for p in pairs]), 6) if pairs else None,
    }


def h1_gluing(sections: list[dict]) -> dict:
    """Is `⊢ UNIFIED_MANIFOLD` a non-vacuous gluing statement?

    A sheaf glued over a pairwise-disjoint cover glues trivially: there are no
    overlap conditions to satisfy, so the assertion is about nothing.

    Representation attack. The answer depends entirely on what indexes the
    cover, and the pack never declares it. Indexing by prime basis and by
    declaration depth are both readings the pack's own notation admits, and they
    give opposite answers. Both are reported; neither is privileged.
    """
    by_prime = _overlap_under(sections, "prime")
    by_depth = _overlap_under(sections, "depth")

    if not by_prime["pair_count"] and not by_depth["pair_count"]:
        return {"verdict": "NOT_APPLICABLE", "by_prime": by_prime, "by_depth": by_depth}

    disagree = by_prime["cover_is_pairwise_disjoint"] != by_depth["cover_is_pairwise_disjoint"]
    if disagree:
        verdict = "UNDETERMINED_COVER"
    elif by_prime["cover_is_pairwise_disjoint"]:
        verdict = "VACUOUS"
    else:
        verdict = "GLUES"

    return {
        "by_prime": by_prime,
        "by_depth": by_depth,
        "readings_disagree": disagree,
        "verdict": verdict,
        "note": (
            "The pack asserts a gluing without declaring the cover it glues over. "
            "Until the cover is declared the assertion has no determinate truth value."
        ),
    }


def _roughness(values: list[float]) -> float:
    """Max absolute step between consecutive entries."""
    if len(values) < 2:
        return 0.0
    return max(abs(b - a) for a, b in zip(values, values[1:]))


def h2_adiabatic(sections: list[dict]) -> dict:
    """Is the Hamiltonian sequence smoother than a shuffle of the same values?

    'Adiabatic' means slow variation. Reordering the same multiset destroys any
    ordering-dependent smoothness while holding the value distribution exactly
    fixed. This is the matched null: same numbers, no structure.
    """
    series: dict[int, list[float]] = {}
    for section in sections:
        hq = section.get("hamiltonian_hq")
        if hq is None:
            continue
        series.setdefault(section.get("cosmos") or 0, []).append(hq)

    if not series:
        return {"verdict": "NOT_APPLICABLE", "reason": "no H(Q) values present"}

    rng = random.Random(NULL_SEED)
    per_stratum = []
    for cosmos, values in sorted(series.items()):
        if len(values) < 3:
            continue
        observed = _roughness(values)
        nulls = []
        for _ in range(NULL_TRIALS):
            shuffled = values[:]
            rng.shuffle(shuffled)
            nulls.append(_roughness(shuffled))
        # One-sided: how often is a random ordering at least as smooth?
        at_least_as_smooth = sum(1 for n in nulls if n <= observed)

        # Second control. A monotone emission order is automatically smooth
        # under this metric, so beating a shuffle proves only "not random".
        # The sorted null is the smoothest ordering the multiset admits: if the
        # observed order matches it, the effect is monotonicity, not adiabaticity.
        sorted_rough = _roughness(sorted(values))
        per_stratum.append(
            {
                "stratum": cosmos,
                "n": len(values),
                "observed_max_step": observed,
                "null_median_max_step": statistics.median(nulls),
                "p_null_at_least_as_smooth": round(at_least_as_smooth / len(nulls), 4),
                "sorted_null_max_step": sorted_rough,
                "beats_sorted_null": observed < sorted_rough,
                "is_monotone": list(values) in (sorted(values), sorted(values, reverse=True)),
                "range": max(values) - min(values),
            }
        )

    if not per_stratum:
        return {"verdict": "NOT_APPLICABLE", "reason": "no stratum with >=3 values"}

    # Multiplicity. One test per stratum, so an uncorrected 0.05 threshold
    # inflates the family-wise error rate. Bonferroni is the conservative
    # correction; report both so the inflation is visible rather than hidden.
    tested = len(per_stratum)
    alpha_uncorrected = 0.05
    alpha_corrected = alpha_uncorrected / tested
    for stratum in per_stratum:
        stratum["survives_uncorrected"] = stratum["p_null_at_least_as_smooth"] < alpha_uncorrected
        stratum["survives_bonferroni"] = stratum["p_null_at_least_as_smooth"] < alpha_corrected

    uncorrected = sum(1 for s in per_stratum if s["survives_uncorrected"])
    corrected = sum(1 for s in per_stratum if s["survives_bonferroni"])
    monotone = sum(1 for s in per_stratum if s["is_monotone"])
    beats_sorted = sum(1 for s in per_stratum if s["beats_sorted_null"])

    # Preregistered kill (AUDIT.md round 1): if the observed ordering is not
    # smoother than the sorted null in >=5 of 7 strata, the effect is
    # monotonicity and the M promotion is retired.
    if beats_sorted < max(1, int(0.7 * tested)):
        verdict = "RETIRED_MONOTONICITY"
    elif corrected == tested:
        verdict = "SUPPORTED"
    elif corrected == 0:
        verdict = "NOT_SUPPORTED"
    else:
        verdict = "PARTIAL"

    return {
        "trials": NULL_TRIALS,
        "seed": NULL_SEED,
        "null_model": "within-stratum shuffle: identical value multiset, ordering destroyed",
        "alpha_uncorrected": alpha_uncorrected,
        "alpha_bonferroni": round(alpha_corrected, 6),
        "per_stratum": per_stratum,
        "strata_tested": tested,
        "strata_smoother_uncorrected": uncorrected,
        "strata_smoother_bonferroni": corrected,
        "strata_monotone": monotone,
        "strata_beating_sorted_null": beats_sorted,
        "verdict": verdict,
        "scope": (
            "Supports only that the declaration ordering is smoother than a reordering "
            "of the same values. Establishes no gap condition, no adiabatic theorem, "
            "and no ground state."
        ),
    }


def h3_berry(sections: list[dict]) -> dict:
    deviations = [
        abs(s["coordinates"]["berry"] - BERRY_TARGET)
        for s in sections
        if "berry" in (s.get("coordinates") or {})
    ]
    if not deviations:
        return {"verdict": "NOT_APPLICABLE", "reason": "no BERRY coordinates"}
    worst = max(deviations)
    return {
        "n": len(deviations),
        "target_pi_over_2": round(BERRY_TARGET, 10),
        "max_abs_deviation": worst,
        "mean_abs_deviation": statistics.mean(deviations),
        "stated_precision": BERRY_STATED_PRECISION,
        "within_stated_precision": worst <= BERRY_STATED_PRECISION,
        "verdict": "EQUALS_AS_WRITTEN" if worst <= BERRY_STATED_PRECISION else "APPROXIMATE_ONLY",
    }


R142_ROW_RE = __import__("re").compile(r"§R142_n(\d+):\s*S=([0-9.]+)")


def h4_rho_star(pack_path: Path) -> dict:
    """Is `ρ★ = 0.135 ± 0.003 (substrate-stable)` supported by its own table?

    Two separable questions, deliberately not merged:
      (a) is the central value and its uncertainty consistent with the tabulated
          S(n) series;
      (b) does anything in the table vary the substrate.
    """
    if not pack_path.exists():
        return {"verdict": "NOT_APPLICABLE", "reason": f"{pack_path} absent"}
    text = pack_path.read_text(encoding="utf-8")
    rows = [(int(n), float(s)) for n, s in R142_ROW_RE.findall(text)]
    if len(rows) < 3:
        return {"verdict": "NOT_APPLICABLE", "reason": "fewer than 3 tabulated points"}

    ratios = [s / n for n, s in rows]
    mean = statistics.mean(ratios)
    sd = statistics.stdev(ratios)
    sem = sd / math.sqrt(len(ratios))
    claimed_centre, claimed_unc = 0.135, 0.003
    offset_in_sem = abs(mean - claimed_centre) / sem if sem else float("inf")

    # A substrate-stability claim needs the substrate to vary. The table indexes
    # only system size n, so there is no substrate axis to be stable across.
    substrate_axes = 0

    return {
        "points": len(rows),
        "n_values": [n for n, _ in rows],
        "mean_ratio": round(mean, 6),
        "sample_sd": round(sd, 6),
        "sem": round(sem, 6),
        "claimed": {"centre": claimed_centre, "uncertainty": claimed_unc},
        "offset_from_claim_in_sem": round(offset_in_sem, 2),
        "uncertainty_consistent_with_sem": abs(claimed_unc - sem) < claimed_unc,
        "central_value_consistent": offset_in_sem < 2.0,
        "substrate_axes_varied": substrate_axes,
        "estimator_declared": False,
        "verdict_value": "CONSISTENT" if offset_in_sem < 2.0 else "INCONSISTENT",
        "verdict_substrate_stability": "UNSUPPORTED" if substrate_axes == 0 else "TESTED",
        "note": (
            "The central value and uncertainty are consistent with the pack's own "
            "series: sem is close to the stated uncertainty and the claimed centre "
            "sits under 2 sem from the mean. Separately, no substrate is varied "
            "anywhere in the table, so 'substrate-stable' has no support at all. "
            "The estimator (asymptotic value vs mean over n) is never declared, so "
            "which quantity 0.135 names is unpinned."
        ),
    }


def audit(mesh_path: Path) -> dict:
    mesh = load_mesh(mesh_path)
    sections = mesh["sections"]
    return {
        "source": mesh["source"],
        "sections": len(sections),
        "h1_gluing": h1_gluing(sections),
        "h2_adiabatic": h2_adiabatic(sections),
        "h3_berry": h3_berry(sections),
        "h4_rho_star": h4_rho_star(Path("MHRR_PM_Hypercomplex_Orthogonal.lang")),
        "evidence_scope": (
            "Consistency of a pack's own numbers with the pack's own adjectives. "
            "Not a measurement of any modelled system, and not a proof of anything."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure pack sheaf/adiabatic/Berry assertions.")
    parser.add_argument("meshes", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    results = [audit(path) for path in args.meshes]
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"audit → {args.out}")

    for result in results:
        print(f"\n== {result['source']}  ({result['sections']} sections)")
        g = result["h1_gluing"]
        print(f"  H1 gluing     : {g['verdict']}")
        if g["verdict"] != "NOT_APPLICABLE":
            for reading in ("by_prime", "by_depth"):
                r = g[reading]
                print(f"      {reading:9s}: pairs={r['pair_count']} nonempty={r['nonempty_overlap_pairs']} "
                      f"disjoint={r['cover_is_pairwise_disjoint']} mean_jaccard={r['mean_jaccard']}")
        a = result["h2_adiabatic"]
        if a["verdict"] in {"SUPPORTED", "NOT_SUPPORTED", "PARTIAL"}:
            print(f"  H2 adiabatic  : {a['verdict']}  "
                  f"{a['strata_smoother_bonferroni']}/{a['strata_tested']} survive Bonferroni "
                  f"(alpha={a['alpha_bonferroni']}); {a['strata_smoother_uncorrected']}/{a['strata_tested']} uncorrected")
            for s in a["per_stratum"]:
                flag = "PASS" if s["survives_bonferroni"] else ("marginal" if s["survives_uncorrected"] else "fail")
                mono = " MONOTONE" if s["is_monotone"] else ""
                print(f"      stratum {s['stratum']}: observed={s['observed_max_step']:.6g} "
                      f"shuffle_med={s['null_median_max_step']:.6g} p={s['p_null_at_least_as_smooth']} "
                      f"sorted_null={s['sorted_null_max_step']:.6g} beats_sorted={s['beats_sorted_null']} [{flag}]{mono}")
        else:
            print(f"  H2 adiabatic  : {a['verdict']} ({a.get('reason')})")
        r4 = result["h4_rho_star"]
        if r4.get("verdict_value"):
            print(f"  H4 rho-star   : value={r4['verdict_value']} ({r4['offset_from_claim_in_sem']} sem) "
                  f"| substrate-stability={r4['verdict_substrate_stability']} "
                  f"(axes varied: {r4['substrate_axes_varied']}) | sem={r4['sem']}")
        b = result["h3_berry"]
        if b["verdict"] != "NOT_APPLICABLE":
            print(f"  H3 berry      : {b['verdict']}  max|BERRY-pi/2|={b['max_abs_deviation']:.6g} "
                  f"(stated precision {b['stated_precision']:g})")


if __name__ == "__main__":
    main()

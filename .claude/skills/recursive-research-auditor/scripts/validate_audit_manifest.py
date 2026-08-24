#!/usr/bin/env python3
"""Validate a Recursive Research Auditor JSON manifest.

The validator checks structural completeness and flags common self-validation
failure modes. It does not determine whether a scientific claim is true.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

EVIDENCE_TAGS = {"P", "A", "M", "H", "S", "R"}
METRIC_TYPES = {"scalar", "interval", "distribution", "partial_order", "typed_tuple"}
DIRECTIONS = {"higher_is_better", "lower_is_better", "two_sided", "partial_order"}

REQUIRED_TOP = {
    "task_id",
    "claim",
    "specification",
    "implementation",
    "metric",
    "tests",
    "controls",
    "preregistration",
    "evidence",
    "round_trip",
    "result",
}

REQUIRED_NESTED: dict[str, set[str]] = {
    "claim": {"text", "scope", "status_before", "assumptions", "forbidden_promotions"},
    "specification": {"intended_object", "invariants", "known_answer_cases"},
    "implementation": {"artifact", "commit", "environment", "live_entrypoint", "representation"},
    "metric": {
        "name",
        "type",
        "units",
        "direction",
        "raw_before_clipping",
        "semantic_invariance_claimed",
        "equivalence_attacks",
    },
    "tests": {"black_box", "structural", "property_based", "metamorphic", "fuzzing", "historical"},
    "controls": {
        "matched_baselines",
        "negative_controls",
        "compute_parity",
        "parameter_parity",
        "sampling_parity",
        "data_access_parity",
    },
    "preregistration": {
        "prediction",
        "primary_metric",
        "uncertainty_method",
        "kill_condition",
        "stop_condition",
        "promotion_rule",
    },
    "evidence": {"primary_sources", "execution_records", "independent_witnesses", "claim_to_artifact_map"},
    "round_trip": {"edges"},
    "result": {"observed", "effect_size", "uncertainty", "status_after", "retired_claims", "active_remainder"},
}


def blank(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a JSON object")
    return data


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing_top = sorted(REQUIRED_TOP - data.keys())
    if missing_top:
        errors.append(f"missing top-level fields: {', '.join(missing_top)}")

    for section, fields in REQUIRED_NESTED.items():
        value = data.get(section)
        if not isinstance(value, dict):
            errors.append(f"{section} must be an object")
            continue
        missing = sorted(fields - value.keys())
        if missing:
            errors.append(f"{section} missing fields: {', '.join(missing)}")
        allowed_empty = {("result", "retired_claims")}
        for field in fields & value.keys():
            if blank(value[field]) and (section, field) not in allowed_empty:
                warnings.append(f"{section}.{field} is blank; explain why it is not applicable")

    claim = data.get("claim", {})
    result = data.get("result", {})
    before = claim.get("status_before")
    after = result.get("status_after")
    if before not in EVIDENCE_TAGS:
        errors.append(f"claim.status_before must be one of {sorted(EVIDENCE_TAGS)}")
    if after not in EVIDENCE_TAGS:
        errors.append(f"result.status_after must be one of {sorted(EVIDENCE_TAGS)}")

    metric = data.get("metric", {})
    if metric.get("type") not in METRIC_TYPES:
        errors.append(f"metric.type must be one of {sorted(METRIC_TYPES)}")
    if metric.get("direction") not in DIRECTIONS:
        errors.append(f"metric.direction must be one of {sorted(DIRECTIONS)}")
    if metric.get("raw_before_clipping") is not True:
        warnings.append("metric.raw_before_clipping should be true to expose preprocessing artifacts")
    if metric.get("semantic_invariance_claimed") is True and not metric.get("equivalence_attacks"):
        errors.append("semantic invariance is claimed but metric.equivalence_attacks is empty")
    if metric.get("type") == "scalar":
        warnings.append("scalar metric: justify why intervals, distributions, typed tuples, or partial orders are inadequate")

    tests = data.get("tests", {})
    independent_test_families = sum(bool(tests.get(name)) for name in ("property_based", "metamorphic", "black_box"))
    if independent_test_families == 0:
        warnings.append("no black-box, property-based, or metamorphic test family is declared")
    if not tests.get("structural"):
        warnings.append("no structural/white-box test is declared")
    if not tests.get("historical"):
        warnings.append("no historical regression test is declared")

    controls = data.get("controls", {})
    if not controls.get("matched_baselines"):
        errors.append("controls.matched_baselines must contain at least one baseline")
    if not controls.get("negative_controls"):
        warnings.append("no negative control is declared")
    for field in ("compute_parity", "parameter_parity", "sampling_parity", "data_access_parity"):
        text = str(controls.get(field, "")).strip().lower()
        if not text:
            errors.append(f"controls.{field} must be stated or marked not applicable with a reason")

    prereg = data.get("preregistration", {})
    for field in ("kill_condition", "stop_condition", "promotion_rule"):
        if blank(prereg.get(field)):
            errors.append(f"preregistration.{field} is required")
    kill = str(prereg.get("kill_condition", "")).lower()
    if "clip" in kill and metric.get("raw_before_clipping") is not True:
        warnings.append("kill condition mentions clipping but raw values are not explicitly required")

    evidence = data.get("evidence", {})
    witnesses = evidence.get("independent_witnesses", [])
    if not isinstance(witnesses, list) or not witnesses:
        warnings.append("no independent witness is declared; self-review is correlated evidence")
    else:
        origins = {
            str(w.get("origin", "")).strip().lower()
            for w in witnesses
            if isinstance(w, dict) and str(w.get("origin", "")).strip()
        }
        if len(origins) < 1:
            warnings.append("independent witnesses do not declare their independence origin")

    if not evidence.get("claim_to_artifact_map"):
        errors.append("evidence.claim_to_artifact_map must map important claims to artifacts")
    if not evidence.get("execution_records"):
        warnings.append("no execution record is declared; runtime claims remain reported rather than reproduced")

    round_trip = data.get("round_trip", {})
    edges = round_trip.get("edges", [])
    if not isinstance(edges, list) or len(edges) < 6:
        warnings.append("round_trip.edges should normally cover the full requirement-to-interpretation cycle")
    else:
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                errors.append(f"round_trip.edges[{index}] must be an object")
                continue
            for field in ("from", "to", "preserved", "transformed", "lost", "remainder"):
                if field not in edge:
                    errors.append(f"round_trip.edges[{index}] missing {field}")

    if after == "P" and not evidence.get("primary_sources"):
        warnings.append("result is tagged P but no primary source or proof artifact is listed")
    if after == "M" and blank(result.get("uncertainty")):
        errors.append("measured result requires result.uncertainty")
    if after in {"P", "M"} and not evidence.get("claim_to_artifact_map"):
        errors.append("promoted result lacks a claim-to-artifact map")

    forbidden = claim.get("forbidden_promotions", [])
    if not forbidden:
        warnings.append("claim.forbidden_promotions is empty; state what the result must not be used to claim")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to audit manifest JSON")
    args = parser.parse_args()

    try:
        data = load_manifest(args.manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data)
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

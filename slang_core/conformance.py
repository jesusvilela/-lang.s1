"""Manifest-driven conformance runner for §-LANG S1 Core."""

from __future__ import annotations

from collections import Counter
import argparse
import json
from pathlib import Path
from typing import Any

from .core import CoreRuntimeError, CoreSyntaxError, run_source


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "core" / "conformance.json"


def _case_result(case: dict[str, Any], root: Path) -> dict[str, Any]:
    case_id = case["id"]

    if case.get("applicable") is False:
        return {
            "id": case_id,
            "status": "NOT_APPLICABLE",
            "reason": case.get("reason", "case declared not applicable"),
        }

    if case.get("tested") is False:
        return {
            "id": case_id,
            "status": "NOT_TESTED",
            "reason": case.get("reason", "no conformance test implemented"),
        }

    path = root / case["file"]
    try:
        result = run_source(path.read_text(encoding="utf-8"))
    except (OSError, CoreSyntaxError, CoreRuntimeError) as exc:
        return {
            "id": case_id,
            "status": "FAIL",
            "reason": f"execution error: {exc}",
        }

    problems: list[str] = []
    expected_status = case.get("expected_program_status")
    if result["status"] != expected_status:
        problems.append(
            f"program status {result['status']} != expected {expected_status}"
        )

    if "expected_emissions" in case and result["emissions"] != case["expected_emissions"]:
        problems.append(
            f"emissions {result['emissions']!r} != expected {case['expected_emissions']!r}"
        )

    if "expected_evidence_count" in case:
        actual = len(result["evidence"])
        expected = case["expected_evidence_count"]
        if actual != expected:
            problems.append(f"evidence count {actual} != expected {expected}")

    return {
        "id": case_id,
        "status": "FAIL" if problems else "PASS",
        "program": case["file"],
        "observed_program_status": result["status"],
        "problems": problems,
    }


def run_conformance(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = manifest_path.resolve().parents[1]
    cases = [_case_result(case, root) for case in manifest["cases"]]
    counts = Counter(case["status"] for case in cases)
    overall = "FAIL" if counts["FAIL"] else "PASS"
    return {
        "schema": "slang.s1.conformance.v1",
        "status": overall,
        "manifest_schema": manifest.get("schema"),
        "tested_programs": sum(1 for case in manifest["cases"] if "file" in case),
        "case_status_counts": {
            status: counts.get(status, 0)
            for status in ("PASS", "FAIL", "NOT_APPLICABLE", "NOT_TESTED")
        },
        "cases": cases,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run §-LANG S1 Core conformance.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    report = run_conformance(args.manifest)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    else:
        print(f"§-LANG S1 conformance: {report['status']}")
        for case in report["cases"]:
            print(f"{case['status']:>14}  {case['id']}")

    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())

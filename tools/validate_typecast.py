#!/usr/bin/env python3
"""Evidence-bounded structural validation for §-LANG sources.

This tool validates declared textual profiles. It does not prove semantics,
mathematical theorems, runtime behavior, or external scientific claims.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

OUT_JSON = Path("research/validation_report.json")
OUT_MD = Path("research/validation_report.md")
OUT_ALL_JSON = Path("research/validation_report_all.json")
OUT_ALL_MD = Path("research/validation_report_all.md")
SOURCE_MANIFEST = Path("validation/sources.json")
EXPECTED_SECTION_DIMENSION = 8
POINCARE_BOUNDARY_MARGIN = 0.999

PASS = "PASS"
FAIL = "FAIL"
NOT_APPLICABLE = "NOT_APPLICABLE"
NOT_TESTED = "NOT_TESTED"

BLOCK_RE = re.compile(r"^§\|LANG\|([A-Z_]+)\{")
SECTION_RE = re.compile(r"^§S\{label=([^,]+), x=\[([^\]]+)\], sal=([0-9.]+)\}$")
PACK_RE = re.compile(r"^§PACK\s+(.+)$")
VERSION_RE = re.compile(r"^§VERSION\s+(.+)$")

PROFILES: dict[str, dict[str, object]] = {
    "unified_geometry": {
        "required": ["SOURCE", "AXIOMS", "OUTPUT", "BASES", "SORTS", "FUNCTORS", "SEMANTICS", "REDUCTION_BETA", "TURING_ENCODING", "SPECTRAL_PIPELINE", "FISHER_UPDATE", "INTER_MANIFOLD", "GRAMMAR", "NOTATION_MAP", "SEMANTICS_TOPOS", "AML_DEFINITION", "NMATRIX_SELFREF", "FIBER_BUNDLE_POSSIBILITY_SPACE", "ADIABATIC_MOBIUS_FLOW", "CONCLUSIONS"],
    },
    "tower_geom": {"required": ["SOURCE", "SORTS", "AXIOMS", "TOWER_STRUCTURE", "INVARIANTS", "REDUCTION", "OUTPUT", "NOTES"]},
    "substrate": {"required": ["SOURCE", "NATIVE_SUBSTRATE", "AXIOMS", "HAMILTONIAN_FLOW", "HOLOGRAPHIC_SCREEN_SN", "OUTPUT", "NOTES"]},
    "recursive_sectional": {"required": ["SOURCE", "RECURSIVE_SUBSTRATE", "AXIOMS", "SECTIONAL_COMPUTER_RECURSION", "HOLOGRAPHIC_NESTING", "OUTPUT", "NOTES"]},
    "actor_critic": {"required": ["SOURCE", "ACF_ROLES", "ACTOR_CRITIC_DYNAMICS", "FUZZER_EXPLORATION", "OUTPUT", "NOTES"]},
    "topos_ai": {"required": ["SOURCE", "TOPOS_AI_COSMOS_STRUCTURE", "NATIVE_PHYSICS_AXIOMS", "RECURSIVE_OPERATOR_FLOW", "HOLOGRAPHIC_COMMIT_PROTOCOL", "OUTPUT", "NOTES"]},
    "chomsky_hyperdim": {"required": ["SOURCE", "CHOMSKY_GEOMETRIC_SPACE", "HYPERDIM_MATRIX_CONTEXT", "SELF_GODEL_IDENTITY", "OTHERS_RESONANCE", "N_COSMO_BUNDLE_SHEAF", "HAMILTONIAN_HOLOPORTATION", "MIND_QUALITIES_EIGHT", "STEPWISE_IMPLEMENTATION", "OUTPUT", "NOTES"]},
    "dialects": {"required": ["DIALECT_TREE", "DIALECT_RULES", "DIALECT_NOTES"]},
    "mhrr_pack_v1": {"required": []},
}


@dataclass
class SectionPoint:
    label: str
    x: list[float]
    sal: float

    @property
    def norm(self) -> float:
        return math.sqrt(sum(v * v for v in self.x))


def load_manifest(path: Path = SOURCE_MANIFEST) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("sources")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path} must contain a non-empty 'sources' array")
    normalized: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("path") or not entry.get("profile"):
            raise ValueError(f"invalid source entry in {path}: {entry!r}")
        normalized.append({"path": str(entry["path"]), "profile": str(entry["profile"])})
    return normalized


def declared_profile(src: Path, manifest_entries: list[dict[str, str]]) -> str | None:
    target = src.as_posix()
    for entry in manifest_entries:
        if Path(entry["path"]).as_posix() == target:
            return entry["profile"]
    return None


def property_status(sections: list[SectionPoint], predicate: Callable[[SectionPoint], bool]) -> str:
    if not sections:
        return NOT_APPLICABLE
    return PASS if all(predicate(section) for section in sections) else FAIL


def validate_source(src: Path, profile: str) -> dict:
    if profile not in PROFILES:
        return {
            "source": str(src), "profile": profile, "surface": "unknown",
            "num_lines": 0, "num_blocks": 0, "unique_blocks": [],
            "missing_required_blocks": [], "num_sections": 0,
            "checks": {"declared_profile_known": FAIL},
            "geometry": {"max_section_norm": None, "margin_to_boundary_0_999": None},
            "notes": ["Unknown profile. Validation was not silently defaulted."],
        }

    lines = src.read_text(encoding="utf-8").splitlines()
    blocks: list[str] = []
    sections: list[SectionPoint] = []
    pack_name: str | None = None
    version: str | None = None

    for raw in lines:
        line = raw.strip()
        if match := BLOCK_RE.match(line):
            blocks.append(match.group(1))
        if match := SECTION_RE.match(line):
            sections.append(SectionPoint(match.group(1), [float(v.strip()) for v in match.group(2).split(",")], float(match.group(3))))
        if match := PACK_RE.match(line):
            pack_name = match.group(1).strip()
        if match := VERSION_RE.match(line):
            version = match.group(1).strip()

    block_set = set(blocks)
    required = list(PROFILES[profile]["required"])
    missing = [name for name in required if name not in block_set]

    if profile == "mhrr_pack_v1":
        surface_status = PASS if pack_name and version else FAIL
        block_status = NOT_APPLICABLE
        notes = ["MHRR pack surface recognized by explicit §PACK and §VERSION headers.", "Semantic, theorem, and empirical claims are NOT_TESTED by this validator."]
    else:
        surface_status = PASS
        block_status = PASS if not missing else FAIL
        notes = []

    checks = {
        "declared_profile_known": PASS,
        "surface_recognized": surface_status,
        "block_headers_present": block_status,
        "section_vectors_dimension_8": property_status(sections, lambda p: len(p.x) == EXPECTED_SECTION_DIMENSION),
        "section_norm_below_0_999": property_status(sections, lambda p: p.norm < POINCARE_BOUNDARY_MARGIN),
        "salience_positive": property_status(sections, lambda p: p.sal > 0),
        "semantic_correctness": NOT_TESTED,
        "mathematical_claims": NOT_TESTED,
        "empirical_claims": NOT_TESTED,
    }

    max_norm = max((p.norm for p in sections), default=None)
    margin = None if max_norm is None else POINCARE_BOUNDARY_MARGIN - max_norm
    return {
        "source": str(src), "profile": profile,
        "surface": "pack" if pack_name else "legacy_block",
        "pack": pack_name, "version": version,
        "num_lines": len(lines), "num_blocks": len(blocks),
        "unique_blocks": sorted(block_set), "missing_required_blocks": missing,
        "num_sections": len(sections), "checks": checks,
        "geometry": {
            "max_section_norm": None if max_norm is None else round(max_norm, 6),
            "margin_to_boundary_0_999": None if margin is None else round(margin, 6),
        },
        "notes": notes,
    }


def report_passes(report: dict) -> bool:
    return all(value != FAIL for value in report["checks"].values())


def status_icon(status: str) -> str:
    return {PASS: "✅", FAIL: "❌", NOT_APPLICABLE: "➖", NOT_TESTED: "⚪"}.get(status, "?")


def report_to_md_lines(report: dict) -> list[str]:
    lines = [
        "# Validation and Typecast Report", "",
        "> Structural validation only. PASS is not a semantic or mathematical proof.", "",
        f"- Source: `{report['source']}`", f"- Profile: `{report['profile']}`",
        f"- Surface: `{report['surface']}`", f"- Lines: {report['num_lines']}",
        f"- Blocks: {report['num_blocks']}", f"- Sections: {report['num_sections']}", "",
        "## Checks",
    ]
    for name, status in report["checks"].items():
        lines.append(f"- {status_icon(status)} `{name}` — `{status}`")
    if report["missing_required_blocks"]:
        lines.extend(["", f"Missing required blocks: `{report['missing_required_blocks']}`"])
    if report["notes"]:
        lines.extend(["", "## Notes"] + [f"- {note}" for note in report["notes"]])
    return lines


def build_aggregate_md(reports: list[dict]) -> list[str]:
    all_pass = all(report_passes(r) for r in reports)
    lines = [
        "# §-LANG Aggregate Validation Report", "",
        "> Scope: declared structural surfaces only. `NOT_TESTED` and `NOT_APPLICABLE` are not passes.", "",
        f"## Summary {'✅' if all_pass else '❌'}", "",
        "| Source | Profile | Surface | Sections | Structural result |",
        "|---|---|---:|---:|---|",
    ]
    for report in reports:
        lines.append(f"| `{report['source']}` | `{report['profile']}` | `{report['surface']}` | {report['num_sections']} | {'PASS' if report_passes(report) else 'FAIL'} |")
    lines.append("")
    for report in reports:
        lines.extend([f"## `{report['source']}`", ""])
        for name, status in report["checks"].items():
            lines.append(f"- {status_icon(status)} `{name}` — `{status}`")
        lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate declared §-LANG structural surfaces.")
    parser.add_argument("--source", type=Path, default=Path("LANG.v1.2.0.unified_geometry.lang"))
    parser.add_argument("--profile", help="Explicit profile for --source; otherwise read from validation/sources.json")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    try:
        manifest = load_manifest()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Manifest error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    if args.all:
        reports: list[dict] = []
        failed = False
        for entry in manifest:
            src = Path(entry["path"])
            if not src.exists():
                report = {"source": str(src), "profile": entry["profile"], "surface": "missing", "num_lines": 0, "num_blocks": 0, "unique_blocks": [], "missing_required_blocks": [], "num_sections": 0, "checks": {"source_exists": FAIL}, "geometry": {"max_section_norm": None, "margin_to_boundary_0_999": None}, "notes": ["Manifest-declared source is missing."]}
            else:
                report = validate_source(src, entry["profile"])
            reports.append(report)
            ok = report_passes(report)
            failed = failed or not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {src}")
        OUT_ALL_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_ALL_JSON.write_text(json.dumps(reports, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        OUT_ALL_MD.write_text("\n".join(build_aggregate_md(reports)) + "\n", encoding="utf-8")
        raise SystemExit(1 if failed else 0)

    profile = args.profile or declared_profile(args.source, manifest)
    if profile is None:
        print("Source is not declared in validation/sources.json; pass --profile explicitly.", file=sys.stderr)
        raise SystemExit(2)
    if not args.source.exists():
        print(f"Source not found: {args.source}", file=sys.stderr)
        raise SystemExit(2)
    report = validate_source(args.source, profile)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text("\n".join(report_to_md_lines(report)) + "\n", encoding="utf-8")
    raise SystemExit(0 if report_passes(report) else 1)


if __name__ == "__main__":
    main()

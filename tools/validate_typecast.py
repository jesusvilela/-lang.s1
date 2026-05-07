#!/usr/bin/env python3
"""Validate and typecast §-LANG sources locally."""

from __future__ import annotations

import json
import math
import re
import sys
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

OUT_JSON = Path("research/validation_report.json")
OUT_MD = Path("research/validation_report.md")
OUT_ALL_JSON = Path("research/validation_report_all.json")
OUT_ALL_MD = Path("research/validation_report_all.md")
EXPECTED_SECTION_DIMENSION = 8
POINCARE_BOUNDARY_MARGIN = 0.999

BLOCK_RE = re.compile(r"^§\|LANG\|([A-Z_]+)\{")
SECTION_RE = re.compile(
    r"^§S\{label=([^,]+), x=\[([^\]]+)\], sal=([0-9.]+)\}$"
)

REQUIRED_BLOCKS_UNIFIED_GEOMETRY = [
    "SOURCE",
    "AXIOMS",
    "OUTPUT",
    "BASES",
    "SORTS",
    "FUNCTORS",
    "SEMANTICS",
    "REDUCTION_BETA",
    "TURING_ENCODING",
    "SPECTRAL_PIPELINE",
    "FISHER_UPDATE",
    "INTER_MANIFOLD",
    "GRAMMAR",
    "NOTATION_MAP",
    "SEMANTICS_TOPOS",
    "AML_DEFINITION",
    "NMATRIX_SELFREF",
    "FIBER_BUNDLE_POSSIBILITY_SPACE",
    "ADIABATIC_MOBIUS_FLOW",
    "CONCLUSIONS",
]

REQUIRED_BLOCKS_TOWER_GEOM = [
    "SOURCE",
    "SORTS",
    "AXIOMS",
    "TOWER_STRUCTURE",
    "INVARIANTS",
    "REDUCTION",
    "OUTPUT",
    "NOTES",
]

REQUIRED_BLOCKS_SUBSTRATE = [
    "SOURCE",
    "NATIVE_SUBSTRATE",
    "AXIOMS",
    "HAMILTONIAN_FLOW",
    "HOLOGRAPHIC_SCREEN_SN",
    "OUTPUT",
    "NOTES",
]

REQUIRED_BLOCKS_RECURSIVE_SECTIONAL = [
    "SOURCE",
    "RECURSIVE_SUBSTRATE",
    "AXIOMS",
    "SECTIONAL_COMPUTER_RECURSION",
    "HOLOGRAPHIC_NESTING",
    "OUTPUT",
    "NOTES",
]

REQUIRED_BLOCKS_ACTOR_CRITIC = [
    "SOURCE",
    "ACF_ROLES",
    "ACTOR_CRITIC_DYNAMICS",
    "FUZZER_EXPLORATION",
    "OUTPUT",
    "NOTES",
]

REQUIRED_BLOCKS_TOPOS_AI = [
    "SOURCE",
    "TOPOS_AI_COSMOS_STRUCTURE",
    "NATIVE_PHYSICS_AXIOMS",
    "RECURSIVE_OPERATOR_FLOW",
    "HOLOGRAPHIC_COMMIT_PROTOCOL",
    "OUTPUT",
    "NOTES",
]

REQUIRED_BLOCKS_DIALECTS = [
    "DIALECT_TREE",
    "DIALECT_RULES",
    "DIALECT_NOTES",
]

TYPECAST_UNIFIED_GEOMETRY = {
    "SOURCE": "meta_binding",
    "AXIOMS": "logical_foundation",
    "OUTPUT": "operational_contract",
    "BASES": "geometric_and_logical_base_layers",
    "SORTS": "type_universe",
    "FUNCTORS": "categorical_morphisms",
    "SEMANTICS": "topos_semantics",
    "REDUCTION_BETA": "geometric_computation",
    "TURING_ENCODING": "computability_bridge",
    "SPECTRAL_PIPELINE": "frequency_semantics",
    "FISHER_UPDATE": "information_geometry_learning",
    "INTER_MANIFOLD": "cross_bundle_exchange",
    "GRAMMAR": "surface_syntax",
    "NOTATION_MAP": "notation_lowering",
    "SEMANTICS_TOPOS": "classifier_topos_layer",
    "AML_DEFINITION": "autonomous_agent_layer",
    "NMATRIX_SELFREF": "self_referential_operator_dynamics",
    "FIBER_BUNDLE_POSSIBILITY_SPACE": "global_section_possibility_geometry",
    "ADIABATIC_MOBIUS_FLOW": "reversible_cross_manifold_information_flow",
    "CONCLUSIONS": "theory_closure",
}

TYPECAST_TOWER_GEOM = {
    "SOURCE": "meta_binding",
    "SORTS": "tower_type_universe",
    "AXIOMS": "geometric_laws",
    "TOWER_STRUCTURE": "vertical_horizontal_transport_layout",
    "INVARIANTS": "stability_constraints",
    "REDUCTION": "tower_evolution_dynamics",
    "OUTPUT": "operational_contract",
    "NOTES": "semantic_interpretation_and_scope",
}

TYPECAST_SUBSTRATE = {
    "SOURCE": "meta_binding",
    "NATIVE_SUBSTRATE": "symplectic_manifold_type_definitions",
    "AXIOMS": "hamiltonian_geometric_laws",
    "HAMILTONIAN_FLOW": "energy_preserving_phase_space_dynamics",
    "HOLOGRAPHIC_SCREEN_SN": "boundary_projection_geometry",
    "OUTPUT": "operational_contract",
    "NOTES": "semantic_interpretation_and_scope",
}

TYPECAST_RECURSIVE_SECTIONAL = {
    "SOURCE": "meta_binding",
    "RECURSIVE_SUBSTRATE": "nested_setting_type_definitions",
    "AXIOMS": "recursive_adiabatic_laws",
    "SECTIONAL_COMPUTER_RECURSION": "self_referential_coupling_dynamics",
    "HOLOGRAPHIC_NESTING": "nested_holographic_projection",
    "OUTPUT": "operational_contract",
    "NOTES": "semantic_interpretation_and_scope",
}

TYPECAST_ACTOR_CRITIC = {
    "SOURCE": "meta_binding",
    "ACF_ROLES": "agent_role_type_definitions",
    "ACTOR_CRITIC_DYNAMICS": "reinforcement_loop_semantics",
    "FUZZER_EXPLORATION": "adversarial_boundary_search",
    "OUTPUT": "operational_contract",
    "NOTES": "semantic_interpretation_and_scope",
}

TYPECAST_TOPOS_AI = {
    "SOURCE": "meta_binding",
    "TOPOS_AI_COSMOS_STRUCTURE": "recursive_cosmos_type_definitions",
    "NATIVE_PHYSICS_AXIOMS": "hamiltonian_n_cosmos_laws",
    "RECURSIVE_OPERATOR_FLOW": "nested_operator_compatibility",
    "HOLOGRAPHIC_COMMIT_PROTOCOL": "boundary_commit_decision_semantics",
    "OUTPUT": "operational_contract",
    "NOTES": "semantic_interpretation_and_scope",
}

TYPECAST_DIALECTS = {
    "DIALECT_TREE": "inheritance_hierarchy",
    "DIALECT_RULES": "block_permission_and_extension_rules",
    "DIALECT_NOTES": "policy_and_complexity_claims",
}


@dataclass
class SectionPoint:
    label: str
    x: list[float]
    sal: float

    @property
    def norm(self) -> float:
        return math.sqrt(sum(v * v for v in self.x))


def infer_profile(source: Path) -> str:
    name = source.name
    if "tower.geom" in name:
        return "tower_geom"
    if "substrate_realization" in name:
        return "substrate"
    if "recursive_sectional" in name:
        return "recursive_sectional"
    if "actor_critic" in name:
        return "actor_critic"
    if "topos_ai" in name:
        return "topos_ai"
    if "DIALECTS" in name or "dialect" in name.lower():
        return "dialects"
    return "unified_geometry"


def get_profile_config(profile: str) -> tuple[list[str], dict[str, str]]:
    configs: dict[str, tuple[list[str], dict[str, str]]] = {
        "unified_geometry": (REQUIRED_BLOCKS_UNIFIED_GEOMETRY, TYPECAST_UNIFIED_GEOMETRY),
        "tower_geom": (REQUIRED_BLOCKS_TOWER_GEOM, TYPECAST_TOWER_GEOM),
        "substrate": (REQUIRED_BLOCKS_SUBSTRATE, TYPECAST_SUBSTRATE),
        "recursive_sectional": (REQUIRED_BLOCKS_RECURSIVE_SECTIONAL, TYPECAST_RECURSIVE_SECTIONAL),
        "actor_critic": (REQUIRED_BLOCKS_ACTOR_CRITIC, TYPECAST_ACTOR_CRITIC),
        "topos_ai": (REQUIRED_BLOCKS_TOPOS_AI, TYPECAST_TOPOS_AI),
        "dialects": (REQUIRED_BLOCKS_DIALECTS, TYPECAST_DIALECTS),
    }
    return configs.get(profile, configs["unified_geometry"])


def validate_sections_property(
    sections: list[SectionPoint],
    predicate: Callable[[SectionPoint], bool],
    default: bool = True,
) -> bool:
    return default if not sections else all(predicate(section) for section in sections)


def validate_source(src: Path) -> dict:
    """Validate a single .lang source file and return a report dict."""
    profile = infer_profile(src)
    required_blocks, typecast_map = get_profile_config(profile)

    text = src.read_text(encoding="utf-8").splitlines()

    blocks: list[str] = []
    sections: list[SectionPoint] = []

    for line in text:
        b = BLOCK_RE.match(line.strip())
        if b:
            blocks.append(b.group(1))

        s = SECTION_RE.match(line.strip())
        if s:
            label = s.group(1)
            vec = [float(v.strip()) for v in s.group(2).split(",")]
            sal = float(s.group(3))
            sections.append(SectionPoint(label=label, x=vec, sal=sal))

    block_set = set(blocks)
    missing = [b for b in required_blocks if b not in block_set]

    dim_ok = validate_sections_property(
        sections, lambda p: len(p.x) == EXPECTED_SECTION_DIMENSION
    )
    norm_ok = validate_sections_property(
        sections, lambda p: p.norm < POINCARE_BOUNDARY_MARGIN
    )
    sal_ok = validate_sections_property(sections, lambda p: p.sal > 0)

    max_norm = max((p.norm for p in sections), default=0.0)
    min_margin = POINCARE_BOUNDARY_MARGIN - max_norm

    return {
        "source": str(src),
        "profile": profile,
        "num_lines": len(text),
        "num_blocks": len(blocks),
        "unique_blocks": sorted(block_set),
        "missing_required_blocks": missing,
        "num_sections": len(sections),
        "checks": {
            "block_headers_present": len(missing) == 0,
            "section_vectors_dimension_8": dim_ok,
            "section_norm_below_0_999": norm_ok,
            "salience_positive": sal_ok,
        },
        "geometry": {
            "max_section_norm": round(max_norm, 6),
            "margin_to_boundary_0_999": round(min_margin, 6),
        },
        "typecast": {k: typecast_map[k] for k in required_blocks},
    }


def report_to_md_lines(report: dict) -> list[str]:
    """Convert a single-source report dict into Markdown lines."""
    required_blocks = list(report["typecast"].keys())
    lines = [
        "# Validation and Typecast Report",
        "",
        "## Status",
        f"- Source: `{report['source']}`",
        f"- Profile: `{report['profile']}`",
        f"- Lines: {report['num_lines']}",
        f"- Blocks discovered: {report['num_blocks']} ({len(report['unique_blocks'])} unique)",
        f"- Section nodes discovered: {report['num_sections']}",
        "",
        "## Checks",
    ]
    for name, ok in report["checks"].items():
        icon = "✅" if ok else "❌"
        lines.append(f"- {icon} `{name}`")

    lines.extend(
        [
            "",
            "## Geometric Boundary",
            f"- Max section norm: {report['geometry']['max_section_norm']}",
            f"- Margin to invariant 0.999: {report['geometry']['margin_to_boundary_0_999']}",
            "",
            "## Typecast Map",
        ]
    )
    for block in required_blocks:
        lines.append(f"- `{block}` → `{report['typecast'][block]}`")

    lines.extend(
        [
            "",
            "## Postulate",
            "A fully sectional hyperbolic self-referential computer is admissible when section norms remain strictly interior to the Poincaré boundary and recursion is mediated by reversible transport over the bundle.",
        ]
    )
    return lines


def build_aggregate_md(reports: list[dict]) -> list[str]:
    """Build an aggregate Markdown report covering all validated sources."""
    all_pass = all(all(r["checks"].values()) for r in reports)
    summary_icon = "✅" if all_pass else "❌"

    lines = [
        "# §-LANG Aggregate Validation Report",
        "",
        "> **Scope:** Syntactic and structural validation only.",
        "> These checks confirm block presence, section-vector geometry, and salience positivity.",
        "> They do **not** prove semantic correctness, mathematical theorems, or LLM-induced",
        "> meta-semantic claims. See `VERIFICATION.md` for a full scope statement.",
        "",
        f"## Summary {summary_icon}",
        "",
        "| Source | Profile | Lines | Blocks | Sections | All checks |",
        "|--------|---------|-------|--------|----------|------------|",
    ]
    for r in reports:
        ok = "✅" if all(r["checks"].values()) else "❌"
        lines.append(
            f"| `{r['source']}` | `{r['profile']}` | {r['num_lines']} "
            f"| {r['num_blocks']} | {r['num_sections']} | {ok} |"
        )

    lines.append("")
    for r in reports:
        lines.append(f"## `{r['source']}`")
        lines.append("")
        for name, ok in r["checks"].items():
            icon = "✅" if ok else "❌"
            lines.append(f"- {icon} `{name}`")
        if r["missing_required_blocks"]:
            lines.append(f"- ⚠️  Missing required blocks: {r['missing_required_blocks']}")
        lines.append(
            f"- Max section norm: {r['geometry']['max_section_norm']} "
            f"(margin to 0.999: {r['geometry']['margin_to_boundary_0_999']})"
        )
        lines.append("")

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and typecast §-LANG sources.")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("LANG.v1.2.0.unified_geometry.lang"),
        help="Path to the .lang source file to validate.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all .lang files found in the current directory and write an aggregate report.",
    )
    args = parser.parse_args()

    if args.all:
        sources = sorted(Path(".").glob("*.lang"))
        if not sources:
            print("No .lang files found in the current directory.", file=sys.stderr)
            sys.exit(1)

        reports = []
        failed = False
        for src in sources:
            report = validate_source(src)
            reports.append(report)
            ok = all(report["checks"].values())
            status = "PASS" if ok else "FAIL"
            if not ok:
                failed = True
            print(f"[{status}] {src}")

        OUT_ALL_JSON.write_text(
            json.dumps(reports, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        OUT_ALL_MD.write_text(
            "\n".join(build_aggregate_md(reports)) + "\n", encoding="utf-8"
        )
        print(f"\nAggregate JSON  → {OUT_ALL_JSON}")
        print(f"Aggregate MD    → {OUT_ALL_MD}")
        sys.exit(1 if failed else 0)
    else:
        src = args.source
        report = validate_source(src)

        OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        OUT_MD.write_text("\n".join(report_to_md_lines(report)) + "\n", encoding="utf-8")
        print(f"JSON → {OUT_JSON}")
        print(f"MD   → {OUT_MD}")
        ok = all(report["checks"].values())
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

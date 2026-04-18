#!/usr/bin/env python3
"""Validate and typecast §-LANG sources locally."""

from __future__ import annotations

import json
import math
import re
import argparse
from dataclasses import dataclass
from pathlib import Path

OUT_JSON = Path("research/validation_report.json")
OUT_MD = Path("research/validation_report.md")

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


@dataclass
class SectionPoint:
    label: str
    x: list[float]
    sal: float

    @property
    def norm(self) -> float:
        return math.sqrt(sum(v * v for v in self.x))


def infer_profile(source: Path) -> str:
    if "tower.geom" in source.name:
        return "tower_geom"
    return "unified_geometry"


def get_profile_config(profile: str) -> tuple[list[str], dict[str, str]]:
    if profile == "tower_geom":
        return REQUIRED_BLOCKS_TOWER_GEOM, TYPECAST_TOWER_GEOM
    return REQUIRED_BLOCKS_UNIFIED_GEOMETRY, TYPECAST_UNIFIED_GEOMETRY


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and typecast §-LANG sources.")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("LANG.v1.2.0.unified_geometry.lang"),
        help="Path to the .lang source file to validate.",
    )
    args = parser.parse_args()

    src = args.source
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

    dim_ok = all(len(p.x) == 8 for p in sections)
    norm_ok = all(p.norm < 0.999 for p in sections)
    sal_ok = all(p.sal > 0 for p in sections)

    max_norm = max((p.norm for p in sections), default=0.0)
    min_margin = 0.999 - max_norm

    report = {
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

    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Validation and Typecast Report",
        "",
        "## Status",
        f"- Source: `{src}`",
        f"- Profile: `{profile}`",
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
        lines.append(f"- `{block}` → `{typecast_map[block]}`")

    lines.extend(
        [
            "",
            "## Postulate",
            "A fully sectional hyperbolic self-referential computer is admissible when section norms remain strictly interior to the Poincaré boundary and recursion is mediated by reversible transport over the bundle.",
        ]
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

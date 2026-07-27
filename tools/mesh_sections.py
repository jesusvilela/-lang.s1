#!/usr/bin/env python3
"""Project a declared §-LANG pack into a structural mesh.

Emits the section/link topology implied by a pack's §THEOREM declarations so a
mesh viewer can be driven by declared repository artifacts instead of synthetic
nodes.

Evidence scope. This is a re-encoding of text that already exists in the pack.
A section here is a *declaration* the pack contains, not a proved theorem; a
link is *adjacency in the declaration tree*, not an inference step; the emitted
coordinates are the numbers the pack states, not measurements this repository
reproduced. Projecting a pack into a mesh adds no authority to it. See PACKS.md
and CLAIMS.yaml (SLANG-MESH-001).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_typecast import PACK, PROFILES, load_manifest  # noqa: E402

# §THEOREM_D1_0b86e0:  /  §THEOREM_C1_D1:
THEOREM_RE = re.compile(r"^§THEOREM_(?:C(?P<cosmos>\d+)_)?D(?P<depth>\d+)(?:_(?P<tag>[0-9a-f]+))?\s*:(?P<rest>.*)$")
PRIME_CALL_RE = re.compile(r"P_(?P<prime>\d+)")
PRIME_BASIS_RE = re.compile(r"^§ORTHO_PRIME_BASIS:\s*(?P<prime>\d+)")
COORD_RE = re.compile(r"(?P<key>CP|BERRY|TELOS)=(?P<val>-?[0-9.]+)")
HQ_RE = re.compile(r"Mind Hamiltonian H\(Q\):\s*(?P<val>-?[0-9.eE+-]+)")
COMMIT_RE = re.compile(r"⊢\s*(?P<verdict>[A-Z_]+)")


def parse_pack(path: Path) -> list[dict]:
    """Extract one record per §THEOREM declaration, in file order."""
    sections: list[dict] = []
    current: dict | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if match := THEOREM_RE.match(line):
            rest = match.group("rest")
            prime_call = PRIME_CALL_RE.search(rest)
            verdict = COMMIT_RE.search(rest)
            current = {
                "index": len(sections),
                "id": line.split(":", 1)[0].removeprefix("§THEOREM_"),
                "cosmos": int(match.group("cosmos")) if match.group("cosmos") else None,
                "depth": int(match.group("depth")),
                "prime": int(prime_call.group("prime")) if prime_call else None,
                # Recorded verbatim. A verdict token is text the generator emitted.
                "declared_verdict": verdict.group("verdict") if verdict else None,
                "coordinates": {},
                "hamiltonian_hq": None,
            }
            sections.append(current)
            continue

        if current is None:
            continue

        for coord in COORD_RE.finditer(line):
            current["coordinates"][coord.group("key").lower()] = float(coord.group("val"))
        if match := HQ_RE.search(line):
            current["hamiltonian_hq"] = float(match.group("val"))
        if match := PRIME_BASIS_RE.match(line):
            current["prime"] = int(match.group("prime"))

    return sections


def build_links(sections: list[dict]) -> list[dict]:
    """Link each section to the previous one at the shallowest smaller depth.

    This reconstructs the declaration tree only. It asserts nothing about
    logical dependency between the linked declarations.
    """
    links: list[dict] = []
    last_at_depth: dict[tuple[int | None, int], int] = {}

    for section in sections:
        key_scope = section["cosmos"]
        depth = section["depth"]
        parent = None
        for candidate_depth in range(depth - 1, -1, -1):
            if (key_scope, candidate_depth) in last_at_depth:
                parent = last_at_depth[(key_scope, candidate_depth)]
                break
        if parent is not None:
            links.append({"source": parent, "target": section["index"], "kind": "declaration_adjacency"})
        last_at_depth[(key_scope, depth)] = section["index"]

    return links


def summarize(sections: list[dict], links: list[dict]) -> dict:
    depths = sorted({s["depth"] for s in sections})
    primes = sorted({s["prime"] for s in sections if s["prime"] is not None})
    cosmoi = sorted({s["cosmos"] for s in sections if s["cosmos"] is not None})
    verdicts: dict[str, int] = {}
    for section in sections:
        verdict = section["declared_verdict"]
        if verdict:
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
    return {
        "sections": len(sections),
        "links": len(links),
        "distinct_depths": len(depths),
        "distinct_primes": len(primes),
        "prime_range": [primes[0], primes[-1]] if primes else None,
        "cosmos_levels": len(cosmoi),
        "declared_verdicts": verdicts,
        "sections_with_coordinates": sum(1 for s in sections if s["coordinates"]),
        "sections_with_hamiltonian": sum(1 for s in sections if s["hamiltonian_hq"] is not None),
    }


def resolve_pack(target: str) -> tuple[Path, str]:
    """Only manifest-declared packs may be projected."""
    for entry in load_manifest():
        if entry["path"] == target:
            profile = entry["profile"]
            if PROFILES.get(profile, {}).get("surface") != PACK:
                raise SystemExit(f"{target} is declared as '{profile}', which is not a pack surface.")
            return Path(entry["path"]), profile
    raise SystemExit(f"{target} is not declared in validation/sources.json; refusing to project an undeclared source.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Project a declared pack into a structural mesh.")
    parser.add_argument("pack", help="Path of a pack declared in validation/sources.json")
    parser.add_argument("--out", type=Path, help="Write mesh JSON here")
    parser.add_argument("--limit", type=int, help="Emit at most this many sections")
    args = parser.parse_args()

    path, profile = resolve_pack(args.pack)
    sections = parse_pack(path)
    if args.limit:
        sections = sections[: args.limit]
    links = build_links(sections)
    summary = summarize(sections, links)

    mesh = {
        "schema_version": 1,
        "source": str(path),
        "profile": profile,
        "evidence_scope": (
            "Structural projection of declared pack text. Sections are declarations, "
            "not proved theorems. Links are declaration adjacency, not inference. "
            "Coordinates are values the pack states, not measurements reproduced here."
        ),
        "forbidden_readings": [
            "a section is a verified theorem",
            "a link is a discharged inference",
            "the coordinates are measured quantities",
            "mesh size is evidence of capability",
        ],
        "summary": summary,
        "sections": sections,
        "links": links,
    }

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(mesh, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"mesh → {args.out}")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()

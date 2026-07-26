# §-LANG Status

Last status correction: 2026-07-26.

## Current defensible claim

§-LANG is an evidence-governed symbolic research language programme with
structural validation tooling and experimental geometric research packs.

## Not currently claimed

This repository is not presently claimed to be:

- a complete executable implementation of all §-LANG constructs;
- a self-contained machine-checked proof of UTAI or the full n-Cosmos;
- an independent verification of external Lean/Bunny artifacts;
- a proof that the boot banner satisfies Löb's theorem;
- a reproducible confirmation that R142 constants are universal or substrate-stable;
- a proof of a complexity lower bound from positive defect density.

## Evidence tags

- `P`: proved or definitionally closed by an exact verified artifact.
- `A`: assumption, axiom, surrogate, conditional bridge, or externally dependent claim.
- `M`: bounded measurement with data, controls, uncertainty, and provenance.
- `H`: hypothesis, theorem target, proposed mechanism, or unverified interpretation.
- `S`: semantic, architectural, metaphorical, or design language.
- `R`: retired or demoted interpretation preserved in correction history.

These tags are not an automatic promotion ladder.

## Publication gates

| Gate | Current state | Requirement |
|---|---|---|
| Repository integrity | Improved | No merge markers, no broken canonical links, coherent identity |
| Declared grammar/source set | Implemented for structural validator | `validation/sources.json` controls the validated set |
| Non-vacuous validation | Implemented | Missing objects return `NOT_APPLICABLE`, not `PASS` |
| Claim-to-artifact ledger | Initial version | Expand every influential claim in `CLAIMS.yaml` |
| Minimal executable kernel | Open | Parser, AST, evidence checker, transport and round-trip semantics |
| Formal traceability | Open | Pinned proof source, theorem name, toolchain, clean build |
| Empirical reproducibility | Open | Raw data, scripts, seeds, uncertainty and environment |
| Independent witness | Open | Clean-room parser, external proof build, or independent reproduction |
| Citation metadata | Open | Add `CITATION.cff` once canonical title/authors/version are frozen |
| Reuse license | Open | Author must select an explicit license; all rights currently reserved |

## Stop rule

Do not use a new dialect, cosmos, mind-quality layer, or theorem surface to rescue
a failed validation or empirical interpretation. Further architectural lifts are
allowed as exploratory `S/H` work, but they must not delay or overwrite the
bounded core publication gates.

## Promotion rule

A claim may be promoted only when the exact artifact supports the exact wording,
controls and representation attacks have been addressed, uncertainty is stated
where applicable, and the evidence tag matches the artifact type.

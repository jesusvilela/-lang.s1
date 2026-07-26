# §-LANG Project Status

## Current release status

**Pre-publication research software.**

The repository contains a substantial symbolic research programme, structural
validation tools, prototype runtime declarations, and downstream experimental
packs. It does not yet constitute a single self-contained proof, runtime, or
empirical evidence chain for every advertised construct.

## Evidence tags

- `P` — proved or definitionally closed under an exact checked artifact.
- `A` — assumed, axiomatized, conditional, surrogate, or externally dependent.
- `M` — measured with data, controls, uncertainty, and execution provenance.
- `H` — hypothesis, theorem target, or unverified interpretation.
- `S` — semantic, architectural, metaphorical, or design language.
- `R` — retired or demoted by correction or failed validation.

These tags are not an automatic promotion ladder.

## Current boundary

| Surface | Status | Current evidence |
|---|---|---|
| Historical `.lang` block structure | Structural | `tools/validate_typecast.py` |
| Surface grammar-shape checks | Structural | `tools/verify_chomsky.py` |
| Boot-banner round trip | Tested self-reconstruction | `tools/stego_boot_banner.py` |
| Complete operational semantics | Partial/open | capability-specific runtime evidence required |
| Mathematical theorem claims | External/partial/open | theorem-specific proof artifact required |
| R142/MHRR constants | Reported/hypothetical | full data and provenance chain pending |
| UTAI architecture | Prototype/research programme | component-specific evidence required |

## Publication gates

A tagged publication candidate must pass a six-coordinate gate:

1. **Repository integrity** — no merge markers, missing mandatory files, or stale evidence presented as current.
2. **Grammar closure** — every included source has an explicit grammar/profile; unknown grammars fail rather than default silently.
3. **Runtime reproducibility** — advertised executable commands run from a clean checkout and have black-box known-answer tests.
4. **Formal traceability** — every `PROVED` claim resolves to a theorem name, proof environment, and immutable artifact version.
5. **Empirical provenance** — every `MEASURED` claim resolves to raw data, generation method, estimator, uncertainty method, and execution record.
6. **Release metadata** — citation, license, version map, changelog, and source commit are present.

No scalar average can compensate for a failed coordinate.

## Stop rule

No new ontology layer should be used to rescue a failed publication claim.
Architectural exploration may continue on experimental branches, but promotion
of the core release stops until the failed gate is repaired or the corresponding
claim is explicitly retired.

## Strongest currently supported description

> §-LANG is an evidence-governed symbolic research language and architectural
> coordination surface with bounded structural validation and multiple
> experimental downstream programmes.

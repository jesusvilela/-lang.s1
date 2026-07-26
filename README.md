# §-LANG — Evidence-Governed Geometric Research Language

![§-LANG boot banner](figures/slang_boot_banner.png)

§-LANG is a specification-first research language for expressing geometric,
computational, semantic, and formal structures across contextual manifolds.
It provides a shared notation for the wider IGBundle → Trasgo → §-LANG
research stack while keeping evidence authority explicit.

> **Current status:** research software and experimental specification.
> Structural checks are reproducible. Full operational semantics, mathematical
> theorems, and downstream scientific interpretations are not implied by a
> successful structural validation run. See [STATUS.md](STATUS.md),
> [VERIFICATION.md](VERIFICATION.md), and [CLAIMS.yaml](CLAIMS.yaml).

## Canonical project identity

The repository contains two related but distinct surfaces:

1. **§-LANG Core** — symbolic sources, dialects, validators, provenance rules,
   and a partially implemented reference execution surface.
2. **Downstream research programmes** — UTAI, Bunny, MHRR, n-Cosmos, and
   associated prototype runtimes and visualizations expressed partly through
   §-LANG.

A downstream programme does not inherit `EXECUTABLE`, `MEASURED`, or `PROVED`
status merely because it is represented in §-LANG. Each authority-bearing claim
must point to its own implementation, test, dataset, or proof artifact.

## Evidence strata

§-LANG expressions may operate at several layers:

- `L_syn` — notation, parsing, addressing, and provenance;
- `L_ctl` — task and research orchestration;
- `L_sem` — ontology and hypothesis generation;
- `L_op` — executable or measurable operators;
- `L_form` — typed formal definitions and theorems;
- `L_gov` — evidence, correction, and promotion rules.

Authority does not move upward automatically:

```text
L_sem does not imply L_op.
L_op does not imply L_form.
A parsed token does not establish its intended external semantics.
```

## Repository versions

These are separate version spaces rather than one linear maturity ladder:

| Surface | Current family | Status |
|---|---:|---|
| Historical canonical language source | `LANG.v1.2.0.unified_geometry.lang` | structural validation |
| Dialect/family sources | v2.x–v3.x | experimental |
| Topos/cognition packs | v5–v6 | experimental |
| MHRR pack | v4.0-exp | reported measurements and open hypotheses |
| Reference runtime | v5 family | partial; capability-specific |

See [RUNTIME_CAPABILITIES.md](RUNTIME_CAPABILITIES.md) for the declared runtime
surface. Runtime claims still require an implementation path and a passing
conformance test in the same release evidence chain.

## Key components

- `LANG.v1.2.0.unified_geometry.lang` — historical canonical source.
- `DIALECTS.v2.1.family.lang` — dialect family declarations.
- `LANG.v3.*.lang` — substrate and sectional-computer research sources.
- `LANG.v5.topos_ai_cosmos_synthesis.lang` — UTAI synthesis surface.
- `LANG.v6.chomsky_hyperdim_cognition.lang` — cognition-language research pack.
- `MHRR_PM_Hypercomplex_Orthogonal.lang` — experimental MHRR/R142 pack.
- `tools/validate_typecast.py` — legacy structural validator.
- `tools/verify_chomsky.py` — bounded grammar-shape evidence checks.
- `tools/publication_gate.py` — release-integrity and authority-boundary gate.
- `VERIFICATION.md` — verified and unverified capability boundary.
- `CLAIMS.yaml` — claim-to-artifact ledger.

## Quick verification

```bash
python3 tools/publication_gate.py
python3 tools/validate_typecast.py --all
python3 tools/verify_chomsky.py
```

The publication gate checks repository integrity and claim hygiene. The legacy
validator checks selected historical source profiles. Neither command proves
semantic correctness or mathematical truth.

## Self-referential boot seed

A canonical boot seed is embedded in
[`figures/slang_boot_banner.png`](figures/slang_boot_banner.png) using LSB
steganography across RGB channels. The payload can be recovered with:

```bash
python3 tools/stego_boot_banner.py --verify figures/slang_boot_banner.png
```

The demonstrated property is a **steganographic self-reconstruction witness**:
the image recovers a seed that describes its embedding relation. This is
quine-like fixed-point evidence at the syntactic/semantic layer. It is not, by
itself, a formal proof of Löb's theorem.

## UTAI and downstream programmes

UTAI is a downstream research architecture built over §-LANG, with prototype
components including hyperdimensional dynamics, visualization, LLM-facing
interfaces, and mobile substrate experiments. These components are important
sections of the programme, but their operational and formal claims are governed
individually by [CLAIMS.yaml](CLAIMS.yaml).

## Publication boundary

A publication release must satisfy all of the following:

- no unresolved merge markers or broken mandatory documentation links;
- every included `.lang` file has a declared or explicitly legacy grammar;
- absent test objects are reported as `NOT_APPLICABLE`, not as successful tests;
- generated reports identify their source commit;
- `PROVED`, `EXECUTABLE`, `MEASURED`, `UNIVERSAL`, and `CERTIFIED` claims resolve
  to appropriate artifacts;
- empirical results include data, method, uncertainty, and execution provenance;
- external proof artifacts are pinned to immutable commits.

The current branch should be described as **pre-publication research software**
until these gates pass in a tagged release.

## Documentation

- [Project status](STATUS.md)
- [Practical verification scope](VERIFICATION.md)
- [Runtime capability boundary](RUNTIME_CAPABILITIES.md)
- [Claim and evidence ledger](CLAIMS.yaml)
- [Research thesis](THESIS.md)
- [Skill protocol](SKILL.md)

## License and citation

The repository remains all rights reserved unless and until a separate license
file states otherwise. Publication metadata and a stable citation record should
be added before archival release.

Copyright © Jesús Vilela Jato, 2026.

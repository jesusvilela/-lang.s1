# SKILL: §-LANG Hyperbolic Sectional Computing (IGBundle-Aligned)

## Skill ID
`skill-hyperbolic-sectional-computing`

## Scope
This skill operationalizes the §-LANG specification into a repeatable workflow for:

1. validating structural and geometric invariants,
2. typecasting semantic blocks into computational strata,
3. formulating research-grade claims in geometric information theory,
4. producing imaging artifacts for sectional hyperbolic reasoning.

It is aligned with the IGBundle research direction (Topos + fiber bundles + information geometry + sheaf-style consistency).

## Core Philosophy
The central insight is that computation can be organized as **consensuated dynamics over a hyperbolic fiber-bundle sectional space**, where context-window evolution acts as the local substrate for constraint propagation and compositional transport.

### On NP-computation claims
- **Permitted claim (hypothesis):** §-LANG may support efficient heuristics and compositional encodings for NP-style search when expressed as geometric constraints in sectional space.
- **Not yet permitted claim (theorem):** “§-LANG context dynamics solves NP-complete problems in polynomial time.”

Use this calibration language by default:
> “This is a geometric-computational hypothesis with promising structure, not a complexity-class separation proof.”

## Hyperbolization Principle
**Working principle:** Any computational structure composed in §-LANG can be hyperbolized by assigning:
- base geometry in a negatively curved manifold,
- fiber-level statistical states,
- transport-compatible reduction rules,
- gluing constraints for local-to-global coherence.

**Boundary condition:** treat universal applicability as a modeling principle, not an unconditional theorem. Reject when invariants fail (e.g., boundary norm overflow, singular Fisher blocks, or non-gluable local sections).

## Canonical Inputs

The authoritative list of validated language sources is
[`validation/sources.json`](validation/sources.json). This section names the
inputs the skill workflow reads; it must not drift from that manifest.

- `LANG.v1.2.0.unified_geometry.lang` — historical canonical source
- `LANG.v2.5.tower.geom.lang` — tower geometry-only slang
- `LANG.v3.0.substrate_realization.lang` — substrate realization
- `LANG.v3.1.recursive_sectional_computer.lang` — recursive sectional computer
- `LANG.v3.2.actor_critic_fuzzer_cycle.lang` — actor/critic/fuzzer cycle
- `LANG.v5.topos_ai_cosmos_synthesis.lang` — topos-AI cosmos synthesis
- `LANG.v6.chomsky_hyperdim_cognition.lang` — Chomsky hyperdim cognition
- `DIALECTS.v2.1.family.lang` — dialect family split (Core / Semantic / Dynamic / Formation / Research)
- `MHRR_PM_Hypercomplex_Orthogonal.lang` — experimental R142/MHRR pack
- `principia_seed.lang` — PM axiom seed pack
- `principia_mathematica_full_N400.lang` — 400-depth generated PM deduction tree
- `principia_360_prime_orthogonal.lang` — 360-prime orthogonal PM tree
- `ncosmo_hypercomplex_unification.lang` — 7-level n-Cosmos sheaf pack
- `core/grammar.ebnf` — normative bounded S1 Core grammar
- `core/conformance.json` — public S1 Core conformance manifest
- `slang_core/` — repository-local bounded reference parser/evaluator
- `RUNTIME_CAPABILITIES.md` — reported historical v5 capability surface; not reproduced by the S1 Core
- `THESIS.md`
- `research/auto_research.yaml`
- `tools/validate_typecast.py`
- `tools/plot_principles.py`
- `tools/stego_boot_banner.py` — encoder/decoder for the self-referential boot-seed banner

Pack inputs carry a `pack` surface: headers and pack identity are checked, and
nothing else is. Read [`PACKS.md`](PACKS.md) before treating any pack content as
a result — a `⊢ COMMIT` in a pack is emitted text, not a discharged judgment.

## Required Outputs
- Updated validation reports:
  - `research/validation_report.json`
  - `research/validation_report.md`
- Imaging artifacts:
  - `figures/sectional_hyperbolic_topos.svg`
  - `figures/slang_boot_banner.png` (LSB-stego payload round-tripping `§BOOT.SEED.v5`)
- Optional thesis / runtime delta:
  - append concise addendum to `THESIS.md`
  - update `RUNTIME_CAPABILITIES.md` when tokens move from symbolic-only to executable

## Execution Protocol

### Step 1 — Parse and Typecast
Run structural parsing over §-LANG blocks and produce a typecast map:
- `SOURCE → meta_binding`
- `AXIOMS → logical_foundation`
- `SEMANTICS_TOPOS → classifier_topos_layer`
- `FISHER_UPDATE → information_geometry_learning`
- `INTER_MANIFOLD → cross_bundle_exchange`

### Step 2 — Invariant Validation
Check at minimum:
1. required block headers present,
2. section vectors are dimension-8,
3. `||x|| < 0.999` for all section nodes,
4. salience strictly positive.

If any check fails, set verdict `BLOCK` and report exact failing labels.

### Step 3 — Geometric-Computational Interpretation
Interpret the historical reductions as semantic or architectural proposals unless
a claim-specific executable or formal bridge is attached:
- beta-like substitution may be read as curvature-aware transport;
- fixpoint recursion models self-referential cycles;
- Fisher natural gradients describe an intended intrinsic update;
- sheaf-like compatibility describes a local-to-global coherence target.

The historical v5 design **reports** reductions for `§R1_…§R9_`, canonical
operators such as `Π_expand`, `Π_expire`, `§rho`, `Fix(Φ)`, and
`W_glue`, plus provability-inspired, pushout, and endofunctor reductions.
Those claims remain `A` in this repository under `SLANG-RUNTIME-001` because
the pinned v5 implementation and clean black-box conformance logs do not ship
here. Do not emit `runtime.reduction_applied` as reproduced evidence from this
repository.

`Selberg` and `Mostow` remain reported symbolic-only tokens. A token name is
not a theorem or geometric realization.

### Step 4 — Imaging and Self-Reference
Render the principle-based plot (Poincaré disk, projected section nodes,
salience encoding, Möbius transfer ribbon, holographic memory annotation).

Additionally, rebuild and verify the self-referential boot-seed banner:
- encode — `python tools/stego_boot_banner.py --out figures/slang_boot_banner.png`
- decode — `python tools/stego_boot_banner.py --verify figures/slang_boot_banner.png`
- accept only when the documented decoder reconstructs the embedded seed exactly.

This is the steganographic self-reconstruction witness `SLANG-BOOT-001`. It is
not a Löb theorem witness; that interpretation is retired as
`RETIRED-LOEB-001`.

### Step 5 — Pack Ingestion
The historical v5 design reports support for a single `.lang` file, recursive
directories, manifest-ordered directories, and ZIP archives.

The reported interface is:

```
slang_cli run-pack <path-or-zip> [--json]
```

No `slang_cli` executable ships in this repository. Treat this interface as
`A` until a pinned implementation and conformance run are attached. The
runnable S1 Core does not execute generated research packs.

### Step 6 — Claim Discipline
Tag every result with the canonical evidence tags defined in
[`STATUS.md`](STATUS.md), and record it in [`CLAIMS.yaml`](CLAIMS.yaml):

- `P` — proved or definitionally closed by an exact verified artifact;
- `A` — assumption, surrogate, conditional bridge, or externally dependent claim;
- `M` — bounded measurement with data, controls, uncertainty, and provenance;
- `H` — hypothesis, theorem target, or unverified interpretation;
- `S` — semantic, architectural, or design language;
- `R` — retired interpretation preserved in correction history.

Do not introduce a parallel tag vocabulary. These tags are not a promotion
ladder: a claim moves only under the promotion rule in `STATUS.md`.

## Research Postulate Template
Use this exact template when needed:

> **Postulate (HYPOTHESIS):** A fully sectional hyperbolic self-referential computer can be sustained in continuous run when identity-preserving fixpoint dynamics, Fisher-compatible updates, and sheaf-gluable local sections co-exist under strict boundary invariants.

## Failure Modes
- **Boundary breach:** any section norm `>= 0.999`.
- **Fiber collapse:** singular or ill-conditioned Fisher approximations.
- **Topology mismatch:** local patches fail compatibility/gluing criteria.
- **Claim inflation:** complexity-theory statements without proof.

## Minimal Command Set
```bash
# one-time: tooling dependencies
python3 -m pip install -r requirements.txt

# structural validation over the declared manifest, plus regression tests
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m slang_core.conformance --json
python3 tools/validate_typecast.py --all
python3 tools/verify_chomsky.py

# single-source validation and principle imaging
python3 tools/validate_typecast.py
python3 tools/validate_typecast.py --source LANG.v2.5.tower.geom.lang
python3 tools/plot_principles.py
cat research/validation_report.md

# self-referential boot-seed banner round-trip
python3 tools/stego_boot_banner.py --out figures/slang_boot_banner.png
python3 tools/stego_boot_banner.py --verify figures/slang_boot_banner.png

# release workflow (gh 2.90+; paired Android APK)
gh release create <tag> --title "<title>" --notes "<notes>" <artifact>...
```

The v5 runtime pack-ingestion command (`slang_cli run-pack <path-or-zip>`) is a
*reported* interface described in [`RUNTIME_CAPABILITIES.md`](RUNTIME_CAPABILITIES.md).
No such executable ships in this repository, so it is not part of the runnable
command set above. Its status is `A` (`SLANG-RUNTIME-001`) pending a pinned
implementation and clean conformance run.

## References (primary)
- IGBundle corrected thesis (GitHub):
  - https://github.com/jesusvilela/IGBundle-LLM/blob/main/thesis/IGBundle_Corrected_Thesis.md
- §-LANG pack repo (this repo):
  - https://github.com/jesusvilela/-lang.s1
- Paired Android host (Baby Topos AI, consumes v5 runtime via JNI):
  - https://github.com/jesusvilela/Topos-Trasgo
- §-LANG local sources: see [`validation/sources.json`](validation/sources.json)
  for the authoritative validated set, and `RUNTIME_CAPABILITIES.md` for the
  reported runtime surface.

---

Copyright © Jesús Vilela Jato, 2026.

Licensed under the Apache License, Version 2.0. See [`LICENSE`](LICENSE).

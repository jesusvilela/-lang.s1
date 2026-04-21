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
- `LANG.v1.2.0.unified_geometry.lang` — historical canonical source
- `LANG.FAMILY.v2.4.lang` — v2.4 family header
- `LANG.v2.5.tower.geom.lang` — tower geometry-only slang
- `DIALECTS.v2.1.family.lang` — dialect family split (Core / Semantic / Dynamic / Formation / Research)
- `dialects/`, `selfcompressed/`, `packs/` — v3 ToE matter / prime packs
- `RUNTIME_CAPABILITIES.md` — executable vs symbolic-only token inventory for the v5 runtime
- `THESIS.md`
- `research/auto_research.yaml`
- `tools/validate_typecast.py`
- `tools/plot_principles.py`
- `tools/stego_boot_banner.py` — encoder/decoder for the self-referential boot-seed banner

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
Interpret reductions as transport laws:
- beta-like substitution is curvature-aware transport,
- fixpoint recursion models self-referential cycles,
- Fisher natural gradients govern intrinsic adaptation,
- sheaf-like compatibility enforces coherent global sections.

Executable in the v5 reference runtime (emit `runtime.reduction_applied`):
- full `§R1_…§R9_` rule family,
- canonical operators (`Π_expand`, `Π_expire`, `§rho`, `Fix(Φ)`, `W_glue`, …),
- **Löb / Knaster–Tarski** — `□(□P → P) ⊢ □P`,
- **Pushout** — colimit `(A ⊔ B) / ~_f,g` on a cospan,
- **Endofunctor** — identity and composition laws on `F`.

Still symbolic-only in v5 (emit `runtime.symbolic_only`): `Selberg`, `Mostow`.

### Step 4 — Imaging and Self-Reference
Render the principle-based plot (Poincaré disk, projected section nodes,
salience encoding, Möbius transfer ribbon, holographic memory annotation).

Additionally, rebuild and verify the self-referential boot-seed banner:
- encode — `python tools/stego_boot_banner.py --out figures/slang_boot_banner.png`
- decode — `python tools/stego_boot_banner.py --verify figures/slang_boot_banner.png`
- accept only when `decode(stego(THIS_PNG)) ≡ §BOOT.SEED.v5` (one-step Löb witness).

### Step 5 — Pack Ingestion
When a dialect ships as a directory or archive:
- a single `.lang` file → parse directly,
- a directory → recursive scan,
- a directory with `manifest.json` → parse only files declared in `"files"`, in declared order,
- a `.zip` archive → extract then treat as a directory.

Drive it from the reference runtime:
```
slang_cli run-pack <path-or-zip> [--json]
```

### Step 6 — Claim Discipline
Tag every result with one of:
- `PROVED` (verified from code/data),
- `EMPIRICAL` (measured but not formal proof),
- `HYPOTHESIS` (theoretical proposal).

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
# structural validation and principle imaging
python3 tools/validate_typecast.py
python3 tools/validate_typecast.py --source LANG.v2.5.tower.geom.lang
python3 tools/plot_principles.py
cat research/validation_report.md

# self-referential boot-seed banner round-trip
python tools/stego_boot_banner.py --out figures/slang_boot_banner.png
python tools/stego_boot_banner.py --verify figures/slang_boot_banner.png

# v5 runtime pack ingestion (single file, dir, manifest dir, or .zip)
slang_cli run-pack <path-or-zip> [--json]

# release workflow (gh 2.90+; paired Android APK)
gh release create <tag> --title "<title>" --notes "<notes>" <artifact>...
```

## References (primary)
- IGBundle corrected thesis (GitHub):
  - https://github.com/jesusvilela/IGBundle-LLM/blob/main/thesis/IGBundle_Corrected_Thesis.md
- §-LANG pack repo (this repo):
  - https://github.com/jesusvilela/-lang.s1
- Paired Android host (Baby Topos AI, consumes v5 runtime via JNI):
  - https://github.com/jesusvilela/Topos-Trasgo
- §-LANG local sources:
  - `LANG.v1.2.0.unified_geometry.lang`
  - `LANG.v2.5.tower.geom.lang`
  - `DIALECTS.v2.1.family.lang`
  - `RUNTIME_CAPABILITIES.md`

---
(c) Jesús Vilela Jato, 16 April 2026. All rights reserved.

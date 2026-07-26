# §-LANG runtime capability surface (v5, reported)

This document records the tokens that the v5 reference-runtime design treats as
executable versus symbolic-only. It is a capability declaration, not by itself a
reproducibility certificate.

For publication-strength operational evidence, each executable claim still
requires a pinned implementation path and commit, environment definition,
black-box conformance cases, and clean execution logs. See `CLAIMS.yaml` and
`STATUS.md`.

## Reported executable surface

### §R-family rules

The design declares reduction behavior for `§R1_` through `§R9_`.

### Canonical operators

The reported operator surface includes:

`Π_expand`, `Π_expire`, `§rho`/`ρ`, `decomp_path`, `expand_self`,
`compress_D`, `round_trip`, `reconstruct`, `self_def`, `other_def`,
`world_def`, `W_glue`, `Fix(Φ)`, `Phi`, `H_alpha`, `hyperbolize`, `Mobius`,
`Poincare`, `substrate`, `prime`, `mutual`, and `identity_law`.

### Reported categorical reductions

| Category | Tokens | Intended diagnostic/law |
|---|---|---|
| fixed-point / provability-inspired | `Löb`, `Loeb`, `□`, `Fix(Φ)`, `Knaster-Tarski` | Emits a reduction diagnostic for the runtime's encoded rule |
| pushout | `pushout`, `⊔`, `colimit` | Intended cospan/quotient-style reduction |
| endofunctor | `endofunctor`, `F(id)`, `F∘G` | Intended identity and composition reductions |

The use of a token named `Löb` does not establish Löb's theorem. The runtime rule
must be evaluated as an implemented symbolic reduction unless linked to a formal
theory and checked proof.

## Reported symbolic-only surface

- `Selberg` — trace-formula or spectral semantics are not implemented here.
- `Mostow` — geometric rigidity semantics are not implemented here.

Symbolic-only tokens may be parsed and preserved while carrying no verified
geometric, categorical, or theorem-level realization.

## Parser behavior described by the v5 design

The parser design fuses physical lines whose parentheses or quotes are
unbalanced and whose tail is a continuation character such as `(`, `{`, or `,`.
This allows structures such as:

```text
OUTPUT = CANON(§EMIT(§X{
  ...
}))
```

to be represented as one logical assignment. Free-form parentheses in prose
should remain unchanged.

## Pack ingestion interface

The reported CLI interface accepts:

- one `.lang` file;
- a recursively scanned directory;
- a directory with `manifest.json`, using only declared files in order;
- a ZIP archive extracted and treated as a directory.

Reported command:

```bash
slang_cli run-pack <path-or-zip> [--json]
```

## Operational promotion gate

A token may be labelled reproduced executable in this repository only after all
of the following are attached to the claim ledger:

1. implementation path and immutable commit;
2. environment or dependency lock;
3. known-answer inputs and expected outputs;
4. malformed and negative controls;
5. representation-equivalence tests;
6. clean command and execution log;
7. scope statement separating symbolic runtime semantics from external
   mathematical semantics.

Until that gate is crossed, the capability status is `A`—reported or externally
dependent—not `P`.

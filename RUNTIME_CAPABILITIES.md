# §-LANG runtime capabilities (v5)

Which tokens in `.lang` / `.dialect.lang` / `.SelfCompressed.lang` files the
reference runtime treats as *executable* (carry reduction semantics) vs
*symbolic-only* (parsed and preserved, but have no geometric/categorical
realisation yet).

Pack authors can use this list to gauge how much of a new dialect the
runtime will actually evaluate versus just surface as metadata.

## Executable in v5

**§R-family rules** — full `§R1_` through `§R9_`.

**Canonical operators** — `Π_expand`, `Π_expire`, `§rho`/`ρ`, `decomp_path`,
`expand_self`, `compress_D`, `round_trip`, `reconstruct`, `self_def`,
`other_def`, `world_def`, `W_glue`, `Fix(Φ)`, `Phi`, `H_alpha`, `hyperbolize`,
`Mobius`, `Poincare`, `substrate`, `prime`, `mutual`, `identity_law`.

**New in v5 — categorical reductions** (emit
`runtime.reduction_applied` info diagnostics):

| Category   | Tokens                                         | Law applied |
|------------|------------------------------------------------|-------------|
| loeb       | `Löb`, `Loeb`, `□`, `Fix(Φ)`, `Knaster-Tarski` | Löb discharge `□(□P→P) ⊢ □P` / lfp–gfp witness |
| pushout    | `pushout`, `⊔`, `colimit`                      | Colimit `(A ⊔ B)/~_f,g` on a cospan |
| endofunctor| `endofunctor`, `F(id)`, `F∘G`                  | Identity + composition laws on endofunctors |

## Still symbolic-only in v5

- `Selberg` — trace-formula / spectral side not yet wired.
- `Mostow` — rigidity not yet realised geometrically.

These still parse and validate; the runtime records
`runtime.symbolic_only` diagnostics for each occurrence.

## Parser

The v5 parser fuses physical lines whose parentheses or quotes are
unbalanced and whose tail is a continuation character (`(`, `{`, `,`).
This lets patterns like

```
OUTPUT = CANON(§EMIT(§X{
  ...
}))
```

parse as a single logical assignment. Lines that merely contain
free-form parens in natural-language text (e.g. `q ∈ (0,2]`) are left
alone.

## Pack ingestion

The CLI now accepts:

- a single `.lang` file,
- a directory (recursive scan),
- a directory containing `manifest.json` (only the files declared in
  `"files"` are parsed, in the declared order),
- a `.zip` archive (extracted, then treated as a directory).

Command:

```
slang_cli run-pack <path-or-zip> [--json]
```

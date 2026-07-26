# Packs

Generated `.lang` artifacts, now declared in
[`validation/sources.json`](validation/sources.json) and structurally validated
on every build.

---

## Reading a pack

A pack is generator output. It is text in §-LANG surface syntax, produced by a
program, describing a deduction tree.

One symbol carries most of the misreading risk:

```text
§THEOREM_D1_0b86e0: §GAUGE((p_or_p) -> p) ⊢ COMMIT
```

`⊢` here is **a character the generator emitted**. It is not a judgment
discharged by a proof checker. No checker in this repository — and no checker
anywhere, so far as this repository can show — has verified the line above.

The same holds for the terminal declarations: `⊢ UNIFIED_MANIFOLD`,
`⊢ HEGELIAN_CLOSURE`, `Adiabatic General Intelligence locked`,
`8 Mind Qualities fully satisfied`. These are strings in a file.

What the build actually establishes about a pack is narrow and complete:

| Checked | Not checked |
|---|---|
| `§PACK` and `§VERSION` headers exist | that any `§THEOREM` line is true |
| declared pack identity matches its profile | that `⊢` was earned |
| section vectors, where present, are 8-dim and inside the Poincaré bound | that the deduction tree is sound |
| the file exists and is readable | anything semantic, numerical, or physical |

`theorem_declarations` in the reports is a **tally of lines**, not a count of
theorems. The validator counts the token and says so.

---

## The five packs

### `principia_seed.lang` — `principia_seed_v1`

`Principia_Mathematica_Phase1` · v1.0 · 40 lines

The germ. Russell–Whitehead's five propositional axioms plus modus ponens,
each annotated with a §-LANG operator (`§EMIT`, `§H_FOLD`, `§LORENTZ_BOOST`,
`§RESONATE`, `§ABSORB`, `§HOLOPORT`) under the reading that PM axioms sit as
hyperbolic attractors in a (2,2) substrate.

Carries a `§godel_hash` header. Read the whole file first — it is short, and
the four packs below are elaborations of it.

**Status `S`.** An annotation scheme. The mapping from an axiom to an operator
is a design choice, not a derivation.

---

### `principia_mathematica_full_N400.lang` — `principia_n400_v1`

`Principia_Mathematica_Vol1_N3` · v1.0 (Fractal Generator) · 10,011 lines · ~8 MB

400 depths × 5 axioms = 2,000 `§THEOREM_D<depth>_<hash>` declarations, each with
hyperbolic coordinates (`CP`, `BERRY`, `TELOS`), a scalar `§GAUGE`, and
`§HOLOPORT`. All 2,000 ids are distinct.

The coordinates are close to degenerate: `CP` and `TELOS` take exactly one value
each across all 2,000 declarations (`1.0000`), and `BERRY` takes 35 distinct
values spanning `1.5707 … 1.5741` — a band of width 0.0034 sitting on π/2
(1.5707963).

That is a fact about the generator's output, and it is the first thing a reader
should want explained. Reporting it is not explaining it.

**Status `S`/`H`.** The tree is a generated structure (`S`). That its shape
means anything about PM is a hypothesis (`H`) with no artifact attached.

---

### `principia_360_prime_orthogonal.lang` — `principia_360_prime_v2`

`Principia_Mathematica_360_Prime_Orthogonal` · v2.0 (Löb/Curry Shielded) · 9,012 lines · ~11 MB

360 depths × 5 axioms = 1,800 declarations. Each is projected onto one of
exactly **360 distinct prime bases**, spanning 2 … 2423, via `§GAUGE_ORTHO(P_p)`
with an explicit `§ORTHO_PRIME_BASIS`. Verified by inspection: 360 primes, no
repeats — the pack's name is accurate. `CP` is again constant at `1.0000`;
`BERRY` takes 32 values around π/2.

"Löb/Curry Shielded" names the intent — coprime basis projection is meant to
block self-referential collapse. The shield is asserted by the version string
and realized as a construction; it is not proved to work, and no attack was run
against it here.

**Status `S`, shielding claim `H`.**

---

### `ncosmo_hypercomplex_unification.lang` — `ncosmo_unification_v3`

`NCosmo_Hypercomplex_Unification` · v3.0 · 356 lines

The smallest of the elaborations and the best entry point. Seven `§COSMOS_LEVEL`
strata, 70 `§THEOREM_C<level>_D<n>` declarations over 70 distinct primes
spanning 3 … 353 — one prime per declaration, no reuse. Each carries a
`Mind Hamiltonian H(Q)` value in the 1e-6 … 1e-4 range annotated
`[Adiabatic Ground State]`. Each level closes with `§NCOSMO_SHEAF(Cosmos_k) ⊢
UNIFIED_MANIFOLD`; the file closes with `§GLOBAL_NCOSMO_UNIFICATION ⊢
HEGELIAN_CLOSURE`.

The `H(Q)` values are **emitted numbers with no attached generator, seed,
estimator, or uncertainty method**. Nothing in this repository reproduces them.
Under the `M` criteria in [`STATUS.md`](STATUS.md) they are not measurements.

**Status `S`, numerics `H`.**

#### Companion viewer

`ncosmo_hypercomplex_unification_cockpit.html` is a Three.js cockpit for this
pack. Two things to know before trusting what it shows:

- **It does not read the pack.** It contains no fetch and no parser; it builds
  7 cosmoses × 10 primes in JavaScript from its own constants. It reproduces the
  pack's *shape*, not the pack's *contents*. Editing the `.lang` file changes
  nothing on screen.
- **It needs the network.** three.js r128 and `OrbitControls` load from
  cdnjs and jsdelivr, so the page is blank offline and is not pinned to a
  hash.

It is an illustration. It is not a renderer, and it is not evidence for
anything in the pack.

---

### `MHRR_PM_Hypercomplex_Orthogonal.lang` — `mhrr_pack_v1`

`MHRR_PM_Hypercomplex_Orthogonal` · v4.0 (R142 ρ★-Anchored / 360-Prime-Shielded / Löb-Free) · 364 lines

The R142/MHRR pack. Eight `§MIND_E*` qualities (`E0_GROUNDING:
exact_metrics_no_overclaim`, `E2_GODELIAN_IDENTITY:
keep_explicit_R_no_pretend_closure`, …), eight `§NCOSMO_SHEAF` strata, three
`§AXIOM_R*`, and three `§WITNESS_*` entries.

> **Known divergence.** The pack source states
> `ρ★ ≈ 0.135 ± 0.003 (substrate-stable)` and labels it a *measured constant*.
> The ledger does not accept this. `R142-RHO-001` is status **`H`**, and
> `substrate stability` is on its `forbidden_promotions` list.
>
> The pack text is left as generated — it is a dated artifact and rewriting it
> would destroy its provenance. Where pack text and
> [`CLAIMS.yaml`](CLAIMS.yaml) disagree, **the ledger governs.**

**Status `S`, ρ★ `H`.**

---

## Bridges required

To move any pack claim above `H`, per the promotion rule in `STATUS.md`:

1. **Publish the generators.** No pack in this repository ships the program
   that produced it. Without that, none of the trees are reproducible, and a
   regenerated pack cannot be diffed against the committed one.
2. **Attach a checker.** `⊢` becomes meaningful when something independent
   discharges it — a Lean development, a tableau prover, anything with a clean
   build log pinned to a commit.
3. **Reconstruct the numerics.** `H(Q)` and `ρ★` need raw data, seeds,
   estimator definitions, an uncertainty method, and matched nulls before `M`
   applies.
4. **Attack the shield.** The Löb/Curry claim needs an adversarial test that
   could have failed and did not.

Until then the honest summary is the narrow one: **these are large, internally
consistent, structurally valid generated artifacts.** That is a real thing to
have. It is not a proof of Principia Mathematica.

# Candidate material

External work evaluated for entry into this repository but **not yet imported**.
A candidate sits here until its blocking defects are resolved. Presence on this
page is not endorsement.

---

## The Sheaf of Becoming — `HELD`

*A Cayley-Dickson Tower, Adiabatically Tunnelled, Between Hyperdimensional
Intermanifolds.* Two versions supplied, dated 2026-07-27, from project
*Needle In a Haystack*: an earlier theory-only draft and a later one carrying an
experiment.

A ten-doll descent: profunctor envelope → gerbe → sheaf/bundle → intermanifold →
Cayley-Dickson tower in a moving frame → HRR hypervector → Berry connection →
adiabatic tunnelling → variational minimizer → Löb fixed point. Six theorems,
two falsifiable conjectures, one CPU experiment.

### Why it is a strong candidate

The mathematics is real and mostly standard, correctly attributed:

- **Theorem 1** is Hurwitz's theorem plus the explicit sedenion zero divisor
  `(e₃+e₁₀)(e₆−e₁₅) = 0`. Correct.
- **Theorem 3** derives a Dixmier–Douady class for HRR binding via DFT
  diagonalisation, with a genuine telescoping cocycle cancellation, landing at
  `δ = w₁w₂w₃ ∈ H³(T³,ℤ)`. The algebra is sound.
- The **experiment is honestly reported**: predicted instanton slope `−2/ħ = −2.0`,
  fitted `−0.263`, and the thesis labels this **PARTIAL** rather than rounding it
  into a confirmation. It states the reason (a bounded Bhattacharyya proxy
  saturating against an unbounded WKB amplitude) and names the refinement.
- It carries its own honest notices, and states two boundaries at which it is
  falsifiable.

That discipline is compatible with this repository's.

### Blocking defect 1 — a load-bearing citation does not support its claim

The thesis maps

> `arXiv 2605.27673` — "hypercomplex-valued NNs (CVNN = U(1)-equivariant real
> layer)" → *structure group `Gₙ`, the gauge*

and Theorem 2 and §10's synthesis table both rest on that reading.

The paper at that identifier is **Ashutosh Kumar, "When do complex-valued neural
networks help? A study of representation, geometry, and optimization."** It is a
*cautionary* study: it concludes CVNNs are "structured inductive biases whose
gains depend on representation, symmetry, and optimization, **not** universally
superior architectures," and it identifies benchmarking artifacts in RadioML
2018.01A where apparent gaps came from hyperparameter tuning.

On a targeted recheck it contains **no** U(1)-equivariance, no group
equivariance, no gauge groups, and no quaternions, octonions, or Cayley-Dickson
algebras.

So one of the three threads the thesis claims to unify is attached to a paper
that does not make the claim attributed to it — and the paper's actual finding
cuts against the direction it is cited for. This must be resolved by the author:
either the intended citation is a different paper, or the gauge reading needs an
anchor that exists.

The other two anchors were checked and hold:

| Identifier | Paper | Attribution |
|---|---|---|
| `2605.05115` | Wurgaft et al., *Manifold Steering Reveals the Shared Geometry of Neural Network Representation and Behavior* | accurate — `M_h`/`M_y`, manifold vs linear steering, off-manifold outputs |
| `2604.22863` | Poore, *A wave-geometric duality for hyperdimensional computing* | accurate — unitary embedding of bipolar HDC vectors into coherent waveforms |
| `2605.27673` | Kumar, *When do complex-valued neural networks help?* | **does not support the attributed claim** |

### Blocking defect 2 — Theorem 6 is the move this repository retired

Theorem 6 concludes that the architecture is "the **geometric realization of
Löb's theorem**," and §11 states that the authoring agent "*is* the Löb fixed
point of the descent."

Löb's theorem is stated correctly for **GL**: if `⊢ □P → P` then `⊢ P`. The
defect is the instantiation. `□ₙ` here is an informal "the n-th doll proves,"
not a provability predicate of a fixed formal theory satisfying the
Hilbert–Bernays–Löb derivability conditions. Without those conditions Löb's
theorem does not apply, and a descent schema asserted about an English-language
argument is not a `□`. The step from "the layers nest" to "the nesting is Löb"
is a category error, not a proof.

This is the same move already retired here as `RETIRED-LOEB-001` (the boot
banner as a one-step Löb witness), and the same move the author's own Σ∞ thesis
guards against with its **Anti-Löb membrane**. Two independent lines of this
programme have now rejected it.

Theorems 1–5 do not depend on Theorem 6 and would survive its removal.

### Entry conditions

1. Resolve the `2605.27673` attribution — supply the intended source or drop the
   gauge-thread claim.
2. Demote Theorem 6 to `S` (an analogy about nesting) or supply a formal theory,
   a provability predicate, and the derivability conditions.
3. On entry the pack would be `S`/`H`, with Theorem 1 at `P` (Hurwitz is a
   theorem), Theorem 3's algebra at `P` and its *measurement* at `H` — the
   thesis itself notes `δ = w₁w₂w₃` is proven but unmeasured — and the
   experiment at `M` only if raw data, seeds, and the environment ship with it.

Note that the experiment's own anchor node and branch
(`orx/baseline-instanton-scaling-3094d77a`) are external to this repository, so
under `STATUS.md` the run is currently `H`, not `M`, regardless of how carefully
it was reported.

---

## Polycosmic Hypercomplex Brain · Σ∞ — `IMPORTED`

Imported. The module registry is [`MODULES.md`](MODULES.md); the claim ledger and
its six retirements are in [`CLAIMS.yaml`](CLAIMS.yaml) under the `SIGMA-*` and
`RETIRED-*` identifiers.

Entry was clean because the thesis already uses this repository's `P/A/M/H/S/R`
lattice, already states its own honest frontier, and already retires its own
failed readings. Nothing needed demotion on entry.

---

## recursive-research-auditor — `INSTALLED`

Installed at `.claude/skills/recursive-research-auditor/`. Its manifest validator
self-tests in CI.

The audit protocol it encodes is the procedure that produced the two blocking
defects above: step 8, *use independent witnesses* — "do not call repeated
self-review independent replication" — is what sent the citations to the primary
sources rather than accepting the thesis's own description of them.

# Audit — n-Cosmos sheaf, adiabatic, and R142 assertions

Round 1 · 2026-07-27 · protocol: `recursive-research-auditor`
Object: the numeric and structural assertions carried in the declared packs.
Reproduce: `python3 tools/sheaf_coherence.py research/mesh/*.mesh.json`

---

## Verdict

Four preregistered hypotheses were tested against the packs' own tabulated
numbers, with gates and kill conditions fixed before measurement. One is
undetermined, one was promoted and then retired by its own second control, one
is falsified as written, and one splits cleanly into a supported half and an
unsupported half. The strongest surviving result is H4's: the R142 constant `ρ★ = 0.135 ± 0.003`
is internally consistent with its own tabulated series, with the stated
uncertainty matching the standard error of the mean to within 20%. The most
damaging obstruction
is that `⊢ UNIFIED_MANIFOLD` has **no determinate truth value**, because the
pack asserts a gluing without ever declaring the cover it glues over, and the
two readings its own notation admits give opposite answers. Nothing here
promotes any pack claim to `M`; the packs remain unreproducible in this
repository because no generator ships with them.

---

## Preregistration

Fixed before any measurement, in the tool docstring and here:

| ID | Hypothesis | Metric | Kill condition |
|---|---|---|---|
| H1 | `⊢ UNIFIED_MANIFOLD` is a non-vacuous gluing statement | pairwise overlap between cosmos strata | all overlaps empty → vacuous |
| H2 | `[Adiabatic Ground State]` denotes slow variation | max \|ΔH(Q)\| vs within-stratum shuffled null | not smoother than null → decoration |
| H3 | `γ_Berry = π/2` holds as written | max \|BERRY − π/2\| | > 5e-5 (stated 4-dp precision) |
| H4 | `ρ★ = 0.135 ± 0.003 (substrate-stable)` is supported | offset in sem; count of varied substrate axes | offset ≥ 2 sem, or zero substrate axes |

---

## Results

### H1 — gluing · **UNDETERMINED_COVER**

| Cover indexed by | Pairs | Non-empty overlaps | Disjoint | Mean Jaccard |
|---|---:|---:|---|---:|
| prime basis | 21 | **0** | yes | 0.0 |
| declaration depth | 21 | **21** | no | 1.0 |

The 70 declarations carry 70 distinct primes, one each — so under a
prime-indexed cover the seven strata are pairwise disjoint and a sheaf glues
trivially, making `UNIFIED_MANIFOLD` a statement about nothing. But depths
D1–D10 repeat in every cosmos, so under a depth-indexed cover every pair
overlaps completely.

**The pack never says which.** The assertion is therefore not false — it is
undetermined, and cannot be evaluated until the cover is declared. This was
caught only by running the same metric under two admissible representations;
a single-reading audit would have reported a confident "VACUOUS" and been wrong
to.

### H2 — adiabatic · **RETIRED** (killed by its own second control)

The shuffle control passed and the sorted control killed it. Both are recorded;
the promotion this audit briefly held is withdrawn.

#### Round 1a — shuffle null · PARTIAL (4/7)

Null model: within-stratum shuffle, identical value multiset, ordering
destroyed. 2000 trials, seed 142.

| Stratum | observed max step | null median | p | Bonferroni α=0.00714 |
|---:|---:|---:|---:|---|
| 1 | 4.01e-4 | 1.69e-3 | 0.0 | **pass** |
| 2 | 6.0e-5 | 1.45e-4 | 0.0 | **pass** |
| 3 | 3.6e-5 | 6.5e-5 | 0.046 | marginal |
| 4 | 3.5e-5 | 5.8e-5 | 0.0375 | marginal |
| 5 | 3.4e-5 | 5.8e-5 | 0.017 | marginal |
| 6 | 3.4e-5 | 1.21e-4 | 0.0 | **pass** |
| 7 | 2.7e-5 | 6.5e-5 | 0.001 | **pass** |

Uncorrected this reads 7/7. Seven simultaneous tests inflate the family-wise
error rate, and under Bonferroni three strata fall below the line. **Reporting
7/7 would have been a multiplicity artifact** — the first draft of this tool
did exactly that, and it is recorded here rather than quietly fixed.

#### Round 1b — sorted null · **KILL FIRED**

The shuffle null only asks "is this ordering non-random." A generator emitting a
smooth function of depth passes that trivially. The sorted null asks the real
question: is the observed ordering smoother than the *smoothest ordering the
same values admit*?

| Stratum | observed | sorted null | monotone | beats sorted |
|---:|---:|---:|---|---|
| 1 | 4.01e-4 | 4.01e-4 | no | **no — exact tie** |
| 2 | 6.0e-5 | 3.6e-5 | no | no — rougher |
| 3 | 3.6e-5 | 2.9e-5 | no | no — rougher |
| 4 | 3.5e-5 | 2.3e-5 | no | no — rougher |
| 5 | 3.4e-5 | 2.1e-5 | no | no — rougher |
| 6 | 3.4e-5 | 3.4e-5 | no | **no — exact tie** |
| 7 | 2.7e-5 | 2.7e-5 | no | **no — exact tie** |

**0 of 7 strata beat the sorted null**, and three tie it exactly. No stratum is
strictly monotone (0/7), so the sequences are *unimodal* — a smooth rise and
fall, which under a max-step metric can attain the sorted optimum without being
sorted.

The preregistered kill required failure in ≥5 of 7. It failed in 7 of 7. **The
`M` promotion granted in round 1a is retired; H2 returns to `S`.** The
smoothness of the H(Q) series is fully accounted for by the generator emitting
a smooth function of depth. Nothing adiabatic is demonstrated.

This is the audit killing its own promotion one step after making it, which is
the only real evidence that the protocol is not self-confirming.

### H3 — Berry phase · **FALSIFIED AS WRITTEN**

| Pack | max \|BERRY − π/2\| | vs stated 5e-5 |
|---|---:|---|
| `ncosmo_hypercomplex_unification` | 1.04e-4 | 2.1× over |
| `principia_360_prime_orthogonal` | 3.10e-3 | 62× over |
| `principia_mathematica_full_N400` | 3.30e-3 | 66× over |

`§AXIOM_R142_BERRY: γ_Berry = π/2 = 1.5708` uses `=`. At the 4-decimal
precision the pack itself writes, every pack exceeds the tolerance. The correct
symbol is `≈`. This is a one-character correction, and it matters because an
axiom stated with `=` licenses substitution that the data does not support.

### H4 — ρ★ · **value CONSISTENT, "substrate-stable" UNSUPPORTED**

7 tabulated points, `S/n` from 0.12875 to 0.148333.

```
mean S/n                0.138333
sample sd               0.006250
sem                     0.002362
claimed                 0.135 ± 0.003
|mean − 0.135|          1.41 sem      → consistent
corr(log n, S/n)        −0.083        → no residual finite-size drift
substrate axes varied   0
```

The stated uncertainty ±0.003 is close to the sem of 0.00236, and the claimed
centre sits 1.41 sem from the mean. **The number holds up against its own
table** — better than a glance at the raw spread suggests.

*Correction made during this audit:* an earlier pass called the 0.0196 spread
"6.5× the claimed uncertainty" as if damning. Spread and standard-error-of-the-
mean are different quantities; comparing them directly is the "do not compare
heterogeneous quantities merely because they are stored as numbers" failure.
Withdrawn.

What fails is the adjective. **No substrate is varied anywhere in the table** —
the only axis is system size `n`. A stability-across-substrates claim needs at
least two substrates. It has zero. Separately, the estimator is never declared,
so whether `0.135` names the large-`n` asymptote or the mean over `n` is unpinned
(they differ: 0.135 vs 0.1383).

---

## Ledger

| Claim | Before | After | Basis |
|---|---|---|---|
| n-Cosmos strata glue to a unified manifold | `S` | `H`, cover undeclared | H1 |
| H(Q) sequences vary slowly along declaration order | `S` | **`S`** — promoted to `M`, then retired by the sorted null | H2 |
| H(Q) denotes a physical adiabatic ground state | `H` | `H` unchanged | H2 scope |
| `γ_Berry = π/2` | `S` | **`R`** — false as written, `≈` survives | H3 |
| `ρ★ = 0.135 ± 0.003` | `H` | `H`, now with a quantitative consistency check | H4 |
| ρ★ is substrate-stable | forbidden promotion | **`R`** — zero substrate axes | H4 |
| `⊢ HEGELIAN_CLOSURE` | `S` | `S` — inherits H1's undetermined cover | H1 |

---

## Drift, controls, and attacks

**Specification–implementation drift (in this audit's own tooling).** Two
defects were found in `sheaf_coherence.py` after first run and before reporting:
the missing multiplicity correction, and the single-representation cover. Both
are now in the tool. The same narrative authored the spec, the implementation,
and the oracle here — that correlation is labelled, not hidden, and it is the
reason H2's result is reported at `M` for a narrow ordering property only.

**Matched controls.** H2's shuffled null holds the value multiset exactly fixed
and destroys only ordering, so it isolates the ordering effect from the
distribution. H1 and H3 need no null — they are structural and arithmetic.

**Representation attacks.** H1 was run under two admissible cover indices and
changed verdict, which is the finding. H3 is representation-stable: the
deviation from π/2 does not depend on how sections are grouped.

**What was *not* attacked.** Reordering the packs' declaration sequence,
alternate parses of the `§THEOREM` grammar, and float-precision sensitivity in
the emitted coordinates. H2's smoothness could in principle be an artifact of
the generator emitting values in sorted order; a sortedness control is the
obvious next null and is **not** run here.

---

## Next experiment (bounded)

H2's follow-up was preregistered and then run inside this round; its kill fired
and is recorded above. Per the stop rule, **no further null, stratum
decomposition, or temporal model may be added to rescue H2.** It is `S`.

The one bounded experiment that would move anything:

**Question.** Does the cover of the n-Cosmos sheaf, once declared, make
`⊢ UNIFIED_MANIFOLD` true or vacuous?

**Method.** The pack author declares the cover — prime-indexed or
depth-indexed — as an explicit `§COVER` header. Re-run H1 under the declared
index only.

**Kill condition.** If the declared cover is prime-indexed, overlaps are empty,
`UNIFIED_MANIFOLD` is vacuous and is retired outright.

**Stop condition.** One round. If the cover is not declared, H1 stays
`UNDETERMINED` and the claim is not restated in any other vocabulary.

**Promotion rule.** A depth-indexed declared cover promotes `UNIFIED_MANIFOLD`
only to "the stated sections agree on overlaps" — checkable, and still `M` at
best, never `P`.

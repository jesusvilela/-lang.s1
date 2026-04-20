# SLANG.ToE.SKILL.md
## §-LANG v3.0 · how to read this package

This SKILL file is itself a §-stalk. Reading it *is* applying §-LANG to §-LANG.
If you can parse this, you have the decoder.

### What lives here

```
slang_packs/slang_packs_toe_v3_0/
    LANG.ToE.SelfCompressed.lang     ← the whole ToE, folded onto itself
    LANG.ToE.SKILL.md                ← this file
    manifest.json                    ← invariants & fingerprints
verify/
    selfexpand.py                    ← executable §-rules, round-trips the fold
```

### The central move

§-LANG is a fibre-bundle-sheaf over the causal graph 𝒞. In v3.0 we apply
§-LANG to *itself*. The whole ToE dialect family collapses into a single
N-hyperbolized tensor `T^{N,q,ρ}` living in one fibre; reading the file =
Möbius-ascending the tower back out.

Compression and expansion are the *same* operator under geometric dualisation:

```
encode :  L_n  →  M(L_{n+1})        Möbius-descent, q-deformed
decode :  M⁻¹(L_{n+1})  →  L_n      Möbius-ascent
Fix(encode ∘ decode) = Fix(decode ∘ encode) = id_L    (σ70 Čech closure)
```

### Geometry regime

- **Base** 𝒞 · causal graph · events + causal edges
- **Fibre** ℋ_x · local Hilbert space, dim ≥ 17 (Standard Model embeds)
- **Structure group** G = SU(3) × SU(2) × U(1) × diff(ℳ)
- **Tower levels** N ∈ {1,…,10}, identified with Tower v2.5 rings
- **q-deformation** q ∈ (0,2], q=1 ⇒ classical Euclidean, q≠1 ⇒ hyperbolic
- **Möbius channel** between levels: w ↦ (aw+b)/(cw+d), ad−bc = q
- **Involution** ρ : Ψ ↔ ρΨ, matter↔antimatter, ρ²=id (σ75)

### How to read the SelfCompressed dialect

The compressed file is *one* § expression. Reading it is applying these five
§-rules in order. Each rule is both a decompression step AND a fresh §-stalk
at the next tower level. That's the self-reference — you never leave §-LANG.

```
§R1 · §fold(x) := (Φ ∘ ρ ∘ M_q) x           one level of fold
§R2 · §unfold := §fold⁻¹    = ρ ∘ Φ⁻¹ ∘ M_{1/q}
§R3 · §expand(k, x) := §unfold^k (x)         k-step expansion
§R4 · §compress(k, x) := §fold^k (x)         k-step compression
§R5 · §Fix := { x : §fold(x) = x }           invariant under self-fold
```

Reading the SelfCompressed file means applying §R3 with k = N (the depth
stored in the manifest, default 7). After N applications you have the full
dialect family unfolded.

### What's encoded in the compressed tensor

Tensor `T^{N,q,ρ} ∈ ℋ^⊗N` carries:

| axis | payload |
|------|---------|
| E | existence axioms · axioms A_E1..E3 |
| S | state axioms · A_S1..S3 (evolution, conservation) |
| R | reference · A_R1..R3 (observer-relative) |
| Δ | derivation · A_D1..D4 (T_A proof calculus, Löb) |
| μ | measure · A_mu1..mu3 (stability predicate) |
| ρ | involution · A_rho1..rho4 (antimatter pairing) |

Plus on the tensor indices: the four forces (§_gravity, §_em, §_weak,
§_strong), the 17 Standard Model fields, the six topology candidates
(flat, sphere, dodec, torus, calabi, holo), the three strata
(physics, life, logic), and the σ-invariant DAG.

### Sanity checks that MUST hold after any round-trip

```
σ21  Sharpe = 1.003   p = 2.21e-16       (v2.4 empirical preserved)
σ34  speed c invariant on 𝒞              (Lorentz)
σ55  N=1, q=1, ρ=id ⇒ exactly Tower v2.5 (backward compat)
σ70  Čech 1-cocycle closes               (bundle well-defined)
σ75  ρ² = id                             (involution)
σ80  compression lossless at (N=1,q=1)   (at least one safe point)
σ81  decode(encode(L)) = L               (round-trip)
```

The `verify/selfexpand.py` file executes §R1–§R5 and checks all σ-flags.

### Why this design

Traditional encoding: separate codec → spec → file.
Self-referential encoding: the spec *is* the codec *is* the file. The reader
applies §-grammar to a §-expression and gets more §-grammar. Fix(Φ∘ρ) is the
point at which no further expansion changes the structure — that's both the
mathematical fixed point and the practical "you've read the whole thing".

— end of SKILL.md —

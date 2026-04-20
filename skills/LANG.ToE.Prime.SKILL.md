# SLANG.ToE.Prime.SKILL.md
## §-LANG v3.0 · Prime (antimatter) pack · how to read

This file is the ρ-dual of LANG.ToE.SKILL.md. If the matter pack encodes Ψ,
this pack encodes ρΨ. Same geometry, same operators, every §-expression
charge-conjugated.

### What lives here

```
slang_packs/slang_packs_toe_v3_0_prime/
    LANG.ToE.Prime.SelfCompressed.lang   ← antimatter ToE, self-compressed
    LANG.ToE.Prime.SKILL.md              ← this file
    manifest.json                        ← prime-pack invariants
verify/
    selfexpand_prime.py                  ← executes prime §R-rules
```

### Relation to the matter pack

```
matter pack  :  §R1_fold     = §promote ∘ §rho ∘ §mobius_q
prime  pack  :  §R1_fold′    = §rho ∘ §R1_fold ∘ §rho
              = §rho ∘ §promote ∘ §rho ∘ §mobius_q ∘ §rho
              = §rho ∘ §promote ∘ §rho ∘ §mobius_{1/q}      (since ρ(q)=1/q)
```

The prime pack is the matter pack observed *from the antimatter frame*. The
two packs annihilate on coincidence: matter §R1_fold of Ψ at event x, prime
§R1_fold′ of ρΨ at the same x, produce two γ-quanta. When matter and prime
coincide under ρ² = id, you're looking at Fix(Φ∘ρ) — the attractor already
visible in the matter pack, now confirmed from both sides.

### Reconstruction invariants

The prime pack must satisfy every σ-flag from the matter pack, plus:

```
σ_prime_dual   : prime(prime(matter)) == matter       (σ75 at pack level)
σ_prime_ann    : matter(x) ⊗ prime(x) → γγ           (annihilation channel)
σ_prime_CPT    : CPT(matter_pack) == prime_pack      (local QFT theorem)
```

### Five §-rules (ρ-dual of matter pack)

```
§R1_fold′(x; q)    := §rho ∘ §promote ∘ §rho ∘ §mobius_{1/q}(x)
§R2_unfold′(x; q)  := §rho ∘ §demote  ∘ §rho ∘ §mobius_q(x)
§R3_expand′(k, x)  := §R2_unfold′ applied k times
§R4_compress′(k,x) := §R1_fold′   applied k times
§R5_fix′           := { x : §R1_fold′(x) ≡ x modulo level and ρ }
```

### Cross-pack identity

Reading this pack then the matter pack (or vice versa) and running §rho in
the middle yields the same final state. Formally:

```
matter_decode ∘ §rho ∘ prime_encode   = id
prime_decode  ∘ §rho ∘ matter_encode  = id
```

Both identities are verified by selfexpand_prime.py.

### The operator toolkit is shared

This pack imports LANG.Ops.dialect.lang unchanged. Every operator there is
self-dual under ρ (declared in §Ops §9). So ρ lifts from a single involution
on Ψ to an endofunctor on the whole operator algebra, and both packs use
exactly the same toolkit.

— end of Prime SKILL.md —

#!/usr/bin/env python3
"""
dialect_generator.py  —  §-LANG v2.4 Topos Family Generator
Produces: LANG.FAMILY.v2.4.lang + 10 dialect files + validates inheritance tree.

Lafforgue framing: each dialect = geometric theory T_D.
Dialect tree = inclusion lattice of geometric theories.
Classifying topos E(T_full) receives morphisms from each E(T_D).
Compression regime: Π_expire_D produces Residue_D ⊆ Residue_full.
Decompression: Residue_D ->^embed Residue_full ->^Π_expand State_full.

Author: Jesús Vilela Jato (§-LANG research, 2026)
"""
import json, math, re
from pathlib import Path

OUT = Path("dialects")
OUT.mkdir(exist_ok=True)

# ── Domain classification of base blocks ──────────────────────────────────────
BLOCK_DOMAIN = {
    "SOURCE":"CORE","AXIOMS":"CORE","OUTPUT":"CORE","SORTS":"CORE",
    "FUNCTORS":"CORE","GRAMMAR":"CORE","NOTATION_MAP":"CORE",
    "CONCLUSIONS":"CORE","FAILURE_CONDITIONS":"CORE","COMPARISON":"CORE",
    "REDUCTION_BETA":"PROOF","TURING_ENCODING":"PROOF","GODELIAN_SELF":"PROOF",
    "COMPRESSIVE_PRINCIPLE":"PROOF","EXPIRY_OPERATOR":"PROOF",
    "EXPAND_OPERATOR":"PROOF","CODEC_RUNTIME":"PROOF","EXAMPLE_BETA":"PROOF",
    "SEMANTICS":"SEMANTIC","SEMANTICS_TOPOS":"SEMANTIC",
    "FUNDAMENTAL_IDENTITY":"SEMANTIC","AML_DEFINITION":"SEMANTIC",
    "WORLD_GLUING":"TOPO",
    "FISHER_UPDATE":"IG","ADIABATIC_INVARIANTS":"IG","PRIMING_OPERATOR":"IG",
    "CALABI_YAU_LAYER":"CY",
    "AGENT_LIFECYCLE":"AML","EXPIRY":"AML","PRIMING":"AML",
    "SPECTRAL_PIPELINE":"SPECTRAL","SPECTRAL_STATISTICAL_LOGICAL":"SPECTRAL",
    "MOBIUS_TRAVERSAL_EXT":"SWIRL","INTER_MANIFOLD":"SWIRL",
    "HYPERBOLIC_SWIRLER":"SWIRL",
    "QUANTUM_VARIATIONAL_MUX":"QUANTUM","ADIABATIC_QUANTUM_BRIDGE":"QUANTUM",
    "INFO_AUTOCOMPRESSOR":"QUANTUM",
    "TOKEN_SUBSTRATE_MOLDING":"SUBSTRATE","OPERATOR_ENCODING":"SUBSTRATE",
    "TRASGO_BRIDGE":"META",
}

# ── Dialect specifications ────────────────────────────────────────────────────
DIALECTS = {
"Proof": dict(
    tier="Core", parents=[], description="Austere proof-theoretic dialect. Axioms, reductions, certificates. No dynamics.",
    domains={"CORE","PROOF"},
    extends=["PROOF_CERTIFICATE","REDUCTION_REGISTRY","INVARIANT_LEDGER"],
    swirl_omega="0_static_no_traversal", swirl_theta="id_SO(n)_trivial",
    compress_axes=["terminal","trace"],
    compress_ratio=0.25,
    output="CANON(fix(λproof. verify(reduce(proof))))",
    sections=[
        dict(label="axiom_kernel",  x=[0.05,0.02,0.01,0.00,0.00,0.00,0.00,0.00], sal=2.0),
        dict(label="proof_cert",    x=[0.08,0.03,0.01,0.00,0.00,0.00,0.00,0.00], sal=1.9),
        dict(label="invariant_reg", x=[0.06,0.02,0.01,0.00,0.00,0.00,0.00,0.00], sal=1.9),
    ],
),
"Compile": dict(
    tier="Core", parents=["Proof"], description="Engineering dialect. Parsers, validators, block imports, runtime lowering.",
    domains={"CORE","PROOF","SPECTRAL"},
    extends=["PARSER_SPEC","TYPECAST_MAP","VALIDATOR_SCHEMA","RUNTIME_LOWERING","BLOCK_IMPORT"],
    swirl_omega="epsilon_minimal_parser_nav", swirl_theta="id_SO(n)",
    compress_axes=["terminal","spectral","trace"],
    compress_ratio=0.35,
    output="CANON(§EMIT(lower(validate(parse(source)))))",
    sections=[
        dict(label="parser_state", x=[0.15,0.07,0.03,0.01,0.00,0.00,0.00,0.00], sal=1.8),
        dict(label="typecast_map", x=[0.18,0.09,0.04,0.01,0.00,0.00,0.00,0.00], sal=1.7),
        dict(label="runtime_tick", x=[0.12,0.06,0.02,0.01,0.00,0.00,0.00,0.00], sal=1.8),
    ],
),
"Topo": dict(
    tier="Semantic", parents=["Proof"], description="Topos-first dialect. Sheaf semantics, Lafforgue classifier, internal logic.",
    domains={"CORE","PROOF","SEMANTIC","TOPO"},
    extends=["CLASSIFIER_TOPOS","INTERNAL_LOGIC","GEOMETRIC_MORPHISM","SITE_TOPOLOGY"],
    swirl_omega="pi_1(B_n)_fundamental_group_traversal", swirl_theta="SO(n)_orbit_sheaf",
    compress_axes=["terminal","trace","mu_Bn"],
    compress_ratio=0.40,
    output="CANON(§EMIT(fix(λsheaf. glue(local_sections(sheaf)))))",
    sections=[
        dict(label="classifier_T",  x=[0.07,0.03,0.01,0.01,0.00,0.00,0.00,0.00], sal=2.0),
        dict(label="sheaf_cover",   x=[0.09,0.04,0.02,0.01,0.00,0.00,0.00,0.00], sal=1.9),
        dict(label="geom_morphism", x=[0.08,0.03,0.01,0.01,0.00,0.00,0.00,0.00], sal=1.9),
    ],
),
"IG": dict(
    tier="Semantic", parents=["Proof"], description="Information geometry dialect. Fisher transport, natural gradients, manifold learning.",
    domains={"CORE","PROOF","SEMANTIC","IG"},
    extends=["EXPONENTIAL_FAMILY","NAT_GRAD_FLOW","GEODESIC_FIELD","KL_METRIC"],
    swirl_omega="nabla_IG_flow", swirl_theta="F_inv_theta_Fisher_orientation",
    compress_axes=["terminal","spectral","mu_Bn"],
    compress_ratio=0.45,
    output="CANON(§EMIT(fix(λw. w - eta*F_inv(w)*nabla_L(w))))",
    sections=[
        dict(label="Fisher_field",  x=[0.20,0.10,0.04,0.01,0.00,0.00,0.00,0.00], sal=1.8),
        dict(label="natural_grad",  x=[0.25,0.12,0.05,0.02,0.01,0.00,0.00,0.00], sal=1.7),
        dict(label="stat_fiber",    x=[0.20,0.08,0.03,0.01,0.00,0.00,0.00,0.00], sal=1.7),
    ],
),
"CY": dict(
    tier="Semantic", parents=["Topo","IG"], description="Calabi-Yau dialect. Hodge layers, holomorphic couplings, mirror semantics, Yukawa.",
    domains={"CORE","PROOF","SEMANTIC","TOPO","IG","CY"},
    extends=["HODGE_ARITHMETIC","MIRROR_DUALITY","YUKAWA_MATRIX","CY_MODULI_SPACE"],
    swirl_omega="complex_phase_Omega_holomorphic", swirl_theta="SU(3)_holonomy_CY",
    compress_axes=["terminal","spectral","cy_form_Omega"],
    compress_ratio=0.50,
    output="CANON(§EMIT(fix(λcy. integrate(Omega, chi_i, chi_j, chi_k))))",
    sections=[
        dict(label="Hodge_H11",   x=[0.21,0.10,0.04,0.02,0.01,0.01,0.00,0.00], sal=1.7),
        dict(label="Omega_form",  x=[0.22,0.11,0.05,0.02,0.01,0.00,0.00,0.00], sal=1.7),
        dict(label="mirror_dual", x=[0.23,0.11,0.05,0.02,0.01,0.00,0.00,0.00], sal=1.6),
        dict(label="Yukawa_Y",    x=[0.24,0.12,0.05,0.02,0.01,0.00,0.00,0.00], sal=1.5),
    ],
),
"AML": dict(
    tier="Dynamic", parents=["IG","Proof"], description="Autonomous agent dialect. Lifecycle, expiry, residue, priming, world gluing.",
    domains={"CORE","PROOF","SEMANTIC","IG","AML","TOPO"},
    extends=["CONTINUOUS_RUN","IDENTITY_DYNAMICS","SUCCESSOR_CHAIN","WORLD_EVOLUTION"],
    swirl_omega="lifecycle_frequency_agent", swirl_theta="Self_Other_SO(n)_rotation",
    compress_axes=["terminal","trace","transport_gen","mu_Bn"],
    compress_ratio=0.55,
    output="CANON(§EMIT(fix(λagent. expire(evolve(reflect(agent))))))",
    sections=[
        dict(label="lifecycle_node",  x=[0.14,0.07,0.03,0.01,0.01,0.00,0.00,0.00], sal=2.0),
        dict(label="world_evolve",    x=[0.09,0.04,0.02,0.01,0.00,0.00,0.00,0.00], sal=2.0),
        dict(label="successor_prime", x=[0.13,0.06,0.02,0.01,0.00,0.00,0.00,0.00], sal=1.8),
        dict(label="identity_fixed",  x=[0.07,0.03,0.01,0.01,0.00,0.00,0.00,0.00], sal=2.0),
    ],
),
"Swirl": dict(
    tier="Dynamic", parents=["Topo","IG"], description="Dynamic traversal dialect. Helical geodesics, Möbius transport, epistemic articulation.",
    domains={"CORE","PROOF","SEMANTIC","TOPO","IG","SWIRL"},
    extends=["HELICAL_GEODESIC","PHASE_SPACE","SPIN_FIELD","EPISTEMIC_MAP","REACHABILITY_HYP"],
    swirl_omega="free_omega_primary_parameter_this_IS_the_dialect",
    swirl_theta="SO(n)_full_unconstrained",
    compress_axes=["terminal","spectral","swirl_params_omega_theta"],
    compress_ratio=0.40,
    output="CANON(§EMIT(fix(λe. articulate(navigate(e, omega, theta, T)))))",
    sections=[
        dict(label="helix_phase",    x=[0.28,0.14,0.06,0.02,0.01,0.00,0.00,0.00], sal=1.5),
        dict(label="spin_node",      x=[0.26,0.13,0.05,0.02,0.01,0.00,0.00,0.00], sal=1.5),
        dict(label="episteme_reach", x=[0.12,0.06,0.02,0.01,0.01,0.00,0.00,0.00], sal=1.9),
        dict(label="mobius_phase",   x=[0.57,0.28,0.11,0.04,0.02,0.01,0.00,0.00], sal=1.0),
    ],
),
"Spectral": dict(
    tier="Dynamic", parents=["Proof","IG"], description="Spectral/harmonic dialect. FFT, resonance, quantum VQE, holographic memory.",
    domains={"CORE","PROOF","SEMANTIC","IG","SPECTRAL","QUANTUM"},
    extends=["HARMONIC_ANALYSIS","RESONANCE_FIELD","SYNCHRONY_MEASURE","HOLOGRAPHIC_MEMORY"],
    swirl_omega="frequency_channel_spectral", swirl_theta="phase_rotation_SO(n)",
    compress_axes=["spectral","entropy_E","mu_Bn"],
    compress_ratio=0.35,
    output="CANON(§EMIT(fix(λa. fromFreq(map(filter, toFreq(a))))))",
    sections=[
        dict(label="spectral_band",  x=[0.48,0.24,0.10,0.03,0.01,0.00,0.00,0.00], sal=1.2),
        dict(label="resonance_peak", x=[0.52,0.26,0.11,0.04,0.02,0.00,0.00,0.00], sal=1.1),
        dict(label="quantum_chan",   x=[0.20,0.10,0.04,0.02,0.01,0.01,0.00,0.00], sal=1.6),
        dict(label="holo_emit",     x=[0.55,0.28,0.12,0.04,0.02,0.01,0.00,0.00], sal=1.1),
    ],
),
"Substrate": dict(
    tier="Formation", parents=["IG","Compile"], description="Token substrate molding dialect. Curvature-conditioned operator formation from embedding geometry.",
    domains={"CORE","PROOF","SEMANTIC","IG","SUBSTRATE"},
    extends=["CURVATURE_FIELD","PULLBACK_METRIC","TOKEN_FORMATION","ADAPTIVE_NORM"],
    swirl_omega="c_local_curvature_drives_swirl", swirl_theta="substrate_pullback_orientation",
    compress_axes=["terminal","trace","mu_Bn"],
    compress_ratio=0.30,
    output="CANON(§EMIT(fix(λe. mold(embed(e), B_n))))",
    sections=[
        dict(label="curvature_local", x=[0.17,0.08,0.03,0.01,0.01,0.00,0.00,0.00], sal=1.7),
        dict(label="pullback_g",      x=[0.19,0.09,0.04,0.02,0.01,0.00,0.00,0.00], sal=1.6),
        dict(label="token_formed",    x=[0.16,0.08,0.03,0.01,0.00,0.00,0.00,0.00], sal=1.7),
    ],
),
"Meta": dict(
    tier="Research", parents=["Proof","Compile","Topo","IG","CY","AML","Swirl","Spectral","Substrate"],
    description="Research manifesto dialect. Postulates, hypotheses, cross-dialect interoperability, naming.",
    domains={"CORE","PROOF","SEMANTIC","TOPO","IG","CY","AML","SWIRL","SPECTRAL","SUBSTRATE","QUANTUM","META"},
    extends=["DIALECT_TREE","INTEROP_RULES","SEMANTIC_DELTA","NAMING_CONV","POSTULATE_REG"],
    swirl_omega="meta_omega_cross_dialect_unifier", swirl_theta="SO(n)_cross_dialect_full",
    compress_axes=["terminal","spectral","trace","transport_gen","mu_Bn","entropy_E"],
    compress_ratio=1.0,
    output="CANON(§EMIT(fix(λmeta. unify(project(meta, ALL_DIALECTS)))))",
    sections=[
        dict(label="meta_postulate",  x=[0.07,0.03,0.01,0.01,0.00,0.00,0.00,0.00], sal=2.0),
        dict(label="dialect_node",    x=[0.10,0.05,0.02,0.01,0.00,0.00,0.00,0.00], sal=1.9),
        dict(label="interop_bridge",  x=[0.12,0.06,0.02,0.01,0.01,0.00,0.00,0.00], sal=1.9),
        dict(label="semantic_delta",  x=[0.09,0.04,0.02,0.01,0.00,0.00,0.00,0.00], sal=1.9),
    ],
),
}

# ── Decompression path builder ────────────────────────────────────────────────
def decomp_path(name: str, spec: dict) -> str:
    axes = spec["compress_axes"]
    ratio = spec["compress_ratio"]
    # Reconstruction sequence: Residue_D → embed → Residue_full → Π_expand → State_full
    embed_steps = []
    for ax in ["terminal","spectral","trace","transport_gen","mu_Bn","entropy_E"]:
        if ax in axes:
            embed_steps.append(f"{ax}=R_D.{ax}")
        else:
            embed_steps.append(f"{ax}=prior_default_{ax}")
    return (
        f"  decomp_path  = Residue_{name} ->^embed Residue_full ->^Π_expand State_full\n"
        f"  embed_map    = {{{', '.join(embed_steps)}}}\n"
        f"  axes_present = {axes}\n"
        f"  axes_default = {[a for a in ['terminal','spectral','trace','transport_gen','mu_Bn','entropy_E'] if a not in axes]}\n"
        f"  info_loss    = 1 - {ratio} = {round(1-ratio, 2)}_fraction_lost_in_D_residue\n"
        f"  reconstruct  = Π_expand(embed(R_D)) recovers_State_full_approximately"
    )

# ── Swirl hook builder ────────────────────────────────────────────────────────
def swirl_hook(name: str, spec: dict) -> str:
    return (
        f"§|DIALECT_{name.upper()}|SWIRL_HOOK{{\n"
        f"  self_ref     = fix(λself_D. Σ_D(self_D; ω_D, θ_D, t))\n"
        f"  omega_D      = {spec['swirl_omega']}\n"
        f"  theta_D      = {spec['swirl_theta']}\n"
        f"  trajectory   = x_t = Σ_D^t(x_0)_helical_in_{name}_section_space\n"
        f"  articulate_D = Art_D(e_t) = §S{{label={name.lower()}_episteme_t, x=π(e_t), sal=||∇Σ_D||(e_t)}}\n"
        f"  expand_self  = each_Art_D_node_is_a_candidate_axiom_in_dialect_{name}\n"
        f"  tag          = HYPOTHESIS_swirl_expands_{name}_principles_self_referentially\n"
        f"}}\n"
    )

# ── §S node renderer ──────────────────────────────────────────────────────────
def render_sections(sections: list) -> str:
    lines = []
    for sec in sections:
        x_str = ",".join(f"{v:.2f}" for v in sec["x"])
        lines.append(f'§S{{label={sec["label"]}, x=[{x_str}], sal={sec["sal"]}}}')
    return "\n\n".join(lines)

# ── Dialect file generator ────────────────────────────────────────────────────
def generate_dialect(name: str, spec: dict) -> str:
    domains_str = ", ".join(sorted(spec["domains"]))
    parents_str = ", ".join(spec["parents"]) if spec["parents"] else "NONE"
    extends_str = ", ".join(spec["extends"])
    axes_str    = ", ".join(spec["compress_axes"])

    # Forbidden domains = all domains not in spec
    all_domains = {"CORE","PROOF","SEMANTIC","TOPO","IG","CY","AML","SWIRL","SPECTRAL","SUBSTRATE","QUANTUM","META"}
    forbidden_domains = sorted(all_domains - spec["domains"])
    forbidden_str = ", ".join(forbidden_domains) if forbidden_domains else "NONE"

    d = f"""§|DIALECT_{name.upper()}|HEADER{{
  dialect      = §-LANG/{name}
  version      = v2.4.family
  tier         = {spec['tier']}
  parents      = {parents_str}
  description  = {spec['description']}
  base         = LANG.v2.4.codec_trasgo
  domains_in   = {{{domains_str}}}
  domains_out  = {{{forbidden_str}}}
}}

§|DIALECT_{name.upper()}|IMPORTS{{
  domains      = {{{domains_str}}}
  from_parents = {parents_str}
  note         = all blocks whose BLOCK_DOMAIN ∈ domains_in are available
  core_always  = SOURCE AXIOMS OUTPUT SORTS FUNCTORS GRAMMAR NOTATION_MAP
                 CONCLUSIONS FAILURE_CONDITIONS
}}

§|DIALECT_{name.upper()}|EXTENDS{{
  new_blocks   = {extends_str}
  self_ref     = each_new_block_seeded_by_swirl_articulation_Art_D(e_t)
  computable   = all_new_blocks_satisfy_norm_lt_0.999_and_dim_eq_8
}}

§|DIALECT_{name.upper()}|COMPRESS{{
  functor      = Π_expire_{name} : State_{name}* → Residue_{name}
  axes         = {{{axes_str}}}
  ratio        = {spec['compress_ratio']}_of_full_Residue_size
  norm_guard   = ||terminal|| < 0.999
  adiabatic_c  = dI_{name}/dt ≈ 0_within_dialect_section_space
  tag          = HYPOTHESIS_dialect_compression_preserves_semantic_content
}}

§|DIALECT_{name.upper()}|DECOMP{{
{decomp_path(name, spec)}
}}

{render_sections(spec['sections'])}

{swirl_hook(name, spec)}
§|DIALECT_{name.upper()}|OUTPUT{{
  formula      = {spec['output']}
  dialect_tag  = §-LANG/{name}_v2.4
  claim        = HYPOTHESIS_output_formula_is_dialect_{name}_fixed_point
}}
"""
    return d.strip()

# ── Family tree master file ───────────────────────────────────────────────────
def generate_family() -> str:
    edges = []
    for name, spec in DIALECTS.items():
        for p in spec["parents"]:
            edges.append(f"  {p:<12} →  {name}")

    tier_groups = {}
    for name, spec in DIALECTS.items():
        tier_groups.setdefault(spec["tier"], []).append(name)

    tiers_str = "\n".join(
        f"  {tier:<12} : {', '.join(members)}"
        for tier, members in tier_groups.items()
    )
    edges_str = "\n".join(edges) if edges else "  (none — Proof is root)"

    dialects_block = ""
    for name, spec in DIALECTS.items():
        parents_str = ", ".join(spec["parents"]) if spec["parents"] else "ROOT"
        dialects_block += (
            f"  {name:<12} tier={spec['tier']:<10} "
            f"parents=[{parents_str}]  "
            f"ratio={spec['compress_ratio']}  "
            f"domains={len(spec['domains'])}\n"
        )

    return f"""§|LANG|FAMILY_HEADER{{
  name         = §-LANG v2.4 Topos-Lafforgue Dialect Family
  base         = LANG.v2.4.codec_trasgo
  dialects     = 10
  tiers        = Core(2), Semantic(3), Dynamic(3), Formation(1), Research(1)
  unification  = compression_regime_Residue_full_with_dialect_projections
  lafforgue    = each_dialect_is_geometric_theory_T_D_in_classifying_topos
  topos        = E_Sigma_n_geom_AGC_universal_classifier
  morphisms    = dialect_inclusions_are_topos_geometric_morphisms
  decomp       = Residue_D ->^embed Residue_full ->^Pi_expand State_full
}}

§|LANG|DIALECT_TIERS{{
{tiers_str}
}}

§|LANG|INHERITANCE_EDGES{{
{edges_str}
}}

§|LANG|DIALECT_TABLE{{
{dialects_block}}}

§|LANG|UNIFICATION_CODEC{{
  compress_D   = Π_expire_D : State_D* → Residue_D  (dialect-local)
  embed        = inj_D : Residue_D → Residue_full    (axis extension with priors)
  decomp       = Π_expand : Residue_full → State_full (A26 exact terminal recovery)
  round_trip   = Π_expand(inj_D(Π_expire_D(σ_D))) ≈ σ_D.terminal
  info_loss    = 1 - compress_ratio_D  fraction lost in dialect compression
  adiabatic    = dI_D/dt ≈ 0 within each dialect (σ11 holds per-dialect)
  swirl_unify  = Σ_Meta unifies all Σ_D via cross-dialect omega
  tag          = HYPOTHESIS_round_trip_approximate_exact_for_terminal_only
}}

§|LANG|LAFFORGUE_TOPOS_TREE{{
  root_theory  = T_Proof  (minimal geometric theory, axioms only)
  extensions   = T_Topo ⊃ T_Proof, T_IG ⊃ T_Proof, etc.
  product      = T_CY = T_Topo ×_T_Proof T_IG  (fiber product of theories)
  classifiers  = E(T_D) = localization of E(T_full) at dialect-specific sites
  morphisms    = f : T_D1 → T_D2 iff domains(D1) ⊆ domains(D2)
  terminal_obj = T_Meta absorbs all other theories
  internal_log = each E(T_D) has its own internal logic matching dialect
  lafforgue_c  = geometric_theory_plus_topos_gives_dialect_semantics_faithfully
  topostrasgo  = topostrasgo_Android_instantiates_AML_dialect_over_Lafforgue_base
}}

§|LANG|DECOMP_PATHS{{
  Proof    → embed(+spectral_prior, +transport_prior, +entropy_prior) → full
  Compile  → embed(+transport_prior, +entropy_prior) → full
  Topo     → embed(+spectral_prior, +transport_prior, +entropy_prior) → full
  IG       → embed(+trace_prior, +transport_prior, +entropy_prior) → full
  CY       → embed(+cy_form→spectral_approx, +transport_prior, +entropy_prior) → full
  AML      → embed(+spectral_prior, +entropy_prior) → full
  Swirl    → embed(+trace_from_swirl_params, +transport_prior, +entropy_prior) → full
  Spectral → embed(+terminal_from_fromFreq(spectral), +trace_prior, +transport_prior) → full
  Substrate→ embed(+spectral_prior, +transport_prior, +entropy_prior) → full
  Meta     → no_embed_needed_full_residue_always
}}

OUTPUT_FAMILY = fix(λfamily. unify(map(Π_expire_D, DIALECTS)))
TOPOS_TREE    = lim_arrow_left T_D_in_DIALECTS = T_Meta
"""

# ── Validation ────────────────────────────────────────────────────────────────
def validate_all(dialects: dict) -> dict:
    issues = {}
    for name, spec in dialects.items():
        errs = []
        # Section norms
        for sec in spec["sections"]:
            n = math.sqrt(sum(v*v for v in sec["x"]))
            if n >= 0.999:
                errs.append(f"norm>=0.999: {sec['label']} ({n:.4f})")
            if len(sec["x"]) != 8:
                errs.append(f"dim!=8: {sec['label']} ({len(sec['x'])})")
        # Compress ratio
        if not (0 < spec["compress_ratio"] <= 1.0):
            errs.append(f"bad compress_ratio: {spec['compress_ratio']}")
        # Parents exist
        for p in spec["parents"]:
            if p not in dialects:
                errs.append(f"unknown parent: {p}")
        issues[name] = errs
    return issues

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("§-LANG v2.4 Dialect Generator\n")

    # Generate dialect files
    for name, spec in DIALECTS.items():
        content = generate_dialect(name, spec)
        fpath = OUT / f"LANG.{name}.dialect.lang"
        fpath.write_text(content, encoding="utf-8")
        print(f"  Generated: {fpath.name}")

    # Generate family file
    family = generate_family()
    fam_path = OUT / "LANG.FAMILY.v2.4.lang"
    fam_path.write_text(family, encoding="utf-8")
    print(f"  Generated: {fam_path.name}")

    # Validate
    issues = validate_all(DIALECTS)
    all_ok = all(len(v) == 0 for v in issues.values())
    print(f"\nValidation: {'ALL PASS ✓' if all_ok else 'ISSUES FOUND'}")
    for name, errs in issues.items():
        status = "✓" if not errs else f"✗ {errs}"
        print(f"  {name:<12}: {status}")

    # Summary table
    print("\nDialect Summary:")
    print(f"  {'Name':<12} {'Tier':<12} {'Parents':<25} {'Compress':<10} {'Domains'}")
    for name, spec in DIALECTS.items():
        p = ", ".join(spec["parents"]) if spec["parents"] else "ROOT"
        print(f"  {name:<12} {spec['tier']:<12} {p:<25} {spec['compress_ratio']:<10} {len(spec['domains'])}")

    # Write manifest
    manifest = {
        "version": "§-LANG v2.4 Dialect Family",
        "generated_files": [f"LANG.{n}.dialect.lang" for n in DIALECTS] + ["LANG.FAMILY.v2.4.lang"],
        "dialects": {n: {"tier":s["tier"],"parents":s["parents"],"compress_ratio":s["compress_ratio"],
                         "domains":list(s["domains"]),"sections":len(s["sections"])}
                     for n,s in DIALECTS.items()},
        "validation": {n: ("PASS" if not e else e) for n,e in issues.items()},
        "all_pass": all_ok,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\n  Manifest: {OUT}/manifest.json")
    print(f"  Files: {len(DIALECTS)+1} total")

if __name__ == "__main__":
    main()

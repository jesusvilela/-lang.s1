# §-LANG Practical Verification

> **Truth-discipline notice:**  
> This document carefully distinguishes *syntactic/structural* checks
> (machine-executable, reproducible) from *semantic* and *theoretical* claims
> (not yet machine-verified). Read each section header.

---

## 1. What is practically verified

The following checks are **fully reproducible** by running one command:

```bash
python3 tools/validate_typecast.py --all
python3 tools/verify_chomsky.py
```

### 1.1 Checks performed (structural / parser-level)

| Check | Description |
|-------|-------------|
| `block_headers_present` | Every required `§\|LANG\|<BLOCK>{` header is found in the file. |
| `section_vectors_dimension_8` | All `§S{...}` section-point vectors have exactly 8 components (matching the claimed 8-dimensional hyperbolic embedding space). |
| `section_norm_below_0_999` | All section-point Euclidean norms satisfy `‖x‖ < 0.999`, staying strictly inside the Poincaré unit-ball boundary. |
| `salience_positive` | All `sal=` values are positive reals. |

### 1.2 Results (as of last run)

All 7 `.lang` source files **pass** all structural checks:

| File | Profile | Blocks | Sections | Status |
|------|---------|--------|----------|--------|
| `DIALECTS.v2.1.family.lang` | `dialects` | 3 | 0 | ✅ |
| `LANG.v1.2.0.unified_geometry.lang` | `unified_geometry` | 22 | 19 | ✅ |
| `LANG.v2.5.tower.geom.lang` | `tower_geom` | 8 | 0 | ✅ |
| `LANG.v3.0.substrate_realization.lang` | `substrate` | 7 | 0 | ✅ |
| `LANG.v3.1.recursive_sectional_computer.lang` | `recursive_sectional` | 7 | 0 | ✅ |
| `LANG.v3.2.actor_critic_fuzzer_cycle.lang` | `actor_critic` | 6 | 0 | ✅ |
| `LANG.v5.topos_ai_cosmos_synthesis.lang` | `topos_ai` | 7 | 0 | ✅ |

Full per-file reports: [`research/validation_report_all.md`](research/validation_report_all.md)  
Machine-readable JSON: [`research/validation_report_all.json`](research/validation_report_all.json)

### 1.3 Single-file validation

```bash
# default (unified_geometry profile)
python3 tools/validate_typecast.py

# explicit source
python3 tools/validate_typecast.py --source LANG.v2.5.tower.geom.lang
python3 tools/validate_typecast.py --source LANG.v3.1.recursive_sectional_computer.lang
```

### 1.4 Automated CI

A GitHub Actions workflow (`.github/workflows/validate.yml`) runs these checks
automatically on every push or pull request that touches a `.lang` file or the
validation tooling. Validation reports are uploaded as CI artifacts.

### 1.5 Chomsky hierarchy evidence checks

`tools/verify_chomsky.py` performs practical checks against the declared
`GRAMMAR` block in `LANG.v1.2.0.unified_geometry.lang`:

| Check | Description |
|-------|-------------|
| `grammar_block_present` | Confirms the unified source declares a `GRAMMAR` block. |
| `productions_extracted` | Extracts production-like `lhs = rhs` rules from the block. |
| `surface_grammar_is_context_free_shape` | Confirms every extracted production has a single nonterminal-like left-hand side, the syntactic shape required for a Type-2/context-free grammar. |
| `surface_grammar_has_nonregular_recursion_evidence` | Finds recursive/nested productions such as `term = §.(term)` and `term = term term`, which are evidence the surface grammar is not merely Type-3/regular. |
| `recursive_witnesses_parse` | Runs a small recursive recognizer on nested witness terms `§.(a)`, `§.(§.(a))`, ... up to depth 6. |
| `semantic_type0_markers_present` | Confirms symbolic markers for λ, `fix`, `TURING_ENCODING`, and the declared computability claim are present. This is evidence only, not a semantic proof. |

Full report: [`research/chomsky_verification_report.md`](research/chomsky_verification_report.md)  
Machine-readable JSON: [`research/chomsky_verification_report.json`](research/chomsky_verification_report.json)

---

## 2. What is NOT verified by these checks

The structural checks above are **parser-only / symbolic-only**. They do not verify:

| Claim type | Status |
|-----------|--------|
| Semantic correctness of `fix`, λ-calculus, and Turing-encoding blocks | ❌ Not machine-verified — no executable interpreter exists in this repository. |
| Mathematical theorems (Hamiltonian conservation, symplectic closure, Mostow rigidity, Selberg trace formula) | ❌ Not machine-verified — stated as postulates; no proof assistant or checker is present. |
| Sheaf gluing constraints and topos-classifier consistency | ❌ Structural check confirms the block headers exist, but does not evaluate their content. |
| Self-reference and prime-other (`§'`) mutual resonance | ❌ Semantic concept described in natural language; no executable test. |
| LLM-induced meta-semantic negotiation and expansion | ❌ Inherently not statically verifiable; depends on external, open-ended LLM interaction. |
| Hyperbolic embedding validity beyond norm bounds | ❌ Only ‖x‖ < 0.999 is checked; actual Poincaré-disk/geodesic geometry is not evaluated. |
| Chomsky-hierarchy placement of the semantic layer | ⚠️ Symbolic markers are checked by `tools/verify_chomsky.py`, but Type-0 semantic equivalence is not machine-proven. |

---

## 3. Chomsky hierarchy summary (informational, not proven here)

| Layer | Classification | Basis |
|-------|---------------|-------|
| Lexical tokens | Type-3 Regular | Token patterns are regular expressions. |
| Surface `.lang` syntax | Type-2 Context-Free | Block/section nesting requires a stack (CFG). |
| Typed/scoped §-LANG | At least Type-1 | Binding correctness, arity, invariant checks are beyond CFG. |
| Executable semantics with `fix` and Turing encoding | Type-0 Recursively Enumerable | λ-calculus + fixpoint + claimed Turing completeness. |
| LLM-induced meta-semantics | Meta-formal / oracle-like | Not capturable in the classical Chomsky hierarchy. |

This table summarises the classification discussed in the repository conversation.
`tools/verify_chomsky.py` now provides practical evidence for the lexical and
surface-syntax rows, and marker evidence for the semantic row. It remains **not**
a formal proof of the complete language semantics.

---

## 4. How to add more verification

To strengthen the checks beyond structural validation:

1. **Interpreter / reducer** — implement a β-reduction evaluator for the
   `REDUCTION_BETA` block and add a test suite of known normal forms.
2. **Proof assistant** — encode axioms in Lean/Coq/Agda and attempt type-check.
3. **Grammar parser** — extract the `GRAMMAR` block and build a PEG/ANTLR parser;
   run example terms from `EXAMPLE_BETA` through it.
4. **Geometric unit tests** — add more `§S{...}` section points to v3.x files and
   verify norm invariants are preserved under claimed transformations.

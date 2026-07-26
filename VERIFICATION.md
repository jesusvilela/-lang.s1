# §-LANG Practical Verification

> **Truth-discipline notice:** this document distinguishes structural checks,
> operational reproduction, empirical measurement, and formal proof. Evidence
> from one category must not be promoted into another without an explicit bridge.

## 1. Reproducible structural checks

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/validate_typecast.py --all
python3 tools/verify_chomsky.py
```

The authoritative structural source set is declared in
[`validation/sources.json`](validation/sources.json). Generated reports must be
read together with the repository commit that produced them.

### Structural statuses

| Status | Meaning |
|---|---|
| `PASS` | The tested object exists and satisfies the implemented structural predicate. |
| `FAIL` | A required or present tested object violates the predicate. |
| `NOT_APPLICABLE` | No object of that type exists in the source. This is not a pass. |
| `NOT_TESTED` | The validator does not implement a test for that semantic level. |

### Legacy block-source checks

For declared legacy profiles the validator checks:

- required `§|LANG|<BLOCK>{` headers;
- eight components in each parsed `§S{...}` vector;
- Euclidean norm below the configured `0.999` boundary for present vectors;
- positive salience for present vectors.

### Experimental pack checks

The current `mhrr_pack_v1` structural profile checks only that explicit `§PACK`
and `§VERSION` headers exist. Its semantic, mathematical, runtime, and empirical
claims remain `NOT_TESTED` by this validator.

Unknown profiles fail explicitly. Profiles are not inferred from filenames.

## 2. Regression and representation tests

`tests/test_validate_typecast.py` covers the audit defects that motivated the
current correction:

1. absent sections return `NOT_APPLICABLE`, not vacuous `PASS`;
2. unknown profiles fail rather than defaulting silently;
3. experimental packs require explicit surface headers;
4. pack recognition does not depend on the filename;
5. present vectors are actually checked.

These tests are correlated repository evidence, not independent replication.

## 3. Chomsky hierarchy evidence checks

`tools/verify_chomsky.py` provides practical evidence for lexical and surface
syntax properties in the declared historical source. It checks grammar-block
presence, production extraction, context-free surface shape, recursive witness
parsing, and the presence of markers associated with richer semantics.

It does **not** prove semantic Type-0 equivalence, Turing completeness of the
implemented system, or the behavior of an executable interpreter.

## 4. What is not verified here

| Claim type | Current status |
|---|---|
| Semantic correctness of `fix`, lambda-calculus, or Turing blocks | Not verified by structural tooling |
| Complete runtime behavior of documented operators | Requires pinned implementation and black-box conformance logs |
| Hamiltonian conservation, symplectic closure, Mostow rigidity, Selberg trace formula | Requires exact proof artifacts or bounded numerical experiments |
| Sheaf gluing and topos-classifier consistency | Header presence only where applicable |
| Self-reference and prime-other mutual resonance | Semantic/research construct unless operationalized |
| LLM-induced meta-semantic negotiation | External open-ended interaction; not statically verified |
| Full Poincare or geodesic geometry | Norm-bound checks only |
| Complete UTAI or n-Cosmos machine verification | Requires pinned theorem sources and clean builds |
| R142 universality or substrate stability | Requires raw data, methods, controls, uncertainty, and provenance |
| Complexity lower bound from defect density | Open theorem target |

## 5. Evidence governance

Consult [`CLAIMS.yaml`](CLAIMS.yaml) for the current claim-to-artifact mapping and
[`STATUS.md`](STATUS.md) for publication gates. In particular:

- `P` is reserved for exact, artifact-backed statements;
- `M` requires data, controls, uncertainty, and execution provenance;
- `A` marks assumptions, surrogates, or external dependencies;
- `H` marks hypotheses and theorem targets;
- `S` marks semantic or architectural language;
- `R` preserves retired interpretations and their replacements.

## 6. Next verification steps

1. Publish a grammar and independent parser for a bounded §-LANG Core.
2. Implement a minimal evaluator with known-answer and metamorphic tests.
3. Pin every Lean/Bunny claim to repository, commit, theorem, toolchain, and log.
4. Reconstruct R142 with raw data, seeds, estimator, uncertainty, and matched nulls.
5. Add an independent witness not authored from the same specification narrative.

Passing the current workflow supports only the claim that the declared structural
surfaces satisfy their implemented structural predicates.

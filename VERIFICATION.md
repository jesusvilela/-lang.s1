# §-LANG Practical Verification

> **Truth-discipline notice:** this document distinguishes structural checks,
> operational reproduction, empirical measurement, and formal proof. Evidence
> from one category must not be promoted into another without an explicit bridge.

## 1. Reproducible structural checks

Run:

```bash
python3 -m pip install -r requirements.txt

python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m slang_core core/examples/01_bindings.s1 --json
python3 -m slang_core.conformance --json
python3 tools/validate_typecast.py --all
python3 tools/validate_typecast.py
python3 tools/verify_chomsky.py
python3 tools/stego_boot_banner.py --verify figures/slang_boot_banner.png
```

The authoritative structural source set is declared in
[`validation/sources.json`](validation/sources.json). A declared source that is
absent from the working tree fails the run; it is never skipped.

Generated reports must be read together with the repository commit that produced
them. The committed reports under `research/` are regenerated and diffed in CI,
so a committed report that the current tooling would not reproduce fails the
build. This makes the reports an artifact of the commit rather than a historical
snapshot of an older validator.

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

### Pack surface checks

Five packs are declared with `pack`-surface profiles. For each, the validator
checks that explicit `§PACK` and `§VERSION` headers exist, and that the declared
`§PACK` identity matches the profile it was declared under — so one pack file
cannot silently stand in for another. Their semantic, mathematical, runtime, and
empirical claims remain `NOT_TESTED`.

The validator also tallies `§THEOREM` lines, `§AXIOM` lines, and `⊢ COMMIT`
markers per source. These are reported under `declarations`, deliberately
separate from `checks`: they are counts of text, and counting a `§THEOREM` line
is not checking a theorem. A turnstile in a pack is a character a generator
emitted, not a judgment a checker discharged. See [`PACKS.md`](PACKS.md).

Unknown profiles fail explicitly. Profiles are not inferred from filenames.

## 2. Regression and representation tests

`tests/test_validate_typecast.py` covers the audit defects that motivated the
current correction:

1. absent sections return `NOT_APPLICABLE`, not vacuous `PASS`;
2. unknown profiles fail rather than defaulting silently;
3. packs require explicit surface headers;
4. pack recognition does not depend on the filename;
5. present vectors are actually checked;
6. a well-formed pack whose identity does not match its declared profile fails;
7. a matching pack identity passes, and legacy block profiles report the
   identity check as `NOT_APPLICABLE` rather than borrowing it;
8. theorem tallies are recorded as declarations and never appear as checks.

These tests are correlated repository evidence, not independent replication.

## 3. Bounded S1 Core operational checks

[`core/grammar.ebnf`](core/grammar.ebnf) defines the bounded Core surface.
[`slang_core/core.py`](slang_core/core.py) parses and evaluates only that
surface. [`core/conformance.json`](core/conformance.json) drives canonical
known-answer cases, a negative assertion, an assertion-free `NOT_TESTED` case,
and explicit `NOT_APPLICABLE` / `NOT_TESTED` capability boundaries.

`python3 -m slang_core.conformance --json` emits the machine-readable
`slang.s1.conformance.v1` result. A conformance `PASS` establishes only that
the bounded Core behaved as its local specification requires. It does not
validate the historical v5 runtime, generated packs, theorem markers, or
geometric semantics.

**Current execution status (2026-09-28):** the latest GitHub Actions attempts
terminated before any workflow step was assigned, including one explicit
rerun. That is an infrastructure/runner failure, not a successful or failed
validation run. Until one clean Python 3.11 unit-test + conformance execution
completes, `SLANG-CORE-EXEC-001` remains `A`, not `P`.

## 4. Chomsky hierarchy evidence checks

`tools/verify_chomsky.py` provides practical evidence for lexical and surface
syntax properties in the declared historical source. It checks grammar-block
presence, production extraction, context-free surface shape, recursive witness
parsing, and the presence of markers associated with richer semantics.

It does **not** prove semantic Type-0 equivalence, Turing completeness of the
implemented system, or the behavior of an executable interpreter.

## 5. What is not verified here

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

## 5b. Mesh projection

`tools/mesh_sections.py` re-encodes a declared pack's `§THEOREM` declarations as
a section/link graph. It refuses any source not declared as a pack surface in
`validation/sources.json`, and the emitted JSON carries its own scope statement
and a `forbidden_readings` list.

What projection establishes is only that the declaration tree was transcribed.
A section is a declaration, a link is adjacency, and a coordinate is a value the
pack states. `declared_verdict` records the turnstile token verbatim and is
never converted into a status.

Each pack is a **forest**: the five PM axioms at depth 1 are roots, so link
count is `sections − roots`, not `sections − 1`. A regression test pins this so
a future change cannot silently produce a single spanning tree.

## 5c. External material

Work originating outside this repository is held in [`CANDIDATES.md`](CANDIDATES.md)
until its blocking defects are named and resolved. Citation attributions are
checked against primary sources rather than against the candidate's own
description of them — repeated self-review is not independent replication.

The procedure is installed as a skill at
`.claude/skills/recursive-research-auditor/`; its manifest validator is
self-tested on every build.

## 6. Evidence governance

Consult [`CLAIMS.yaml`](CLAIMS.yaml) for the current claim-to-artifact mapping and
[`STATUS.md`](STATUS.md) for publication gates. In particular:

- `P` is reserved for exact, artifact-backed statements;
- `M` requires data, controls, uncertainty, and execution provenance;
- `A` marks assumptions, surrogates, or external dependencies;
- `H` marks hypotheses and theorem targets;
- `S` marks semantic or architectural language;
- `R` preserves retired interpretations and their replacements.

## 7. Next verification steps

1. Add metamorphic/property tests around the bounded S1 Core without widening its semantics implicitly.
2. Reproduce selected historical v5 operators only when each receives black-box conformance cases and a pinned semantic contract.
3. Pin every Lean/Bunny claim to repository, commit, theorem, toolchain, and log.
4. Reconstruct R142 with raw data, seeds, estimator, uncertainty, and matched nulls.
5. Add an independent witness not authored from the same specification narrative.

Passing the current workflow supports only the claim that the declared structural
surfaces satisfy their implemented structural predicates.

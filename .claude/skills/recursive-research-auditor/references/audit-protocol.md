# Audit protocol

## Evidence tags

- `P` — proved or definitionally closed under an exact statement and verified artifact.
- `A` — axiomatized, assumed, surrogate, or conditional bridge made explicit.
- `M` — measured under a bounded instrument with data, controls, uncertainty, and execution provenance.
- `H` — hypothesis, theorem target, proposed mechanism, or unverified interpretation.
- `S` — semantic, architectural, metaphorical, or design language.
- `R` — retired or demoted by correction, bug analysis, scaling, matched controls, or contradiction.

Never treat the tags as an automatic promotion ladder. Record the bridge required for any promotion.

## Seven recurrent failure modes

### 1. Specification-implementation bifurcation
The prose describes the right abstraction while the live code executes another object. Tests pass because they validate the implemented surrogate.

Countermeasures:
- executable invariants written before implementation;
- known-answer cases;
- independent reference implementation;
- requirement-to-behavior round trip.

### 2. Direction reversal
An upper bound is described as a lower bound, an estimate as a certificate, correlation as causation, or a sufficient condition as necessary.

Countermeasures:
- write inequalities explicitly;
- name the quantified object;
- state assumptions and direction in words;
- construct a minimal counterexample.

### 3. Syntactic metric gaming
Equivalent programs or representations receive different scores although the claim is semantic.

Countermeasures:
- identity and canceling-block attacks;
- alternate decompositions and compiler settings;
- gauge/frame/encoding changes;
- canonicalization only as one control, never as proof of invariance.

### 4. Tautological validation
The test verifies a property already forced by clipping, construction, filtering, or generator design.

Countermeasures:
- inspect raw preprocessed values;
- test outside the generator's home distribution;
- include negative and adversarial cases;
- distinguish construction invariants from discovered regularities.

### 5. Correlated witnesses
Specification, code, tests, and review inherit the same hidden assumption.

Countermeasures:
- independent oracle or reviewer;
- separately written reference model;
- black-box tests based on public behavior;
- external source or replication.

### 6. Scalar collapse
A heterogeneous object is compressed into one score, erasing units, uncertainty, context, or trade-offs.

Countermeasures:
- typed coordinates;
- intervals and distributions;
- Pareto or partial-order comparisons;
- preregistered causal advantage regions.

### 7. Ontological escape
A failed metric or experiment is rescued by adding richer terminology rather than testing the current object.

Countermeasures:
- explicit stop rule;
- no new layer without a measured unresolved obstruction;
- prefer the simplest adequate baseline;
- retire the interpretation when the kill condition fires.

## Verification matrix

| Risk | Minimum check |
|---|---|
| Wrong live code path | Trace entrypoint to observable output |
| Weak oracle | Analytic case or independent reference |
| Missing edge cases | Property-based generation and shrinking |
| No direct oracle | Metamorphic relations |
| Representation dependence | Equivalent-form attacks |
| Security/safety | Threat model, static analysis, fuzzing |
| Benchmark overfit | Held-out generators, graph families, seeds, and regimes |
| Resource unfairness | Compute, parameter, sampling, data-access, and tuning parity |
| Statistical overclaim | Effect size, uncertainty, multiplicity, and preregistered primary metric |
| Global drift | Round-trip coherence or cycle audit |

## Round-trip coherence record

For each edge, record the source object, transport rule, destination object, preserved invariants, transformed fields, lost information, and remainder.

1. Requirement -> formal specification
2. Formal specification -> data/model representation
3. Representation -> implementation
4. Implementation -> tests and instrumentation
5. Instrumentation -> measured result
6. Result -> interpretation
7. Interpretation -> original requirement

A local pass on every edge does not guarantee cycle consistency. Compare the returned requirement/claim with the original.

## Promotion discipline

Promote only when all are true:
- the artifact supports the exact claim;
- controls and resource parity are satisfied;
- uncertainty is quantified where applicable;
- representation attacks do not destroy the effect;
- no simpler baseline matches the result;
- the claimed evidence tag matches the artifact type;
- independent evidence exists for influential claims.

Otherwise narrow, demote, or retire the interpretation.

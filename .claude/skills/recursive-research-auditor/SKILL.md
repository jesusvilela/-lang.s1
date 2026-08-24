---
name: recursive-research-auditor
description: Adversarially audit and improve novel technical, scientific, mathematical, or software work before treating it as reliable. Use for model-generated research, repository experiments, architecture proposals, theorem or benchmark claims, peer review, implementation reviews, and long multi-round investigations where specification-implementation drift, self-authored tests, metric gaming, evidence overpromotion, unmatched controls, hidden scalar collapse, or correlated self-validation may occur. Trigger especially when the user asks to self-reflect, verify, falsify, peer-review, reproduce, harden, or convert an ambitious idea into executable evidence.
---

# Recursive Research Auditor

Apply a correction-preserving audit to the claim, specification, implementation, tests, measurements, and interpretation. Prefer a narrower supported conclusion over an elegant unsupported one.

## Core workflow

1. **Freeze the object before improving it**
   - State the exact claim, scope, intended object, observable, and decision being audited.
   - Separate source-derived content, external research, inference, hypothesis, and design language.
   - Record the current evidence tag using `P/A/M/H/S/R` as defined in `references/audit-protocol.md`.
   - Do not silently repair the claim before documenting its original form.

2. **Build the claim-to-artifact map**
   - Map each important claim to the artifact that could support or falsify it: proof, code path, dataset, test, benchmark, execution log, or external source.
   - Mark any claim with no supporting artifact as `H` or `S`.
   - Distinguish build success, theorem content, runtime behavior, measurement, and external relevance.

3. **Audit semantic direction and type**
   - Check every implication, bound, optimization direction, denominator, unit, interval, and monotonicity statement.
   - Reject language such as “certified,” “necessary,” “optimal,” or “proved” when the artifact only supplies an estimate, upper bound, sampled observation, or conditional result.
   - Forbid comparison across different units, frames, resource theories, datasets, or task definitions unless an explicit transport or normalization is supplied and its losses are recorded.
   - Prefer intervals, distributions, partial orders, or effect regions over a scalar when the object is heterogeneous.

4. **Separate specification, implementation, test, and interpretation**
   - Write the intended invariants independently of the implementation.
   - Inspect whether the live code path actually instantiates the intended object.
   - Treat tests written from the same implementation narrative as correlated evidence, not independent confirmation.
   - Require at least one of: analytic toy case, independent reference implementation, property-based invariant test, metamorphic relation, black-box oracle, or external reproduction.

5. **Attack representation dependence**
   - Test semantically equivalent representations: reordered operations, alternate decompositions, compiler settings, seeds, encodings, gauges, frames, canceling blocks, and optimized versus unoptimized forms.
   - Demand invariance where invariance is claimed.
   - If an equivalent no-op or identity transformation changes the score, classify the metric as syntax-sensitive and retire any stronger interpretation.

6. **Run matched controls and resource parity checks**
   - Compare against the simplest plausible baseline and structure-matched null.
   - Check compute, parameters, data access, oracle construction, sampling, tuning, and wall-clock cost separately.
   - Print raw values before clipping, normalization, thresholding, or aggregation.
   - Reject kill conditions that are guaranteed by the implementation, such as testing a value after forcibly clipping it into the accepted range.

7. **Perform the round-trip coherence audit**
   - Trace `requirement -> formal object -> implementation -> test -> measurement -> interpretation -> requirement`.
   - Identify where meaning changes, information is dropped, or a local patch fails to preserve the global claim.
   - Treat a loop defect as load-bearing even when every individual edge appears locally reasonable.

8. **Use independent witnesses**
   - Search current primary sources when facts, tools, standards, or software versions may have changed.
   - Prefer official documentation, original papers, standards, and direct repository artifacts.
   - When possible, use a separate model, human reviewer, independent code path, or independently generated test oracle.
   - Do not call repeated self-review independent replication.

9. **Apply preregistered decision gates**
   - State prediction, primary metric, controls, uncertainty method, kill condition, stop condition, and promotion rule before interpreting results.
   - Promote only the narrow claim that crossed its declared gate.
   - Retire a killed interpretation while preserving the measurement and correction history.
   - Do not introduce a richer ontology merely to rescue a failed claim.

10. **Enforce the stop rule**
    - Freeze further architectural lifts until the current typed object produces a reproducible, externally meaningful effect or is retired.
    - Permit a new abstraction only when a specific measured obstruction cannot be represented or resolved in the current layer.

## Execution protocol

For substantial audits, create an audit manifest using `references/manifest-schema.md`, then run:

```bash
python scripts/validate_audit_manifest.py path/to/audit-manifest.json
```

Fix all errors. Address warnings explicitly in the report; do not hide them.

For code or repository work, include at least these verification families when applicable:

- analytic known-answer cases;
- black-box functional tests;
- structural or white-box tests;
- property-based invariants;
- metamorphic/equivalence tests;
- fuzzing or adversarial generation;
- historical regression cases;
- security/threat-model checks;
- independent reproduction or reference implementation.

## Required output

Use the structure in `references/output-template.md`. Always include:

- a one-paragraph verdict;
- a claim and evidence ledger;
- the strongest surviving result;
- the most damaging obstruction;
- specification-implementation-test drift findings;
- matched-control and resource-parity findings;
- representation or equivalence attacks;
- what is proved, measured, hypothesized, semantic, or retired;
- one bounded next experiment with explicit kill and stop conditions.

## Non-negotiable rules

- Do not equate passing tests with proving the intended claim.
- Do not let the same narrative author specification, implementation, oracle, and promotion without labeling the correlation.
- Do not infer a lower bound from an implemented upper-bound algorithm.
- Do not infer causal benefit from complexity, novelty, dimensionality, quantum notation, or mathematical ornament.
- Do not compare heterogeneous quantities merely because they are stored as numbers.
- Do not conceal negative results by escalating to a richer metaphor.
- Do not claim independent verification unless the witness is genuinely independent in data, code path, assumptions, or authorship.
- Preserve correction history and name the exact claim that was narrowed or retired.

## References

- Read `references/audit-protocol.md` for evidence tags, common failure patterns, and test selection.
- Read `references/manifest-schema.md` before creating or validating an audit manifest.
- Read `references/output-template.md` before writing the final audit.
- Read `references/source-notes.md` when selecting external verification methods or sources.

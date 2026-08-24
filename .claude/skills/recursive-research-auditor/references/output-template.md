# Audit output template

# [Object or claim audited]

## Verdict
One paragraph stating what survives, what fails, and the current confidence boundary.

## Claim and evidence ledger
| Claim | Before | Artifact | Audit result | After |
|---|---:|---|---|---:|

## Strongest surviving result
State the narrowest important result that remains supported. Include scope, assumptions, uncertainty, and why the controls are adequate.

## Load-bearing obstruction
State the most damaging flaw. Distinguish mathematical, semantic, implementation, measurement, statistical, and operational failures.

## Specification -> implementation -> test audit
Describe the intended object, the live object, what the tests actually establish, and any divergence.

## Direction, type, and metric audit
Check bound direction, units, intervals, clipping, aggregation, comparison legality, and representation invariance.

## Controls and resource parity
Report matched baselines, negative controls, compute/parameter/sampling/data parity, and any hidden oracle or preprocessing cost.

## Independent-witness status
Name genuinely independent witnesses and identify correlated evidence that must not be counted twice.

## Round-trip coherence
Summarize drift around requirement -> formalization -> implementation -> test -> result -> interpretation -> requirement.

## Corrections and retirements
List the exact claims narrowed, demoted, or retired. Preserve useful measurements separately from killed interpretations.

## Next bounded experiment
- Object:
- Prediction:
- Primary metric or effect region:
- Controls:
- Representation attacks:
- Kill condition:
- Stop condition:
- Promotion rule:

## Final evidence map
Summarize all important objects under `P/A/M/H/S/R`.

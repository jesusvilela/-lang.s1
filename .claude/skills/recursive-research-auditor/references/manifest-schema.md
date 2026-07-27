# Audit manifest schema

Create a UTF-8 JSON object with these top-level fields.

```json
{
  "task_id": "short-stable-id",
  "claim": {
    "text": "Exact claim being audited",
    "scope": "Domain and limits",
    "status_before": "H",
    "assumptions": ["..."],
    "forbidden_promotions": ["What this result must not be used to claim"]
  },
  "specification": {
    "intended_object": "Formal or operational object",
    "invariants": ["..."],
    "known_answer_cases": ["..."]
  },
  "implementation": {
    "artifact": "path, URL, or identifier",
    "commit": "commit or version",
    "environment": "runtime and dependencies",
    "live_entrypoint": "actual executed path",
    "representation": "encoding or model"
  },
  "metric": {
    "name": "metric name",
    "type": "scalar|interval|distribution|partial_order|typed_tuple",
    "units": "declared units or dimensionless",
    "direction": "higher_is_better|lower_is_better|two_sided|partial_order",
    "raw_before_clipping": true,
    "semantic_invariance_claimed": true,
    "equivalence_attacks": ["identity/canceling/alternate representation cases"]
  },
  "tests": {
    "black_box": ["..."],
    "structural": ["..."],
    "property_based": ["..."],
    "metamorphic": ["..."],
    "fuzzing": ["..."],
    "historical": ["..."]
  },
  "controls": {
    "matched_baselines": ["..."],
    "negative_controls": ["..."],
    "compute_parity": "method",
    "parameter_parity": "method or not applicable",
    "sampling_parity": "method or not applicable",
    "data_access_parity": "method or not applicable"
  },
  "preregistration": {
    "prediction": "direction and expected range",
    "primary_metric": "single primary metric or declared effect region",
    "uncertainty_method": "confidence interval, posterior, proof obligation, etc.",
    "kill_condition": "condition that retires the interpretation",
    "stop_condition": "condition that stops further ontology expansion",
    "promotion_rule": "exact evidence transition"
  },
  "evidence": {
    "primary_sources": ["..."],
    "execution_records": ["..."],
    "independent_witnesses": [
      {"name": "witness", "origin": "different author/code/data/assumptions", "artifact": "..."}
    ],
    "claim_to_artifact_map": ["claim -> artifact"]
  },
  "round_trip": {
    "edges": [
      {
        "from": "requirement",
        "to": "formal specification",
        "preserved": ["..."],
        "transformed": ["..."],
        "lost": ["..."],
        "remainder": ["..."]
      }
    ]
  },
  "result": {
    "observed": "result",
    "effect_size": "effect or not applicable",
    "uncertainty": "uncertainty or proof status",
    "status_after": "P|A|M|H|S|R",
    "retired_claims": ["..."],
    "active_remainder": ["open questions"]
  }
}
```

Use `"not applicable: reason"` instead of omitting a field. Empty required arrays are allowed only when accompanied by an explicit reason in a nearby string field.

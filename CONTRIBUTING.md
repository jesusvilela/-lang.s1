# Contributing to §-LANG S1

§-LANG S1 is a research alpha with a deliberately narrow executable Core.
Contributions are welcome when they make the specification, implementation, or
evidence boundary more precise without silently widening authority.

## The contribution contract

A change to the bounded S1 Core should update every affected layer:

1. the normative surface in `core/grammar.ebnf` or `core/README.md`;
2. the reference implementation under `slang_core/`;
3. unit or conformance cases that can falsify the change;
4. `CLAIMS.yaml` when the supported claim changes;
5. `VERIFICATION.md` or `STATUS.md` when the publication boundary changes.

A parser feature is not automatically an operator semantic. An operator semantic
is not automatically a theorem or measurement.

## Independent implementations

Independent implementations are explicitly encouraged. They do not need to
derive from the Python reference Core. Conformance should be argued from behavior
against the published S1 contract and conformance cases.

If you build an independent implementation, an issue or pull request linking the
implementation and its conformance results is useful even when no code is being
contributed to this repository.

## Evidence discipline

Use the repository's canonical evidence tags:

- `P` — proved or definitionally closed by an exact artifact;
- `A` — assumption, surrogate, conditional bridge, or externally dependent;
- `M` — bounded measurement with data, controls, uncertainty, and provenance;
- `H` — hypothesis or theorem target;
- `S` — semantic, architectural, or design language;
- `R` — retired or demoted interpretation.

Do not promote a claim merely because syntax parses, a test passes, or a token
uses mathematical notation.

## Pull requests

Keep changes bounded and explain:

- what contract changes;
- what remains unchanged;
- which test or artifact could falsify the change;
- whether any evidence tag changes.

Avoid combining a language-surface change with unrelated research expansion.

## License

Unless explicitly stated otherwise, contributions intentionally submitted for
inclusion are accepted under the Apache License 2.0, consistent with Section 5
of the repository license.

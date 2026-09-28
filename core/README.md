# §-LANG S1 Core

The Core is intentionally smaller than the research-language family around it.

```text
§-LANG
├── Core          bounded executable semantics
├── Annotation    evidence / provenance metadata
├── Geometry      research coordinates and sectional models
├── Packs         generated research corpora
└── Research      hypotheses · measurements · theorem targets
```

## Contract

Implemented here:

- one bounded grammar: [`grammar.ebnf`](grammar.ebnf);
- one independent repository-local parser;
- one minimal evaluator;
- literal, binding, emission, equality-assertion, and evidence-annotation statements;
- a closed operator set: `add`, `sub`, `mul`, `div`, `neg`, `concat`,
  `list`, `len`, `identity`, `canon`;
- six canonical programs, including a negative control and a no-assertion case;
- one manifest-driven conformance command;
- machine-readable JSON results.

Not implemented by S1 Core:

- the historical v5 runtime surface;
- geometric, sheaf, topos, Hamiltonian, or physical semantics;
- theorem checking or a proof kernel;
- transport semantics beyond ordinary data operations;
- execution of generated packs;
- claims that a `P/A/M/H/S/R` annotation is true merely because it parses.

A parsed `§evidence` statement is metadata. It preserves a claim identifier,
evidence tag, and text; it does not validate the claim.

## Run

```bash
python3 -m slang_core core/examples/01_bindings.s1 --json
python3 -m slang_core.conformance --json
```

The conformance report itself uses four statuses:

- `PASS` — an implemented case behaved as specified;
- `FAIL` — an implemented case contradicted its expected result;
- `NOT_APPLICABLE` — the case is explicitly outside S1 Core;
- `NOT_TESTED` — the capability is in scope as a future bridge but no test exists.

Absence is never promoted to `PASS`.

## Evidence boundary

At `L_syn`, the grammar is definitionally specified by this directory. At
`L_op`, the parser/evaluator are executable repository artifacts and are
checked by unit and conformance tests. Neither fact promotes the larger
`§-LANG` research family to theoremhood, empirical validity, or physical
realizability.

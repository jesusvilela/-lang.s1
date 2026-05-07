# Chomsky Hierarchy Practical Verification Report

- Source: `LANG.v1.2.0.unified_geometry.lang`
- Scope: practical evidence for Chomsky-hierarchy classification; not a formal proof

## Checks
- ✅ `grammar_block_present`
- ✅ `productions_extracted`
- ✅ `surface_grammar_is_context_free_shape`
- ✅ `surface_grammar_has_nonregular_recursion_evidence`
- ✅ `recursive_witnesses_parse`
- ✅ `semantic_type0_markers_present`

## Lexical layer
- Classification evidence: **Type-3 / regular**
- `var = alphanumeric_identifier` is a regular-token description
- numeric field/salience literals are matched by finite regular patterns in existing validators

## Surface syntax layer
- Classification evidence: **Type-2 / context-free**
- Context-free production shape: `True`
- Non-regular recursion/nesting evidence: `True`

### Non-regular evidence from declared productions
- `backquote = `term marks_section_active` nests or embeds nonterminal `term`
- `paren = (term) grouping` nests or embeds nonterminal `term`
- `programa = sección programa` contains multiple nonterminals on the RHS
- `sección = canon(term)` nests or embeds nonterminal `term`
- `sección = emit(term)` nests or embeds nonterminal `term`
- `sección = fix(term)` nests or embeds nonterminal `term`
- `sección = §.(term)` nests or embeds nonterminal `term`
- `sección = §S{fields}` nests or embeds nonterminal `fields`
- `term = FFT(term)` nests or embeds nonterminal `term`
- `term = canon(term)` nests or embeds nonterminal `term`
- `term = emit(term)` nests or embeds nonterminal `term`
- `term = fix(term)` nests or embeds nonterminal `term`
- `term = term term` contains multiple nonterminals on the RHS
- `term = §.(term)` nests or embeds nonterminal `term`
- `term = λvar.term` contains multiple nonterminals on the RHS

### Recursive witness terms

| Depth | Term | Recursive parser | Single-wrap regular regex |
|-------|------|------------------|---------------------------|
| 1 | `§.(a)` | ✅ | ✅ |
| 2 | `§.(§.(a))` | ✅ | ❌ |
| 3 | `§.(§.(§.(a)))` | ✅ | ❌ |
| 4 | `§.(§.(§.(§.(a))))` | ✅ | ❌ |
| 5 | `§.(§.(§.(§.(§.(a)))))` | ✅ | ❌ |
| 6 | `§.(§.(§.(§.(§.(§.(a))))))` | ✅ | ❌ |

## Semantic/computational layer
- Classification evidence: **Type-0 / recursively enumerable markers present**
- ✅ `lambda_symbol_present`
- ✅ `fixpoint_operator_present`
- ✅ `turing_encoding_block_present`
- ✅ `declared_computability_claim_present`

> Limitation: The repository contains symbolic `fix`, λ-calculus, and Turing-encoding declarations, but no executable interpreter or proof checker establishing full semantic equivalence.

## Limitations
- This script does not prove that the full language is exactly Type-2 or Type-0.
- It verifies declared grammar shape and concrete recursive-syntax witnesses only.
- Semantic claims about self-reference, prime-other resonance, and LLM-induced expansion remain unverified by executable evidence.

#!/usr/bin/env python3
"""Practical Chomsky-hierarchy checks for the §-LANG surface grammar.

This script checks executable evidence only. It classifies the declared GRAMMAR
block syntactically and records symbolic evidence for computational semantics;
it does not prove mathematical, semantic, or LLM-induced claims.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SOURCE = Path("LANG.v1.2.0.unified_geometry.lang")
OUT_JSON = Path("research/chomsky_verification_report.json")
OUT_MD = Path("research/chomsky_verification_report.md")

BLOCK_HEADER_RE = re.compile(r"^§\|LANG\|([A-Z_]+)\{")
IDENT_PATTERN = r"[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*"
IDENT_RE = re.compile(rf"^{IDENT_PATTERN}$")
SHALLOW_SECTION_RE = re.compile(r"^§\.\([A-Za-z_][A-Za-z0-9_]*\)$")


@dataclass
class Production:
    lhs: str
    alternatives: list[str]


def extract_block(lines: list[str], block: str) -> list[str]:
    in_block = False
    body: list[str] = []
    for line in lines:
        header = BLOCK_HEADER_RE.match(line.strip())
        if header and header.group(1) == block:
            in_block = True
            continue
        if in_block and line.strip() == "}":
            return body
        if in_block:
            body.append(line.rstrip())
    return body


def parse_productions(block_lines: list[str]) -> list[Production]:
    productions: list[Production] = []
    current_lhs: str | None = None
    rhs_buffer = ""

    def flush() -> None:
        nonlocal current_lhs, rhs_buffer
        if current_lhs is None:
            return
        alternatives = [
            part.strip()
            # Avoid splitting the surface pipe operator `|>` as an alternative separator.
            for part in re.split(r"\s*\|(?!>)\s*", rhs_buffer)
            if part.strip()
        ]
        productions.append(Production(lhs=current_lhs, alternatives=alternatives))
        current_lhs = None
        rhs_buffer = ""

    for raw_line in block_lines:
        line = raw_line.strip()
        if not line:
            continue
        if "=" in line and not line.startswith("|"):
            candidate_lhs, rhs = line.split("=", 1)
            lhs = candidate_lhs.strip()
            if IDENT_RE.match(lhs):
                flush()
                current_lhs = lhs
                rhs_buffer = rhs.strip()
                continue
        if current_lhs is not None:
            rhs_buffer += " " + line
    flush()
    return productions


def matching_outer_call(expr: str, prefix: str) -> str | None:
    if not expr.startswith(prefix + "(") or not expr.endswith(")"):
        return None
    start = len(prefix)
    depth = 0
    for index, char in enumerate(expr[start:], start=start):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(expr) - 1:
                return None
    return expr[start + 1 : -1] if depth == 0 else None


def matching_outer_parens(expr: str) -> str | None:
    return matching_outer_call(expr, "")


def parse_surface_term(expr: str) -> bool:
    """Recognize a small recursive subset declared by the GRAMMAR block."""
    expr = expr.strip()
    if IDENT_RE.match(expr):
        return True
    if expr.startswith("λ") and "." in expr:
        var, body = expr[1:].split(".", 1)
        return IDENT_RE.match(var) is not None and parse_surface_term(body)
    for prefix in ("fix", "emit", "canon", "FFT", "§."):
        inner = matching_outer_call(expr, prefix)
        if inner is not None:
            return parse_surface_term(inner)
    inner = matching_outer_parens(expr)
    return parse_surface_term(inner) if inner is not None else False


def nonterminal_occurrences(rhs: str, nonterminals: set[str]) -> list[tuple[str, int]]:
    occurrences: list[tuple[str, int]] = []
    for nt in nonterminals:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_À-ÿ]){re.escape(nt)}(?![A-Za-z0-9_À-ÿ])"
        )
        for match in pattern.finditer(rhs):
            occurrences.append((nt, match.start()))
    return sorted(occurrences, key=lambda item: item[1])


def classify_grammar(productions: list[Production]) -> dict:
    nonterminals = {production.lhs for production in productions}
    context_free_lhs = all(IDENT_RE.match(p.lhs) for p in productions)

    nonregular_reasons: list[str] = []
    for production in productions:
        for alt in production.alternatives:
            occurrences = nonterminal_occurrences(alt, nonterminals)
            if len(occurrences) > 1:
                nonregular_reasons.append(
                    f"`{production.lhs} = {alt}` contains multiple nonterminals on the RHS"
                )
            elif occurrences:
                nt, pos = occurrences[0]
                at_left_edge = pos == 0
                at_right_edge = pos + len(nt) == len(alt)
                wrapped_recursive = "(" in alt[:pos] and ")" in alt[pos + len(nt) :]
                if wrapped_recursive or not (at_left_edge or at_right_edge):
                    nonregular_reasons.append(
                        f"`{production.lhs} = {alt}` nests or embeds nonterminal `{nt}`"
                    )

    return {
        "type_2_context_free_shape": context_free_lhs,
        "not_type_3_regular_surface_evidence": bool(nonregular_reasons),
        "nonregular_evidence": sorted(set(nonregular_reasons)),
    }


def build_report(source: Path) -> dict:
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()
    grammar_lines = extract_block(lines, "GRAMMAR")
    productions = parse_productions(grammar_lines)
    grammar_classification = classify_grammar(productions)

    nested_witnesses = []
    term = "a"
    # Depths 1-6 give bounded, reproducible witnesses for recursive nesting:
    # enough to demonstrate the unbounded pattern's shape while keeping the
    # report compact and avoiding any claim of a formal all-depth proof.
    for depth in range(1, 7):
        term = f"§.({term})"
        nested_witnesses.append(
            {
                "depth": depth,
                "term": term,
                "recursive_parser_accepts": parse_surface_term(term),
                "single_wrap_regular_regex_accepts": SHALLOW_SECTION_RE.match(term) is not None,
            }
        )

    semantic_evidence = {
        "lambda_symbol_present": "λ" in text or "lambda" in text,
        "fixpoint_operator_present": "fix(" in text or "fixpoint" in text,
        "turing_encoding_block_present": bool(extract_block(lines, "TURING_ENCODING")),
        "declared_computability_claim_present": "every_computable_f_expressible" in text,
    }

    checks = {
        "grammar_block_present": bool(grammar_lines),
        "productions_extracted": bool(productions),
        "surface_grammar_is_context_free_shape": grammar_classification["type_2_context_free_shape"],
        "surface_grammar_has_nonregular_recursion_evidence": grammar_classification[
            "not_type_3_regular_surface_evidence"
        ],
        "recursive_witnesses_parse": all(w["recursive_parser_accepts"] for w in nested_witnesses),
        "semantic_type0_markers_present": all(semantic_evidence.values()),
    }

    return {
        "source": str(source),
        "scope": "practical evidence for Chomsky-hierarchy classification; not a formal proof",
        "productions": [
            {"lhs": production.lhs, "alternatives": production.alternatives}
            for production in productions
        ],
        "classification_evidence": {
            "lexical_layer": {
                "classification": "Type-3 / regular evidence",
                "evidence": [
                    "`var = alphanumeric_identifier` is a regular-token description",
                    "numeric field/salience literals are matched by finite regular patterns in existing validators",
                ],
            },
            "surface_syntax_layer": {
                "classification": "Type-2 / context-free evidence",
                **grammar_classification,
                "nested_term_witnesses": nested_witnesses,
            },
            "semantic_layer": {
                "classification": "Type-0 / recursively enumerable evidence only",
                "evidence": semantic_evidence,
                "limitation": "The repository contains symbolic `fix`, λ-calculus, and Turing-encoding declarations, but no executable interpreter or proof checker establishing full semantic equivalence.",
            },
        },
        "checks": checks,
        "limitations": [
            "This script does not prove that the full language is exactly Type-2 or Type-0.",
            "It verifies declared grammar shape and concrete recursive-syntax witnesses only.",
            "Semantic claims about self-reference, prime-other resonance, and LLM-induced expansion remain unverified by executable evidence.",
        ],
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# Chomsky Hierarchy Practical Verification Report",
        "",
        f"- Source: `{report['source']}`",
        f"- Scope: {report['scope']}",
        "",
        "## Checks",
    ]
    for name, ok in report["checks"].items():
        icon = "✅" if ok else "❌"
        lines.append(f"- {icon} `{name}`")

    lines.extend(
        [
            "",
            "## Lexical layer",
            "- Classification evidence: **Type-3 / regular**",
        ]
    )
    for item in report["classification_evidence"]["lexical_layer"]["evidence"]:
        lines.append(f"- {item}")

    surface = report["classification_evidence"]["surface_syntax_layer"]
    lines.extend(
        [
            "",
            "## Surface syntax layer",
            "- Classification evidence: **Type-2 / context-free**",
            f"- Context-free production shape: `{surface['type_2_context_free_shape']}`",
            f"- Non-regular recursion/nesting evidence: `{surface['not_type_3_regular_surface_evidence']}`",
            "",
            "### Non-regular evidence from declared productions",
        ]
    )
    for reason in surface["nonregular_evidence"]:
        lines.append(f"- {reason}")

    lines.extend(
        [
            "",
            "### Recursive witness terms",
            "",
            "| Depth | Term | Recursive parser | Single-wrap regular regex |",
            "|-------|------|------------------|---------------------------|",
        ]
    )
    for witness in surface["nested_term_witnesses"]:
        parser_ok = "✅" if witness["recursive_parser_accepts"] else "❌"
        regex_ok = "✅" if witness["single_wrap_regular_regex_accepts"] else "❌"
        lines.append(
            f"| {witness['depth']} | `{witness['term']}` | {parser_ok} | {regex_ok} |"
        )

    semantic = report["classification_evidence"]["semantic_layer"]
    lines.extend(
        [
            "",
            "## Semantic/computational layer",
            "- Classification evidence: **Type-0 / recursively enumerable markers present**",
        ]
    )
    for name, ok in semantic["evidence"].items():
        icon = "✅" if ok else "❌"
        lines.append(f"- {icon} `{name}`")
    lines.extend(["", f"> Limitation: {semantic['limitation']}", "", "## Limitations"])
    for item in report["limitations"]:
        lines.append(f"- {item}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report(SOURCE)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(report)
    print(f"JSON → {OUT_JSON}")
    print(f"MD   → {OUT_MD}")
    failed = [name for name, ok in report["checks"].items() if not ok]
    if failed:
        print(f"Failed checks: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

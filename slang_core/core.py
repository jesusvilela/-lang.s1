"""A deliberately small, repository-local executable core for §-LANG S1.

This module implements only the grammar in core/grammar.ebnf. It does not
implement the historical v5 runtime surface, geometric semantics, proof
semantics, or the generated research packs.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any


STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_NOT_APPLICABLE = "NOT_APPLICABLE"
STATUS_NOT_TESTED = "NOT_TESTED"
EVIDENCE_TAGS = frozenset("PAMHSR")


class CoreSyntaxError(ValueError):
    """Raised when source is outside the bounded S1 grammar."""


class CoreRuntimeError(ValueError):
    """Raised when a valid S1 expression cannot be evaluated."""


@dataclass(frozen=True)
class Expr:
    kind: str
    value: Any = None
    args: tuple["Expr", ...] = ()


@dataclass(frozen=True)
class Statement:
    kind: str
    line: int
    name: str | None = None
    expr: Expr | None = None
    left: Expr | None = None
    right: Expr | None = None
    tag: str | None = None
    text: str | None = None


_TOKEN = re.compile(
    r"""\s*(?:
        (?P<number>-?(?:\d+(?:\.\d*)?|\.\d+))
      | (?P<string>"(?:\\.|[^"\\])*")
      | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
      | (?P<lpar>\()
      | (?P<rpar>\))
      | (?P<comma>,)
    )""",
    re.VERBOSE,
)


def _tokenize(text: str) -> list[tuple[str, str]]:
    text = text.strip(" \\t")
    if not text:
        raise CoreSyntaxError("empty expression")
    out: list[tuple[str, str]] = []
    pos = 0
    while pos < len(text):
        match = _TOKEN.match(text, pos)
        if match is None:
            raise CoreSyntaxError(f"unexpected token near {text[pos:pos + 20]!r}")
        kind = match.lastgroup
        assert kind is not None
        out.append((kind, match.group(kind)))
        pos = match.end()
    return out


class _ExprParser:
    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self, kind: str | None = None) -> bool:
        if self.pos >= len(self.tokens):
            return False
        return kind is None or self.tokens[self.pos][0] == kind

    def _take(self, kind: str) -> str:
        if not self._peek(kind):
            found = self.tokens[self.pos][0] if self._peek() else "end of expression"
            raise CoreSyntaxError(f"expected {kind}, found {found}")
        value = self.tokens[self.pos][1]
        self.pos += 1
        return value

    def parse(self) -> Expr:
        expr = self._atom()
        if self.pos != len(self.tokens):
            raise CoreSyntaxError(f"unexpected trailing token {self.tokens[self.pos][1]!r}")
        return expr

    def _atom(self) -> Expr:
        if self._peek("number"):
            raw = self._take("number")
            return Expr("literal", float(raw) if "." in raw else int(raw))

        if self._peek("string"):
            raw = self._take("string")
            try:
                return Expr("literal", json.loads(raw))
            except json.JSONDecodeError as exc:
                raise CoreSyntaxError(f"invalid JSON string literal: {exc.msg}") from exc

        if self._peek("ident"):
            name = self._take("ident")
            if name == "true":
                return Expr("literal", True)
            if name == "false":
                return Expr("literal", False)
            if name == "null":
                return Expr("literal", None)
            if not self._peek("lpar"):
                return Expr("name", name)

            self._take("lpar")
            args: list[Expr] = []
            if not self._peek("rpar"):
                while True:
                    args.append(self._atom())
                    if self._peek("comma"):
                        self._take("comma")
                        continue
                    break
            self._take("rpar")
            return Expr("call", name, tuple(args))

        found = self.tokens[self.pos][1] if self._peek() else "end of expression"
        raise CoreSyntaxError(f"expected expression, found {found!r}")


def parse_expr(text: str) -> Expr:
    return _ExprParser(_tokenize(text)).parse()


def _split_top_level_equality(text: str) -> tuple[str, str]:
    depth = 0
    in_string = False
    escaped = False

    for i, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                raise CoreSyntaxError("unbalanced closing parenthesis")
        elif char == "=" and i + 1 < len(text) and text[i + 1] == "=" and depth == 0:
            left = text[:i].strip()
            right = text[i + 2 :].strip()
            if not left or not right:
                raise CoreSyntaxError("§assert requires expressions on both sides of ==")
            return left, right

    raise CoreSyntaxError("§assert requires a top-level == comparison")


def parse_program(source: str) -> list[Statement]:
    statements: list[Statement] = []

    for line_no, raw in enumerate(source.splitlines(), start=1):
        line = raw.strip(" \\t\\r\\n")
        if not line or line.startswith("//"):
            continue

        match = re.fullmatch(r"§let\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)", line)
        if match:
            statements.append(
                Statement("let", line_no, name=match.group(1), expr=parse_expr(match.group(2)))
            )
            continue

        if line.startswith("§emit "):
            statements.append(Statement("emit", line_no, expr=parse_expr(line[6:].strip())))
            continue

        if line.startswith("§assert "):
            left, right = _split_top_level_equality(line[8:].strip())
            statements.append(
                Statement("assert", line_no, left=parse_expr(left), right=parse_expr(right))
            )
            continue

        match = re.fullmatch(
            r"§evidence\s+([A-Za-z0-9_.-]+)\s+\[([PAMHSR])\]\s+(.+)",
            line,
        )
        if match:
            try:
                text = json.loads(match.group(3))
            except json.JSONDecodeError as exc:
                raise CoreSyntaxError(
                    f"line {line_no}: §evidence text must be a JSON string literal"
                ) from exc
            if not isinstance(text, str):
                raise CoreSyntaxError(
                    f"line {line_no}: §evidence text must be a JSON string literal"
                )
            statements.append(
                Statement(
                    "evidence",
                    line_no,
                    name=match.group(1),
                    tag=match.group(2),
                    text=text,
                )
            )
            continue

        raise CoreSyntaxError(f"line {line_no}: unsupported S1 statement {line!r}")

    if not statements:
        raise CoreSyntaxError("program contains no S1 statements")

    return statements


def _require_arity(name: str, args: list[Any], count: int) -> None:
    if len(args) != count:
        raise CoreRuntimeError(f"{name} expects {count} argument(s), got {len(args)}")


def _require_number(name: str, value: Any) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CoreRuntimeError(f"{name} expects numeric arguments")
    return value


def _call(name: str, args: list[Any]) -> Any:
    if name in {"add", "sub", "mul", "div"}:
        _require_arity(name, args, 2)
        a = _require_number(name, args[0])
        b = _require_number(name, args[1])
        if name == "add":
            return a + b
        if name == "sub":
            return a - b
        if name == "mul":
            return a * b
        if b == 0:
            raise CoreRuntimeError("div by zero")
        return a / b

    if name == "neg":
        _require_arity(name, args, 1)
        return -_require_number(name, args[0])

    if name == "concat":
        if not args or any(not isinstance(item, str) for item in args):
            raise CoreRuntimeError("concat expects one or more string arguments")
        return "".join(args)

    if name == "list":
        return list(args)

    if name == "len":
        _require_arity(name, args, 1)
        if not isinstance(args[0], (str, list)):
            raise CoreRuntimeError("len expects a string or list")
        return len(args[0])

    if name == "identity":
        _require_arity(name, args, 1)
        return args[0]

    if name == "canon":
        _require_arity(name, args, 1)
        try:
            return json.dumps(
                args[0],
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
        except (TypeError, ValueError) as exc:
            raise CoreRuntimeError(f"canon cannot encode value: {exc}") from exc

    raise CoreRuntimeError(f"unknown S1 operator {name!r}")


def _eval_expr(expr: Expr, env: dict[str, Any]) -> Any:
    if expr.kind == "literal":
        return expr.value
    if expr.kind == "name":
        if expr.value not in env:
            raise CoreRuntimeError(f"unbound name {expr.value!r}")
        return env[expr.value]
    if expr.kind == "call":
        args = [_eval_expr(arg, env) for arg in expr.args]
        return _call(str(expr.value), args)
    raise CoreRuntimeError(f"unknown expression kind {expr.kind!r}")


def evaluate_program(statements: list[Statement]) -> dict[str, Any]:
    env: dict[str, Any] = {}
    emissions: list[Any] = []
    assertions: list[dict[str, Any]] = []
    evidence: list[dict[str, str]] = []

    for statement in statements:
        if statement.kind == "let":
            assert statement.name is not None and statement.expr is not None
            env[statement.name] = _eval_expr(statement.expr, env)
        elif statement.kind == "emit":
            assert statement.expr is not None
            emissions.append(_eval_expr(statement.expr, env))
        elif statement.kind == "assert":
            assert statement.left is not None and statement.right is not None
            left = _eval_expr(statement.left, env)
            right = _eval_expr(statement.right, env)
            assertions.append(
                {
                    "line": statement.line,
                    "pass": left == right,
                    "left": left,
                    "right": right,
                }
            )
        elif statement.kind == "evidence":
            assert statement.name is not None
            assert statement.tag in EVIDENCE_TAGS
            assert statement.text is not None
            evidence.append(
                {
                    "id": statement.name,
                    "tag": statement.tag,
                    "text": statement.text,
                }
            )
        else:
            raise CoreRuntimeError(f"unknown statement kind {statement.kind!r}")

    if not assertions:
        status = STATUS_NOT_TESTED
    elif all(item["pass"] for item in assertions):
        status = STATUS_PASS
    else:
        status = STATUS_FAIL

    return {
        "schema": "slang.s1.core.result.v1",
        "status": status,
        "emissions": emissions,
        "assertions": assertions,
        "evidence": evidence,
        "bindings": env,
    }


def run_source(source: str) -> dict[str, Any]:
    return evaluate_program(parse_program(source))

"""Command-line runner for the bounded §-LANG S1 Core."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .core import CoreRuntimeError, CoreSyntaxError, run_source


def _error_payload(exc: Exception) -> dict[str, object]:
    return {
        "schema": "slang.s1.core.result.v1",
        "status": "FAIL",
        "emissions": [],
        "assertions": [],
        "evidence": [],
        "bindings": {},
        "errors": [str(exc)],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a bounded §-LANG S1 Core program.")
    parser.add_argument("program", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    try:
        result = run_source(args.program.read_text(encoding="utf-8"))
    except (OSError, CoreSyntaxError, CoreRuntimeError) as exc:
        result = _error_payload(exc)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"status: {result['status']}")
        for index, value in enumerate(result.get("emissions", []), start=1):
            print(f"emit[{index}]: {value!r}")
        for item in result.get("assertions", []):
            marker = "PASS" if item["pass"] else "FAIL"
            print(f"assert line {item['line']}: {marker}")
        for err in result.get("errors", []):
            print(f"error: {err}", file=sys.stderr)

    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())

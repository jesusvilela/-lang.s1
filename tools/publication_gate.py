#!/usr/bin/env python3
"""Bounded publication gate for §-LANG.

This gate checks repository integrity and evidence-governance hygiene. It does
not establish semantic correctness, theorem validity, or empirical truth.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

MERGE_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
MANDATORY_FILES = (
    "README.md",
    "STATUS.md",
    "VERIFICATION.md",
    "RUNTIME_CAPABILITIES.md",
    "CLAIMS.yaml",
)
LEGACY_PROFILE_HINTS = (
    "unified_geometry",
    "tower.geom",
    "substrate_realization",
    "recursive_sectional",
    "actor_critic",
    "topos_ai",
    "chomsky_hyperdim",
    "DIALECTS",
)
AUTHORITY_WORDS = ("PROVED", "EXECUTABLE", "MEASURED", "UNIVERSAL", "CERTIFIED")


@dataclass
class Finding:
    level: str
    check: str
    path: str
    detail: str


def tracked_text_files(root: Path) -> list[Path]:
    """Return tracked text-like files, falling back to a conservative scan."""
    try:
        output = subprocess.check_output(
            ["git", "ls-files"], cwd=root, text=True, stderr=subprocess.DEVNULL
        )
        paths = [root / line for line in output.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        paths = [path for path in root.rglob("*") if path.is_file()]

    allowed = {".md", ".py", ".lang", ".yaml", ".yml", ".json", ".toml", ".txt"}
    return [path for path in paths if path.suffix.lower() in allowed]


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def source_commit(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def audit(root: Path) -> dict:
    findings: list[Finding] = []

    for relative in MANDATORY_FILES:
        path = root / relative
        if not path.exists():
            findings.append(Finding("ERROR", "mandatory_file", relative, "missing"))

    for path in tracked_text_files(root):
        text = read_text(path)
        if text is None:
            continue
        for marker in MERGE_MARKERS:
            if marker in text:
                findings.append(
                    Finding(
                        "ERROR",
                        "merge_marker",
                        str(path.relative_to(root)),
                        f"contains {marker}",
                    )
                )

    claims_path = root / "CLAIMS.yaml"
    claims_text = read_text(claims_path) or ""
    if "promotion_rules:" not in claims_text or "claims:" not in claims_text:
        findings.append(
            Finding(
                "ERROR",
                "claim_ledger_shape",
                "CLAIMS.yaml",
                "missing promotion_rules or claims section",
            )
        )

    lang_files = sorted(root.glob("*.lang"))
    if not lang_files:
        findings.append(Finding("ERROR", "language_sources", ".", "no root .lang files"))

    for path in lang_files:
        text = read_text(path) or ""
        legacy = any(hint in path.name for hint in LEGACY_PROFILE_HINTS)
        explicit_pack = bool(re.search(r"^§PACK\s+", text, flags=re.MULTILINE))
        if not legacy and not explicit_pack:
            findings.append(
                Finding(
                    "ERROR",
                    "grammar_identity",
                    path.name,
                    "neither a recognized legacy profile nor an explicit §PACK",
                )
            )
        if explicit_pack and "§VERSION" not in text:
            findings.append(
                Finding("ERROR", "pack_version", path.name, "§PACK lacks §VERSION")
            )

        section_count = len(re.findall(r"^§S\{", text, flags=re.MULTILINE))
        if section_count == 0:
            findings.append(
                Finding(
                    "INFO",
                    "section_checks",
                    path.name,
                    "no §S section points: geometric section checks are NOT_APPLICABLE",
                )
            )

        used_authority = [word for word in AUTHORITY_WORDS if word in text]
        if used_authority and path.name not in claims_text:
            findings.append(
                Finding(
                    "WARNING",
                    "authority_ledger",
                    path.name,
                    "authority words present but source path is not named in CLAIMS.yaml: "
                    + ", ".join(used_authority),
                )
            )

    errors = [finding for finding in findings if finding.level == "ERROR"]
    warnings = [finding for finding in findings if finding.level == "WARNING"]
    infos = [finding for finding in findings if finding.level == "INFO"]

    return {
        "gate": "§-LANG publication integrity v0.1",
        "source_commit": source_commit(root),
        "scope": "repository integrity and evidence-governance hygiene only",
        "status": "PASS" if not errors else "FAIL",
        "counts": {
            "errors": len(errors),
            "warnings": len(warnings),
            "info": len(infos),
        },
        "findings": [asdict(finding) for finding in findings],
        "forbidden_interpretations": [
            "semantic correctness",
            "mathematical proof",
            "runtime completeness",
            "empirical universality",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--json", type=Path, default=Path("research/publication_gate.json")
    )
    args = parser.parse_args()

    root = args.root.resolve()
    report = audit(root)
    output_path = root / args.json
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    counts = report["counts"]
    print(
        f"[{report['status']}] publication gate: "
        f"{counts['errors']} error(s), {counts['warnings']} warning(s), "
        f"{counts['info']} informational finding(s)"
    )
    for finding in report["findings"]:
        print(
            f"{finding['level']}: {finding['check']} "
            f"[{finding['path']}] — {finding['detail']}"
        )
    print(f"Report → {output_path.relative_to(root)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

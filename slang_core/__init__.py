"""Bounded executable kernel for §-LANG S1."""

from .core import CoreRuntimeError, CoreSyntaxError, evaluate_program, parse_program, run_source

__all__ = [
    "CoreRuntimeError",
    "CoreSyntaxError",
    "evaluate_program",
    "parse_program",
    "run_source",
]

__version__ = "0.1.0"

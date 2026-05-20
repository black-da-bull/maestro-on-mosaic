"""Maestro Triad Validator.

Deterministic hard-control validator for the three Suno-facing prompt surfaces.
"""

from .validator import validate_triad, ValidationResult
from .profiles import PROFILES, Profile

__version__ = "0.1.0"

__all__ = ["validate_triad", "ValidationResult", "PROFILES", "Profile"]

"""Maestro Authority Map — canon-governance discipline.

See docs/governance/authority-map-v0.1.md for the specification.
"""

from authority_map.schema import (
    AuthorityMap,
    AuthorityTier,
    PromotionMatrixRow,
    ScopePlane,
    SourceClass,
)
from authority_map.loader import load_authority_map
from authority_map.validator import ValidationReport, validate_authority_map

__version__ = "0.1.0"

__all__ = [
    "AuthorityMap",
    "AuthorityTier",
    "PromotionMatrixRow",
    "ScopePlane",
    "SourceClass",
    "ValidationReport",
    "load_authority_map",
    "validate_authority_map",
]

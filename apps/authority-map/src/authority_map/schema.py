"""Authority Map data schema.

Pure dataclasses. No I/O. No YAML. The loader and validator import these.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ScopePlane(str, Enum):
    """Three-plane scope tagging from the v3 protocol."""

    PROJECT_MAESTRO = "PROJECT_MAESTRO"
    WORKSPACE_DEV = "WORKSPACE_DEV"
    BRIDGE_PROJECT_WORKSPACE = "BRIDGE_PROJECT_WORKSPACE"
    UNRESOLVED_SCOPE = "UNRESOLVED_SCOPE"


class SourceClass(str, Enum):
    """The seven source classes SC-0 .. SC-6 per Authority Map v0.1 §1.

    Membership in this enum is a *primary* class. A compound source class
    like "SC-2 + SC-3" is permitted in the seed file and parsed by the
    loader into a tuple of primaries.
    """

    SC_0 = "SC-0"  # operator_current_delta
    SC_1 = "SC-1"  # dev_session_replay
    SC_2 = "SC-2"  # operator_confirmed_artifact
    SC_3 = "SC-3"  # forensic_control_artifact
    SC_4 = "SC-4"  # candidate_runtime_or_product_spec
    SC_5 = "SC-5"  # handoff_or_summary
    SC_6 = "SC-6"  # diagram_or_image


class AuthorityTier(str, Enum):
    """Authority tier — extensible via ADR; six enums in v0.1."""

    HIGH = "high"
    HIGH_WITH_QUALIFIER = "high_with_qualifier"
    MEDIUM = "medium"
    CANDIDATE = "candidate"
    LOW = "low"
    REFERENCE_ONLY = "reference_only"


# Single source of truth for the narrative-field set.
NARRATIVE_FIELDS: tuple[str, ...] = (
    "current_status",
    "promotion_requirement",
    "blocking_reason",
    "downstream_risk_if_promoted_early",
    "recommended_next_action",
)


@dataclass(frozen=True)
class PromotionMatrixRow:
    """One row of the Promotion Matrix.

    All nine fields are required. The four narrative fields below the
    structural fields must each be exactly one sentence — enforced by
    the validator, not the dataclass.
    """

    claim_or_artifact: str
    scope_plane: ScopePlane
    source_classes: tuple[SourceClass, ...]  # 1 or more
    authority_tier: AuthorityTier
    current_status: str
    promotion_requirement: str
    blocking_reason: str
    downstream_risk_if_promoted_early: str
    recommended_next_action: str

    def source_class_label(self) -> str:
        """Render source_classes the way the seed file writes them."""
        return " + ".join(sc.value for sc in self.source_classes)


@dataclass(frozen=True)
class AuthorityMap:
    """The full Authority Map: header metadata plus all Promotion Matrix rows."""

    version: str
    generated_at: str  # ISO-8601
    controlling_principle: str
    rows: tuple[PromotionMatrixRow, ...] = field(default_factory=tuple)

    def find(self, claim_substring: str) -> tuple[PromotionMatrixRow, ...]:
        """Case-insensitive substring search over claim_or_artifact."""
        needle = claim_substring.lower()
        return tuple(
            r for r in self.rows if needle in r.claim_or_artifact.lower()
        )

    def by_scope(self, plane: ScopePlane) -> tuple[PromotionMatrixRow, ...]:
        """Filter rows by scope plane."""
        return tuple(r for r in self.rows if r.scope_plane is plane)

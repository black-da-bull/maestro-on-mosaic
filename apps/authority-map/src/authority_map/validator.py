"""Authority Map validator.

Semantic checks on a loaded AuthorityMap. Parsing errors are surfaced by
the loader; this layer enforces the editorial discipline described in
docs/governance/authority-map-v0.1.md §2:

  - Each narrative field is exactly one sentence.
  - No duplicate `claim_or_artifact` (case-insensitive).
  - No empty narrative fields.

All checks are pure functions returning structured results.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from authority_map.schema import (
    NARRATIVE_FIELDS,
    AuthorityMap,
    PromotionMatrixRow,
)


# A sentence ends in `.`, `!`, or `?`. Multi-sentence content is detected by
# the presence of a sentence terminator followed by whitespace plus a capital
# letter or digit — that's the unambiguous "new sentence" signal.
_SENTENCE_BOUNDARY = re.compile(r"[.!?]\s+(?=[A-Z0-9])")


@dataclass(frozen=True)
class Issue:
    """A single validation issue."""

    row_index: int
    claim: str
    field_name: str
    severity: str  # "error" | "warning"
    message: str


@dataclass
class ValidationReport:
    """Aggregate result of validating an Authority Map."""

    map_version: str
    issues: list[Issue] = field(default_factory=list)

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def passed(self) -> bool:
        return not self.errors


def _count_sentences(text: str) -> int:
    """Count sentences in `text` for the one-sentence-per-subkey check.

    A blank string counts as zero. A string with no terminal punctuation
    counts as one (incomplete but not multi). We only fail on >= 2.
    """
    stripped = text.strip()
    if not stripped:
        return 0
    # Number of boundaries between sentences + 1 = number of sentences.
    return len(_SENTENCE_BOUNDARY.findall(stripped)) + 1


def _check_row_narrative_discipline(
    row: PromotionMatrixRow, index: int
) -> list[Issue]:
    """Verify each narrative field is exactly one sentence and non-empty."""
    issues: list[Issue] = []
    for field_name in NARRATIVE_FIELDS:
        value = getattr(row, field_name)
        count = _count_sentences(value)
        if count == 0:
            issues.append(
                Issue(
                    row_index=index,
                    claim=row.claim_or_artifact,
                    field_name=field_name,
                    severity="error",
                    message=f"empty narrative field {field_name!r}",
                )
            )
        elif count > 1:
            issues.append(
                Issue(
                    row_index=index,
                    claim=row.claim_or_artifact,
                    field_name=field_name,
                    severity="error",
                    message=(
                        f"{field_name!r} contains {count} sentences; "
                        "narrative fields must be exactly one sentence "
                        "(see docs/governance/authority-map-v0.1.md §2)"
                    ),
                )
            )
    return issues


def _check_no_duplicate_claims(amap: AuthorityMap) -> list[Issue]:
    """Surface case-insensitive duplicate `claim_or_artifact` titles."""
    seen: dict[str, int] = {}
    issues: list[Issue] = []
    for i, row in enumerate(amap.rows):
        key = row.claim_or_artifact.lower().strip()
        if key in seen:
            issues.append(
                Issue(
                    row_index=i,
                    claim=row.claim_or_artifact,
                    field_name="claim_or_artifact",
                    severity="error",
                    message=(
                        f"duplicate claim title (case-insensitive); "
                        f"first occurrence at row #{seen[key]}"
                    ),
                )
            )
        else:
            seen[key] = i
    return issues


def validate_authority_map(amap: AuthorityMap) -> ValidationReport:
    """Run all checks and return an aggregate ValidationReport."""
    report = ValidationReport(map_version=amap.version)
    for i, row in enumerate(amap.rows):
        report.issues.extend(_check_row_narrative_discipline(row, i))
    report.issues.extend(_check_no_duplicate_claims(amap))
    return report

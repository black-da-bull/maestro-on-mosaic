"""YAML loader for Authority Map seed files.

Parses a YAML document into the schema dataclasses. Performs *parsing*
errors (malformed YAML, missing required keys, unknown enum values).
Semantic checks (one-sentence narrative fields) live in `validator.py`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from authority_map.schema import (
    AuthorityMap,
    AuthorityTier,
    PromotionMatrixRow,
    ScopePlane,
    SourceClass,
)


REQUIRED_ROW_KEYS: tuple[str, ...] = (
    "claim_or_artifact",
    "scope_plane",
    "source_class",
    "authority_tier",
    "current_status",
    "promotion_requirement",
    "blocking_reason",
    "downstream_risk_if_promoted_early",
    "recommended_next_action",
)

REQUIRED_HEADER_KEYS: tuple[str, ...] = (
    "version",
    "generated_at",
    "controlling_principle",
    "rows",
)


class AuthorityMapLoadError(ValueError):
    """Raised when an Authority Map seed file cannot be parsed."""


def _parse_source_class(raw: str) -> tuple[SourceClass, ...]:
    """Parse 'SC-2' or 'SC-2 + SC-3' into a tuple of SourceClass."""
    if not isinstance(raw, str):
        raise AuthorityMapLoadError(
            f"source_class must be a string, got {type(raw).__name__}: {raw!r}"
        )
    parts = [p.strip() for p in raw.split("+")]
    out: list[SourceClass] = []
    for part in parts:
        try:
            out.append(SourceClass(part))
        except ValueError as exc:
            valid = ", ".join(sc.value for sc in SourceClass)
            raise AuthorityMapLoadError(
                f"unknown source_class {part!r}; expected one of: {valid}"
            ) from exc
    if not out:
        raise AuthorityMapLoadError("source_class must name at least one class")
    return tuple(out)


def _parse_row(raw: dict[str, Any], index: int) -> PromotionMatrixRow:
    """Convert one YAML mapping into a PromotionMatrixRow."""
    missing = [k for k in REQUIRED_ROW_KEYS if k not in raw]
    if missing:
        raise AuthorityMapLoadError(
            f"row #{index}: missing required fields: {missing}"
        )

    try:
        plane = ScopePlane(raw["scope_plane"])
    except ValueError as exc:
        valid = ", ".join(p.value for p in ScopePlane)
        raise AuthorityMapLoadError(
            f"row #{index}: unknown scope_plane {raw['scope_plane']!r}; "
            f"expected one of: {valid}"
        ) from exc

    try:
        tier = AuthorityTier(raw["authority_tier"])
    except ValueError as exc:
        valid = ", ".join(t.value for t in AuthorityTier)
        raise AuthorityMapLoadError(
            f"row #{index}: unknown authority_tier {raw['authority_tier']!r}; "
            f"expected one of: {valid}"
        ) from exc

    sources = _parse_source_class(raw["source_class"])

    return PromotionMatrixRow(
        claim_or_artifact=str(raw["claim_or_artifact"]),
        scope_plane=plane,
        source_classes=sources,
        authority_tier=tier,
        current_status=str(raw["current_status"]),
        promotion_requirement=str(raw["promotion_requirement"]),
        blocking_reason=str(raw["blocking_reason"]),
        downstream_risk_if_promoted_early=str(
            raw["downstream_risk_if_promoted_early"]
        ),
        recommended_next_action=str(raw["recommended_next_action"]),
    )


def load_authority_map(path: str | Path) -> AuthorityMap:
    """Load and parse an Authority Map YAML file.

    Raises AuthorityMapLoadError for any structural issue (missing keys,
    unknown enums, malformed YAML).
    """
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise AuthorityMapLoadError(f"cannot read {p}: {exc}") from exc

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise AuthorityMapLoadError(f"YAML parse error in {p}: {exc}") from exc

    if not isinstance(data, dict):
        raise AuthorityMapLoadError(
            f"top-level YAML must be a mapping, got {type(data).__name__}"
        )

    missing = [k for k in REQUIRED_HEADER_KEYS if k not in data]
    if missing:
        raise AuthorityMapLoadError(
            f"missing required top-level keys: {missing}"
        )

    raw_rows = data["rows"]
    if not isinstance(raw_rows, list):
        raise AuthorityMapLoadError(
            f"`rows` must be a list, got {type(raw_rows).__name__}"
        )

    rows = tuple(_parse_row(r, i) for i, r in enumerate(raw_rows))

    return AuthorityMap(
        version=str(data["version"]),
        generated_at=str(data["generated_at"]),
        controlling_principle=str(data["controlling_principle"]),
        rows=rows,
    )

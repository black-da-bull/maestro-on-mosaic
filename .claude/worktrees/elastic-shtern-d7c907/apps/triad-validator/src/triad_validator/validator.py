"""Triad validator core.

Three deterministic checks, all derived from canonical sources:

1. Length bounds — character counts vs profile budgets.
2. Section order — Creative UST section sequence vs Suno Output Law
   (maestro_v0.md §5.1).
3. Comma policy — INV-04 (no commas outside the LYRICS BLOCK).

Each check is pure (no I/O), takes the relevant Triad field plus profile data,
and returns a ChechResult. The validator aggregates results into a
ValidationResult that serializes to the v4.2.3 E2E_Result JSON shape.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any

from .profiles import Profile, Range


# Suno Output Law — immutable section order for the Creative UST emit.
# Source: maestro_v0.md §5.1 + maestro.md kernel (Suno parsing discipline).
SUNO_OUTPUT_LAW: tuple[str, ...] = (
    "Theory",
    "Voice",
    "CREW_TAGS",
    "Road-Map",
    "LYRICS BLOCK",
    "Style",
    "Timbre",
    "Performance",
)


@dataclass
class CheckResult:
    """Outcome of a single check against one surface or aspect."""
    name: str
    passed: bool
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Aggregate result for a full Triad validation pass."""
    profile: str
    passed: bool
    checks: list[CheckResult]

    def to_e2e_json(self) -> dict[str, Any]:
        """Render to the v4.2.3 E2E_Result audit shape.

        This shape matches what `legacy/E2E_Result_Boy_Icarus.md` ships, so
        a passing validator output is drop-in compatible with historical
        audit artifacts.
        """
        # Bucket the check results by category so the audit shape is stable.
        length_results = {
            c.name: c.detail
            for c in self.checks
            if c.name.startswith("length:")
        }
        order_result = next(
            (c for c in self.checks if c.name == "section_order"), None
        )
        section_presence_result = next(
            (c for c in self.checks if c.name == "section_presence"), None
        )
        comma_result = next(
            (c for c in self.checks if c.name == "comma_policy"), None
        )

        return {
            "profile": self.profile,
            "verdict": "PASS" if self.passed else "FAIL",
            "section_presence": (
                section_presence_result.detail if section_presence_result else {}
            ),
            "section_order_ok": (
                order_result.passed if order_result else None
            ),
            "comma_policy_ok": (
                comma_result.passed if comma_result else None
            ),
            "lengths": length_results,
            "failures": [
                {"check": c.name, "detail": c.detail}
                for c in self.checks
                if not c.passed
            ],
        }


# ---------------------------------------------------------------------------
# Individual checks (pure functions, no I/O)
# ---------------------------------------------------------------------------

def _check_length(
    surface_name: str, text: str | None, budget: Range | None
) -> CheckResult:
    """Validate one surface's character count against its profile budget.

    Returns PASS if budget is None (surface not used in this profile) and the
    text is also absent. Returns FAIL if text is present but budget is None
    (unexpected surface for this profile) or vice versa.
    """
    if budget is None:
        if text is None or text == "":
            return CheckResult(
                name=f"length:{surface_name}",
                passed=True,
                detail={"status": "not_required_by_profile"},
            )
        return CheckResult(
            name=f"length:{surface_name}",
            passed=False,
            detail={
                "status": "unexpected_surface",
                "chars": len(text),
                "reason": (
                    "profile does not declare a budget for this surface; "
                    "remove or switch profile"
                ),
            },
        )

    if text is None:
        return CheckResult(
            name=f"length:{surface_name}",
            passed=False,
            detail={
                "status": "missing_surface",
                "budget_min": budget.min,
                "budget_max": budget.max,
            },
        )

    chars = len(text)
    over_max = chars > budget.max
    under_min = budget.min is not None and chars < budget.min
    passed = not (over_max or under_min)

    return CheckResult(
        name=f"length:{surface_name}",
        passed=passed,
        detail={
            "chars": chars,
            "budget_min": budget.min,
            "budget_max": budget.max,
            "over_max": over_max,
            "under_min": under_min,
        },
    )


# Match Suno-style section headers: lines starting with `[Theory]`, `[Voice]`,
# `[LYRICS BLOCK]`, etc. The regex tolerates inline key=value pairs after
# the section name (e.g., `[Theory | mode=Dorian]`) because Maestro's section
# headers carry parameters.
_SECTION_HEADER_RE = re.compile(
    r"^\s*\[\s*([A-Za-z][A-Za-z\-_ ]*?)\s*(?:\||\])",
    flags=re.MULTILINE,
)


def _extract_sections(creative_ust: str) -> list[str]:
    """Return the ordered list of top-level section names appearing in the UST.

    Filters to the canonical sections in SUNO_OUTPUT_LAW so noise (e.g. internal
    section markers like `[Intro]` within the LYRICS BLOCK) doesn't pollute the
    order check.
    """
    canonical = {s.lower() for s in SUNO_OUTPUT_LAW}
    matches = _SECTION_HEADER_RE.findall(creative_ust)
    found: list[str] = []
    for raw in matches:
        normalized = raw.strip()
        if normalized.lower() in canonical:
            # Map back to the canonical capitalization.
            canonical_form = next(
                s for s in SUNO_OUTPUT_LAW if s.lower() == normalized.lower()
            )
            found.append(canonical_form)
    return found


def _check_section_presence(creative_ust: str) -> CheckResult:
    """Verify all eight Suno Output Law sections appear in the Creative UST."""
    found = set(_extract_sections(creative_ust))
    presence = {s: (s in found) for s in SUNO_OUTPUT_LAW}
    missing = [s for s, present in presence.items() if not present]
    return CheckResult(
        name="section_presence",
        passed=not missing,
        detail={**presence, "missing": missing},
    )


def _check_section_order(creative_ust: str) -> CheckResult:
    """Verify the section sequence matches the Suno Output Law exactly.

    Sections may not be reordered, repeated, or interleaved. Each canonical
    section appears at most once at the top level.
    """
    found = _extract_sections(creative_ust)
    expected = list(SUNO_OUTPUT_LAW)
    # We require found == expected (in order; each section exactly once).
    passed = found == expected
    return CheckResult(
        name="section_order",
        passed=passed,
        detail={
            "expected": expected,
            "found": found,
            "matches": passed,
        },
    )


def _check_comma_policy(creative_ust: str) -> CheckResult:
    """INV-04: no commas outside the LYRICS BLOCK.

    Strategy:
      1. Locate the LYRICS BLOCK section boundaries (start at its header,
         end at the next top-level section header or EOF).
      2. Mask the LYRICS BLOCK content from the source.
      3. Look for any commas in the remaining (non-lyrics) text.
    """
    # Find LYRICS BLOCK header position.
    headers = list(_SECTION_HEADER_RE.finditer(creative_ust))
    lyrics_start: int | None = None
    lyrics_end: int | None = None

    for i, m in enumerate(headers):
        section_name = m.group(1).strip().lower()
        if section_name == "lyrics block":
            lyrics_start = m.start()
            # End is the start of the next canonical header, or EOF.
            for j in range(i + 1, len(headers)):
                next_name = headers[j].group(1).strip().lower()
                if next_name in {s.lower() for s in SUNO_OUTPUT_LAW}:
                    lyrics_end = headers[j].start()
                    break
            if lyrics_end is None:
                lyrics_end = len(creative_ust)
            break

    if lyrics_start is None:
        # No LYRICS BLOCK at all — any comma anywhere violates the policy,
        # but section_presence will already fail. Surface here too.
        commas = [i for i, ch in enumerate(creative_ust) if ch == ","]
        return CheckResult(
            name="comma_policy",
            passed=not commas,
            detail={
                "lyrics_block_found": False,
                "commas_outside_lyrics": len(commas),
                "comma_positions": commas[:10],  # cap reported positions
            },
        )

    # Build the non-lyrics text (before lyrics_start + after lyrics_end).
    before = creative_ust[:lyrics_start]
    after = creative_ust[lyrics_end:] if lyrics_end < len(creative_ust) else ""
    non_lyrics_text = before + after
    comma_count = non_lyrics_text.count(",")

    return CheckResult(
        name="comma_policy",
        passed=comma_count == 0,
        detail={
            "lyrics_block_found": True,
            "lyrics_block_span": [lyrics_start, lyrics_end],
            "commas_outside_lyrics": comma_count,
        },
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_triad(
    triad: dict[str, str | None], profile: Profile
) -> ValidationResult:
    """Run all v0.1 checks on a Triad payload against a profile.

    `triad` is expected to carry the keys:
      - "show_summary"   (str)
      - "creative_ust"   (str — the full prompt with section headers)
      - "persona_profile" (str | None — only used by v0_spec)
      - "persona_style"  (str | None — only used by v0_spec)

    Missing keys are treated as None.
    """
    show_summary = triad.get("show_summary")
    creative_ust = triad.get("creative_ust")
    persona_profile = triad.get("persona_profile")
    persona_style = triad.get("persona_style")

    checks: list[CheckResult] = []

    # Length checks — one per surface.
    checks.append(_check_length("show_summary", show_summary, profile.show_summary))
    checks.append(_check_length("creative_ust", creative_ust, profile.creative_ust))
    checks.append(
        _check_length("persona_profile", persona_profile, profile.persona_profile)
    )
    checks.append(
        _check_length("persona_style", persona_style, profile.persona_style)
    )

    # Structural checks operate on creative_ust if present.
    if creative_ust:
        checks.append(_check_section_presence(creative_ust))
        checks.append(_check_section_order(creative_ust))
        checks.append(_check_comma_policy(creative_ust))
    else:
        # Without a Creative UST we cannot run structural checks; fail hard.
        checks.append(
            CheckResult(
                name="section_presence",
                passed=False,
                detail={"error": "creative_ust is missing"},
            )
        )

    passed = all(c.passed for c in checks)
    return ValidationResult(profile=profile.name, passed=passed, checks=checks)

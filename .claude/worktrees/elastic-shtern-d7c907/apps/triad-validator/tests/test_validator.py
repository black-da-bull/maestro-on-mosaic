"""Tests for the Maestro Triad Validator.

These tests verify the three v0.1 checks against constructed inputs and against
the Boy Icarus example. The Boy Icarus example is synthesized to match the
v4.2.3 audit surface (`legacy/E2E_Result_Boy_Icarus.md`) — a passing validator
output is what the original v4.2.3 run produced for that song.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from triad_validator.profiles import get_profile, PROFILES
from triad_validator.validator import (
    SUNO_OUTPUT_LAW,
    validate_triad,
    _check_length,
    _check_section_presence,
    _check_section_order,
    _check_comma_policy,
    _extract_sections,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = REPO_ROOT / "examples"


# ---------------------------------------------------------------------------
# Length checks
# ---------------------------------------------------------------------------

class TestLengthChecks:
    def test_within_budget_passes(self):
        budget = get_profile("v4_2_3").show_summary
        result = _check_length("show_summary", "hello", budget)
        assert result.passed
        assert result.detail["chars"] == 5

    def test_over_max_fails(self):
        budget = get_profile("v4_2_3").show_summary  # max 1000
        text = "x" * 1001
        result = _check_length("show_summary", text, budget)
        assert not result.passed
        assert result.detail["over_max"] is True

    def test_under_min_fails_in_v0_spec(self):
        budget = get_profile("v0_spec").show_summary  # min 950, max 1000
        result = _check_length("show_summary", "short", budget)
        assert not result.passed
        assert result.detail["under_min"] is True

    def test_missing_surface_in_active_profile_fails(self):
        budget = get_profile("v0_spec").persona_style
        result = _check_length("persona_style", None, budget)
        assert not result.passed
        assert result.detail["status"] == "missing_surface"

    def test_absent_surface_in_inactive_profile_passes(self):
        # v4_2_3 doesn't declare persona_style, and the triad doesn't include it
        result = _check_length(
            "persona_style", None, get_profile("v4_2_3").persona_style
        )
        assert result.passed
        assert result.detail["status"] == "not_required_by_profile"

    def test_unexpected_surface_in_inactive_profile_fails(self):
        # v4_2_3 doesn't declare persona_style; supplying one is an error
        result = _check_length(
            "persona_style", "some persona", get_profile("v4_2_3").persona_style
        )
        assert not result.passed
        assert result.detail["status"] == "unexpected_surface"


# ---------------------------------------------------------------------------
# Section extraction + presence + order
# ---------------------------------------------------------------------------

class TestSectionChecks:
    @pytest.fixture
    def canonical_ust(self) -> str:
        # Headers only, in canonical order — minimal valid input for the
        # section checks.
        return "\n\n".join(f"[{name}]" for name in SUNO_OUTPUT_LAW)

    def test_extract_sections_canonical(self, canonical_ust: str):
        found = _extract_sections(canonical_ust)
        assert found == list(SUNO_OUTPUT_LAW)

    def test_extract_sections_with_inline_params(self):
        ust = "[Theory | mode=Dorian]\n[Voice | lead=alto]\n[CREW_TAGS]\n"
        found = _extract_sections(ust)
        assert found == ["Theory", "Voice", "CREW_TAGS"]

    def test_extract_sections_ignores_nested_markers(self):
        # Section markers inside the LYRICS BLOCK (e.g. [Intro], [Verse 1])
        # are NOT in SUNO_OUTPUT_LAW and should be filtered out by the
        # canonical-set filter inside _extract_sections.
        ust = "[Theory]\n[LYRICS BLOCK]\n[Intro | 4 bars]\n[Verse 1 | 8 bars]\n[Style]\n"
        found = _extract_sections(ust)
        assert found == ["Theory", "LYRICS BLOCK", "Style"]

    def test_presence_passes_with_all_sections(self, canonical_ust: str):
        result = _check_section_presence(canonical_ust)
        assert result.passed
        assert result.detail["missing"] == []

    def test_presence_fails_with_missing_sections(self):
        ust = "[Theory]\n[Voice]\n[LYRICS BLOCK]\n[Style]\n"
        result = _check_section_presence(ust)
        assert not result.passed
        assert set(result.detail["missing"]) == {
            "CREW_TAGS", "Road-Map", "Timbre", "Performance"
        }

    def test_order_passes_in_canonical_sequence(self, canonical_ust: str):
        result = _check_section_order(canonical_ust)
        assert result.passed

    def test_order_fails_when_swapped(self):
        # Swap Voice and CREW_TAGS
        reordered = SUNO_OUTPUT_LAW[:1] + ("CREW_TAGS", "Voice") + SUNO_OUTPUT_LAW[3:]
        ust = "\n".join(f"[{name}]" for name in reordered)
        result = _check_section_order(ust)
        assert not result.passed
        assert result.detail["found"] != list(SUNO_OUTPUT_LAW)


# ---------------------------------------------------------------------------
# Comma policy (INV-04)
# ---------------------------------------------------------------------------

class TestCommaPolicy:
    def test_no_commas_anywhere_passes(self):
        ust = "[Theory]\n[Voice]\n[CREW_TAGS]\n[Road-Map | A -> B -> C]\n[LYRICS BLOCK]\n\"line one\"\n\"line two\"\n[Style]\n[Timbre]\n[Performance]\n"
        result = _check_comma_policy(ust)
        assert result.passed
        assert result.detail["commas_outside_lyrics"] == 0

    def test_commas_inside_lyrics_pass(self):
        # Commas appearing strictly inside the LYRICS BLOCK section are allowed
        # (they're inside quoted lyric content where the parser tolerates them).
        ust = (
            "[Theory]\n[Voice]\n[CREW_TAGS]\n[Road-Map]\n"
            "[LYRICS BLOCK]\n"
            "\"dirt roads, to juke joints\", (ad-lib: lawd)\n"
            "[Style]\n[Timbre]\n[Performance]\n"
        )
        result = _check_comma_policy(ust)
        assert result.passed
        assert result.detail["lyrics_block_found"] is True
        assert result.detail["commas_outside_lyrics"] == 0

    def test_commas_outside_lyrics_fail(self):
        # Comma in the Theory metacontainer — INV-04 violation.
        ust = (
            "[Theory | mode=Dorian, tonal_center=D]\n[Voice]\n[CREW_TAGS]\n"
            "[Road-Map]\n[LYRICS BLOCK]\n\"clean line\"\n"
            "[Style]\n[Timbre]\n[Performance]\n"
        )
        result = _check_comma_policy(ust)
        assert not result.passed
        assert result.detail["commas_outside_lyrics"] >= 1


# ---------------------------------------------------------------------------
# End-to-end: Boy Icarus example
# ---------------------------------------------------------------------------

class TestBoyIcarusE2E:
    @pytest.fixture
    def boy_icarus_triad(self) -> dict[str, str | None]:
        path = EXAMPLES / "boy_icarus_triad.json"
        with path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        # Strip provenance metadata before validation.
        return {k: v for k, v in data.items() if not k.startswith("_")}

    def test_boy_icarus_passes_v4_2_3_profile(self, boy_icarus_triad):
        profile = get_profile("v4_2_3")
        result = validate_triad(boy_icarus_triad, profile)
        # All v0.1 checks should pass — this is the historical PASS verdict
        # that the v4.2.3 run produced for Boy Icarus.
        failed_checks = [c.name for c in result.checks if not c.passed]
        assert result.passed, f"Failures: {failed_checks}"

    def test_boy_icarus_audit_shape_matches_legacy(self, boy_icarus_triad):
        profile = get_profile("v4_2_3")
        result = validate_triad(boy_icarus_triad, profile)
        audit = result.to_e2e_json()

        # Keys present in legacy/E2E_Result_Boy_Icarus.md should be present here.
        assert audit["verdict"] == "PASS"
        assert audit["section_order_ok"] is True
        assert audit["comma_policy_ok"] is True
        assert "section_presence" in audit
        assert "lengths" in audit
        # All eight canonical sections should be flagged present.
        for section in SUNO_OUTPUT_LAW:
            assert audit["section_presence"][section] is True, (
                f"section {section!r} missing from audit"
            )


# ---------------------------------------------------------------------------
# Profile coverage
# ---------------------------------------------------------------------------

class TestProfiles:
    def test_all_profiles_have_basic_fields(self):
        for name, profile in PROFILES.items():
            assert profile.name
            assert profile.show_summary.max > 0
            assert profile.creative_ust.max > 0

    def test_v4_2_3_omits_persona_surfaces(self):
        profile = get_profile("v4_2_3")
        assert profile.persona_profile is None
        assert profile.persona_style is None

    def test_v0_spec_includes_persona_surfaces(self):
        profile = get_profile("v0_spec")
        assert profile.persona_profile is not None
        assert profile.persona_style is not None
        assert profile.persona_style.max == 150

    def test_unknown_profile_raises(self):
        with pytest.raises(KeyError):
            get_profile("v9999")

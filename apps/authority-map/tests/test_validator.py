"""Validator tests — narrative-field discipline + duplicate detection."""

from pathlib import Path

from authority_map.loader import load_authority_map
from authority_map.schema import (
    AuthorityMap,
    AuthorityTier,
    PromotionMatrixRow,
    ScopePlane,
    SourceClass,
)
from authority_map.validator import validate_authority_map


SEED = Path(__file__).resolve().parents[1] / "seed" / "authority_map_v0.1_seed.yaml"


def _row(**overrides) -> PromotionMatrixRow:
    base = dict(
        claim_or_artifact="X",
        scope_plane=ScopePlane.PROJECT_MAESTRO,
        source_classes=(SourceClass.SC_2,),
        authority_tier=AuthorityTier.HIGH,
        current_status="One sentence here.",
        promotion_requirement="One sentence here.",
        blocking_reason="One sentence here.",
        downstream_risk_if_promoted_early="One sentence here.",
        recommended_next_action="One sentence here.",
    )
    base.update(overrides)
    return PromotionMatrixRow(**base)


def _amap(*rows: PromotionMatrixRow) -> AuthorityMap:
    return AuthorityMap(
        version="0.1.0-test",
        generated_at="2026-05-20",
        controlling_principle="Test.",
        rows=rows,
    )


class TestSeedPasses:
    def test_bundled_seed_validates_clean(self):
        amap = load_authority_map(SEED)
        report = validate_authority_map(amap)
        # Helpful diagnostic if this regresses.
        assert report.passed, [
            (i.row_index, i.claim, i.field_name, i.message) for i in report.errors
        ]


class TestOneSentenceDiscipline:
    def test_two_sentences_in_narrative_field_fails(self):
        amap = _amap(_row(
            current_status="This is one. This is two.",
        ))
        report = validate_authority_map(amap)
        assert not report.passed
        assert any(
            i.field_name == "current_status" and "2 sentences" in i.message
            for i in report.errors
        )

    def test_three_sentences_in_narrative_field_fails(self):
        amap = _amap(_row(
            promotion_requirement="One. Two. Three.",
        ))
        report = validate_authority_map(amap)
        assert not report.passed
        assert any(
            i.field_name == "promotion_requirement" and "3 sentences" in i.message
            for i in report.errors
        )

    def test_empty_narrative_field_fails(self):
        amap = _amap(_row(blocking_reason="   "))
        report = validate_authority_map(amap)
        assert not report.passed
        assert any(
            i.field_name == "blocking_reason" and "empty" in i.message
            for i in report.errors
        )

    def test_single_sentence_without_terminal_punctuation_passes(self):
        # A single sentence that lacks a period is incomplete but not multi —
        # we permit it (warning would be over-pedantic for free-form notes).
        amap = _amap(_row(
            recommended_next_action="run the next slice tomorrow"
        ))
        report = validate_authority_map(amap)
        assert report.passed, [i.message for i in report.errors]

    def test_sentence_with_inline_abbreviation_does_not_split(self):
        # Abbreviations followed by lowercase don't trigger a split.
        amap = _amap(_row(
            current_status="e.g. the system runs in candidate mode for now."
        ))
        report = validate_authority_map(amap)
        assert report.passed, [i.message for i in report.errors]


class TestDuplicateDetection:
    def test_exact_duplicate_claim_fails(self):
        amap = _amap(
            _row(claim_or_artifact="Same Claim"),
            _row(claim_or_artifact="Same Claim"),
        )
        report = validate_authority_map(amap)
        assert not report.passed
        assert any("duplicate" in i.message for i in report.errors)

    def test_case_insensitive_duplicate_fails(self):
        amap = _amap(
            _row(claim_or_artifact="Mosaic Engine v0.1"),
            _row(claim_or_artifact="mosaic engine v0.1"),
        )
        report = validate_authority_map(amap)
        assert not report.passed
        assert any("duplicate" in i.message for i in report.errors)

    def test_whitespace_difference_does_not_dedupe(self):
        # "X" and "X " (trailing whitespace) — our key strips whitespace,
        # so they are considered duplicates. Lock in that behavior.
        amap = _amap(
            _row(claim_or_artifact="X"),
            _row(claim_or_artifact="X "),
        )
        report = validate_authority_map(amap)
        assert not report.passed


class TestReportShape:
    def test_passed_property(self):
        amap = _amap(_row())
        report = validate_authority_map(amap)
        assert report.passed is True
        assert report.errors == []

    def test_errors_warnings_split(self):
        amap = _amap(_row(current_status="A. B."))
        report = validate_authority_map(amap)
        assert len(report.errors) == 1
        assert len(report.warnings) == 0

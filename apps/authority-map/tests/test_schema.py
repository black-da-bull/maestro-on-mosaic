"""Schema-level tests — dataclass behavior, no I/O."""

from authority_map.schema import (
    AuthorityMap,
    AuthorityTier,
    PromotionMatrixRow,
    ScopePlane,
    SourceClass,
)


def _row(claim: str, plane: ScopePlane = ScopePlane.PROJECT_MAESTRO) -> PromotionMatrixRow:
    return PromotionMatrixRow(
        claim_or_artifact=claim,
        scope_plane=plane,
        source_classes=(SourceClass.SC_2,),
        authority_tier=AuthorityTier.HIGH,
        current_status="Status sentence.",
        promotion_requirement="Promotion sentence.",
        blocking_reason="Block sentence.",
        downstream_risk_if_promoted_early="Risk sentence.",
        recommended_next_action="Action sentence.",
    )


class TestSourceClassLabel:
    def test_single_source_class(self):
        row = _row("X")
        assert row.source_class_label() == "SC-2"

    def test_compound_source_class(self):
        row = PromotionMatrixRow(
            claim_or_artifact="X",
            scope_plane=ScopePlane.PROJECT_MAESTRO,
            source_classes=(SourceClass.SC_2, SourceClass.SC_3),
            authority_tier=AuthorityTier.HIGH,
            current_status="s.",
            promotion_requirement="p.",
            blocking_reason="b.",
            downstream_risk_if_promoted_early="d.",
            recommended_next_action="a.",
        )
        assert row.source_class_label() == "SC-2 + SC-3"


class TestAuthorityMapFind:
    def test_find_returns_substring_matches(self):
        amap = AuthorityMap(
            version="0.1.0",
            generated_at="2026-05-20",
            controlling_principle="Test.",
            rows=(
                _row("Technical UST is canonical"),
                _row("Creative UST is downstream"),
                _row("SEM substrate"),
            ),
        )
        results = amap.find("ust")
        assert len(results) == 2
        assert all("ust" in r.claim_or_artifact.lower() for r in results)

    def test_find_case_insensitive(self):
        amap = AuthorityMap(
            version="0.1.0",
            generated_at="2026-05-20",
            controlling_principle="Test.",
            rows=(_row("MOSAIC ENGINE v0.1"),),
        )
        assert len(amap.find("mosaic")) == 1
        assert len(amap.find("MoSaIc")) == 1

    def test_find_empty_when_no_match(self):
        amap = AuthorityMap(
            version="0.1.0",
            generated_at="2026-05-20",
            controlling_principle="Test.",
            rows=(_row("Technical UST"),),
        )
        assert amap.find("nonexistent") == ()


class TestAuthorityMapByScope:
    def test_by_scope_filters_correctly(self):
        amap = AuthorityMap(
            version="0.1.0",
            generated_at="2026-05-20",
            controlling_principle="Test.",
            rows=(
                _row("A", ScopePlane.PROJECT_MAESTRO),
                _row("B", ScopePlane.WORKSPACE_DEV),
                _row("C", ScopePlane.PROJECT_MAESTRO),
            ),
        )
        project_rows = amap.by_scope(ScopePlane.PROJECT_MAESTRO)
        assert len(project_rows) == 2
        workspace_rows = amap.by_scope(ScopePlane.WORKSPACE_DEV)
        assert len(workspace_rows) == 1
        bridge_rows = amap.by_scope(ScopePlane.BRIDGE_PROJECT_WORKSPACE)
        assert bridge_rows == ()


class TestEnumIntegrity:
    def test_all_seven_source_classes_present(self):
        # SC-0 through SC-6 — exactly seven classes.
        assert len(list(SourceClass)) == 7
        assert SourceClass("SC-0").value == "SC-0"
        assert SourceClass("SC-6").value == "SC-6"

    def test_all_four_scope_planes_present(self):
        assert len(list(ScopePlane)) == 4
        assert ScopePlane("UNRESOLVED_SCOPE").value == "UNRESOLVED_SCOPE"

    def test_all_six_authority_tiers_present(self):
        assert len(list(AuthorityTier)) == 6
        assert AuthorityTier("candidate").value == "candidate"

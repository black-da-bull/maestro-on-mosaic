"""Loader tests — YAML parsing and structural enforcement."""

from pathlib import Path

import pytest

from authority_map.loader import AuthorityMapLoadError, load_authority_map
from authority_map.schema import AuthorityTier, ScopePlane, SourceClass


SEED = Path(__file__).resolve().parents[1] / "seed" / "authority_map_v0.1_seed.yaml"


# ---- Happy path against the bundled seed --------------------------------


class TestSeedLoadsCleanly:
    def test_seed_parses(self):
        amap = load_authority_map(SEED)
        assert amap.version == "0.1.0"
        assert amap.generated_at == "2026-05-20"
        assert len(amap.rows) >= 15  # 6 ws_3 + at least 9 this-session

    def test_seed_has_ws3_canonical_rows(self):
        amap = load_authority_map(SEED)
        claims = [r.claim_or_artifact.lower() for r in amap.rows]
        assert any("technical ust" in c for c in claims)
        assert any("creative ust" in c for c in claims)
        assert any("sem" in c for c in claims)
        assert any("mosaic engine v0.1" in c for c in claims)
        assert any("maestro v0" in c for c in claims)
        assert any("files4" in c for c in claims)

    def test_seed_has_session_emergent_rows(self):
        amap = load_authority_map(SEED)
        claims = [r.claim_or_artifact.lower() for r in amap.rows]
        assert any("triad-validator" in c for c in claims)
        assert any("adr-0001" in c for c in claims)
        assert any("adr-0002" in c for c in claims)
        assert any("adr-0003" in c for c in claims)
        assert any("authority map v0.1" in c for c in claims)

    def test_seed_enums_parse(self):
        amap = load_authority_map(SEED)
        for row in amap.rows:
            assert isinstance(row.scope_plane, ScopePlane)
            assert isinstance(row.authority_tier, AuthorityTier)
            assert all(isinstance(sc, SourceClass) for sc in row.source_classes)
            assert len(row.source_classes) >= 1


# ---- Compound source_class parsing --------------------------------------


class TestCompoundSourceClass:
    def test_compound_parses_to_tuple(self, tmp_path: Path):
        f = tmp_path / "tiny.yaml"
        f.write_text(
            "version: '0.1.0'\n"
            "generated_at: '2026-05-20'\n"
            "controlling_principle: 'Test.'\n"
            "rows:\n"
            "  - claim_or_artifact: 'X'\n"
            "    scope_plane: PROJECT_MAESTRO\n"
            "    source_class: 'SC-2 + SC-3'\n"
            "    authority_tier: high\n"
            "    current_status: 'A.'\n"
            "    promotion_requirement: 'A.'\n"
            "    blocking_reason: 'A.'\n"
            "    downstream_risk_if_promoted_early: 'A.'\n"
            "    recommended_next_action: 'A.'\n",
            encoding="utf-8",
        )
        amap = load_authority_map(f)
        assert amap.rows[0].source_classes == (SourceClass.SC_2, SourceClass.SC_3)


# ---- Error paths --------------------------------------------------------


class TestErrors:
    def test_missing_file(self, tmp_path: Path):
        with pytest.raises(AuthorityMapLoadError, match="cannot read"):
            load_authority_map(tmp_path / "nope.yaml")

    def test_malformed_yaml(self, tmp_path: Path):
        f = tmp_path / "bad.yaml"
        f.write_text("version: 0.1\nrows: [unclosed", encoding="utf-8")
        with pytest.raises(AuthorityMapLoadError, match="YAML parse error"):
            load_authority_map(f)

    def test_missing_top_level_key(self, tmp_path: Path):
        f = tmp_path / "incomplete.yaml"
        f.write_text("version: '0.1.0'\nrows: []\n", encoding="utf-8")
        with pytest.raises(AuthorityMapLoadError, match="missing required top-level keys"):
            load_authority_map(f)

    def test_rows_not_a_list(self, tmp_path: Path):
        f = tmp_path / "bad_rows.yaml"
        f.write_text(
            "version: '0.1.0'\n"
            "generated_at: '2026-05-20'\n"
            "controlling_principle: 'Test.'\n"
            "rows: 'not a list'\n",
            encoding="utf-8",
        )
        with pytest.raises(AuthorityMapLoadError, match="`rows` must be a list"):
            load_authority_map(f)

    def test_row_missing_field(self, tmp_path: Path):
        f = tmp_path / "missing_field.yaml"
        f.write_text(
            "version: '0.1.0'\n"
            "generated_at: '2026-05-20'\n"
            "controlling_principle: 'Test.'\n"
            "rows:\n"
            "  - claim_or_artifact: 'X'\n"
            "    scope_plane: PROJECT_MAESTRO\n"
            "    source_class: 'SC-2'\n"
            "    authority_tier: high\n"
            # missing the five narrative fields
            ,
            encoding="utf-8",
        )
        with pytest.raises(AuthorityMapLoadError, match="missing required fields"):
            load_authority_map(f)

    def test_unknown_scope_plane(self, tmp_path: Path):
        f = tmp_path / "bad_scope.yaml"
        f.write_text(
            "version: '0.1.0'\n"
            "generated_at: '2026-05-20'\n"
            "controlling_principle: 'Test.'\n"
            "rows:\n"
            "  - claim_or_artifact: 'X'\n"
            "    scope_plane: NOT_A_PLANE\n"
            "    source_class: 'SC-2'\n"
            "    authority_tier: high\n"
            "    current_status: 'A.'\n"
            "    promotion_requirement: 'A.'\n"
            "    blocking_reason: 'A.'\n"
            "    downstream_risk_if_promoted_early: 'A.'\n"
            "    recommended_next_action: 'A.'\n",
            encoding="utf-8",
        )
        with pytest.raises(AuthorityMapLoadError, match="unknown scope_plane"):
            load_authority_map(f)

    def test_unknown_source_class(self, tmp_path: Path):
        f = tmp_path / "bad_sc.yaml"
        f.write_text(
            "version: '0.1.0'\n"
            "generated_at: '2026-05-20'\n"
            "controlling_principle: 'Test.'\n"
            "rows:\n"
            "  - claim_or_artifact: 'X'\n"
            "    scope_plane: PROJECT_MAESTRO\n"
            "    source_class: 'SC-99'\n"
            "    authority_tier: high\n"
            "    current_status: 'A.'\n"
            "    promotion_requirement: 'A.'\n"
            "    blocking_reason: 'A.'\n"
            "    downstream_risk_if_promoted_early: 'A.'\n"
            "    recommended_next_action: 'A.'\n",
            encoding="utf-8",
        )
        with pytest.raises(AuthorityMapLoadError, match="unknown source_class"):
            load_authority_map(f)

    def test_unknown_authority_tier(self, tmp_path: Path):
        f = tmp_path / "bad_tier.yaml"
        f.write_text(
            "version: '0.1.0'\n"
            "generated_at: '2026-05-20'\n"
            "controlling_principle: 'Test.'\n"
            "rows:\n"
            "  - claim_or_artifact: 'X'\n"
            "    scope_plane: PROJECT_MAESTRO\n"
            "    source_class: 'SC-2'\n"
            "    authority_tier: super_high\n"
            "    current_status: 'A.'\n"
            "    promotion_requirement: 'A.'\n"
            "    blocking_reason: 'A.'\n"
            "    downstream_risk_if_promoted_early: 'A.'\n"
            "    recommended_next_action: 'A.'\n",
            encoding="utf-8",
        )
        with pytest.raises(AuthorityMapLoadError, match="unknown authority_tier"):
            load_authority_map(f)

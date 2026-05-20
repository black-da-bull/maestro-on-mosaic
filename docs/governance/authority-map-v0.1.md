# Authority Map v0.1 — specification

**Status**: DRAFT — first user-facing v0 slice. 5-of-6 cross-workspace consensus.
**Date**: 2026-05-20
**Pairs with**: `apps/authority-map/` (executable implementation), ADR-0003
(invariant namespacing — same `Spec.ID` convention applies to source classes:
`AuthorityMap.SC-0` etc., though SC-N is unambiguous within this spec).
**Origin**: Forensic workspace (ws_3) authority_map_seed + promotion_matrix_seed.
Synthesized from the cross-workspace Day-1 prep evidence pass.

---

## §0 — Purpose

Give every claim and artifact in the project **one stable navigation surface**
that answers four questions without re-litigating them per turn:

1. Where does it sit in the source-strata? (`source_class`)
2. What does promoting it require? (`promotion_requirement`)
3. What does promoting it prematurely break? (`downstream_risk_if_promoted_early`)
4. What is the next safe action on it? (`recommended_next_action`)

The Authority Map is **not** a runtime spec. It is **canon-governance** — the
discipline that prevents cross-workspace synthesis from mistaking
*completeness, polish, recency, or coherence* for canon.

## §1 — Source-class taxonomy (`SC-0` … `SC-6`)

| Class | Name | Authority role | Promotion effect |
|---|---|---|---|
| `SC-0` | `operator_current_delta` | Highest active instruction for this turn | Constrains output immediately. Does not rewrite historical canon unless explicitly framed as correction. |
| `SC-1` | `dev_session_replay` | Primary canon-forming evidence | Can promote mutations only when *appearance, clarification, pressure survival, operative carry-forward, and non-supersession* are all shown. |
| `SC-2` | `operator_confirmed_artifact` | Strong evidence when linked to replay or explicit acceptance | Can confirm replay-derived canon. Cannot override replay by polish. |
| `SC-3` | `forensic_control_artifact` | Governs recovery posture, gaps, branch models, blockers | Routes or blocks downstream work. Usually not runtime canon itself. |
| `SC-4` | `candidate_runtime_or_product_spec` | Formal candidate, not promoted canon | May be used as candidate target *only with state labels*. |
| `SC-5` | `handoff_or_summary` | Derivative compression | Helps orient. Cannot promote claims independently. |
| `SC-6` | `diagram_or_image` | Human-view diagnostic or explanatory reference | Can reveal intended distinctions. Cannot establish canon by visual polish. |

The taxonomy is **ordinal**, not strict-monotonic: a `SC-2` claim does not
automatically outrank a `SC-3` claim — the *role* differs. `SC-3` artifacts
govern recovery; `SC-2` artifacts confirm canon. They operate on different
axes.

## §2 — Promotion Matrix row schema

Every Authority-Map row has exactly nine fields:

```yaml
- claim_or_artifact: string                # Short, addressable. Title-case.
  scope_plane: enum                        # PROJECT_MAESTRO | WORKSPACE_DEV |
                                           # BRIDGE_PROJECT_WORKSPACE |
                                           # UNRESOLVED_SCOPE
  source_class: enum                       # SC-0 .. SC-6 (or combined "SC-2 + SC-3")
  authority_tier: enum                     # high | high_with_qualifier |
                                           # medium | candidate | low | reference_only
  current_status: string                   # Single phrase describing state.
  promotion_requirement: string            # One sentence. What must be true to promote.
  blocking_reason: string                  # One sentence. Why not promoted now.
  downstream_risk_if_promoted_early: string  # One sentence. Concrete failure mode.
  recommended_next_action: string          # One sentence. Verb-first.
```

**Enforcement** (`apps/authority-map/`):

- All nine fields are required.
- `scope_plane` must be one of the four enums.
- `source_class` may be a single class (`SC-2`) or a typed compound
  (`SC-2 + SC-3`) — no free-text.
- `authority_tier` must be one of six enums (extensible via ADR).
- The four narrative fields (`current_status`, `promotion_requirement`,
  `blocking_reason`, `downstream_risk_if_promoted_early`,
  `recommended_next_action`) are exactly *one sentence each*. Multi-sentence
  values fail validation — they're a smell that two distinct concerns are
  being merged.

## §3 — Evidence-contract pairing

Each row in the Promotion Matrix should pair with an **evidence contract**
(future v0.2):

```yaml
- claim_or_artifact: <same as above>
  evidence_contract:
    one_sentence_per_subkey: true          # discipline enforced
    binding: string                        # what this claim commits to
    downstream_prediction: string          # what should observably follow
    challenge_cycle: string                # how to falsify
```

v0.1 ships **without** evidence_contract enforcement; v0.2 adds it. The
schema is reserved so the v0.2 migration is non-breaking.

## §4 — Files

| File | Role |
|---|---|
| `apps/authority-map/seed/authority_map_v0.1_seed.yaml` | The authoritative seed rows. Edit here. |
| `apps/authority-map/src/authority_map/schema.py` | Python dataclasses mirroring the row schema. |
| `apps/authority-map/src/authority_map/loader.py` | YAML loader + structural validation. |
| `apps/authority-map/src/authority_map/validator.py` | Run all checks. |
| `apps/authority-map/src/authority_map/cli.py` | `am list`, `am show <claim>`, `am validate`. |
| `apps/authority-map/tests/` | Schema, loader, validator tests. |

## §5 — Promotion procedure

1. Operator (or AI proposing) drafts a new row in the seed YAML or proposes
   a status change on an existing row.
2. The change goes through a PR. ADR-0002 patent quarantine applies — rows
   whose `claim_or_artifact` is Zone B require explicit operator F on the
   PR.
3. `apps/authority-map/` validates structural correctness.
4. Reviewer checks that the four narrative fields are each exactly one
   sentence and that `source_class` and `authority_tier` are honest.
5. Merge updates the seed; downstream slices read from it.

## §6 — What this slice does NOT do (v0.1 scope)

- Does not enforce evidence-contract semantics — that's v0.2.
- Does not auto-promote claims — promotion is always a PR, always operator-gated.
- Does not run against external corpora — the seed is in-repo, hand-curated.
- Does not interact with the triad-validator. That validator works at the
  Suno-emit boundary; the Authority Map works at the canon-governance layer.
- Does not generate Promotion Matrix rows from the cross-workspace synthesis
  automatically. Seed rows are written by hand; automation deferred.

## §7 — Acceptance test

`apps/authority-map/` ships with:

- Loader test that parses the seed YAML without error.
- Schema test that rejects malformed rows (missing fields, wrong enums,
  multi-sentence narrative fields).
- CLI smoke test (`am list` returns ≥ the seed-row count).
- A `validate` command that exits non-zero on any structural failure.

Acceptance: all of the above green, and the seed contains at least the six
rows from ws_3 forensic synthesis plus the four rows that emerged from this
session (triad-validator, ADRs 0001/0002/0003, the rebirth repo itself).

## §8 — Out of scope (deferred)

- Evidence contract enforcement (v0.2).
- Cross-workspace ingestion automation (v0.3).
- Diff/audit of authority-map changes across PRs (v0.4).
- Authority Map as substrate primitive on Mosaic (separate ADR if/when
  promotion is justified).

## §9 — Completion footer

```yaml
completion_status:
  label: PROVISIONAL
  scope_satisfied: true   # within stated v0.1 scope: taxonomy + row schema + seed + validator + CLI
  missing_edges:
    - evidence_contract enforcement (v0.2)
    - cross-workspace ingestion automation (v0.3)
  missing_nodes:
    - audit/diff tooling for authority-map changes
    - integration with the triad-validator audit shape
  unresolved_conflicts:
    - none in v0.1 scope; Promotion Matrix seed rows reflect ws_3 forensic stance, which is one workspace's view
  continuation_required: true
  safe_to_use_downstream: true   # as canon-governance discipline; not as runtime spec
```

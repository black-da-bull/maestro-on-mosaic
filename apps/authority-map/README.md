# Maestro Authority Map

Canon-governance discipline for the rebirth monorepo. Every claim and every
artifact gets one row in the Promotion Matrix that says where it sits in
the source-strata, what promoting it requires, what promoting it
prematurely breaks, and what the next safe action is.

See `docs/governance/authority-map-v0.1.md` for the full specification.

## Scope of v0.1 (this slice)

- **Source-class taxonomy** `SC-0` … `SC-6` (operator delta → diagram).
- **Promotion Matrix** with nine required fields per row, four of which
  are narrative and enforced to be exactly one sentence.
- **Seed file** with 16 rows: the six ws_3 forensic-synthesis rows plus
  ten emergent rows from the Day-1 / Day-2 work (triad-validator, the
  three ADRs, the v3 protocol docs, Mosaic.INV-11 draft, OOP draft,
  Authority Map itself, v4.5.5-clean, the rebirth repo).
- **Validator** that checks structural correctness and the
  one-sentence-per-subkey discipline.
- **CLI** with `list`, `show`, `scope`, and `validate` subcommands.

## What this slice does NOT do (yet)

- No evidence-contract enforcement — that's v0.2.
- No auto-promotion of claims — promotion is always a PR.
- No cross-workspace ingestion automation — seed rows are hand-curated.
- No integration with the triad-validator audit shape.

See spec §6 for the full deferred-items list and §8 for out-of-scope items.

## How it runs

```bash
# from apps/authority-map/
pip install -e .

am validate                                 # exit non-zero on any structural error
am list                                     # one-line summary of every row
am show "mosaic"                            # full row(s) matching a substring
am scope BRIDGE_PROJECT_WORKSPACE           # filter by scope plane
am --json list                              # JSON output for any subcommand
am --seed path/to/other.yaml validate       # validate an alternative seed
```

Default seed location: `apps/authority-map/seed/authority_map_v0.1_seed.yaml`.

## Tests

```bash
python -m pytest -q                         # 33 tests across schema, loader, validator
```

## Patent posture

Per ADR-0002, this slice is **Zone A (safe)**. The schema and discipline
are governance infrastructure, not novelty claims. Individual *rows*
inside the seed may reference Zone B material (kernel invariants, persona
schemas) — those references are pointer-only and contain no Zone B
content.

## Architectural placement

- **Application layer**, not Mosaic substrate. Whether to promote
  Authority Map to a substrate primitive is a future ADR decision.
- Operates at the **canon-governance boundary** — between claims and
  promoted canon — distinct from the triad-validator's **artifact-boundary
  gate** (Suno emit).
- Schema discipline derives from the v3 protocol's reassessment-and-state-
  correction log (see `docs/protocol/`).

## Completion footer

```yaml
completion_status:
  label: PROVISIONAL
  scope_satisfied: true   # within stated v0.1 scope
  missing_edges:
    - evidence_contract pairing (v0.2)
    - cross-workspace ingestion automation (v0.3)
  missing_nodes:
    - audit/diff tooling for authority-map changes across PRs
    - integration with triad-validator audit shape
  unresolved_conflicts:
    - v4.5.5-clean reconstruction row is blocked on missing create_window source
  continuation_required: true
  safe_to_use_downstream: true   # as canon-governance discipline; not as runtime spec
```

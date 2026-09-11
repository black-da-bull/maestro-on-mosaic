# ADR-0002: Patent quarantine boundary

- **Status**: Accepted
- **Date**: 2026-05-20
- **Deciders**: operator (filing status holder) + Claude (productization)
- **Scope**: entire repository while patent filing status is `pre-filing`
- **Supersedes**: none
- **Related**: ADR-0001 (repo layout — defers patent boundary to a separate ADR)

## Context

Operator confirmed patent filing status on Day-2: **pre-filing**. Multiple
novelty claims surfaced across the cross-workspace synthesis (~22 distinct
claims, ~15 flagged `pre_filing_sensitive`). Under pre-filing status, public
disclosure can foreclose patentability in some jurisdictions and weaken
priority dates everywhere.

The repository contains both safe material (e.g., the deterministic triad
validator — implements already-disclosed behavior) and material that is
near-adjacent to pre-filing novelty (e.g., kernel invariants, persona
schemas, UST axis structure). The boundary needs to be explicit so
contributors (human or AI) do not accidentally publish patent-sensitive
material.

## Decision

Adopt a three-zone quarantine for the duration of `pre-filing` status:

### Zone A — SAFE (always committable)

- Re-statements of behavior already publicly disclosed in
  operator-controlled artifacts that pre-date the filing window.
- Standard productization scaffolding: monorepo layout, Python packaging,
  CI configuration, license placeholders, test harnesses.
- The deterministic triad validator (`apps/triad-validator/`) and any future
  slice whose implementation merely enforces already-disclosed rules.
- Repository governance: ADRs, READMEs, contribution guides, this document.
- The v3 protocol documents (`docs/protocol/`) — already disseminated to
  prior operators; pre-dates the filing window.

### Zone B — GATED (commit only with explicit per-item operator F)

- Kernel invariants and substrate primitives (Maestro `INV-NN`, Mosaic
  `INV-NN`, M0–M11 phases, N0–N9 chain, CP1–CP4, NC-01..04, G0–G4).
- Persona stack schema details (the 4-layer or 9-element internal
  structure), persona-to-axis routing rules.
- Technical UST axis catalog beyond the public count (165 cells, 8 axes are
  public; per-axis K-tier internals are gated).
- Reverse-UST / VIG / SEL reverse-compilation pipeline internals.
- Authority Map v0.1 / evidence-contract slice internals (Day-2 next slice
  — operator F gates each artifact at commit time).
- The 14-defect taxonomy applied to operator workflow (not the items
  themselves; the *application as an executable system*).

### Zone C — FORBIDDEN (never committed until filing status advances)

- Per-claim novelty articulations as filed or as preserved for filing
  (the patent draft prose itself, claim language, prior-art citations
  prepared for the application, embodiments selected for inclusion).
- Any artifact tagged `pre_filing_sensitive: true` in cross-workspace
  synthesis without operator F countersign.
- NDA-marked content from any source. Tag at top-of-file but inline
  content never enters the repo.

## Enforcement

1. **Pre-commit lint** (deferred to a follow-up commit) — a script in
   `tools/patent-lint/` scans the diff for Zone C markers and rejects.
   Until that lands, enforcement is human (this ADR + operator review at
   PR time).
2. **PR template field** (when CI lands) — author must declare zone for
   the change.
3. **File-level marker** — Zone B files carry a top-of-file SPDX-style
   tag: `<!-- patent-zone: B -->`. Zone C files do not exist in the repo.
4. **Status transition** — when filing status advances to `in-progress`
   or `filed`, this ADR is amended with an updated zone table. The
   transition is a separate ADR (ADR-0002a or ADR-XXXX), not an in-place
   edit, to preserve the audit trail.

## What this means in practice for current artifacts

| Artifact | Zone | Notes |
|---|---|---|
| `apps/triad-validator/` (all) | A | Behavior already disclosed. Safe. |
| `docs/protocol/` (v3 docs) | A | Pre-dates filing window. |
| `docs/adr/` (all ADRs) | A | Governance, not novelty. |
| `docs/governance/INV-11-bounded-autonomy.md` | B | Mosaic kernel invariant candidate. Operator F to promote from DRAFT. |
| `docs/governance/OOP-operator-onboarding-protocol.md` | B | Mosaic substrate primitive. Operator F to promote. |
| `os/`, `sem/`, `templates/`, `examples/`, `personas/`, `artifacts/` (existing corpus) | A | Operator-committed before this ADR; pre-dates the filing window for repo purposes. Zone classification grandfathered. |
| `source/` (raw transcripts) | A | Provenance material, operator-owned. |

## Consequences

- Day-2 evidence-contract slice (Authority Map v0.1) will require
  per-artifact operator F at commit time — Zone B.
- v4.5.5-clean reconstruction (REPAIR-01..10) is mostly Zone A
  (re-statement of already-emitted behavior) but REPAIR-06 routing tags
  may touch Zone B; operator F at commit.
- Triad-validator profile extensions (`v5_c_freeze` etc.) are Zone A.
- All ADRs (this one included) are Zone A by definition — governance
  decisions, not novelty.

## Out of scope (explicit deferral)

- License selection: blocked by patent-first discipline until filing
  status advances. NOTICE.md may carry a placeholder.
- Public release readiness checklist: drafted only when filing status
  reaches `filed`.
- Bounty / contribution agreement language: drafted only when filing
  status reaches `filed`.

## Revisit triggers

- Filing status advances (any direction).
- A novelty claim is published elsewhere by operator, shifting it from
  Zone B/C to Zone A.
- A new Zone B/C category is identified during a future slice.
- Pre-commit lint lands and changes enforcement semantics.

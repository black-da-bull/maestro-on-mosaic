# ADR-0001: Rebirth repo layout

- **Status**: Accepted
- **Date**: 2026-05-20
- **Deciders**: operator + Claude (Day-1 prep session)
- **Scope**: rebirth monorepo (top-down v0 of Maestro/Mosaic)

## Context

Rebirth originated as a knowledge-corpus repository: `docs/`, `os/`, `sem/`,
`source/`, `artifacts/`, `personas/`, `examples/`, `templates/`,
`living-document/`. The string `source/` here means *source material*
(transcripts, raw exports) — **not** source code.

Day-1 prep introduced the first productization slice (`triad-validator`).
We need a home for runnable code that does not collide with the existing
corpus dirs, and a clearer partition inside `docs/` between governance
artifacts (kernel invariants, operator protocols) and architectural
explanation.

## Decision

Adopt a hybrid layout: standard monorepo `apps/` (and future `packages/`)
for code, plus Diátaxis-aligned partitioning inside `docs/`. Preserve the
knowledge-corpus top-level dirs unchanged because they are domain
categories, not generic repo categories.

```
rebirth/
├── apps/                 # productization slices (deployable)
│   └── triad-validator/  # first slice — INV-04 + length + structure checks
├── packages/             # (future) shared libraries
├── docs/
│   ├── adr/              # Architecture Decision Records (this file lives here)
│   ├── governance/       # kernel invariants, operator protocols
│   ├── ARCHITECTURE.md
│   ├── EVOLUTION.md
│   └── os-diff-report.md
├── os/                   # Maestro/Mosaic OS specs
├── sem/                  # Song Excellence Matrix corpus
├── personas/             # persona definitions
├── source/               # raw transcripts and exports (NOT source code)
├── artifacts/            # generated outputs (memos, monoliths, html)
├── examples/             # song-level example projects
├── templates/            # prompt templates
├── living-document/      # live working doc
├── CHANGELOG.md
├── NOTICE.md
└── README.md
```

## Standards applied

- **Monorepo**: `apps/` (deployables) plural convention — Nx / Turborepo /
  pnpm workspaces / Bazel norm.
- **Python packaging**: PyPA src-layout (`apps/<name>/src/<pkg>/`),
  PEP 621 `pyproject.toml`.
- **Docs**: Diátaxis framework — ADRs as the "explanation" quadrant for
  decisions; governance docs are reference-grade.
- **Migration**: `git mv` preserves history. No content rewritten in this
  ADR's commit; only relocation.
- **Commit hygiene**: Conventional Commits 1.0.

## Consequences

- Existing tooling/links targeting `docs/INV-11-bounded-autonomy.md` or
  `docs/OOP-operator-onboarding-protocol.md` must update to the
  `docs/governance/` paths.
- New productization slices land under `apps/<name>/`.
- The word `source/` continues to mean *source material* in this repo;
  code never lives there.
- Patent-sensitive material (pre-filing) does **not** land in this
  repository — it stays in operator-controlled storage with NDA/scope
  tags. A separate ADR will formalize the patent-quarantine boundary
  when filing status is confirmed.

## Out of scope (deferred)

- License selection (operator decision; patent-first discipline).
- CI/CD wiring (`.github/workflows/`).
- `packages/` introduction (not needed until a second slice shares code).
- Tombstone consolidation of OneDrive `maestro-ai-music-system-main/`
  corpus — handled per-slice as each lands in `apps/`.

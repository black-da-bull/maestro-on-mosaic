# Song Excellence Matrix (SEM)

*The linting system of Maestro / Mosaic — a substrate-layer component.*

The SEM checks a song artifact against a fixed ruleset and produces a score and
gate verdicts. Like a code linter, it **evaluates and flags; it never authors**.
It is the standard the orchestrator enforces — the orchestrator checks each
`value+condition` field against the SEM and nothing else, which is why "the
employees know the manager is based on it": the manager has no private taste,
its authority *is* the linter's output.

This document is the SEM as it stood at the end of its design session. The
iteration that produced it is recorded in `decisions/` and narrated in
`EVOLUTION.md`.

---

## 1. The weighted rubric (12 criteria)

Scale: 0–5 per criterion (0 = missing, 5 = outstanding). Weighted composite
sums to 100. Composite formula: `Σ[(score / 5) × weight%]`.

| # | Criterion | Weight % | Min pass |
|---|---|---|---|
| 1 | Hook Strength (melodic + lyrical memorability) | 18 | 4 |
| 2 | Lyric Integrity & Emotional Clarity | 12 | 3 |
| 3 | Vocal Delivery & Character | 10 | 3 |
| 4 | Melody & Topline Craft | 10 | 3 |
| 5 | Structure & Pacing | 8 | 3 |
| 6 | Production Quality (mix basics) | 12 | 3 |
| 7 | Arrangement Interest & Contrast | 6 | 2 |
| 8 | Commercial Viability & Market Fit | 8 | 3 |
| 9 | Originality / Distinctive Element | 6 | 2 |
| 10 | Metadata & Governance (tags, credits, UST fields) | 4 | 3 |
| 11 | Lyric Syllable Integrity (Suno 6–10 rule) | 4 | 4 |
| 12 | Pre-release QA & Lyric Compliance | 2 | 2 |

Criterion 12 carries a **binary gating field** — Lyric Change Compliance: if any
unauthorized edit to locked lyrics exists, the Production Gate auto-fails
regardless of composite score (see `decisions/0002`).

## 2. Pass threshold

- **Release-grade: composite ≥ 97.5 / 100.** This is operator canon. It is
  calibrated to the operator's somatic activation response, not to a generic
  rubric score.
- 70–97.4: targeted revision required.
- < 70: major rework.

The 97.5 threshold **supersedes** the 70/100 default the rubric was first
drafted with. Any run that quietly reverts to 70 is in violation of operator
canon (see `decisions/0004`).

## 3. Decision tree (go / no-go / iterate)

1. **Metadata Gate** — required fields present and valid? No → HOLD.
2. **Lyric Syllable Gate** — all `[Lyric Block]` lines 6–10 syllables? No → ITERATE.
3. **Hook Gate** — Hook Strength ≥ 4? No → ITERATE (rewrite topline/hook).
4. **Composite** — ≥ 97.5 → release candidate; 70–97.4 → targeted revision; < 70 → major rework.
5. **Production Gate** — mix check (LUFS, no clipping, low-end clarity)? No → mix pass.
6. **Final QA** — stems exported, integration ledger updated? No → finish deliverables.

## 4. SEG and G-Card (the operationalized SEM)

When the SEM is run inside the pipeline it produces two machine-readable
artifacts:

- **SEG** — *Song Excellence Governance*. The full weighted rubric plus gating
  logic, applied to a song. Output: `{criterion_scores, weighted_composite,
  gate_statuses, ranked_deficiencies}`.
- **G-Card** — *Governance Card*. The concise decision artifact for one run:
  `{final_decision, buy_in_pct, top_3_deficiencies, required_actions,
  next_iteration_deadline, ledger_ids}`. Decision is `PASS` / `CONDITIONAL` /
  `HOLD`.

Detection is deterministic: artifacts carry exact marker tokens
(`[[SEG:BEGIN]]…[[SEG:END]]`, `[[G-CARD:BEGIN]]…[[G-CARD:END]]`) and exact keys
(`seg.composite`, `seg.gates`, `gcard.decision`). No fuzzy matching (see
`decisions/0006`).

## 5. Position in the architecture

The SEM is **substrate** — a Mosaic-layer component, not a Maestro-application
feature. In compiler terms it is the **linter / diagnostics pass**: it runs
concurrently with creation (admissibility pressure *during* authoring, not a
post-hoc check) and the orchestrator routes work on its verdicts. It was not
designed top-down; it was iteratively thought into place across the design
session archived here.

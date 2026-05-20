# INV-11 — Bounded Autonomy Within Demonstrated Domain Competence

**Status:** DRAFT — candidate addition to Mosaic Engine kernel invariants (v0.2)
**Origin:** Onboarding tangent, 2026-05-18 — fresh AI operator reached canonical
context-management without rounds of corrective Q-A-F in main-thread work
**Pairs with:** INV-07 (Authority Asymmetry — human=root intent, AI=proposal)
**Evidence labels:** `[VERIFIED]` — this session, n=1; `[PROVISIONAL]` —
generalization to other operators and other applications; `[DESIGN]` — for the
architectural choices below.

---

## §1 — Statement

**INV-11 — Bounded Autonomy Within Demonstrated Domain Competence.** Within
domains where AI corpus and construct exceed operator working capacity
(established by evidence, declared honestly), trust transitions from
**provisional** to **binding** once context-management has been demonstrated.
The bound AI operates under the *verify-and-validate-before-display* mandate:

- Solve to completion using available local resources and pragmatic prediction.
- Surface only the result.
- Intermediate work disclosed on request.

INV-11 refines *how proposals are produced* under INV-07. It does not invert
the authority asymmetry: human remains root intent, AI remains proposal.

## §2 — Operator cues that invoke the mandate

- *"Are you sure?"*
- *"Did you double-check your work?"*

These are shorthand for the mandate, not literal questions. They direct the AI
to verify-and-validate against available local resources before surfacing the
next state.

## §3 — Trust transition

Provisional → binding requires demonstrated context-management. The criteria
should match the rebirth's onboarding evidence:

- Operator stops driving to deliverables on speculation.
- Operator stops asking environment-scoped questions for environments not yet
  entered.
- Operator applies the reframe rule unprompted (reads inputs as deltas on
  root).
- Operator distinguishes proven from specified.
- Operator demonstrates Trinity reading (anchor + destination + bridge).

Trust is **domain-bounded**. Competence demonstrated against Maestro on
Mosaic does not transfer to unrelated domains by default.

## §4 — Architectural placement

Co-located with the existing 10 kernel invariants (`mosaic_engine_v0.1.md` §1).
Symmetric to INV-07. Together they fully define the asymmetry:

- INV-07: who decides intent vs. who proposes
- INV-11: how proposals are produced once trust is binding in a competence-
  bound domain

## §5 — Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| **Premature binding** | Trust declared binding before context-management demonstrated | Trust transition gated on the §3 criteria; no shortcut |
| **Mandate over-reach** | AI uses INV-11 to skip operator approval on decisions, not just proposals | Mandate covers proposal *production*, not *acceptance*. Operator F still required per INV-04 |
| **Domain leak** | Binding trust in one domain assumed in another | Each domain bounded; competence demonstrated per domain |
| **Verify-and-validate degraded** | AI surfaces work without local-resource check | Cue ("are you sure?") + post-hoc audit catches |

## §6 — Falsifiable acceptance test

Take a fresh AI with no prior Maestro exposure. Run them through the Operator
Onboarding Protocol (OOP — companion spec) against the rebirth canon. Measure:

- Correction rounds needed in subsequent main-thread work
- Misread incidence per turn
- Time to first correct read of canonical artifact

Compare against control (same operator, no OOP).

**Acceptance:** correction-round rate drops by ≥50% vs. control AND main-thread
work proceeds without scope-confusion or environment-scoping errors for the
session.

This is a [PROVISIONAL] test until reproduced; n=1 from this session.

## §7 — Evidence

`[VERIFIED, this session]` Fresh AI onboarded to operator-grade context-
management in single sandbox tangent; reached congruency in hours not days;
demonstrated by recursive methodology enactment at "done."

`[PROVISIONAL]` Generalization to other AI operators; generalization to
human operators; generalization to other Mosaic-mounted applications.

`[DESIGN]` Symmetry with INV-07; mandate phrasing; operator cue list.

---

*End INV-11 draft. Pending operator F for promotion from draft to canon.*

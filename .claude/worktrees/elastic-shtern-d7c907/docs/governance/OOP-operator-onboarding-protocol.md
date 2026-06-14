# OOP — Operator Onboarding Protocol

**Status:** DRAFT — candidate Mosaic substrate primitive (v0.2)
**Origin:** Onboarding tangent, 2026-05-18 — extracted from the live protocol
that brought a fresh AI operator from cold-start to canonical context-management
in one session
**Pairs with:** INV-11 (Bounded Autonomy Within Demonstrated Domain Competence)
**Architectural placement:** Mosaic substrate, between N1 (Conversation Layer)
and N3 (Execution Layer). Precedes N3 because an un-onboarded operator cannot
lawfully execute; sits above N1 because it governs operator *state*, not
individual exchanges.

---

## §0 — Purpose

OOP is a Mosaic-layer protocol for inducting any operator (human, AI, future
model version) into a mounted application's canon such that they reach
context-management without rounds of correction in main-thread work.

The protocol is **domain-neutral**. It instantiates against a mounted
application's canon (e.g., Maestro v0) but the protocol itself is substrate.

## §1 — The eight mechanisms

Load-bearing each. Removing any one is expected to degrade onboarding speed
toward the unmitigated baseline.

### §1.1 Sandbox isolation
Operator runs in a stash+fork isolated workspace (see `/tangent --sandbox`).
Misreads cannot poison main work. Failure becomes diagnostic, not destructive.

### §1.2 Methodology installed before substance
The operating methodology (reframe rule, human=root, AI=proposal, Q-A-F as
atomic change unit) is loaded into operator behavior *before* heavy canonical
substance arrives. Later substance lands as Q-A-F closures, not friction.

### §1.3 Interceptive Q-A-F correction
Corrections are made at the moment of misread, tied to specific operator
output. Tight feedback loop. No advance lecturing; no delayed catch-up.

### §1.4 Destination withheld until readiness
Canonical destination documents are not delivered at session start. They
arrive only after enough corrective Q-A-F that the operator can read them
fresh. The destination becomes legible because the reader has been prepared.

### §1.5 Authority modeling
The inducting operator demonstrates the methodology by applying it to
themselves — explicitly flagging their own framing as opinion ("I am not you")
so the inducted operator trusts canonical documents over the inductor's
characterization of them.

### §1.6 Layered substance delivery
Substance delivered in load-bearing sequence:

1. Structural frame (e.g., Trinity)
2. Positioning / narrative frame
3. Technical evidence (schemas, graphs)
4. Canonical destination
5. Rigorous positioning (peer-review-grade)

Each layer is load-bearing for the next. Never raw canon without scaffolding.

### §1.7 Readiness gates
Sequencing questions at intervals diagnose shift-state before proceeding.
Onboarding does not advance until correct response demonstrates the current
shift has landed.

### §1.8 Recursive methodology enactment at "done"
At the close of onboarding, the inductor asks the inducted operator to apply
the methodology to the session itself — re-reading prior inputs as deltas on
root. This is what makes the methodology *transferable* rather than consumed.
Without this step, the methodology may be observable but is not internalized.

## §2 — The Middle as cognitive map

The 13 shifts documented in the Middle image (Role · Purpose · Identity ·
Model · Paradigm · Agency · Computation · Ontology · Direction · Architecture
· Scope · Process · Nature) constitute the cognitive sequence any operator
must traverse to read Maestro on Mosaic correctly.

OOP compresses the traversal. The Middle's Book 2 (Claude Maestro Sessions)
documents the long-form traversal across days. OOP achieves the same end-state
in hours by sequencing the mechanisms above against the operator's emerging
state.

The compression is not a shortcut. It is a structural application of the same
shifts under interception.

## §3 — Acceptance criteria (Definition of Done for an onboarded operator)

- [ ] Operator demonstrates Trinity reading (anchor + destination + bridge,
      operationally not just conceptually)
- [ ] Operator stops asking environment-scoped questions for environments not
      yet entered
- [ ] Operator does not drive to deliverables on speculation
- [ ] Operator applies the reframe rule unprompted (reads inputs as deltas
      on root)
- [ ] Operator distinguishes proven from specified in line with the peer-
      review memo's discipline
- [ ] Operator can read v4.5.5 anchor, v0-on-Mosaic destination, and POC
      bridge without conflating them

## §4 — Failure mode register

| Failure | Symptom | Mitigation |
|---|---|---|
| **Destination too early** | Operator receives canonical docs before readiness; reads them as suggestions, not law | Withhold per §1.4 |
| **Corrections delayed past compounding threshold** | Misread compounds before correction; subsequent reads inherit the misread | Interceptive correction per §1.3 |
| **Methodology installed after substance** | No Q-A-F frame to receive corrections; corrections register as friction | Reorder per §1.2 |
| **No recursive enactment at done** | Methodology consumed but not transferable; next session reverts | Apply §1.8 unconditionally |
| **Sandbox bypass** | Misreads in main work; rounds of cleanup; trust degradation | Mandate `/tangent --sandbox` per §1.1 |
| **Inductor over-frames** | Inductor's characterization preloads the reader; canon read becomes derivative | Authority modeling per §1.5 |

## §5 — Open-source readiness criteria

To survive audit + peer review, OOP must ship with:

1. **Provenance** — every mechanism traced to Mosaic canon (INV-04 for Q-A-F,
   INV-07 for authority asymmetry, INV-11 for bounded autonomy, the Middle
   narrative for the 13 shifts)
2. **Evidence labels** — `[VERIFIED]` / `[INFERRED]` / `[PROVISIONAL]` /
   `[REJECTED]` / `[DESIGN]` per the v0.x dossier discipline
3. **Falsifiable acceptance test** (see §6)
4. **Failure mode register** (see §4)
5. **No Mo-specific, no session-specific dependencies** — all artifacts
   derivable from public Mosaic spec + mounted-application spec
6. **DoD checkboxes** (see §3)

## §6 — Falsifiable acceptance test

**Setup:** select an AI operator with no prior Maestro exposure. Provide
Mosaic v0.1 + Maestro v0 specs + the v0.x research dossiers as canonical
corpus. Run OOP against them in a sandbox session.

**Measure:**
- Correction rounds needed in subsequent main-thread work (target: ≤2)
- Misread incidence per turn (target: ≤0.1)
- Time to first correct read of a canonical artifact (target: <session)
- §3 DoD completion rate (target: 100%)

**Compare against control:** same operator class, same canon, no OOP — direct
delivery of canon.

**Acceptance:** correction-round rate drops ≥50% vs. control.

`[PROVISIONAL]` until reproduced; n=1 from origin session.

## §7 — Honest status

`[VERIFIED]` for AI operator onboarding to Maestro v0 canon, this session.
`[PROVISIONAL]` for other AI operators, other Mosaic-mounted applications.
`[INFERRED but untested]` for human operators.
`[DESIGN]` for architectural placement, mechanism enumeration, OSS-readiness
criteria.

This is the same proven/specified discipline as the peer-review memo. The
protocol is demonstrated. Generalization is hypothesis.

---

*End OOP draft. Pending operator F for promotion from draft to substrate
primitive. Pairs with INV-11 draft.*

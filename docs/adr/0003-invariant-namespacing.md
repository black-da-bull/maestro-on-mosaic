# ADR-0003: Invariant ID namespacing — `Maestro.INV-NN` / `Mosaic.INV-NN`

- **Status**: Accepted
- **Date**: 2026-05-20
- **Deciders**: operator + Claude (Day-2 conflict-resolution pass)
- **Scope**: every `INV-NN` reference across the repository
- **Related**: ADR-0002 (patent quarantine — Zone B includes invariants)
- **Resolves**: cross-workspace Day-1 finding "INV-04 numbering conflict"

## Context

Day-1 cross-workspace synthesis surfaced a numbering conflict:

- A reading of `maestro.md` placed `INV-04` at **"NO COMMAS OUTSIDE LYRICS
  BLOCK"** (a Maestro container-formatting invariant).
- Workspace `ws_4` cited `INV-04` as **"phantom commitment intercept"** —
  the Q-A-F atomicity rule at emit time.

Verification against `mosaic_engine_v0.1.md` §1 (the Mosaic kernel
invariants table) confirmed:

| ID | Invariant | Source spec |
|---|---|---|
| `INV-04` | Q-A-F is atomic change unit; Q+A without F is open ticket | Mosaic |
| `INV-04` | NO COMMAS OUTSIDE LYRICS BLOCK | Maestro |

Both spelling are correct *inside their own spec*. The conflict is a
namespace collision, not a versioning conflict. ws_4 was reading the
Mosaic spec; the earlier read targeted the Maestro spec.

Operator framed the resolution method on Day-2: classify the conflict
first (different items / chronological supersession / human-vs-AI
construct), then apply the appropriate 4E + exploit operator. This
conflict classifies as **different items in different specs**;
resolution operator is **explain**.

## Decision

Adopt namespace-qualified invariant IDs across the repository:

```
<Spec>.INV-NN
```

where `<Spec>` is one of: `Maestro`, `Mosaic`. Examples:

- `Maestro.INV-04` — NO COMMAS OUTSIDE LYRICS BLOCK
- `Mosaic.INV-04` — Q-A-F atomic change unit
- `Mosaic.INV-07` — Authority Asymmetry
- `Mosaic.INV-11` — Bounded Autonomy Within Demonstrated Domain Competence
- `Mosaic.INV-08` — Substrate is depth-accumulation

A bare `INV-NN` reference is **ambiguous** and must be rewritten when
encountered. New artifacts use the qualified form from the start.

The same convention extends to other numbered enumerations when
collisions are found:

- `Maestro.M0` … `Maestro.M11` (workflow phases)
- `Mosaic.N0` … `Mosaic.N9` (substrate chain)
- `Mosaic.CP1` … `Mosaic.CP4` (checkpoints)
- `Mosaic.NC-01` … `Mosaic.NC-04` (negative costs)
- `Mosaic.G0` … `Mosaic.G4` (governance modules)

Operator F is required before promoting any individual invariant ID into
a published spec; namespacing is purely a *reference disambiguation*
decision and does not change the canonical invariants themselves.

## Format choice rationale

- **Dot notation** (`Spec.ID`): familiar from package/module paths,
  unambiguous, parses cleanly in markdown and code, sortable.
- Rejected: slash notation (`Spec/INV-NN`) — collides with file path
  conventions, harder to grep.
- Rejected: hyphen notation (`MAESTRO-INV-04`) — visually noisy, easy
  to mis-parse the hyphens as separator vs internal.
- Rejected: prefix shorthand (`M-INV-04` / `MO-INV-04`) — ambiguous;
  M could mean Maestro or Mosaic.

## Migration

The repository contains few invariant references today. Migration is
performed in this same change-set:

1. `docs/governance/INV-11-bounded-autonomy.md` — rewrite bare `INV-04`,
   `INV-07`, `INV-11` references to `Mosaic.INV-NN` form. Filename
   itself remains `INV-11-...` (file-level disambiguation deferred —
   rename only if a `Maestro.INV-11` candidate emerges).
2. `docs/governance/OOP-operator-onboarding-protocol.md` — apply the
   same rewrite to bare references.
3. `apps/triad-validator/` — currently references `INV-04` (comma
   policy) in code comments and `README.md`. Rewrite to
   `Maestro.INV-04`. The check itself does not change.
4. All future ADRs, governance docs, and code comments use the
   qualified form from the start.

## Enforcement

- **Author discipline** — primary mechanism today.
- **Pre-commit lint** (deferred to `tools/inv-lint/`) — flag bare
  `INV-NN` patterns outside historical artifacts and require either
  qualification or an explicit allowlist (e.g., when quoting a prior
  workspace verbatim).
- **Historical artifacts** (existing `os/`, `sem/`, `templates/`,
  `examples/`, `source/`, `artifacts/`) are **grandfathered** — bare
  references stay. Lint excludes those paths.

## Consequences

- Cross-workspace synthesis documents going forward will be free of
  the INV-04 ambiguity that surfaced this conflict.
- The triad-validator's INV-04 comment becomes self-documenting about
  *which* invariant it enforces.
- A future Maestro vs Mosaic invariant rename (e.g., one spec deprecates
  a number) is now expressible without ambiguity.
- Patent quarantine (ADR-0002) Zone B classification still applies to
  invariant content regardless of namespace; namespacing does not
  declassify anything.

## Out of scope

- Renumbering any existing invariant inside either spec. This ADR is a
  *reference convention*, not a *canon change*.
- Creating a master cross-reference table mapping every bare reference
  in the historical corpus. Lint + author discipline going forward;
  retroactive rewrite only if a specific search-and-replace pass is
  authorized.
- Extending namespacing to other systems (e.g., custom-GPT REPAIRs,
  PRQs, OD/OQ items) — those already carry origin tags in their IDs.

## Revisit triggers

- Pre-commit lint lands → tighten enforcement, narrow grandfather list.
- A third spec joins the kernel (unlikely near-term).
- An invariant moves from one spec to the other (e.g., Maestro promotes
  a rule to substrate level). Such a move must be its own ADR.

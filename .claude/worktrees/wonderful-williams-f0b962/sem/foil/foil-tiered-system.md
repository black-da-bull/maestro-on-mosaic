# FOIL — The Four-Tier Addressing & Cascade System

*A parallel substrate thread. Related to the SEM — not a phase inside it.*

## Provenance and honest placement

This document is reconstructed from a **separate** source conversation
(`source/foil-session.md`, a Big-AGI session dated 3/7/2026), not from the SEM
design session. It is archived on the `sem` branch because both are
**substrate** — Mosaic-layer machinery iteratively thought into place — and
because the two threads intersect directly: the FOIL conversation's own
`song-excellence-yaml` document is labelled the "Song Excellence governance
substrate."

It is **not** filed as "SEM Phase N." The source does not support nesting it
inside the SEM session, and this archive does not invent that structure. FOIL is
the tiered *addressing and cascade* system; SEM is the *linting* system; they
are siblings at the substrate layer.

## 1. The four tiers (sandbox spec v0.1)

FOIL organizes every controllable element of a song into four tiers:

- **Tier 1 — MACRO (globals).** Whole-song settings, declared once.
- **Tier 2 — MICRO (axis values).** Per-axis values: THY, VOC, STY, TIM, PER,
  POST, MAP, LYR.
- **Tier 3 — TACTICAL (section headers; roadmap; repeats).** Section-level
  structure, arrangement, repeat grammar.
- **Tier 4 — VARIABLE+1 (atomic line and word controls).** The smallest
  controllable units — individual lines and words.

The two addressing notations the session bridges:
`macro.key.subkey.variable+1`  ↔  `stanza.section-header.line.word`.

## 2. Cascade and composition

The "FOIL math" is the cascade: a value set at a higher tier flows down to every
lower tier it governs, unless a lower tier explicitly overrides it. This is what
lets a whole-song setting and a single-word control coexist without conflict —
and, in event-sourcing terms, it is why operations at distinct addresses stay
independent: an address names exactly one tier-located cell.

## 3. Duplicate Promotion Up-Shift

When the same value recurs across multiple lower-tier addresses, it is
**promoted upward** to the smallest tier that covers all its occurrences —
MICRO to TACTICAL, TACTICAL to MACRO. Recurrence determines scope. This is the
factoring rule the Maestro back end (FOIL) applies to a locked UST: hoist what
recurs to the smallest enclosing scope.

## 4. Relationship to the SEM

FOIL and SEM meet at the `song-excellence-yaml` the FOIL session defines as a
governance-substrate document. FOIL gives the song an addressable tier
structure; SEM lints the addressed artifact against the excellence ruleset. One
provides the addresses; the other checks what sits at them. Together they are
two of the substrate components Mosaic exists to make explicit.

## Reconstruction note

The FOIL session also contains persona portraits — a "Schema-Driven
Orchestrator" derived from a `STAFF.UST.CANON.V1` kernel, and a "Clarity
Architect" portrait. These are preserved verbatim in `source/foil-session.md`.
They are session artifacts, not part of the FOIL tier spec, and are not folded
into this document.

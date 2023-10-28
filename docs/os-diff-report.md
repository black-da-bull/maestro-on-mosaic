# Maestro OS — Version Diff Report

A line-level comparison of consecutive full **MoMoney Maestro OS** artifacts,
focused on **silent changes**: edits present in the document text that the
version's own announced upgrade notes do not mention.

---

## Corrections to the earlier changelog

Diffing exposed three things the version-label survey missed:

1. **The OS chain runs to v4.5.5, not v4.5.2.** Versions **v4.5.3, v4.5.4, and
   v4.5.5** exist as full monolithic artifacts. They were missed earlier because
   each is declared *deep inside* a very large assistant turn (10k–13k words),
   not in a turn header — `STATUS: COMPILING MoMoney Maestro OS v4.5.4`, etc.

2. **`v3.0` has a codename: `MoMoney Maestro v3.0g`.** In the Dynamic Living
   Document era (v1.1 / v1.2) the envisioned operating system is referred to as
   *"The Creative OS (Codename: MoMoney Maestro v3.0g)."* The `g` is part of the
   codename, not a separate version.

3. **The "196-line deletion" I flagged for v4.4.1 → v4.5.0 was a false alarm.**
   It was not a spec deletion. My artifact boundaries ran to the next timing
   line, so the v4.4.1 artifact over-captured ~180 lines of an *execution log*
   ("SYSTEM RECOVERY & RE-EXECUTION… ThroughTheFog_Test"). The real v4.4.1 →
   v4.5.0 spec change is small (see below).

Also: **"chimera"** is not a version. It appears once, in the app sidebar, as
the name of the project/thread — alongside "car" and "studio."

---

## Important structural caveat

The version-stamped artifacts are **not pure specification**. From v4.4.1
onward, the assistant increasingly appends **execution-run output** (lyric
validation tables, syllable counts, consensus simulations) into the same block
as the system prompt. So raw size and diff counts overstate how much *spec*
changed. Where this happens it is called out below.

---

## v4.5.0 → v4.5.2 — format change, not line-comparable

The artifact format changes here: v4.2.3–v4.5.0 are `SYSTEM PROMPT: … (Updated)`
documents (~2–5k words); v4.5.2 onward are `# MoMoney Maestro OS … (Monolithic
Prompt)` documents (~10–13k words). The line-similarity ratio is 0.00 — they
share almost no identical lines. v4.5.2 is a full re-issue that absorbs the
previously separate modular files (Personas & Teams, Frameworks, Templates,
Knowledge Base) into one monolithic prompt. Treat v4.5.2 as a fresh baseline.

For reference, the genuine spec change across the earlier `(Updated)` series:

- **v4.4.1 → v4.5.0** — the lyrics section header was redefined from
  `[sectionName | bars | production notes | SFX]` to
  `[sectionName | bars | v: vocal notes | s: style notes | SFX]`; `[VocalPersona]`
  gained the note "(consolidated from [Voice] and [CREW_TAGS])"; Phase 0 was
  marked "(Completed for this session)." Small, and broadly consistent with the
  labels.

---

## v4.5.2 → v4.5.3

**Announced:** integrate five new personas (Sonic_Architect, Lyrical_Therapist,
VocalMapper, Historian_Producer, AudioStyleCopilot), an updated AI_Arranger.vx4
directive, and new directives for Lyrical Drafting & Story Framing, Narrative
Arc Design, and Triple-Meaning Hooks.

**Matches the label:**

- The five personas were added to SECTION 2 (15 lines).
- AI_Arranger.vx4's role description was rewritten (now references
  `meta.container.rhythm…` logic).
- New KB sections added: **7.10** Lyrical Drafting & Story Framing Directives,
  **7.11** Narrative Arc Design Principles, **7.12** Hook Design Strategies
  (~23 lines), plus a "Triple-Meaning Hooks" line.

**Silent change (not in the label):**

- **PHASE 7.5 heading recapitalized:** `CROSS-DOMAIN ITERATION & RE-BLUEPRINT`
  → `Cross-Domain Iteration & Re-Blueprint`. Cosmetic, unannounced — and the
  start of a pattern (see below).

---

## v4.5.3 → v4.5.4

**Announced:** define the metacontainer `variable.x` format and the lyrics-block
ad-lib/SFX consolidation rule (including order); rerun lyric processing and
metacontainer formatting.

**Matches the label:**

- Metacontainer variables renamed throughout from `variablex` (lowercase) to
  `variableX` (PascalCase/CamelCase), with new rules added for single values,
  multiple values (`;`-separated), and alternatives (` OR `).
- Lyric-line consolidation rules added (ad-lib/SFX-only lines move to the end of
  the preceding line; defined line order).
- The Suno format template placeholders changed from `{snake_case}` to
  `{CamelCase}` — consistent with the variable rename.

**Silent changes (not in the label):**

- **PHASE 7.5 heading recapitalized again — back to ALL CAPS**
  (`Cross-Domain…` → `CROSS-DOMAIN…`). This now reverses the v4.5.3 edit.
- **~203 lines of execution-log output were embedded into the artifact** — a
  full "RE-EXECUTING WORKFLOW FROM PHASE 1.3" lyric-validation run with
  per-line syllable counts. The "rerun" was announced, but folding its *output*
  into the system-prompt document was not; it inflates the artifact and the
  diff. This is spec + run-log mixed in one block.

---

## v4.5.4 → v4.5.5

**Announced:** prioritize parsing ad-libs/SFX and apply the syllable count to
**quoted lyrical content only**, before consolidation; rerun lyric processing.

**Matches the label:**

- Syllable annotations changed from `(N syllables)` to `(N syllables quoted)`
  throughout the embedded validation log.
- SFX/ad-lib formatting cleaned (`(** ROOM HUSH )"` → `(ROOM HUSH)`); several
  lines that were previously flagged "too long" are now `OK` because the
  ad-lib/SFX text is excluded from the count.
- Validation rule text updated to state the count applies to quoted lyrics only.

**Silent changes (not in the label):**

- **Numbering defect in the Core Mandates list.** In v4.5.4 the numbered
  mandate list runs `1 … 7, 8. Self-Correction & Process Integrity Protocol`.
  In v4.5.5 the same list runs `1 … 7, 9. Self-Correction…` — it **skips item
  8 entirely** (7 → 9). No item was inserted; the heading was simply
  mis-numbered during regeneration. Unannounced, and a genuine defect.
- **PHASE 7.5 heading recapitalized a third time** (`CROSS-DOMAIN…` →
  `Cross-Domain…`). The casing has now flip-flopped across every version in the
  monolithic series: v4.5.3 Title → v4.5.4 CAPS → v4.5.5 Title. This is
  unmanaged formatting drift — a regeneration artifact, not an intentional edit.
- Minor in-place fix to an example value (`mode.GAEolian` → `mode.GAeolian`).

---

## Summary of silent changes

| Version | Silent change | Type | Severity |
|---|---|---|---|
| v4.5.3 | PHASE 7.5 heading recased (CAPS → Title) | cosmetic | low |
| v4.5.4 | PHASE 7.5 heading recased back (Title → CAPS) | cosmetic | low |
| v4.5.4 | ~203 lines of execution-log output embedded in the artifact | structural | medium |
| v4.5.5 | PHASE 7.5 heading recased again (CAPS → Title) | cosmetic | low |
| v4.5.5 | Core Mandates list skips item 8 (numbered 7 → 9) | defect | medium |

**Pattern:** the per-version *announced* changes are accurate — every labelled
change does appear in the diff. The silent issues are all **regeneration
drift**: heading capitalization that oscillates because the document is
re-emitted from scratch each version, a numbering slip in v4.5.5, and execution
output accreting into the spec. None of them change the OS's intended behavior,
but the item-8 skip and the embedded run-logs are worth fixing if these
artifacts are meant to be a clean version-controlled baseline.

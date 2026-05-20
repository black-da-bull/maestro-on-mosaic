# Maestro v3 Protocol — SSOT

This directory is the **single source of truth** for the Maestro v3 protocol
documents. References elsewhere in the repo (skills, ADRs, persona files,
agent prompts) must link here, not duplicate.

## Files

| File | Purpose |
|---|---|
| `MAESTRO_LOAD_SIDECHAIN_SLIPSTREAM_PROTOCOL_v3.md` | The Load / Sidechain / Slipstream model: how artifacts enter the session, how they cross-cut other artifacts, and how they propagate forward across turns. Defines the `sidechain_record`, `slipstream_record`, and `canon_patch` schemas. |
| `MAESTRO_EXECUTION_ENVIRONMENT_NARRATIVE_WIRING_META_PROMPT_v3.md` | The execution-environment wiring: how the protocol composes with the host model, the narrative-wiring meta prompt, and the per-turn completion footer (`v3 §12`). |
| `MAESTRO_REASSESSMENT_AND_STATE_CORRECTION_LOG.md` | The reassessment-and-state-correction discipline: how prior turns are re-read with hindsight, how defects are classified against the 14-defect taxonomy, and how state corrections are emitted as `canon_patch`es. |

## Provenance

Imported 2026-05-20 from operator's local Downloads area (canonical authoring
location at the time). v3 was developed across 2026-05-12 → 2026-05-14 and
behaviorally loaded across multiple sessions. Authorized into the repo as
SSOT per operator decision on Day-2 of the rebirth productization.

See `docs/adr/0001-repo-layout.md` for the layout decision context and
`docs/adr/0002-patent-quarantine.md` for the patent-quarantine boundary that
governs what can and cannot be committed alongside these protocol docs.

## Editing discipline

- Treat these files as **load-bearing canon**. Edits require a `canon_patch`
  entry in `MAESTRO_REASSESSMENT_AND_STATE_CORRECTION_LOG.md` plus the v3 §12
  completion footer on the commit message.
- Never paraphrase or summarize v3 protocol content in downstream artifacts.
  Link instead. (Maestro.INV-01: no summarization of canonical artifacts.)
- Version bumps: append a new file at `MAESTRO_*_v4.md` rather than
  overwriting v3, until v3 is explicitly deprecated by canon_patch.

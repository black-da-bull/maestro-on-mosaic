# Evolution — Why Maestro Changed

This project was not designed top-down. It grew **bottom to top**: every
version exists because something *surfaced* — a dropped detail, a
mis-parsed generation, a missing capability — and the change was the
response. The structure is the residue of that process.

This document tracks the **causal chain**. The version files in `os/` and
`living-document/` are the *what*; this is the *why*. Read it alongside
`examples/`, because most problems surfaced from a generation: the system
produced something, the output exposed a flaw, the flaw forced a version.

## The loop

```
   creative input ─▶ generation ─▶ flaw surfaces in the output
        ▲                                      │
        └──────── new version absorbs it ◀──────┘
```

Three OS versions were driven directly by a generation exposing a defect:
**v4.4.1** (vocals failing), **v4.5.2** (semicolons not detected),
**v4.5.5** (ad-libs counted as lyric syllables). These are marked
*generation-driven* below.

## Beneath the transcript

The version chain below is **not the bottom**. It is the layer where a far
larger body of work was finally written down. MoMoney Maestro is, by the
project's own account, the result of **26,000+ Suno generation sessions and
15,000+ GPT sessions** — roughly 41,000 sessions of generating, listening,
and iterating.

That corpus is the true ground floor. Every empirical rule the OS enforces —
the 6-11 syllable range, the lyrics-block structure, ad-lib and SFX handling,
genre and format conventions — was *discovered* there, by running generations
and hearing what failed. The versions in this archive are where those
findings were consolidated into something executable. So when a release below
is marked *generation-driven*, that single visible run is standing in for
thousands like it: the transcript records the moment a long-known failure
finally got written into the spec.

Read this way, the archive is the tip of the process, not its origin — the
consolidation of tens of thousands of sessions into eighteen versions.

## The founding grievance

One concern recurs from the first day to the last and explains most of the
history: **prior AI sessions silently dropped detail** — through
summarization, truncation, and "(this section unchanged)" placeholders.
Stated explicitly at DLD v1.1, it is the reason the project demanded a
single, auditable, self-contained artifact, and the reason nearly every
later version is a correction of the system losing or mis-handling
something. The project is, in large part, a long fight against entropy in
its own process.

---

## Dynamic Living Document

### v1.0 — initial draft
- **Surfaced:** a research brief on multi-agent AI musicology was provided
  as the starting seed.
- **Response:** first draft of a living document; establishes the AI
  "band" concept.

### v1.1 — creative OS workflow
- **Surfaced:** *the founding grievance* — previous GPT sessions had
  dropped workflow detail via summarization and truncation. The process
  had to become auditable, peer-reviewable, and fully self-executing, with
  no placeholder text.
- **Response:** the Creative OS workflow layer; the no-summarization /
  no-placeholder rule that governs everything after.

### v1.2 — sonic orchestrator and system personas
- **Surfaced:** the document was still incomplete; more of the workflow
  needed writing.
- **Response:** Sonic Orchestrator workflow and the first system personas.

### v1.3 — deepsearch research persona
- **Surfaced:** a request for deeper research grounding (`/deepdive`).
- **Response:** the DeepSearch AI Research Assistant persona.

### v2.0 — full session synthesis
- **Surfaced:** an entire prior working session's design had never been
  captured; the user pasted its full transcript.
- **Response:** the document is rebuilt as a synthesis of that whole
  session.

### v2.1 — integration scaffolding for the creative OS
- **Surfaced:** the AI had drifted into Q&A mode — answering messages
  instead of building cumulatively on every prior one.
- **Response:** reframed as scaffolding for the operating system; a
  re-commitment to iterative-build mode. Hands off to the OS lineage.

---

## MoMoney Maestro OS

### v3.0 — first single-prompt consolidation
- **Surfaced:** the work was scattered across many separate responses and
  inputs and needed to be one consolidated, executable prompt.
- **Response:** the first MoMoney Maestro OS (codename *Maestro v3.0g*).

### v4.2.3 — composer-class operating system
- **Surfaced:** roughly 312 development checkpoints and day-long iterative
  test sessions of prior off-transcript work were at risk of being
  dropped.
- **Response:** re-cast as "The Composer-Class Operating System," folding
  that history in. This is why the number jumps 3.0 → 4.2.3 — the gap is
  inherited history, not lost versions.
- **Generated:** the gospel-trap anthem and the 2026 club banger — the
  first end-to-end runs. The club banger becomes the project's permanent
  test piece.

### v4.3.0 — system-level reconfiguration
- **Surfaced:** many corrective exchanges and UST-structure changes were
  not reflected in the prompt, and legacy USTs using the old crew-tag /
  road-map format would break.
- **Response:** a system-level reconfiguration; defined migration behavior
  for legacy USTs.

### v4.3.1 — visionary chronicler persona
- **Surfaced:** a finished UST had no path to becoming a show summary.
- **Response:** the Visionary Chronicler persona.

### v4.3.2 — dj mo money persona
- **Surfaced:** the user's own creative identity was absent from the
  system it was being built for.
- **Response:** the DJ Mo Money "Sonic Theologian" persona is integrated
  as a core voice.

### v4.4.0 — self-correction protocols
- **Surfaced:** the AI kept failing to absorb the meta-lessons of how the
  user actually works — non-linear, tangent-filled, revisiting earlier
  ideas — and kept losing detail because of it.
- **Response:** self-correction protocols, so the system can take in
  non-linear development without dropping pieces.

### v4.4.1 — syllable and lyrics-block spec  *(generation-driven)*
- **Surfaced:** a generated run exposed the vocals failing. The 6-11
  syllable target and the lyrics-block structure existed in intent but
  were not being enforced on output.
- **Response:** the 6-11 syllables-per-line rule and the formal
  lyrics-block structure with ad-lib / SFX placement.

### v4.5.0 — knowledge ingestion; v:/s: section headers
- **Surfaced:** a body of ingested knowledge needed formal absorption and
  a fresh baseline.
- **Response:** the Phase 0 ingestion pass; the lyrics section header is
  redefined to `[name | bars | v: vocal | s: style | SFX]`; `[VocalPersona]`
  consolidates the older `[Voice]` and `[CREW_TAGS]`.

### v4.5.1 — personas & teams architecture
- **Surfaced:** changes scattered across the previous 5-7 exchanges needed
  consolidating into one clean baseline.
- **Response:** a full rebuild and the Personas & Teams architecture. No
  monolithic spec change is tagged here — the prompt is re-issued whole at
  v4.5.2.

### v4.5.2 — monolithic prompt compile  *(generation-driven)*
- **Surfaced:** a generation revealed that lyrics use semicolons, not
  commas, as line-break points — and the system had failed to detect them.
- **Response:** the OS is re-issued as a single monolithic prompt;
  semicolon-as-line-break detection is enforced.

### v4.5.3 — new personas and KB sections 7.10-7.12
- **Surfaced:** a more advanced external vetting system and a set of new
  personas and directives became available to absorb.
- **Response:** five new personas and KB sections on lyrical drafting,
  narrative arc, and hook design.
- **Silent:** the PHASE 7.5 heading was recapitalized without being noted.

### v4.5.4 — metacontainer variableX formatting  *(generation-driven)*
- **Surfaced:** in practice, metacontainer variable formatting and the
  ad-lib / SFX consolidation rules were too imprecise to apply
  consistently.
- **Response:** strict `variableX` formatting rules; lyric-line
  consolidation rules.
- **Silent:** the PHASE 7.5 heading was recased back; ~200 lines of
  execution output were embedded in the source artifact.

### v4.5.5 — quoted-only syllable counting  *(generation-driven)*
- **Surfaced:** inspecting a generated run's syllable validation showed
  the system was counting ad-libs, SFX, and bad text-formatting as part of
  the vocalist's syllable count — it was validating the wrong thing.
- **Response:** syllable counting is restricted to quoted lyrical content;
  ad-libs and SFX are parsed out first.
- **Silent:** the Core Mandates list lost item 8 (numbered 7 → 9); the
  PHASE 7.5 heading was recased a third time.

---

## What the chain shows

- **Generations are the test instrument.** v4.4.1, v4.5.2, and v4.5.5 — the
  most consequential lyric-handling rules — all came from a run failing in
  a way nobody had specified in advance. The `examples/` folders are not
  decoration; they are where the requirements were discovered.
- **The recurring failure mode is the system losing detail.** v1.1, v2.1,
  v4.3.0, and v4.4.0 are all, at root, the same correction repeated: stop
  dropping things. The self-correction protocols at v4.4.0 are the
  project's attempt to make that fix structural rather than manual.
- **Late-stage drift is real.** From v4.5.3 on, regenerating the whole
  monolithic prompt each version introduced unannounced changes (heading
  case, a numbering skip). The process that fought entropy began to
  generate its own. See `docs/os-diff-report.md`.

# Notice — Provenance

This repository is a **reconstruction**. No git history existed; this archive
restores one for the **Maestro application lineage**.

## Two layers — what is, and is not, in this repository

What is archived here is **Maestro**, the music application. Maestro runs on
**Mosaic**, a domain-neutral cognitive substrate that is **not** in this
repository.

Mosaic is the empirical model of how the target platforms — the language model
and the Suno parser — actually behave: where they drift, where they compress,
what their input fields silently enforce. It was derived from **more than
26,000 Suno generation sessions and more than 15,000 GPT sessions** — roughly
41,000 sessions of generating, listening, and iterating.

That figure is not provenance trivia. It is the **substrate layer**. The
version chain in this repository (`v1.0` → `v4.5.5`) is where Maestro's
application logic was written down and made executable; the ~41,000 sessions
are the substrate beneath it on which the application's empirical rules were
discovered. The single chat session this archive is built from is best read as
the **final assembly** of the application layer, not the origin of the system.

## The lineage, and what lies beyond it

This archive covers `v1.0` → `v4.5.5` — the **proven Maestro lineage**. It is a
working system: it has produced finished, release-grade songs.

Two later stages post-date this archive and are not included:

- **v5** — a known-flawed branch, treated as diagnostic rather than canonical.
- **v0 on Mosaic** — the *rebirth*: the proven system re-founded on the Mosaic
  substrate. It is specified across a separate corpus and is entering
  proof-of-concept. It is designed, not yet verified.

The archive is therefore the proven predecessor of the rebirth, not the current
state of the project.

## How the application's rules were found

The empirical rules the OS enforces — syllable ranges, lyrics-block structure,
ad-lib and SFX handling, genre and format conventions — were **discovered
bottom-up**, by running generations and observing how Suno's parser actually
responded. The eight-axis schema is, in effect, a grammar reverse-engineered
from the platform's behavior across the ~41,000-session substrate. The ontology
is empirical before it is theoretical.

## Reconstruction notes

- Every tracked file is derived from one source export, preserved verbatim at
  `source/raw-export.txt`.
- Version files are clean spec: conversational framing and embedded
  execution-run logs were trimmed. Nothing was paraphrased or rewritten.
- Commit dates are reconstructed to preserve ordering and do not reflect real
  authoring times.
- Commit and tag boundaries follow the version markers declared in the source.
  Where the numbering is non-continuous — the `v3.0` → `v4.2.3` jump, the
  `v4.5.1` iteration that carries no monolithic spec change — that is
  **inherited history**, documented in the relevant commit message and in
  `CHANGELOG.md`. It is not missing versions.

## A note on the diff report

`docs/os-diff-report.md` records line-level differences between consecutive OS
versions, including a few changes the version labels did not call out: a
section heading whose capitalization oscillates across `v4.5.3`–`v4.5.5`, and a
numbered list that skips an item at `v4.5.5`.

These are **artifacts of the documentation medium** — the consequence of
re-emitting a ~13,000-word monolithic prompt by hand each version. They are
noise in the output text, not evidence of the system degrading; the system was
operational throughout the lineage. An earlier edition of this archive framed
them as process "drift"; that framing is **retracted**. They are cosmetic
transcription artifacts, recorded for completeness.

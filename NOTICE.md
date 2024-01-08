# Notice — Provenance

This repository is a **reconstruction**. No git history existed; this archive
restores one.

## Scale

What is captured here is the **consolidation layer** of a much larger effort.
By the project's own account, MoMoney Maestro is the result of **more than
26,000 Suno generation sessions and more than 15,000 GPT sessions** — roughly
41,000 sessions of trial, listening, and iteration.

The version chain in this repository (`v1.0` → `v4.5.5`) is where that
accumulated knowledge was *written down and made executable*. It is not where
the knowledge was discovered. The empirical rules the OS enforces — syllable
ranges, lyrics-block structure, ad-lib/SFX handling, genre and format
conventions — were found by running tens of thousands of generations and
hearing what failed. When OS v4.2.3 "folds in ~312 checkpoints," those
checkpoints are themselves a distillation of that far larger corpus.

The single chat session this archive is built from is therefore best read as
the **final assembly** of that body of work, not its origin.

## Reconstruction notes

This archive was assembled from one source export of that consolidation
session:

- Every tracked file is derived from one source export, preserved verbatim at
  `source/raw-export.txt`.
- Version files are clean spec: conversational framing and embedded
  execution-run logs were trimmed. Nothing was paraphrased or rewritten.
- Commit dates are reconstructed to preserve ordering and do not reflect the
  real authoring times.
- Commit and tag boundaries follow the version markers declared in the source.
  Where the source numbering is itself irregular (the v3.0 to v4.2.3 jump; the
  v4.5.1 iteration that carries no monolithic spec change), this is documented
  in the relevant commit message and in `CHANGELOG.md`.

See `docs/os-diff-report.md` for changes the version labels did not announce.

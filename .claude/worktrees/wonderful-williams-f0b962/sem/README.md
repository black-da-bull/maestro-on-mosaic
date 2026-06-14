# SEM Branch — Song Excellence Matrix (Substrate Layer)

This branch archives the **Song Excellence Matrix (SEM)** and the **FOIL**
tiered-addressing system — two **substrate-layer** components of Maestro /
Mosaic, each iteratively thought into place across its own working session.

It is a branch of the Maestro archive, not a separate repository: checked out
here you have the full Maestro application history (`main`) plus the SEM
substrate work added on top.

## What the SEM is

The SEM is the **linting system**. It checks a song artifact against a fixed
ruleset and emits a score and gate verdicts; like a code linter, it evaluates
and flags but never authors. It is the standard the orchestrator enforces —
which is why "the employees know the manager is based on it": the manager has no
private taste, its authority *is* the linter's output.

## How this branch is built — event sourcing

Reconstructing a canonical artifact from a non-linear working-session transcript
is a long-solved class of problem (the same one posed by dev screen-shares,
engineering call logs, and operative-room transcripts). This branch applies the
established discipline rather than inventing one:

- `source/sem-session.md` — the transcript, treated as an **append-only event
  log**. The source of truth.
- `changes.md` — the **change-operation log**: each operation extracted with an
  address, a scope (macro → atomic), and a `supersedes` pointer where it revises
  an earlier one. Superseded operations are kept, marked, never deleted.
- `song-excellence-matrix.md` — the **canonical SEM**: not authored, but the
  *fold* of the operation log.
- `EVOLUTION.md` — the narrative of the fold, and the unidentified-substrate
  realization that explains why v5 broke.

## Layout

| Path | Contents |
|---|---|
| `sem/song-excellence-matrix.md` | The canonical SEM — the fold of the change log. |
| `sem/changes.md` | The change-operation log (event log of addressed operations). |
| `sem/EVOLUTION.md` | The fold narrative; the unidentified-substrate realization. |
| `sem/foil/foil-tiered-system.md` | The FOIL four-tier addressing system — a parallel substrate thread. |
| `sem/source/sem-session.md` | The SEM design session transcript, cleaned and segmented. |
| `sem/source/foil-session.md` | The FOIL conversation, verbatim. |

## Honest scope notes

- The SEM session is one continuous design arc with **no clean `vX.X` release
  stamps**. The `sem-v*` tags mark **fold checkpoints**, not declared releases.
- The FOIL file is a **separate** conversation, archived here as a related
  substrate thread — not as a phase inside the SEM session. The source does not
  support nesting it, and this archive does not invent that.
- SEG / G-Card / Chaos-Decomposer material is included, as the SEM
  operationalized.
- Nothing is paraphrased; where the source is imprecise (e.g. an operation's
  exact turn), that is flagged in `changes.md` rather than asserted.

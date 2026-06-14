# SEM Change-Operation Log

This is the **event log** for the Song Excellence Matrix. The canonical
`song-excellence-matrix.md` is not authored — it is the *fold* of the operations
below, applied in order. State at any version is a replay up to that point.

Each operation carries an **address** (what it touches), a **scope** (macro →
atomic), and, where it revises an earlier operation, a `supersedes` pointer. The
superseded operation is never deleted; it stays visible here, marked. This is
the append-only amendment discipline — the same one operative reports and
accounting ledgers use.

Source: `source/sem-session.md` (the transcript = the raw event log).

| Op | Turn | Scope | Address | Operation | Supersedes |
|---|---|---|---|---|---|
| SEM-0001 | 1–2 | macro | `sem.rubric` | Create the 12-criterion weighted rubric; weights sum to 100; 0–5 scale. | — |
| SEM-0002 | 1–2 | macro | `sem.threshold` | Set composite pass threshold = **70/100**. | — |
| SEM-0003 | 1–2 | meso | `sem.decision_tree` | Add the go / no-go / iterate decision tree (metadata, syllable, hook, composite, production, QA gates). | — |
| SEM-0004 | 3 | meso | `sem.criterion.12` | Replace generic "Pre-release QA" with **Pre-release QA & Lyric Compliance**; add binary Lyric-Change-Compliance gate (unauthorized edit → auto-fail Production Gate). Rebalance weights to sum 100. | SEM-0001 |
| SEM-0005 | 3 | meso | `sem.versioning` | Add lyric-version semantic numbering and immutable diff pointers (integration ledger). | — |
| SEM-0006 | ~6 | meso | `sem.rubric` | Persona stress-test: six genre-hitmaker personas each return 5 positive / 5 negative critiques of the rubric (adversarial evaluative pressure on the SEM itself). No weight change committed — critiques logged as pressure. | — |
| SEM-0007 | ~10 | macro | `sem.host` | SEM absorbed into **Chaos-Decomposer v1.6** — the multi-agent decomposition engine. SEM becomes the admissibility stage of a larger pipeline (M0–M14). | — |
| SEM-0008 | 13 | macro | `sem.threshold` | **Correct threshold to 97.5/100.** Operator canon: "who said 70%? we are 97.5%." 70 was an AI default; it never reflected operator intent. | **SEM-0002** |
| SEM-0009 | ~24 | meso | `sem.seg` `sem.gcard` | Operationalize SEM as two machine-readable artifacts: **SEG** (Song Excellence Governance — scores + gates) and **G-Card** (the per-run release-decision card). Deterministic marker tokens and exact keys defined. | — |
| SEM-0010 | ~26 | macro | `sem.runtime` | SEM/SEG/G-Card targeted at a **zero-touch monolithic prompt** — one sequential executable: song in → pipeline → final UST + show summary out. | — |

## Reconstruction notes

- This log is **derived from the transcript, not invented.** Where the source
  does not pin an operation to an exact turn, the turn is given as `~N` and
  flagged here rather than asserted precisely.
- The session is one continuous design arc; it carries no clean `vX.X` release
  stamps. The `sem-v*` tags in this branch mark **fold checkpoints** — points
  where the projected state was coherent — not releases the source declared.
- **SEM-0008 supersedes SEM-0002.** Per the append-only rule, SEM-0002 is not
  removed; it remains in this log as the superseded record. The canonical
  `song-excellence-matrix.md` shows 97.5 because it is the fold *after*
  SEM-0008; the 70 is visible here as history.
- The persona stress-test (SEM-0006) applied real adversarial pressure but the
  source commits no resulting weight change — so none is recorded. Pressure
  without a committed delta is logged as pressure, not folded as a change.

# Evolution — The SEM, and the Unidentified Substrate

The Song Excellence Matrix is the **linting system** of Maestro / Mosaic — it
checks a song against a fixed ruleset and emits a score and gate verdicts, and
it never authors content. This document narrates how it was iteratively thought
into place, and records the realization that gives the whole lineage its
through-line.

Read it alongside `changes.md` (the event log) and `song-excellence-matrix.md`
(the fold).

## The fold, in brief

The SEM began (SEM-0001/0002) as a compact 12-criterion weighted rubric with a
**70/100** pass threshold. A lyric-compliance gate was added (SEM-0004). Six
genre-hitmaker personas stress-tested it (SEM-0006) — adversarial pressure on
the rubric itself. It was then absorbed into Chaos-Decomposer v1.6 (SEM-0007),
its threshold corrected to the operator's real standard of **97.5** (SEM-0008),
operationalized as SEG + G-Card artifacts (SEM-0009), and aimed at a zero-touch
monolithic prompt (SEM-0010).

That is the visible arc. The important part is the substrate underneath it.

## The unidentified substrate

The Maestro lineage `v1`–`v4.5.x` ran inside a **custom GPT**. Every dev
session — this SEM session among them — and every execution fed back into that
GPT as knowledge files.

The operator worked on the assumption that those files were **static**: added,
or replaced whole. They were not. When the operator said "update" or "upgrade,"
the AI was **diffing the new onto the old** — merging deltas into the prior
state. That implicit diff-merge was load-bearing: it was doing the work of
holding the accumulated system together across sessions. And it was never
named. It was substrate, and it was unidentified.

This is why **v5 broke.** v5 was an AI-co-authored mega-prompt ported out of the
custom GPT into a distributed file system. Its content was not the problem; the
problem was that the implicit diffing substrate it had been silently standing on
did not port with it. The artifact moved; the engine did not.

It is also why the AI's updates could not be trusted — "false commits." A clean
"updated" report sat on top of a lossy silent merge the operator had no reason
to audit, because they did not know a merge was the operation. What survived the
port was a shell.

## Why this is a solved problem, not a novel one

Reconstructing an authoritative artifact and its change-history from a
transcript of a live, non-linear working session — with edits at several scopes
at once, and later edits revising earlier ones — is a long-solved class of
problem. Software-dev screen-shares, remote-site engineering calls, and
operative-room transcripts all pose it. The disciplines that solve it are
decades old:

- **Event sourcing** — the transcript is an append-only event log; the
  canonical artifact is the *fold* of that log. Later changes never mutate the
  past; they append. (`changes.md` is built this way.)
- **Addressed operations** — every change carries an address, so concurrent
  edits at distinct addresses localize and merge cleanly regardless of order.
  The macro-atomic addressing is what makes "seven places at once" tractable.
- **Append-only amendment** — the operative-report rule: a later record
  supersedes an earlier one with a pointer back; the superseded entry stays
  visible. SEM-0008 superseding SEM-0002 is recorded exactly this way.
- **Three-way merge** — the explicit, audited form of the "diffing new onto
  old" that was running invisibly in the custom GPT.

The correction is not to invent a Maestro-specific method. It is to make the
reconstruction discipline **explicit**. An event log plus a fold function is
substrate-portable by construction — which is exactly what v5 lacked.

## What this archive is

This branch is the SEM rebuilt on that discipline: the transcript as event log,
the change operations extracted with addresses and supersession pointers, the
canonical SEM as the fold. In doing so it does the thing the lineage most
needed — it takes the substrate that was implicit, invisible, and therefore
unportable, and makes it **identified**. That is the bridge from the SEM, past
the v5 break, to Mosaic: Mosaic is the substrate made explicit so the system can
be ported without breaking again.

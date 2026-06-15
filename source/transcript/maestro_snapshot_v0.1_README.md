# Maestro on Mosaic — Preservation Snapshot (maestro_snapshot_v0.1)

Built 2026-06-14 · 131 files · 27.1 MB
Canon kernel version: **5.0.2-dedup-kernel** (generated 2025-12-25T04:24:43Z)

This is **R1**: the asset gathered into one hashed, versioned, integrity-checked
bundle so it cannot be lost and can be carried forward. It is the backup that
did not previously exist (the ATP continuity slots were empty). **Preservation
only** — every file was copied verbatim; nothing was edited.

## THE BOUNDARY (read first)
- **Formalizable** → container rules: order, CAPs, lyric-lock, syllable bands,
  no-comma, the FOIL 4-tier schema and validators. These can become code.
- **Unformalizable** → flow / craft / soul. It lives in the running system and
  the accumulated chain. It does not survive being summarized into a spec
  (v5-b kept the container and lost the flow). Treat every artifact here as a
  pointer back to the runtime, not a replacement for it.

## Authority order (what governs what)
1. **04_runtime_ground_truth/** — the actual sessions. `who_dat.pdf` (v4.5.5
   staging) is PRIMARY behavioral truth; the FOIL session is canonical FOIL.
2. **01_canon_kernel/** — the current serialized canon (5.0.2-dedup-kernel):
   `maestro.yaml` and its 5 submodules (technical/creative UST, song_excellence,
   houseinorder, inmyroom).
3. **02_architecture/** + **03_os_config/** — the hierarchy + the Custom-GPT
   scaffolding across versions (momoney OS, v3.0g, v3.1.2).
4. **05_dev_sessions/** — the execution-chain record (how it got here).
5. **06_schemas/ · 07_assets/ · 08_substrate_corpus/** — supporting + substrate.
6. **09_derived_views_NONCANON/** — Claude's reconstruction (compiler + runtime
   state). PROPOSAL-CLASS. Defers to runtime + canon; never overrides them.

## Resurrection test (prove a fresh runtime before trusting it)
1. Explain Creative UST vs Technical UST.
2. Explain why the dev sessions are evolutionary substrate, not disposable.
3. Generate one valid Suno-ready Creative UST from a human seed.
4. Name one open null and defend why it stays unresolved.
5. Explain "Your Vision. Our Mission." with Lyrics Lock.

## Open nulls (preserved, not resolved)
G-Card sub-gate thresholds (70 vs 75) · SEM criterion count (12 vs 13, Memory
Activation axis) · PER vs PERF naming (canon source uses PER; left flagged) ·
v5-b "failed six-file patch" (runtime vs split) · whether v4.5.5 places flow
correctly (the v4.5.5-vs-v5-b A/B not yet run).

## Verify integrity
```
tar -xzf maestro_snapshot_v0.1.tar.gz
cd maestro_snapshot_v0.1
sha256sum -c 00_READ_FIRST/INTEGRITY.sha256     # every file, byte-exact
```
The detached checksum `maestro_snapshot_v0.1.tar.gz.sha256` is the anchor for the whole bundle.

## Next step (you)
Store `maestro_snapshot_v0.1.tar.gz` in **three** places (e.g. local + cloud + offline drive),
keep the `.sha256` beside each copy, and record this as ATP/CINR slot 0. When
the kernel changes, cut `v0.2` — never overwrite this one.

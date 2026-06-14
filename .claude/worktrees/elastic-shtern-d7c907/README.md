# Maestro Archive

A version-controlled archive of **Maestro** — a creative compiler for AI music
production — reconstructed as a proper git history.

## What Maestro is

Maestro converts an artist's creative intent into controllable, release-grade
music produced through Suno. Structurally it is a **compiler**: a loose creative
seed is the source, the **Technical UST** is the intermediate representation,
and three artifacts that Suno executes are the target. It treats Suno the way a
DAW treats audio — addressable and editable — rather than prompt-and-accept.

See `docs/ARCHITECTURE.md` for the full model.

## What this repository archives

This repository archives **one layer** of the system: the **Maestro
application** and its development lineage, `v1.0` → `v4.5.5`.

Maestro runs on a second layer, **Mosaic** — a domain-neutral cognitive
substrate derived from roughly 41,000 generation and iteration sessions
(26,000+ on Suno, 15,000+ with GPT). Mosaic is the empirical model of how the
target platforms actually behave. It is **not** in this repository; what is
here is the application that mounts on it.

The archive ends at `v4.5.5`, the **proven endpoint** of the lineage. Two later
stages post-date it and are not archived here: `v5`, a known-flawed branch kept
as diagnostic; and the re-platforming of the proven system as `v0` on Mosaic —
the *rebirth*, currently specified and entering proof-of-concept.

## What the archive tracks

1. **Structure** — the OS spec and document as they changed, version by version.
2. **Generations** — real end-to-end runs of the system on actual songs.
3. **The why** — a decision record for every version: what surfaced in use, and
   what changed in response.

## Layout

| Path | Contents |
|---|---|
| `os/maestro-os.md` | The Maestro OS — the application as a single executable prompt. Evolves v3.0 → v4.5.5. |
| `living-document/dynamic-living-document.md` | The earlier document form of the same system. Evolves v1.0 → v2.1. |
| `docs/ARCHITECTURE.md` | The compiler-on-a-substrate model: Mosaic, Maestro, the Technical UST. |
| `decisions/` | One decision record per version: what surfaced → what changed. |
| `docs/EVOLUTION.md` | The causal narrative — the lineage read bottom to top. |
| `personas/` | Persona definitions, added at the release that introduced each. |
| `templates/` | The Universal Song-Prompt Template and the Scalable Songwriting OS spec. |
| `examples/` | End-to-end runs — Maestro executed on real songs — by song and OS version. |
| `source/transcript.md` | The source assembly conversation, cleaned and segmented. |
| `source/raw-export.txt` | The verbatim original chat export, untouched. |
| `CHANGELOG.md` | Human-readable version index and changelog. |
| `docs/os-diff-report.md` | Line-level diff analysis between consecutive OS versions. |
| `NOTICE.md` | Provenance and reconstruction notes. |

## One system, two document forms

The history is **one continuous operational system** whose *codifying document*
changed form:

- **Dynamic Living Document** — `v1.0 → v2.1`. The system written as a living
  design document.
- **Maestro OS** — `v3.0 → v4.5.5`. The same system written as a single
  executable operating-system prompt (codenamed *Maestro v3.0g* in the planning
  era).

These are not two systems and not two separate projects — they are two forms of
the same system being written down. The version count is not continuous because
it carries **inherited history**: the jump from `v3.0` to `v4.2.3` folds in
~312 development checkpoints from earlier, off-transcript sessions. The
numbering reflects real lineage, not missing versions.

## Following the why

Each version has a decision record in `decisions/`, committed alongside the
release it explains. `docs/EVOLUTION.md` threads them into one narrative. The
through-line is **discovery, not repair**: most versions exist because running
the system surfaced a real property of the target platform that then had to be
encoded. From `v4.4.1` onward the system was being run on real songs, and the
runs themselves are where those properties surfaced — four versions are
generation-driven, and their decision records link to the run in `examples/`
that exposed the finding.

```
git log --oneline --all
git show os-v4.5.5            # release notes + Surfaced-by / Decision trailers
git diff os-v4.5.4 os-v4.5.5 -- os/maestro-os.md
```

Commits follow Conventional Commits: `release(os):` / `release(dld):` for
version cuts, `docs(examples):` for run artifacts, `docs:` / `chore:` for
supporting material. Release commits carry `Decision:` and, where applicable,
`Surfaced-by:` trailers.

## Fidelity

Committed version files are clean spec — conversational framing and embedded
execution-run logs were trimmed; nothing was paraphrased. The untouched
original is preserved at `source/raw-export.txt`. See `NOTICE.md` for full
provenance and `docs/ARCHITECTURE.md` for how this lineage relates to the
larger two-layer architecture.

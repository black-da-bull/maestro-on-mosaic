# Maestro Archive

A reconstructed, version-controlled archive of the **MoMoney Maestro** project —
an iteratively developed, single-prompt "operating system" for a songwriting /
rap production workflow.

The project was built entirely inside one long, non-linear AI chat session,
bottom to top, with no version control. This repository restores it as a proper
git history — and, just as importantly, captures **why** it evolved the way it
did. The project was reactive: every version is a response to something that
surfaced in use.

## The three layers

This archive tracks three things in parallel:

1. **Structure** — the OS spec and document as they changed, version by version.
2. **Generations** — real end-to-end runs of the system on actual songs.
3. **The why** — a decision record for every version: what surfaced, and what
   changed in response.

## Layout

| Path | Contents |
|---|---|
| `os/maestro-os.md` | The MoMoney Maestro OS system prompt. Evolves v3.0 → v4.5.5. |
| `living-document/dynamic-living-document.md` | The early scaffolding doc. Evolves v1.0 → v2.1. |
| `decisions/` | One decision record (ADR) per version: what surfaced → what changed. |
| `EVOLUTION.md` | The causal narrative — the project read bottom to top. |
| `personas/` | Persona definitions, added at the release that introduced each. |
| `templates/` | The Universal Song-Prompt Template and the Scalable Songwriting OS spec. |
| `examples/` | End-to-end runs — Maestro executed on real songs — organized by song and OS version. |
| `source/transcript.md` | The full source conversation, cleaned and segmented. |
| `source/raw-export.txt` | The verbatim original chat export, untouched. |
| `CHANGELOG.md` | Human-readable version index and changelog. |
| `docs/os-diff-report.md` | Line-level diff analysis, including silent changes. |
| `NOTICE.md` | Provenance and reconstruction notes. |

## Two lineages

The history is **not** one continuous version count:

- **Dynamic Living Document** — `v1.0 → v2.1`. The early scaffolding phase.
- **MoMoney Maestro OS** — `v3.0 → v4.5.5`. The operating system itself,
  codenamed *MoMoney Maestro v3.0g* in the planning era.

The OS line restarts numbering at `3.0`; the jump from `v3.0` to `v4.2.3`
folds in ~312 development checkpoints from earlier, off-transcript sessions.

## Following the why

Each version has a decision record in `decisions/` — numbered `0001`…`0019`,
committed alongside the release it explains. Every record states what surfaced,
whether a **generation** drove the change, and what was decided. `EVOLUTION.md`
threads them into one narrative.

From `v4.4.1` onward the system was being run on real songs, and the runs
themselves surfaced the problems. Four versions are generation-driven; their
decision records link directly to the run artifact in `examples/` that exposed
the issue.

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
provenance and `docs/os-diff-report.md` for changes the version labels did not
announce.

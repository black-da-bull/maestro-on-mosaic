# Architecture — Maestro as a Creative Compiler on Mosaic

This document describes the model the archived lineage belongs to. The version
files in `os/` and `living-document/` are the **Maestro application** evolving
over time; the architecture below is the system that application is part of,
made explicit. The proven artifact is the `v1.0`–`v4.5.5` lineage; the
compiler-on-a-substrate framing is the lens that lineage is best read through,
and the form the `v0` rebirth makes structural.

## Two layers

**Mosaic** is the substrate — a domain-neutral cognitive runtime that sits
between the operator and the generation model. It is the empirical model of how
the target platforms (the language model and the Suno parser) actually behave,
derived from ~41,000 generation and iteration sessions. A compiler is only as
good as its model of the target machine; Mosaic is that model.

**Maestro** is the application that mounts on Mosaic — the music-domain
compiler. This repository archives Maestro. Mosaic is not in this repository.

## Maestro is a compiler

Maestro has the shape of a compiler:

- **Source** — a creative seed: loose, under-specified human intent.
- **Intermediate representation** — the Technical UST.
- **Target** — three artifacts that map onto Suno's three inputs and that the
  Suno parser executes.

Suno is the target machine. Mosaic is the compiler's model of that machine.

## The Technical UST

The Technical UST (Universal Song Template) is the intermediate representation:
a structured, addressable, canonical object from which everything downstream is
derived. It is a **meso-container** — large enough to hold a whole song's
addressable structure, small enough to execute inside a single Suno input
field. The lyrics-prompt field is treated as a programmable runtime with a
discovered grammar, not as a free-text box.

The UST is organized across **eight constrained axes** — theory, voice, style,
timbre, performance, post-production, roadmap, lyrics. The axes are the grammar;
they bound what can be expressed. Every field is addressable
(`axis.key.subkey.variant`) and holds a **value together with a condition** — a
rule, not a bare datum, which is what makes the representation executable.
**Nulls are first-class**: an empty field is either lawfully filled or
explicitly defended with an argument for why it stays empty. Nothing is silently
dropped; nothing is silently invented.

## The three compiler stages

**Front end.** The creative seed is decomposed — expanded, not summarized —
into granular note fields distributed across the eight axes.

**Optimizer.** Simulated specialist workers (personas, organized into councils)
apply structured, adversarial evaluative pressure. They are treated as fallible
by design — the pressure apparatus exists *because* the workers are not assumed
correct. A bounded controller (the orchestrator) checks each field only against
the admissibility system (SEM) and routes work — back to a worker on failure,
forward on success — and never authors creative content. Deliberation
terminates on convergence rather than a fixed turn count, with an explicit
halt mechanism so it cannot loop forever. SEM and the personas modulate the
UST's formation continuously — concurrent admissibility, not post-hoc review.
The representation that survives the pressure is **locked**.

**Back end (FOIL).** The locked UST is factored: recurring terms are hoisted to
the smallest scope that covers their uses — subkey to key, key to axis, and out
to the style or performer surface. The scope of a term's recurrence determines
which output it lands in; the factoring rule is the routing rule. The result is
emitted as three artifacts that map onto Suno's three inputs. Because all three
are factorings of one locked source, each is a **reversible, editable control
surface** — adjusting any one reverse-maps through the UST to the creative
intent and stays consistent with the other two.

## Suno as a DAW

The effect of the above is that Maestro treats Suno the way a digital audio
workstation treats audio: addressable and editable. Atomic control does not
come from Suno — it comes from the UST giving every element an address inside
the field Suno reads. Control knobs are retained at every level (word, lyric
line, instrument, performance) while recurring global characteristics are
hoisted into the style and performer surfaces.

## Status

The compiler-on-a-substrate framing is the architecture. The proven artifact is
the `v1.0`–`v4.5.5` Maestro lineage archived in this repository. `v0` on Mosaic
— the rebirth that makes this architecture explicit and re-founds the
empirically-discovered rules as enforced invariants — is specified and entering
proof-of-concept. It is designed, not yet verified.

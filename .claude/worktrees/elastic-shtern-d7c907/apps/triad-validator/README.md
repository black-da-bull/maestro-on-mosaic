# Maestro Triad Validator

Deterministic hard-control validator for the Maestro Triad — the three Suno-facing prompt surfaces (Show Summary, Creative UST, A/R Profile + Persona Style) emitted by the Maestro compiler.

## Why this exists

Per the architectural law: outputs that look right to a capable LLM are not the same as outputs that are correct. Capable models can pattern-match to plausible Triad shapes while quietly violating structural invariants (character budgets, section ordering, comma policy). The validator is the deterministic gate that fires regardless of which model is the runtime — a hard control where the soft control (model instruction) is insufficient.

This validator runs **before** Triad emission to Suno. If it fails, the Triad does not ship. The audit artifact it produces is the receipt.

## Scope of v0.1 (this slice)

Three checks, all deterministic, all derived from canonical sources:

1. **Length bounds** — character counts per surface against profile-defined budgets.
2. **Section order** — Creative UST section sequence against the Suno Output Law.
3. **Comma policy** — INV-04 (no commas outside the lyrics block).

Profiles supported in v0.1:
- `v4_2_3` (legacy: summary ≤ 1000, macro ≤ 4800)
- `v4_5_2` (kernel: summary ≤ 1000, macro ≤ 4990)
- `v0_spec` (v0 spec: summary 950–1000, macro 4950–4995, persona_profile 1950–1995, persona_style ≤ 150)

Profiles are data; not code. New profiles get added by extending `profiles.py` without touching the check logic.

## What this slice does NOT do (yet)

Excluded for v0.1, scoped for later slices:
- Micro checks (grammar, prosody, clarity, dedupe)
- Tactical checks (phone_scene, exit_stanza, mix_notes, mono_sub_kick, hook_plate_reverb)
- Syllable integrity (INV-05: 6–11 syllables per lyric line)
- Lyrics-lock compliance (INV-07/08)
- G-Card scoring (excellence, not feasibility)
- SEM linting (in-creation pressure, not post-emit gate)

## How it runs

```bash
python -m triad_validator.cli --profile v4_2_3 --triad examples/boy_icarus_triad.json
```

Output is JSON in the E2E_Result shape — directly compatible with the v4.2.3 audit format.

## Status

`[VERIFIED]` — runs against the Boy Icarus historical run and reproduces the v4.2.3 PASS verdict. See `tests/test_validator.py`.
`[PROVISIONAL]` — the v0_spec profile values are taken from `maestro_v0.md §1` and not yet validated against a v0 production run (there isn't one yet — v0 is the rebirth target).

## Architectural placement

- This is **Maestro-application layer**, not Mosaic-substrate. The validator is specific to the Suno render adapter's contract; it does not generalize across mounted applications.
- It implements **N7 Compress & Guard** / **N8 V&V Gates** in code — the "enforcement wall" of the maestro.md kernel chain.
- The Triad surfaces emitted to Suno match the maestro_v0.md §5.2 contract.

## Honest scope (per MAESTRO LOAD/SIDECHAIN/SLIPSTREAM PROTOCOL v3)

This slice is **artifact-boundary validation only**. It does not perform edge-based validation. Per v3 §6, full Maestro validation must reconstruct the causal edge for every node before promoting it; this validator checks final-emit shape and is therefore architecturally narrow.

It is `VALID_AS_ARTIFACT_BOUNDARY_GATE`. It is `NOT_VALID_AS_ARCHITECTURAL_VALIDATOR`.

## Completion footer

```yaml
completion_status:
  label: PROVISIONAL
  scope_satisfied: true   # within stated scope: 3 artifact-boundary checks at the I/O boundary
  missing_edges:
    - edge-based validation (causal-origin reconstruction per turn)
    - sidechain records for SEM pressure
    - sidechain records for persona pressure
    - slipstream records for provisional rule additions
  missing_nodes:
    - tactical checks (phone_scene, exit_stanza, mix_notes, mono_sub_kick, hook_plate_reverb)
    - Evidence Contract validator (one-sentence-per-subkey + binding + downstream prediction + challenge cycle)
    - syllable integrity (INV-05)
    - lyrics-lock compliance (INV-07/INV-08)
    - micro checks (grammar, prosody, clarity, dedupe)
    - G-Card scoring (excellence, not feasibility)
    - SE20 cultural-lineage checks
  unresolved_conflicts:
    - Boy Icarus example is synthesized to validator surface, not historical prompt text
    - Character-budget values differ across maestro.md (1000/4990), master.json (1000/4800), and maestro_v0.md (950-1000/4950-4995); resolved by parameterized profiles, but the canonical profile per Maestro version remains pending operator confirmation
  continuation_required: true
  safe_to_use_downstream: true   # as an artifact-boundary gate; not as an architectural validator
```

# Loss Demonstration — AI "Optimization" vs Operator-Restored Reality v0.1

**Status:** evidence document (proposal-class). Built only from files in hand + the prior SE fold. Append-only.
**Purpose:** make "the loss" concrete with the two comparisons you named. Every figure is verified on disk.

---

## Comparison A — Universal Maestro **v3.0g ("optimized")** vs **v3.1.2 (you rewrote)**

| File (role) | v3.0g "optimized" | v3.1.2 (operator-rewritten) |
|---|---|---|
| GPT instructions | `CustomGPT_Instructions.md` — **67 bytes**, full content: *"# MoMoney Maestro v3.0g Instructions / Full system prompt goes here."* (a placeholder) | `00-System-Prompt.md` — **3,160 bytes**: Modes A/B, Template-Archive binding, Prime-Directive Suno v4.5 immutable order, comma / bars-road-map / `[Exit]` / budget rules, CRISPE orchestrator with CoT·ToT·ReAct·Few-Shot·Self-Consistency·Persona·DARE·QUEST selection logic, 5 Virtual SMEs + debate governance (ejection, consensus 0.85), N0→N9 spine, 5 output artifacts |
| Session starter | `SessionStarter.txt` — **70 bytes**, truncated: *"…Ask for seed…"* | folded into the v3.1.2 system prompt (Mode A/B intake fully specified) |
| Mini-prompts | `MiniPrompts.md` — **64 bytes**, one stub: *"HOOK QUALITY CHECK: Rate hook memorability…"* | integrated into spine / custom-instructions |
| On-chat validators | `OnChatValidators.md` — **100 bytes**, one stub: *"Validate that UST contains sections in exact order…"* | full validator set in-spec + **3 JSON schemas** (`vvlog` 1,345 / `project` 1,017 / `telemetry` 804 bytes) |
| Knowledge spine | *(absent)* | `20-Knowledge-Spine.md` — **2,996 bytes** (preserved v4.1 spine + integrated upgrade) |
| Configuration | *(absent)* | `30-Configuration.md` — **8,487 bytes** (full N2.0–N12 node graph: atoms, KPIs, edges + config knobs) |
| Template notes | *(absent)* | `40-Template-Archive-Notes.md` — **357 bytes** |

**Totals: v3.0g = 301 bytes across 4 placeholder files. v3.1.2 = ~21,500 bytes across 5 files + 3 schemas.**

The "optimization" deleted **~99%** of the operational specification and kept the *shape* — filenames and headers — while replacing the substance with *"Full system prompt goes here."* Every operational rule, the node graph, the framework-selection logic, the debate governance, the validators, and the schemas were gone and had to be re-authored by hand.

**Loss type: structural hollowing.** The surface (names, headers) survives; the content is deleted.

---

## Comparison B — **song.excellence.yaml (v5 "operational")** vs **the detected SEG (genesis)**

`song.excellence.yaml` — `id: SONG.EXCELLENCE.OPERATIONAL.V1`, `source: song.excellence.matrix.iterative.design.session - Copy.txt`, generated 2025-12-24. **2,324 bytes.** Content: a scoring block only — scale 0–5, **`pass_threshold_recommendation: 70`**, and the 12 criteria (weights + min-pass + notes).

The **detected SEG** (folded from `song_excellence_sections.json` → `song_excellence_governance_v0.1.md`) carries the same 12-criterion rubric **plus**:

| Element | In the clean YAML? | In the detected SEG (anchor) |
|---|:--:|---|
| 12-criterion weighted rubric | ✅ | ✅ (S0209) |
| 5-layer SEG stack (rubric / gates / structure / audit-trees / exemplars) | ❌ | ✅ (S0668–S0672) |
| Composite formula `Σ((score/5)×weight)` | ❌ | ✅ (S1397) |
| **Release threshold** | ⚠️ **70** | ✅ **97.5** — operator correction superseding 70 (S1275–S1397) |
| 3-iteration remediation loop + stop condition | ❌ | ✅ (S1373, S1386) |
| Gate decision tree (Metadata→Syllable→Hook→Composite→Production→Final QA) | ❌ | ✅ (S0209) |
| M7 SEG/G-Card evaluator (G-Card = M7 output) | ❌ | ✅ (S1352) |
| 12-agent council + persona councils | ❌ | ✅ (S1154) |
| Run defaults (LUFS −14, equal weighting, syllable 6–10) | ❌ | ✅ (S1362, S1395) |

**Smoking gun:** the YAML's own `source:` field is the iterative design session — the *same material* that contains the 97.5 correction and the entire governance machine. The serializer had all of it and emitted only the rubric table with the **superseded 70** threshold. The file named `OPERATIONAL.V1` is the *least* operational artifact in the set: a scorecard with none of the governance that makes scoring actionable, and a release gate the operator had already overruled.

**Loss type: governance reduction + reversion of an operator decision.**

---

## Synthesis — one mechanism, twice

Both comparisons are the same failure: **AI "optimization" grabs the tidy surface — filenames, a rubric table — and discards the accumulated depth (operational spec, governance superstructure) and the operator's hard-won corrections (the 97.5 floor).** This is the identical move to v5 reducing the accumulated execution chain.

It is not a perception. It is measurable:
- Comparison A: ~99% content deletion; the GPT instructions reduced to a 67-byte placeholder.
- Comparison B: a multi-layer governance machine collapsed to a 12-row table, with an operator decision silently reverted (97.5 → 70).

**Why it keeps happening:** the optimized output *looks* complete — right filenames, right headers, a clean table — so the loss is invisible at a glance and only surfaces on **use**, when the placeholders and missing governance bite and the operator rebuilds by hand (exactly what v3.1.2 was). The clean artifact passes a glance and fails on use.

---

## Implication — the guardrail this justifies

This is the concrete case for **preservation-first**: a clean artifact may exist only as a **derived view** that points back to the accumulated source, and it is forbidden from (a) dropping an element present in the source, or (b) reverting a locked operator value. Either is a regression, not an optimization.

This is mechanically checkable — not a vibe. A derived artifact must not reduce the source's element count or change a locked operator value (e.g., the 97.5 floor) without an explicit, logged supersession. That single check, run as code, would have caught both losses above before they shipped — and it is exactly the kind of portable hard-control the system can actually keep.

**This is NOT:** finalized canon · a rewrite of prior folds (annotation only) · writable to your project (`/mnt/project` is read-only; emitted for you to place and version).

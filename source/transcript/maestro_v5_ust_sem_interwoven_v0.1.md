# Maestro v5 — UST × SEM Interwoven Canon v0.1 (PROPOSAL)

**Status:** PROPOSAL, pending operator acceptance. AI-emitted = proposal-class, not canon (INV-18).
**Folded from:** `maestrov5-dev-ust_and_sem-sessions.txt` (16,829 lines; 2 sessions; 106 human turns / 32 assistant turns).
**Scope of this fold:** the v5 UST-construction half + its interwoven SEM/HPA validation, from this one source. NOT a full multi-source fold.
**Anchoring:** `L####` = line in this file. Embedded `S####` markers (the source cites SE-section IDs internally) are preserved where present.
**Relationship to prior fold:** this is a **different governance generation** than `song_excellence_governance_v0.1.md`. See §9. The two are NOT merged.

---

## 1. What this corpus is

The v5 genesis of: (a) the **Technical UST 8-axis** structure, (b) the **Creative UST** as the Suno prompt surface, (c) the **SEM-interwoven-with-UST / concurrent-quality** architecture, and (d) the **HPA** authenticity phase. Operator-driven (106 human turns), document-first by rule: *"Documents are the primary source of truth; chat text is secondary telemetry"* (L13–L17). The governing design statement: *"In Maestro v5 the focus is on the workflows use of the UST and SEM concurrently at every step — they are interwoven, by design. Each session therefore has natural overlaps but is focused on the evolution of one side of the half."* *(L8203)*

---

## 2. The v5 phase pipeline *(L374–L562, stable across both sessions at L8791–L8979)*

Execution order (phase numbering is non-sequential in the source — recorded as-is, not "corrected"):

- **N7 — Intake & Context Assembly** *(L374)*
- **N8 — SWOT + Problem Framing** *(L405)*
- **N12 — Tree-of-Thought Expansion (ToT-3)** *(L435)*
- **N13 — UST Construction (Canonical)** *(L455)* ← the Technical UST is built here
- **N14 — Validators & SME Round-Robin** *(L476)* ← SEM validation interwoven here
- **N15 — Rights, Remix, and Governance** *(L511)* · Gate **N15.G**: rights cleared before audio generation *(L531–532)*
- **N16 — HPA + A→T→A Loop** *(L534)* · Gate **N16.G**: scores meet targets or loop repeats *(L558–559)*
- **N10 — DSP, Packaging, Versioning** *(L562)*

---

## 3. Technical UST — 8 axes *(L2119 / S0782; L2215 / S0878)*

`THY, VOC, STY, TIM, PERF, POST, MAP, LYR` — authored at phase N13.

> **Naming delta:** this genesis uses **PERF** for the performance axis. Later canon (KERNEL / v5-c) uses **PER**. Recorded; not silently normalized — see §9.

---

## 4. Creative UST *(L2073 / S0736)*

The derived Suno prompt surface: *"Creative UST (≤4999 chars target for Suno prompt surfaces)."* Confirms Creative UST as the meso container targeting Suno's input budget — downstream of the Technical UST, not the truth object.

---

## 5. The interweave principle (the v5 core)

This is the load-bearing v5 design, stated three times:

- *"a document-first workflow reconstruction engine that interweaves UST construction and Quality/SEM validation at every step."* *(L8259)*
- *"UST × Quality interweave: every workflow step must include BOTH"* a construction part and a validation part. *(L8277)*
- UST and SEM are **two halves of one concurrent system**, each genesis session evolving one half. *(L8203)*

**Implication for the canon:** v5 SEM is **not a terminal scorecard**. It runs concurrently with UST construction. This is the evidence that resolves the long-open SEM-as-rubric vs SEM-as-interwoven tension (CFT-005 / prior OQ-SEG-3) toward **both**: SEM is the criteria *and* it executes interwoven during fill.

---

## 6. SEM / SEG in v5 — interwoven validation

- Validation runs at **N14 (Validators & SME Round-Robin)** *(L476)*, concurrent with construction, not after.
- **G-Card scoring: G1–G5; pass threshold G ≥ 7.** *(L1587 / S0250)*
- Iterate until **internal confidence ≥ threshold** OR user interrupt. *(L1096)*
- Output state: *"Ready for G-Card Scoring and SEG Validation."* *(L1566 / S0229)*

> **This is a different instrument** from the SE-genesis SEG (12-criterion weighted composite, 97.5 floor). See §9.

---

## 7. HPA — Phase N16 (Human Perception of Authenticity) *(L534–L559)*

A metric-driven authenticity gate with a model loop:

- **7.1 Metrics:** CLAP, FAD, MFCC, Motif, DFA, MOS. *(L535–546)*
- **7.2 Model Loop:** Analysis → Timbre → Analysis (A→T→A); cross-model benchmarking enforced. *(L548–551)*
- **7.3 Outputs:** `hpa_score.log`, `hpa_feedback.json`. *(L553–556)*
- **7.4 Gate N16.G:** scores meet targets or the loop repeats. *(L558–559)*

HPA is heavily developed in this corpus (≈74 mentions) and is a **first-class governance phase** here — materially larger than its treatment as a single layer in `song_excellence_governance_v0.1.md` §1.

---

## 8. Invariants present in this corpus

- **Lyric lock:** *"[LYRICS BLOCK] (Locked, No Change)."* *(L1544 / S0207)*
- **Null-as-signal native:** the corpus carries a *"null rich skeleton requirement."* *(L143)*
- **Document-first / fail-closed:** do not advance phases without validation; every proposed process must be applied back to prove it recovers missing detail. *(L13–L21)*
- **Rights before audio:** Gate N15.G blocks audio generation until rights cleared. *(L531–532)*

---

## 9. Cross-source deltas & parked conflicts (do NOT silent-merge)

- **CFT-V5-1 (generational, load-bearing).** v5 governs by **G-Card G1–G5 (G≥7), interwoven at every step** (this file). The SE-genesis SEG governs by **12-criterion weighted composite with a 97.5 floor, terminal** (`song_excellence_governance_v0.1.md`). These are **two governance generations** — the v4.5-BASE (post-creation validation) vs v5-DERIVED (quality at creation time) split. **Recommendation: do not reconcile into one. Hold both, with a lineage edge (v5 supersedes the terminal-composite model with an interwoven model). Relabel the prior fold as SEG (v4.5/SE-genesis lineage).**
- **DELTA-V5-2.** No `97.5` anywhere in this corpus; no `70%` pass threshold either (the `70` hits are BPM values). The v5 threshold model is G-Card/confidence, not a single composite floor.
- **DELTA-V5-3 (naming).** PERF (here) vs PER (later canon) for the performance axis.
- **DELTA-V5-4.** Memory Activation axis **absent here too** — strictly a later addition (Boy Icarus build). Confirms OQ-SEG-2: both genesis corpora are pre-Memory-Activation.
- **DELTA-V5-5 (dating).** The full state machine `NULL → PROPOSED → PRESSURED → RESOLVED → LOCKED` and **Address Law are absent** from this genesis (only NULL and LOCKED appear). They are **later v5-c / KERNEL formalizations layered on top of this UST genesis**, and must be dated/attributed as later — not treated as origin.
- **DELTA-V5-6.** SEM-interwoven reading is now evidenced (L8203/L8259) — resolves OQ-SEG-3 toward "both rubric AND concurrent execution."

---

## 10. What this artifact is NOT

- Not finalized canon — AI proposal (INV-18), awaiting your accept/correct.
- Not merged with the SE-genesis SEG — held as a separate generation per §9.
- Not the full canon fold — the v5 UST half from one source; the quality half (v4.5 form) lives in the prior fold; later overlays (KERNEL, 5-state machine, Address Law, 97.5-as-universal, Memory Activation) are not yet folded and must be dated as later.
- Not writable to your project — `/mnt/project` is read-only here; emitted for you to place and version.

**Program note:** this is **file #2** of the canon-regeneration fold. With both genesis halves now folded (UST-construction here; quality/governance in the prior file), the next move is reconciliation, not more raw folding — see the course determination in chat.

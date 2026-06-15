# Song Excellence Governance (SEG) — Canon v0.1 (PROPOSAL)

**Status:** PROPOSAL, pending operator acceptance. AI-emitted artifact = proposal-class, not canon (INV-18).
**Folded from:** `song_excellence_sections.json` (2,131 sections, S0001–S2131) — the Song Excellence / Chaos-Decomposer dev-session corpus.
**Scope of this fold:** the SEG/SEM governance slice from this one source. This is NOT the full multi-pass, multi-source fold of all canon. Other canon files need their own baseline+delta passes (see program note at end).
**Discipline:** every element carries S#### evidence anchors. Within-corpus supersessions are folded forward but the superseded draft is recorded, not erased. Unresolved items are parked in §8, not silently merged.

---

## 1. What SEG is (corrected from prior under-credit)

SEG is a **layered governance system**, not a scorecard. The corpus defines five operative layers (S0668–S0672):

- **L1 — Creative Rubric.** Weighted 0–5 scoring across 12 criteria, with hitmaker-persona overlays for genre-specific red-penning. *(S0668, S0209)*
- **L2 — Governance Gates.** Binary pass/fail checks (metadata, syllables, production, QA) tied to ledger fields. *(S0669)*
- **L3 — Structural Architecture.** Section decomposition (intro / verse / pre-chorus / chorus / bridge / outro) with clarity checks: hook placement, harmonic shifts. *(S0670)*
- **L4 — Heuristic Audit Trees.** Each rubric node broken into task → subtask → audit check → KPI, traceable via atomic instruction trees. *(S0671)*
- **L5 — Application Exemplars.** Real track descriptors (from the Suno tab) used as benchmarks for timbre / style / FX modules. *(S0672)*

**SEM vs SEG (evidence-supported reading):** SEM = the Creative Rubric (L1). SEG = the full L1–L5 stack plus the gate logic and the M7 evaluator. The corpus calls the matrix "a rubric **plus** gating system" (S2028, S0352) and frames the rubric as **Layer 1 of a five-layer framework** (S0668). This supports SEM ⊂ SEG. The precise boundary is parked in §8 for ratification.

---

## 2. SEM — the 12-criterion weighted rubric *(S0209)*

Scale 0–5 (0 missing · 1 very weak · 2 weak · 3 competent · 4 strong · 5 outstanding). Weights sum to 100.

| # | Criterion | Weight % | Min pass | Measurement |
|---|-----------|---------:|:--------:|-------------|
| 1 | Hook Strength (melodic + lyrical memorability) | 18 | 4 | Hook = chorus/lead motif; earworm test (hum after 30s) |
| 2 | Lyric Integrity & Emotional Clarity | 12 | 3 | Narrative coherence; truthfulness; no lyric edits outside [Lyric Block] |
| 3 | Vocal Delivery & Character | 10 | 3 | Tone, timing, persona fit, intelligibility |
| 4 | Melody & Topline Craft | 10 | 3 | Contour, singability, interval choices |
| 5 | Structure & Pacing (arrangement) | 8 | 3 | Section balance; hook placement; dynamics arc |
| 6 | Production Quality (mix basics) | 12 | 3 | Balance, low-end clarity, vocal sit, no clipping |
| 7 | Arrangement Interest & Contrast | 6 | 2 | Transitions, automation, instrumentation choices |
| 8 | Commercial Viability & Market Fit | 8 | 3 | Tempo/genre fit, DSP playlist targets, length |
| 9 | Originality / Distinctive Element | 6 | 2 | Unique twist, persona, sample, or production idea |
| 10 | Metadata & Governance (tags, credits, UST fields) | 4 | 3 | Semicolons, persona_map, CREW_TAGS, release metadata completeness |
| 11 | Lyric Syllable Integrity (Suno rule 6–10) | 4 | 4 | All lines in [Lyric Block] between 6–10 syllables |
| 12 | Pre-release QA Checks (deliverables) | 2 | 2 | WAV/LUFS/ISRC, stems, stems naming, integration ledger entry |

**Binary criteria** (e.g., metadata present) are scored 0 or 5 only, then converted to scale *(S0209)*.

---

## 3. Composite scoring + release threshold

- **Composite formula:** `composite = Σ( (score_i / 5) × weight_i )`, max 100. *(S1397; S0209 states the looser "score × weight, max 100" — S1397 is the precise normalized form and governs.)*
- **Release threshold: composite ≥ 97.5.** Operator-canonical. *(S1275–S1277, S1372, S1386, S1397)*

> **FOLDED SUPERSESSION (within this corpus).** The initial rubric draft set pass = 70/100 with bands (60–69 → targeted revision, <60 → major rework) *(S0209)*. The operator then corrected this: *"who said 70% pass? we are 97.5% pass"* *(S1275)*, and the assistant acknowledged 70 as its own error *(S1276)*. **Fold result: 97.5 is canonical; 70 and its bands are superseded draft, recorded here as lineage, not erased.** This is the CR-009 catch in its source form.

- **Remediation loop:** attempt up to **3** remediation iterations to reach ≥97.5; if not reached, stop and output current best + a single prioritized top-remediation note. *(S1373, S1386)*
- **Worked instance (genesis run):** `song_test_2025-12-07_001` scored composite **76.8/100** (deficit 20.7), remediated to **≈97.6**. *(S1278, S1292, S1362)*

---

## 4. Gate decision tree (Go / No-Go / Iterate) *(S0209)*

- **Metadata Gate** — required metadata fields present and valid? (N → HOLD: fix metadata)
- **Lyric Syllable Gate** — all [Lyric Block] lines 6–10 syllables? (N → ITERATE: edit phrasing / overlay fills; not a lyric rewrite if integrity lock applies)
- **Hook Gate** — Hook Strength ≥ 4? (N → ITERATE: rewrite topline/hook)
- **Composite Gate** — composite ≥ **97.5**? (Y → RELEASE candidate) *(threshold folded per §3; draft tree said ≥70)*
- **Production Gate** — mix check pass (LUFS, no clipping, low-end clarity)? (N → mix pass & re-evaluate)
- **Final QA** — stems exported; integration ledger updated; release pack ready? (Y → PUSH TO DISTRIBUTION)

---

## 5. M7 — SEG / G-Card evaluator (runtime placement) *(S1352)*

- **Purpose:** apply gating (SEG/G-Card thresholds + composite scoring).
- **Inputs:** `A_chain_report`, normalized rubric weights.
- **Outputs:** `A_validation_report` (composite score + gate statuses). The **G-Card is the M7 output artifact**.
- **Steps:** M7.1 per-criterion scores (atomic per criterion) → M7.2 composite (atomic) → M7.3 evaluate gate rules: metadata, syllable, roadmap (atomic per gate) → M7.4 mark `ready_for_serialize` or `revision_needed`.
- **Role in pipeline:** excellence / gating layer **before serialization**; also evaluates EmotionalFidelity, GenreAuthenticity, Maestro-Loop buy-in. *(S1102)*

---

## 6. Scoring council *(S1154)*

- **Agent_Council (12):** PromptAgent, MemoryAgent, CriticAgent, VoiceAgent, BridgeAgent, DynamicsAgent, LyricAgent, StructureAgent, MelodyAgent, HarmonyAgent, RhythmAgent, ChaosAgent.
- **Persona_Councils:** RapCouncil, SongCouncil (genre-specific red-pen overlays; the "5 positive / 5 negative hitmaker traits" stress-test method, S0209).
- Each criterion is scored by simulated SME agents; **equal agent weighting** by default. *(S1397)*

---

## 7. Run defaults (ASSUMED_DEFAULT unless operator overrides)

- Mastering loudness: **LUFS −14** integrated. *(S1362, S1395)*
- Agent weighting: **equal**. *(S1362, S1364, S1397)*
- Syllable guideline: **6–10** enforced on [Lyric Block]. *(S0209, S1395)*
- Commas: **none outside lyrics**. *(S1395)*
- Test-mode override: lyric_lock may be ignored only under explicit TEST_OVERRIDE_EDIT, which must create a ledger LCR object. *(S1360, S1375)*

---

## 8. Parked — open questions & conflicts (do NOT silent-merge)

- **OQ-SEG-1 — sub-gate thresholds still null.** The source itself flags: *"Exact numeric thresholds for Maestro_Loop_buyin_score and SEG/G-card pass thresholds (human to specify: e.g., 70 vs 75)."* *(S1196)*. This is distinct from the 97.5 **composite** floor (which is resolved, §3); it concerns buy-in / sub-gate cutoffs. Human to specify.
- **OQ-SEG-2 — SEM criterion count: 12 vs 13.** This corpus defines **12** criteria (S0209) with **no Memory Activation axis**. A later session flagged "Memory Activation Likelihood" as a validated SEM addition (Boy Icarus build). Reconcile: is current SEM 12, or 13 with Memory Activation? Surfaced, not merged.
- **OQ-SEG-3 — SEM/SEG boundary.** Evidence supports SEM = L1 rubric, SEG = full L1–L5 + gates + M7 (§1). Confirm or correct as canon. (Prior tension logged as CFT-005: SEM-as-rubric vs SEM-as-interwoven-substrate.)
- **DEDUP — S1873 ≡ S1878** are byte-identical (the same `run_20251207_001` session_export). Collapse to one on the master fold.

---

## 9. What this artifact is NOT

- Not finalized canon — it is an AI proposal (INV-18) awaiting your accept/correct.
- Not the full canon regeneration — it is the SEG slice from one corpus. The rest needs baseline+delta passes (program note below).
- Not writable back to your project automatically — `/mnt/project` is read-only here; this is emitted for you to place and version.

**Program note:** treat this as file #1 of the canon-regeneration fold. Remaining canon (version changelog, consolidation snapshot, workspace specs, KERNEL) each need their own baseline read → session-delta replay → emit. KERNEL is flagged separately: you disavowed it as prior-AI-authored, so it is reference, not authority, until you say otherwise.

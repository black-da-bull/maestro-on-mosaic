# Maestro Canon — Dev-Log Audit Addendum (delta to v1)

**What this is.** A delta to `maestro_grounded_canon_and_reflection_v1.md`. It records a **targeted audit** (not a full read) of the four large dev logs against the open NULLs from §7 of v1. Method: UTF-8-safe regex probes with line-anchored matches. Provenance is `file:line`. **Honesty flag:** this is a probe pass, not an exhaustive read; greps can miss. Statuses below are upgrades/downgrades *relative to v1*, not final.

Logs audited: `longDevWorkLog.txt`, `longDevWorkLog2.txt`, `maestro_devsession_iterative_1.txt`, `maestrov5-dev-ust_and_sem-sessions.txt`. v5 marker density places them on the timeline: `longDevWorkLog` (v5 ×0 → v4-era), `longDevWorkLog2` (×5), `maestro_devsession_iterative_1` (×8), `maestrov5-dev-ust_and_sem` (×40 → the v5 build session).

---

## NULL #3 — PER vs PERF → **RESOLVED**

The development sessions author the performance axis as **`PERF`**, with full human-readable key/subkey names:

- `maestro_devsession_iterative_1.txt:1174` — "instantiate the 8 axes (THY/VOC/STY/TIM/**PERF**/POST/MAP/LYR) in canonical order."
- `maestro_devsession_iterative_1.txt:1242` — "theory_axis, vocals_axis, style_axis, timbre_axis, **performance_axis**, post_production_axis, road_map_axis, lyrics_block_axis."
- `maestro_devsession_iterative_1.txt:1763` and `maestrov5-dev-ust_and_sem-sessions.txt:1644` — "## 5. **PERFORMANCE_AXIS (PERF)**."
- `maestrov5-dev-ust_and_sem-sessions.txt:1646` — "### **PERF.K1 Groove** — PERF.K1.S1 **pocket_definition** — PERF.K1.S2 **push_pull_rules** …"

`PERF` occurs 76–166× per log. **The authored canonical label is `PERF`.** The `PER` in `template.technical.ust.yaml` is the **reduced serialization id** — the v5 serializer shortened `PERF` → `PER` and emptied the name slot.

---

## NULL #2 — `axis_name` / `key_name` null → **REFRAMED: names existed, lost in serialization (recoverable)**

`axis_name:` as a populated YAML field returns **0 matches across all four logs** — but that is because, in the dev sessions, the names live as **markdown headers and labels**, not YAML fields:

- Axes are named in prose: `performance_axis`, `theory_axis`, … (`maestro_devsession_iterative_1.txt:1242`).
- Keys/subkeys are named: `PERF.K1 Groove`, `PERF.K1.S1 pocket_definition`, `PERF.K1.S2 push_pull_rules` (`…:1646`).

So the YAML's `axis_name: null` / `key_name: null` do **not** mean the names were never defined. They mean the v5 serialization captured **ids + types** and **dropped the names**, which still sit in the markdown source. **The names are recoverable** by mapping the dev-session headers back onto the YAML ids.

> **Thesis impact.** This is the reduction-destroys-value finding *at the field level, inside the canonical artifact*: named, semantically rich axes (`PERF.K1 = Groove`, subkeys `pocket_definition` / `push_pull_rules`) were serialized down to anonymous typed slots. The v5 build kept the skeleton's *shape* and dropped its *labels* — the same move the unified-hierarchy Executive Note describes at the document level ("partially collapsed in prior iterations").

---

## NULL #5 — G-Card threshold (97.5 vs 70 vs a "75" sub-gate) → **NARROWED**

- **Corroborated by a second independent source:** `maestro_devsession_iterative_1.txt:580` — "Lock your true pass threshold canon (note: one canon states ~97.5% pass target superseding earlier 70%)." This matches the SEM session's S1275 ("we are 97.5% pass") from a *different* file, so 97.5-supersedes-70 is now confirmed across two sources.
- **No separate "75" sub-gate found.** The probe for a `75 … pass` threshold returned nothing in any log. The only thresholds in evidence are the **composite 97.5** plus the **per-criterion minimums** in the rubric (Hook ≥4; others ≥2/3/4). Absent new evidence, there is no distinct "75" gate.
- **Still open:** the dev note phrases it as "Lock your true pass threshold canon" — i.e., it was flagged as needing a final lock. Treat 97.5 as the superseding composite target; per-criterion minimums as the sub-gates.

---

## NULL #6 — v5-b "failed six-file patch" → **DOWNGRADED (unsupported by these logs)**

The "six-file" framing came from earlier conversation. The probe's "6 file" / "16 file" / "26 file" hits in `longDevWorkLog.txt` (e.g., `:438` "unnamed:_0: 16 file: suno-wip.md topic: lyrics excerpt: …") are a **citation/line-index format**, not a six-file patch. No "failed patch" or "six-file" event surfaced. **These logs neither confirm nor describe a failed six-file patch.** The claim remains unverified, and the earlier phrasing may have been imprecise. Do not treat it as established.

---

## NULL #4 — SEM 12 vs 13 criteria → **STILL OPEN (evidence isolated to the SEM session)**

"Lyric Change Compliance," "13 criteria," "thirteenth," and "criterion 13" return **0 matches across all four dev logs.** The only place the 13th-criterion idea appears is the SEM session itself (`song_excellence.yaml`, S0134 / S0137 / S0357), where it is framed as an *addition under Pre-release QA & Lyric Compliance*, not a confirmed standalone 13th line. **Unresolved**; the rubric of record is 12.

---

## NULL #1 — which container order is operative → **STILL OPEN, but elevated to "syntax"**

- `maestrov5-dev-ust_and_sem-sessions.txt:2517` (and dup `:10934`) — "S1180: Highlighter: **container order becomes 'syntax'**." The v5 session explicitly promotes container order to grammar-level enforcement — corroborating the boundary claim that container order is a **hard, formalizable rule (→ code)**.
- **Likely lineage delta:** `[Structure]` and `[FX]` appear in `maestro.yaml`'s 10-container order but in neither the v2.5 Prime-Directive order nor the Technical-UST axes; the v5 session carries heavy `Structure` density (×226). This suggests **`[Structure]` and `[FX]` are v5.0.2 additions** to the top-level container set.
- **Still unresolved:** which exact ordering is the *current operative* one — the typed 8-axis Technical-UST and the 10-container `maestro.yaml` both ship in the same dedup bundle and disagree. Resolve only by replaying the live chain.

---

## CANON sharpened — Mosaic is a later name → **CONFIRMED**

`Mosaic` returns **0 matches across all four dev logs**, consistent with the earlier evolution-evidence file (mosaic ×0) and the FOIL session. **The dev work is "Maestro"; "Mosaic" is the retrospective name for the substrate/realm, applied after these sessions.** This tightens v1 §5: Mosaic post-dates the captured dev work.

---

## Net effect on v1's NULL list

| NULL | v1 status | after audit |
|------|-----------|-------------|
| #1 container order operative | open | **open** (but order = "syntax"; Structure/FX = v5 additions) |
| #2 axis_name/key_name null | open gap | **reframed** — names existed in dev logs, lost in serialization, recoverable |
| #3 PER vs PERF | lean PER | **resolved** — authored = `PERF`; `PER` = reduced id |
| #4 SEM 12 vs 13 | open | **open** (evidence isolated to SEM session) |
| #5 G-Card threshold | open | **narrowed** — 97.5>70 corroborated 2×; no "75" gate |
| #6 v5-b six-file patch | open | **downgraded** — unsupported by these logs |
| #8 dev logs unread | unread | **audited by probe** (still not exhaustively read) |

**Remaining true gap:** these four logs were *probed*, not fully read. A complete `(end state) − (root input) = work` reconstruction of each — especially `maestrov5-dev-ust_and_sem-sessions.txt` as the v5 build trace — is the next real increment if you want the v5 reduction itself reconstructed move-by-move. The probe already shows what it would find: named axes collapsing into anonymous typed slots, container order hardening into syntax, and 97.5 superseding 70 — the chain compressing as it serialized.

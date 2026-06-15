#!/usr/bin/env python3
"""
Pass 5 — Process Tree Emission.

(1) Mine control-flow PRIMITIVES from the chronology to ground the tree in data:
    gate / branch / stop-condition / convergence / phase-order.
(2) Emit the ordered execution PROCESS TREE reconstructed from the runtime
    sessions (who_dat boot+run, v5-b mount, preview_window) and the phase
    contracts, with each control point annotated by where the data supports it.
Deterministic mining + reconstructed ordering. Pass 6 (PPP) reads this.
"""
import re, os, json
PRIM = {
 "gate":        r'(?i)\b(gate\b|SEM gate|G-?Card|validation|admissib|promote\b|freeze|checkpoint|entry (rule|condition)|exit (rule|condition))',
 "branch":      r'(?i)\b(rap ?mode|song ?mode|\bif \b|\belse\b|branch|pass/iterate/hold|mode (determination|is|=)|route\b|either\b)',
 "stop":        r'(?i)\b(lyric.?lock|never (mutate|trim|rewrite)|\bhalt\b|block(ed|s)?\b|stop[- ]?(line|condition)|do not (emit|proceed)|fail[- ]?closed)',
 "convergence": r'(?i)\b(97\.?5|composite|threshold|consensus|converge|baseline lock|lock(ed)?\b|release gate)',
 "phase_order": r'(?i)\b(phase \d|step \d|pass \d|stage \d|load order|run order|boot sequence|pipeline|sequence|order of)',
}
def run():
    src="/mnt/user-data/outputs/pass1_reassessed"; cnt={k:0 for k in PRIM}
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        for e in json.load(open(os.path.join(src,fn)))["events"]:
            for k,p in PRIM.items():
                if re.search(p,e["text"]): cnt[k]+=1
    # Reconstructed ordered process tree (from runtime sessions + phase contracts)
    tree=[
     {"stage":"0 BOOT","type":"sequential","steps":[
        "0.1 Load Mosaic substrate → validate invariants",
        "0.2 Init CINR (restore from ATP if provided, else fresh/empty)",
        "0.3 Mount Maestro → validate manifest",
        "0.4 Open conversation layer; load knowledge K1–K10 on-demand"],
      "control":[("GATE","Load Completion Protocol (LCP): all packets valid, version-matched, blocker-free → PASS before any execution")]},
     {"stage":"1 INTAKE","type":"sequential","steps":[
        "1.1 Operator provides creative seed / lyrics",
        "1.2 Mode determination",
        "1.3 Lyric intake (LEVEL_0)"],
      "control":[("BRANCH","mode → RapMode | SongMode"),
                 ("STOP","lyric-lock: words LOCKED — never mutate/trim/rewrite supplied lyrics")]},
     {"stage":"2 UST CONSTRUCTION","type":"sequential + interwoven","steps":[
        "2.1 Creative UST (meso surface, ≤4999 chars, Suno-facing)",
        "2.2 → formalized into Technical UST (8 axes THY/VOC/STY/TIM/PER/POST/MAP/LYR)"],
      "control":[("SIDECHAIN","SEM/SEG pressures quality DURING construction — interwoven, upstream of output, not terminal")]},
     {"stage":"3 GOVERNANCE / PRESSURE","type":"loop","steps":[
        "3.1 Council/SME pressure (bounded SMEs, null-by-null, downstream-aware)",
        "3.2 HPA validation (perceptual authenticity)",
        "3.3 SEG governance (ratchet / preload substrate)"],
      "control":[("BRANCH/LOOP","revision loop → pass | iterate | hold"),
                 ("CONVERGENCE","SEM composite → 97.5 release floor (operator-grounded)"),
                 ("GATE","G-Card decision → pass / promote")]},
     {"stage":"4 TRIAD OUTPUT","type":"concurrent emission","steps":[
        "4.1 A/R Persona Surface + Show Summary + Creative UST — emitted concurrently, intertwined, lyric-locked",
        "4.2 FOIL: duplicated/recurrent terms upshift one scope level; unique local detail stays granular"],
      "control":[("GATE","container validation: CAPs, no-comma-outside-lyrics, lyric word preservation, syllable bands"),
                 ("STOP","container fail → do not emit")]},
     {"stage":"5 RENDER","type":"sequential","steps":[
        "5.1 Suno-facing surfaces derived from LOCKED Technical UST"],
      "control":[("STOP","external audio generation NOT executed in chat")]},
    ]
    json.dump({"primitives":cnt,"process_tree":tree},
              open("/mnt/user-data/outputs/process_tree_v0.1.json","w"),ensure_ascii=False,indent=1)
    print("control-flow primitives mined from chronology (grounding):")
    for k,v in sorted(cnt.items(),key=lambda x:-x[1]): print(f"  {k:<14}{v:>6}")
    print("\n"+"="*78+"\nMAESTRO PROCESS TREE (reconstructed execution logic)\n"+"="*78)
    for n in tree:
        print(f"\n[{n['stage']}]  ({n['type']})")
        for s in n["steps"]: print(f"    {s}")
        for typ,desc in n["control"]: print(f"    ⟐ {typ}: {desc}")
    print(f"\n-> process_tree_v0.1.json written")
if __name__=="__main__": run()

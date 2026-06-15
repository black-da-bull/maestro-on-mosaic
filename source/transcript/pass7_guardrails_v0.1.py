#!/usr/bin/env python3
"""
Pass 7 — Guardrails & Guidelines. Extracts failure-prevention rules, allowed
creativity, forbidden collapse patterns, and escalation triggers. Grounded by
mining failure/forbidden lines; canonical set curated from documented failures
(reductions, skeletons, flow-loss, phantom commitment) + skill failure modes.
"""
import re, os, json
GUARD_LINE=re.compile(r'(?im)^.{15,170}?\b(never|forbidden|must not|do not|avoid|prevent|collapse|drift|phantom|skeleton|premature|degrade)\b.{0,150}$')
def mine():
    src="/mnt/user-data/outputs/pass1_reassessed"; lines=[]; n=0
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        for e in json.load(open(os.path.join(src,fn)))["events"]:
            for m in GUARD_LINE.finditer(e["text"]):
                n+=1; ln=re.sub(r'\s+',' ',m.group(0)).strip()
                if 25<len(ln)<150: lines.append(ln)
    seen=set(); uq=[]
    for l in lines:
        k=l.lower()[:55]
        if k not in seen: seen.add(k); uq.append(l)
    return n, uq

FAILURE_PREVENTION=[
 "FP1 Runtime stays primary — emit derived views only; never summarize the accumulated chain into clean specs (prevents the reduction loss).",
 "FP2 Container-PASS ≠ quality — never green-light on container validation alone; HPA / 97.5 / somatic gates must also clear (prevents validated-but-flow-broken output).",
 "FP3 No skeleton files — every classification carries its instance + evidence (prevents placeholder collapse).",
 "FP4 Lyric-lock at intake, before any generation (prevents lyric mutation downstream).",
 "FP5 Process Technical UST as a loop, not a turn-based shortcut (prevents shallow/premature resolution).",
 "FP6 Preserve the ugly parts — corrections, frustration, wrong branches are causal evidence (prevents loss of the 'why').",
 "FP7 No-drop / no-revert — a derived artifact may not drop a source element or revert a locked value without logged supersession (prevents the 97.5→70 loss).",
]
ALLOWED_CREATIVITY=[
 "AC1 Inside the LOCKED Technical UST the render is free — 'enough structure to create freely without becoming generic.'",
 "AC2 Show Summary & A/R Persona carry the global explanatory/style burden, freeing Creative UST to be a producer's session sheet.",
 "AC3 Sacred Imperfection — governed, meaningful imperfection is allowed and wanted, not sterile perfection.",
 "AC4 Voice, persona, and stylistic variation within the 8 axes are open creative space.",
]
FORBIDDEN_COLLAPSE=[
 "FC1 Reduction — flattening the chain into tidy specs that drop depth + operator corrections.",
 "FC2 Skeletonization — classification with no instance; placeholders ('Full system prompt goes here').",
 "FC3 Flow-loss — mechanical stamping (e.g. (mm)+sfx every line) that violates the song's own restraint.",
 "FC4 Phantom commitment — elevating AI's prior text to canon; treating mid-stream as final.",
 "FC5 Mythologizing — treating documents as an executing runtime substrate (over-claiming).",
 "FC6 Premature finalization — locking before the middle (the work) is done.",
 "FC7 Lyric mutation — trimming/rewriting supplied lyrics for character economy.",
 "FC8 Collapsing distinctions — Maestro→Mosaic, SEM→SEG, Creative UST→Technical UST, Technical UST as output.",
]
ESCALATION=[
 "ET1 Container validation FAIL → do not emit; return to revision.",
 "ET2 Composite below 97.5 → iterate; do not release.",
 "ET3 Contradiction surfaced → park to register; never silent-merge.",
 "ET4 Blocked doc / missing evidence → halt; request from operator; do not fabricate.",
 "ET5 Drift detected (mode / canon / lyric) → revert to canon.",
 "ET6 Operator correction → apply retroactively with provenance; supersede AI paraphrase.",
]
def run():
    n, mined = mine()
    json.dump({"failure_prevention":FAILURE_PREVENTION,"allowed_creativity":ALLOWED_CREATIVITY,
               "forbidden_collapse":FORBIDDEN_COLLAPSE,"escalation_triggers":ESCALATION,
               "grounding_count":n,"mined_samples":mined[:40]},
              open("/mnt/user-data/outputs/guardrails_v0.1.json","w"),ensure_ascii=False,indent=1)
    print(f"GUARDRAILS & GUIDELINES   [grounding: {n} failure/forbidden lines mined; {len(mined)} distinct]\n")
    print("FAILURE-PREVENTION RULES");  [print("  "+x) for x in FAILURE_PREVENTION]
    print("\nALLOWED CREATIVITY (bounded freedom)"); [print("  "+x) for x in ALLOWED_CREATIVITY]
    print("\nFORBIDDEN COLLAPSE PATTERNS"); [print("  "+x) for x in FORBIDDEN_COLLAPSE]
    print("\nESCALATION TRIGGERS"); [print("  "+x) for x in ESCALATION]
    print("\n  mined examples (verbatim):")
    for l in mined[:4]: print(f"    · {l[:120]}")
    print(f"\n-> guardrails_v0.1.json written")
if __name__=="__main__": run()

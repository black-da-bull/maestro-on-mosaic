#!/usr/bin/env python3
"""
Pass 6 — PPP Emission. Separates POLICY (what must be true) / PROCESS (how it
flows) / PROCEDURE (step-by-step). Policy is grounded by mining imperative/
invariant lines from the chronology; the canonical policy set is curated from
the full reconstruction. Process = Pass-5 spine. Procedure = ordered steps.
"""
import re, os, json
POLICY_LINE = re.compile(r'(?im)^.{15,180}?\b(must|never|always|shall|required|invariant|forbidden|non-negotiable|may not|do not)\b.{0,160}$')

def mine_policy():
    src="/mnt/user-data/outputs/pass1_reassessed"; lines=[]; n=0
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        for e in json.load(open(os.path.join(src,fn)))["events"]:
            for m in POLICY_LINE.finditer(e["text"]):
                n+=1; ln=re.sub(r'\s+',' ',m.group(0)).strip()
                if 25<len(ln)<160: lines.append(ln)
    seen=set(); uniq=[]
    for l in lines:
        k=l.lower()[:60]
        if k not in seen: seen.add(k); uniq.append(l)
    return n, uniq

POLICY = [
 "P1  Lyric-lock — never mutate/trim/rewrite supplied lyrics; words LOCKED, lineation normalize-only.",
 "P2  97.5 release floor — output must meet it; refusal to let AI-average pass as emotionally complete.",
 "P3  Container validation must PASS before emit — CAPs, no-comma-outside-lyrics, syllable bands.",
 "P4  Technical UST is the upstream truth object — all output derives from the LOCKED UST.",
 "P5  Quality is interwoven — SEM/SEG sidechain upstream of output, never terminal.",
 "P6  Operator = ROOT authority; AI = proposal-class — re-reads never elevate AI text to canon.",
 "P7  Excellence ratchet — proven excellence becomes the new baseline; no regression to average.",
 "P8  No step-loss — the process must preserve what it learns (the accumulated chain).",
 "P9  Sacred Imperfection — governed meaningful failure, not generic flaw-seeking.",
 "P10 Fail-closed boot — LCP must PASS before any execution begins.",
 "P11 No external audio generation in chat — render is handed to the operator.",
 "P12 Mosaic ≠ Maestro — substrate and application are distinct; preserve the separation.",
]
PROCESS = [
 "BOOT → INTAKE → UST CONSTRUCTION → GOVERNANCE/PRESSURE(loop) → TRIAD OUTPUT(concurrent) → RENDER",
 "quality pressure is a SIDECHAIN at UST construction (interwoven), not a terminal gate",
 "fail-closed at both ends: LCP boot gate + container-validation output gate; 3 hard stops",
]
PROCEDURE = {
 "BOOT":["load Mosaic; assert invariants","init CINR (restore ATP | fresh)","mount Maestro; validate manifest",
         "load K1–K10 on-demand","run LCP → PASS or HALT"],
 "INTAKE":["receive seed/lyrics","classify mode (Rap|Song)","ingest lyrics LEVEL_0; set lyric-lock","surface risks (title/metadata)"],
 "UST CONSTRUCTION":["build Creative UST (≤4999, Suno-facing)","map to Technical UST 8 axes",
         "apply SEM/SEG pressure per axis (upstream)","process Technical UST sequentially as a loop","lock Technical UST"],
 "GOVERNANCE/PRESSURE":["Council/SME pressure null-by-null","HPA perceptual validation","SEG ratchet carry-forward",
         "revision loop → pass|iterate|hold","SEM composite → check 97.5","G-Card decision → promote | return"],
 "TRIAD OUTPUT":["derive A/R + Show Summary + Creative UST concurrently from locked UST","preserve lyrics verbatim",
         "FOIL: upshift recurrence, keep local detail","run container validators","emit telemetry; any FAIL → do not emit"],
 "RENDER":["derive Suno surfaces from locked UST","hand to operator (no audio in chat)"],
}
def run():
    n, mined = mine_policy()
    json.dump({"policy":POLICY,"policy_evidence_count":n,"process":PROCESS,"procedure":PROCEDURE,
               "mined_policy_samples":mined[:40]},
              open("/mnt/user-data/outputs/ppp_v0.1.json","w"),ensure_ascii=False,indent=1)
    print(f"POLICY  (what must be true)   [grounding: {n} imperative/invariant lines mined; {len(mined)} distinct]\n")
    for p in POLICY: print("  "+p)
    print("\n  mined examples (operator/system, verbatim):")
    for l in mined[:4]: print(f"    · {l[:120]}")
    print("\nPROCESS  (how it flows)\n")
    for p in PROCESS: print("  • "+p)
    print("\nPROCEDURE  (step-by-step)\n")
    for stage,steps in PROCEDURE.items():
        print(f"  {stage}: "+" → ".join(steps))
    print(f"\n-> ppp_v0.1.json written")
if __name__=="__main__": run()

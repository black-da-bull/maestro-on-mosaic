#!/usr/bin/env python3
"""
Pass 4 — Architecture Extraction, validated against the v5-c canonical target.

Instead of extracting a graph blind, we score the corpus against the canonical
4-plane architecture (the uploaded v5-c spec): for each named architectural
element, how strongly is it evidenced in the folded substrate? This confirms
the compiler's substrate actually contains the target architecture -- the
precondition for standing it up as a runtime. Sparse elements are flagged.
"""
import re, os, json
from collections import Counter

ELEMENTS = {
 "P1 staffed runtime": {
   "worker_roster": r'(?i)\b(Canon Orchestrator|Megazord|Sibling Architect|Melody Scout|Analog Confessor|\bSage\b|\bVanessa\b|\bAlan\b|\bDave\b|\bEldrik\b|\bAnva\b|\bHuan\b|\bIsla\b)',
   "SME / workforce": r'(?i)\b(SME(s)?|workforce|virtual label|council|persona(s)?|subagent)',
   "bounded controller": r'(?i)\b(controller|orchestrat(or|ion)|procedural only|non-?creative)',
   "deliberation/pressure": r'(?i)(round.?robin|deliberat|\bpressure\b|contradiction|null.?hunt|challenge cycle)',
 },
 "P2 canonical substrate": {
   "Technical UST": r'(?i)(technical[ ._]ust|\bUST\b)',
   "8 axes / addressing": r'(?i)(8 ax|AXIS\.KEY|\bTHY\b|\bVOC\b|\bSTY\b|\bTIM\b|\bPOST\b|\bMAP\b|\bLYR\b)',
   "null discipline": r'(?i)(nullable|null-?preserv|nulls? are signal|zero-?skip|deliberate null)',
   "definitive lock / SoT": r'(?i)(definitive lock|technical\.ust lock|source of truth|sole source)',
 },
 "P3 reverse compilation": {
   "FOIL": r'(?i)\bFOIL\b',
   "reverse comp / dedup": r'(?i)(reverse compil|promotion|dedup|compression discipline|repeated section)',
   "gates (SEG/G-Card/SE20/CAP)": r'(?i)(\bSEG\b|G-?Card|\bSE20\b|\bSEM\b|\bCAP\b|feasibility gate|character budget)',
   "preserve-not-genericize": r'(?i)(fuel for nuance|no genericiz|preserve meaning|reinvest)',
 },
 "P4 external API (triad)": {
   "triad": r'(?i)\btriad\b',
   "Show Summary": r'(?i)show summary',
   "Creative UST": r'(?i)creative[ ._]ust',
   "Persona / A&R": r'(?i)(persona[ ._/]?(surface|profile)|A&R|A/?R surface)',
 },
}

def run():
    src="/mnt/user-data/outputs/pass1_reassessed"
    texts={}
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        d=json.load(open(os.path.join(src,fn)))
        texts[d["source"]]=" ".join(e["text"] for e in d["events"])
    blob_all="\n".join(texts.values())
    report={}
    print(f"{'plane / element':<34}{'hits':>6}{'files':>6}  top source")
    print("-"*78)
    for plane, elems in ELEMENTS.items():
        print(f"\n[{plane}]")
        pl_total=0
        for name,pat in elems.items():
            hits=len(re.findall(pat, blob_all))
            byf=Counter()
            for f,t in texts.items():
                c=len(re.findall(pat,t))
                if c: byf[f]=c
            top=byf.most_common(1)[0][0][:30] if byf else "-"
            flag="  <-- SPARSE" if hits<5 else ""
            print(f"  {name:<32}{hits:>6}{len(byf):>6}  {top}{flag}")
            report.setdefault(plane,{})[name]={"hits":hits,"files":len(byf),"top":byf.most_common(3)}
            pl_total+=hits
        print(f"  {'= plane evidence total':<32}{pl_total:>6}")
    json.dump(report, open("/mnt/user-data/outputs/pass4_architecture_validation.json","w"), ensure_ascii=False)
    print("\n-> pass4_architecture_validation.json written")
if __name__=="__main__": run()

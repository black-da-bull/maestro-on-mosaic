#!/usr/bin/env python3
"""
Pass 4 — Architecture Extraction.

From the chronology, mine named COMPONENTS (recurring system entities) by
frequency, their INTERCONNECTS (co-occurrence weight across events), and assign
each to a PLANE/runtime layer. node/edge/authority/boundary mutations from Pass
2 are what these correspond to: components=nodes, interconnects=edges, planes=
runtime layers, authority/boundary=control surfaces. Deterministic; the seed
vocabulary + plane map encode the architectural judgment. Pass 5 reads this.
"""
import re, os, json
from itertools import combinations

COMP = {
 "Maestro": r'\bMaestro\b', "Mosaic": r'\bMosaic\b',
 "Technical UST": r'technical[ _.]?ust', "Creative UST": r'creative[ _.]?ust', "UST(umbrella)": r'\bUST\b',
 "SEM": r'\bSEM\b', "SEG": r'\bSEG\b', "Song Excellence": r'song excellence',
 "FOIL": r'\bFOIL\b', "FOLD": r'\bFOLD\b', "HPA": r'\bHPA\b', "G-Card": r'G-?Card',
 "blueprint.json": r'blueprint[._]?json', "knowledge.md": r'knowledge\.md',
 "monolith/megaprompt": r'monolith|mega[ _]?prompt', "Triad": r'\btriad\b',
 "A/R Persona Surface": r'persona surface|a/?r persona|bio.?a&r', "Show Summary": r'show summary',
 "CINR": r'\bCINR\b', "ATP": r'\bATP\b', "Sacred Imperfection": r'sacred imperfection',
 "Council/SME": r'\bcouncil\b|\bSME\b', "Revision Loop": r'revision loop', "Sidechain": r'sidechain',
 "VIRAL-5": r'viral-?5', "Rap/SongMode": r'rap ?mode|song ?mode',
 "Load Protocol(LCP)": r'\bLCP\b|load completion|KBCP|\bMRP\b|MMCP', "Validator/CAP": r'validator|\bCAP\b',
 "Lyric Lock": r'lyric.?lock|lyrics?[ _-]?lock', "Suno": r'\bSuno\b',
}
PLANE = {
 "L0 runtime": ["Maestro","monolith/megaprompt","knowledge.md","blueprint.json","Rap/SongMode"],
 "L1 substrate": ["Mosaic","CINR","ATP","FOLD"],
 "L2 governance": ["SEM","SEG","Song Excellence","HPA","G-Card","Sacred Imperfection","Council/SME","Revision Loop","Sidechain","VIRAL-5"],
 "L3 UST pipeline": ["Technical UST","Creative UST","UST(umbrella)","Triad","A/R Persona Surface","Show Summary","FOIL","Suno"],
 "L4 hard control": ["Load Protocol(LCP)","Validator/CAP","Lyric Lock"],
}
plane_of = {c:p for p,cs in PLANE.items() for c in cs}

def run():
    src="/mnt/user-data/outputs/pass1_reassessed"
    freq={c:0 for c in COMP}; pair={}; pats={c:re.compile(p,re.I) for c,p in COMP.items()}
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        for e in json.load(open(os.path.join(src,fn)))["events"]:
            t=e["text"]; present=[c for c,pt in pats.items() if pt.search(t)]
            for c in present: freq[c]+=1
            for a,b in combinations(sorted(present),2):
                pair[(a,b)]=pair.get((a,b),0)+1
    arch={"components":[{"name":c,"freq":freq[c],"plane":plane_of.get(c,"?")} for c in sorted(freq,key=lambda x:-freq[x]) if freq[c]],
          "interconnects":[{"a":a,"b":b,"weight":w} for (a,b),w in sorted(pair.items(),key=lambda x:-x[1]) if w>=15],
          "planes":list(PLANE)}
    json.dump(arch, open("/mnt/user-data/outputs/architecture_v0.1.json","w"), ensure_ascii=False, indent=1)

    print("COMPONENTS by plane (freq across events):")
    for p in PLANE:
        comps=[(c,freq[c]) for c in PLANE[p] if freq[c]]
        comps.sort(key=lambda x:-x[1])
        line=" · ".join(f"{c} {n}" for c,n in comps)
        print(f"\n  {p}\n    {line}")
    print("\n\nTOP INTERCONNECTS (co-occurrence weight, cross-plane marked *):")
    for it in arch["interconnects"][:16]:
        x=" *" if plane_of.get(it["a"])!=plane_of.get(it["b"]) else "  "
        print(f"  {x} {it['a']:<22} — {it['b']:<22} {it['weight']}")
    print(f"\n-> architecture_v0.1.json written ({len(arch['components'])} components, {len(arch['interconnects'])} interconnects)")
if __name__=="__main__": run()

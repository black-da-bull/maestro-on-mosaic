#!/usr/bin/env python3
"""
Pass 9 — Graph Emission. Typed directed graph over the reconstructed system.
nodes = stable concepts/artifacts (+ lineage & null nodes); edges carry a TYPE
(dependency/authority/causality/mutation/contradiction/runtime_flow) and a
direction. Edge weights are pulled from Pass-4 co-occurrence where the pair
exists. This is the structural substrate Pass 10 serializes for boot.
"""
import json, os
arch=json.load(open("/mnt/user-data/outputs/architecture_v0.1.json"))
W={(min(i["a"],i["b"]),max(i["a"],i["b"])):i["weight"] for i in arch["interconnects"]}
def w(a,b): return W.get((min(a,b),max(a,b)),0)

# nodes: components + lineage + null nodes
nodes=[{"id":c["name"],"type":"component","plane":c["plane"],"freq":c["freq"]} for c in arch["components"]]
extra=[("v4.x runtime","lineage","L0 runtime"),("v5 build","lineage","-"),("Chimera","lineage","-"),
       ("SEM·12crit","null","L2 governance"),("SEM·13crit","null","L2 governance"),
       ("G-Card·70","null","L2 governance"),("G-Card·75","null","L2 governance"),
       ("97.5 floor","control","L2 governance"),("LCP","control","L4 hard control"),
       ("Council pressure","process","L2 governance"),("Revision Loop","component","L2 governance")]
have={n["id"] for n in nodes}
for nid,ty,pl in extra:
    if nid not in have: nodes.append({"id":nid,"type":ty,"plane":pl,"freq":0}); have.add(nid)

E=[ # (src, dst, type, label)
 ("Creative UST","Technical UST","runtime_flow","formalized into"),
 ("Technical UST","Triad","runtime_flow","derive"),
 ("Triad","A/R Persona Surface","runtime_flow","emit"),
 ("Triad","Show Summary","runtime_flow","emit"),
 ("Triad","Creative UST","runtime_flow","emit (lyric-locked)"),
 ("Technical UST","Suno","runtime_flow","render from LOCKED UST"),
 ("FOIL","Technical UST","runtime_flow","compile / upshift recurrence"),
 ("Show Summary","Suno","runtime_flow","render-facing"),
 ("A/R Persona Surface","Suno","runtime_flow","render-facing"),
 ("Maestro","Mosaic","dependency","mounts onto"),
 ("Maestro","monolith/megaprompt","dependency","runtime prompt"),
 ("Maestro","knowledge.md","dependency","K1-K10 on-demand"),
 ("Maestro","blueprint.json","dependency","active project truth"),
 ("Mosaic","CINR","dependency","continuity register"),
 ("Mosaic","ATP","dependency","transfer pack restore"),
 ("Mosaic","FOLD","dependency","graph compile"),
 ("SEM","Technical UST","authority","sidechain pressure (upstream)"),
 ("SEG","Technical UST","authority","interwoven, upstream of output"),
 ("SEG","SEM","authority","operationalizes (rubric ⊂ governance)"),
 ("SEG","G-Card","authority","decision surface"),
 ("SEG","Revision Loop","authority","drives pass|iterate|hold"),
 ("SEG","HPA","authority","perceptual validation"),
 ("SEG","Song Excellence","authority","institutional memory (ratchet)"),
 ("Council/SME","Technical UST","authority","pressure null-by-null"),
 ("Sacred Imperfection","SEM","authority","governs meaningful failure"),
 ("G-Card","Triad","authority","gate / promote"),
 ("Validator/CAP","Triad","authority","container gate"),
 ("Lyric Lock","Triad","authority","stop-condition (words LOCKED)"),
 ("97.5 floor","SEG","authority","release threshold (operator-grounded)"),
 ("LCP","Maestro","authority","fail-closed boot gate"),
 ("Creative UST","Technical UST","mutation","Creative proves -> Technical abstracts"),
 ("v4.x runtime","v5 build","mutation","REDUCED (the loss)"),
 ("Chimera","v5 build","mutation","ideas-for"),
 ("monolith/megaprompt","Mosaic","mutation","implicit substrate NAMED (v5)"),
 ("Council/SME","Revision Loop","causality","pressure -> revision"),
 ("Revision Loop","97.5 floor","causality","iterate until threshold"),
 ("SEM·12crit","SEM·13crit","contradiction","criterion count null (Memory Activation axis)"),
 ("G-Card·70","G-Card·75","contradiction","sub-gate threshold null"),
 ("97.5 floor","G-Card","contradiction","RESOLVED: not rivals (threshold vs decision)"),
]
edges=[{"source":s,"target":d,"type":t,"label":l,"weight":w(s,d)} for s,d,t,l in E]
TYPES=["dependency","authority","causality","mutation","contradiction","runtime_flow"]
graph={"nodes":nodes,"edges":edges,"edge_types":TYPES,
       "stats":{"nodes":len(nodes),"edges":len(edges)}}
json.dump(graph, open("/mnt/user-data/outputs/graph_v0.1.json","w"), ensure_ascii=False, indent=1)

from collections import Counter
ec=Counter(e["type"] for e in edges); nc=Counter(n["type"] for n in nodes)
print(f"GRAPH: {len(nodes)} nodes, {len(edges)} edges\n")
print("nodes by type:  "+", ".join(f"{k}={v}" for k,v in nc.items()))
print("edges by type:")
for t in TYPES: print(f"  {t:<14}{ec.get(t,0)}")
print("\nspine (runtime_flow), weighted:")
for e in edges:
    if e["type"]=="runtime_flow": print(f"  {e['source']:<20} →[{e['weight']:>3}] {e['target']:<22} {e['label']}")
print("\nkey authority edges:")
for e in edges:
    if e["type"]=="authority" and e["weight"]>0:
        print(f"  {e['source']:<20} ⇒ {e['target']:<22} {e['label']} (w{e['weight']})")
print(f"\n-> graph_v0.1.json written")

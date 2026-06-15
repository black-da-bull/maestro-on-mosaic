#!/usr/bin/env python3
"""
Pass 3 — Causal Chain Reconstruction.

Tags each event with lifecycle STAGE(s), then reconstructs causal arcs:
a trouble stage (troubleshoot/root_cause, or a Pass-1 failure) followed within
a window by a resolution stage (test/success/formalize/certify) = one arc.
This recovers the spec backbone theory->execution->troubleshoot->root_cause->
test->success->formalize->certify from the ordered chronology. Deterministic;
stage patterns encode the classification judgment. Pass 4 reads the arcs.
"""
import re, os, json
WINDOW = 12
STAGE = {
 "theory":           r'(?i)\b(what if|hypothes|in theory|conceptual|\bpropos|the idea\b|let.?s define|intend|design (a|the)|should (be|work)|treat .* as)',
 "live_execution":   r'(?i)(\bexecuting\b|\brunning\b|here.?s |here is |generated\b|\boutput\b|produced\b|rendered\b|\bbuilt\b|let me\b|i.?ll (build|run|create)|STATE:)',
 "troubleshoot":     r'(?i)\b(issue|problem|broke\b|error|not working|stuck\b|drift|wrong\b|failed|blocked|doesn.?t|isn.?t|won.?t|can.?t|missing|\bgap\b)',
 "root_cause":       r'(?i)(because\b|the reason|root cause|caused by|due to|the (issue|problem) is|turns out|that.?s why|stems from|the tell\b)',
 "test":             r'(?i)\b(test(s|ing)?|verif(y|ied)|\bcheck\b|validate|baseline|let.?s see|\btry(ing)?\b|measure)',
 "success":          r'(?i)\b(works?\b|passed\b|success|fixed\b|resolved|nailed|that.?s it|correct\b|solved|confirmed)',
 "formalize":        r'(?i)\b(formaliz|\block(ed)?\b|\bcanon\b|codif|freeze|frozen|establish|standard\b|\brule\b)',
 "certify":          r'(?i)(certif|validated|\bPASS\b|G-?Card|approved|locked_words|telemetry|verified and validated|admissib)',
}
ORD = {k:i+1 for i,k in enumerate(STAGE)}
TROUBLE = {"troubleshoot","root_cause"}
RESOLVE = {"test","success","formalize","certify"}
def stages(x): return [k for k,p in STAGE.items() if re.search(p,x)]

def run():
    src="/mnt/user-data/outputs/pass1_reassessed"; out="/mnt/user-data/outputs/pass3_causal"; os.makedirs(out,exist_ok=True)
    stageN={k:0 for k in STAGE}; arcs=[]; per_file={}
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        d=json.load(open(os.path.join(src,fn))); evs=d["events"]
        tagged=[]
        for e in evs:
            st=set(stages(e["text"]))
            if "failure" in e.get("types",[]): st.add("troubleshoot")
            for s in st: stageN[s]+=1
            tagged.append((e,st))
        fa=0
        for i,(e,st) in enumerate(tagged):
            if st & TROUBLE:
                for j in range(i+1, min(i+1+WINDOW, len(tagged))):
                    e2,st2=tagged[j]
                    if st2 & RESOLVE:
                        seq=[]
                        for k in range(i,j+1):
                            s=tagged[k][1]
                            if s: seq.append((tagged[k][0]["id"], "/".join(sorted(s,key=lambda x:ORD[x]))))
                        arcs.append(dict(source=d["source"], start=e["id"], end=e2["id"], span=j-i+1,
                                         trouble="/".join(sorted(st&TROUBLE,key=lambda x:ORD[x])),
                                         resolve="/".join(sorted(st2&RESOLVE,key=lambda x:ORD[x])),
                                         start_snip=re.sub(r'\s+',' ',e["text"])[:90],
                                         end_snip=re.sub(r'\s+',' ',e2["text"])[:90]))
                        fa+=1; break
        per_file[d["source"]]=fa
    json.dump(arcs, open(os.path.join(out,"causal_chains.json"),"w"), ensure_ascii=False)
    print(f"causal arcs reconstructed: {len(arcs)}  (trouble -> resolution, window {WINDOW})\n")
    print("lifecycle stage distribution (event-level):")
    mx=max(stageN.values())
    for k,_ in sorted(ORD.items(), key=lambda x:x[1]):
        v=stageN[k]; print(f"  {ORD[k]}. {k:<16}{v:>6}  {'#'*(v*36//mx)}")
    print("\narcs per file (top 10):")
    for f,a in sorted(per_file.items(), key=lambda x:-x[1])[:10]:
        if a: print(f"  {f[:50]:<50}{a:>5}")
    # exemplar arc from the soul session if present, else first non-empty
    pick=next((a for a in arcs if "Lyric_quality" in a["source"]), arcs[0] if arcs else None)
    if pick:
        print(f"\nexemplar arc  [{pick['source']}]  {pick['start']} -> {pick['end']}  (span {pick['span']})")
        print(f"  trouble({pick['trouble']}): {pick['start_snip']}")
        print(f"  resolve({pick['resolve']}): {pick['end_snip']}")
    print(f"\n-> causal_chains.json written ({len(arcs)} arcs)")
if __name__=="__main__": run()

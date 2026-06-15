#!/usr/bin/env python3
"""
Pass 2 — Mutation Detection (Transcript-to-Architecture Compiler).

Reads the Pass-1 event chronology and classifies, per event, WHAT CHANGED
across the 10 spec categories. Signal patterns encode the AI-classification
judgment; Python applies them deterministically at scale. Events carrying >=1
mutation are "meaningful turns"; the rest are content. Full text is not copied
here (it lives in the Pass-1 logs) — the mutation log references id + sha8.
Pass 3 (causal chains) refines these candidates.
"""
import re, os, json

MUT = {
 "boundary": r'(?i)\b(scope|boundar|out of scope|in scope|upshift|promot|demot|tier\b|macro\.micro|≤\s*\d|\bCAP\b|character (limit|economy)|truncat|granular)',
 "node": r'(?i)(\bdefine[ds]?\b|\bintroduc|new (object|artifact|concept|node|surface)|\bis a\b|≡|:=|canonical (object|truth))',
 "edge": r'(?i)(sidechain|→|->|depends on|feeds? (in|into)|derived from|mounts? (on|onto)|upstream|downstream|\bconnects?\b|relationship between|maps? to)',
 "authority": r'(?i)\b(authorit|\broot\b|\bcanon\b|supersed|overrid|governs?|frozen|locked|proposal[- ]class|operator (decides|root)|ROOT authority)',
 "workflow": r'(?i)\b(workflow|phase \d|pass \d|step \d|pipeline|sequence|\bgate\b|\bstage\b|\bloop\b|order of|revision loop|run order)',
 "policy": r'(?i)\b(must\b|shall\b|required\b|mandatory|invariant|\bnever\b|\balways\b|forbidden|\bpolicy\b|\blaw\b|non-negotiable)',
 "heuristic": r'(?i)\b(heuristic|when (to|not to)|rule of thumb|\bprefer\b|tends to|judgment|when it (works|applies)|portable judgment)',
 "runtime_behavior": r'(?i)\b(runtime|executes?|generate[ds]?|render[ds]?|\bboot\b|mount(s|ed)?|STATE:|behaves?|live (session|execution))',
 "emotional_validation": r'(?i)(the music is good|\bsoul\b|aliveness|emotional(ly)? (real|complete|present)|feels (real|alive)|love it|nailed it|🔥|😍|🙌)',
 "rights_provenance": r'(?i)\b(patent|provenance|\bIP\b|ownership|authorship|licens|attribution|lineage|supersession|\brights\b)',
}
def mtag(x): return [k for k, p in MUT.items() if re.search(p, x)]

def run():
    src = "/mnt/user-data/outputs/pass1_reassessed"
    out = "/mnt/user-data/outputs/pass2_mutations"; os.makedirs(out, exist_ok=True)
    catN = {k: 0 for k in MUT}; per_file = {}; mlog = []
    total_ev = total_mut = 0
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        d = json.load(open(os.path.join(src, fn)))
        fcat = {k: 0 for k in MUT}; fmut = 0
        for e in d["events"]:
            total_ev += 1
            cats = mtag(e["text"])
            if not cats: continue
            total_mut += 1; fmut += 1
            for c in cats: catN[c] += 1; fcat[c] += 1
            mlog.append(dict(id=e["id"], source=d["source"], role=e["role"],
                             event_types=e.get("types", []), mutations=cats,
                             chars=e["chars"], sha8=e["sha8"],
                             snippet=re.sub(r'\s+', ' ', e["text"])[:140]))
        per_file[d["source"]] = (fmut, len(d["events"]), fcat)
    json.dump(mlog, open(os.path.join(out, "mutation_log.json"), "w"), ensure_ascii=False)

    print(f"events scanned: {total_ev}   meaningful mutations: {total_mut} "
          f"({100*total_mut//max(1,total_ev)}%)\n")
    print("corpus-wide mutation categories:")
    for k, v in sorted(catN.items(), key=lambda x: -x[1]):
        bar = "#" * (v * 40 // max(catN.values()))
        print(f"  {k:<22}{v:>6}  {bar}")
    print("\nper-file mutation density (top categories):")
    print(f"  {'file':<46}{'mut':>5}{'/ev':>6}  dominant")
    for f, (m, n, fc) in sorted(per_file.items(), key=lambda x: -x[1][0])[:14]:
        dom = ", ".join(k for k, _ in sorted(fc.items(), key=lambda x: -x[1])[:3] if _ )
        top3 = ", ".join(f"{k}:{v}" for k, v in sorted(fc.items(), key=lambda x: -x[1])[:3] if v)
        print(f"  {f[:46]:<46}{m:>5}{n:>6}  {top3}")
    print(f"\n-> mutation_log.json written ({len(mlog)} mutation events)")
if __name__ == "__main__": run()

#!/usr/bin/env python3
"""
Pass 8 — Knowledge Spine & Heuristics. Distills repeated successful behavior
into portable judgment (why / when / when-not / prevents). Heuristic signals are
sparse in the record (Pass-2: 172) because the judgment is tacit; this pass
formalizes it from the recurring patterns. Mining is grounding only.
"""
import re, os, json
H_LINE=re.compile(r'(?im)^.{15,160}?\b(heuristic|when to|when not|rule of thumb|prefer\b|tends to|the trick is|the point is|that.?s why it works)\b.{0,140}$')
def mine():
    src="/mnt/user-data/outputs/pass1_reassessed"; ls=[]; n=0
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".events.json"): continue
        for e in json.load(open(os.path.join(src,fn)))["events"]:
            for m in H_LINE.finditer(e["text"]):
                n+=1; t=re.sub(r'\s+',' ',m.group(0)).strip()
                if 25<len(t)<150: ls.append(t)
    seen=set(); uq=[l for l in ls if not (l.lower()[:50] in seen or seen.add(l.lower()[:50]))]
    return n, uq

SPINE=[
 ("H1 Interwoven quality (sidechain, not terminal gate)","shape the artifact while it's still malleable","quality is judgable mid-build","signal exists only post-render","late rejection / validates-but-doesn't-sing"),
 ("H2 Lock the upstream truth object before deriving outputs","one locked source keeps surfaces consistent","multiple outputs must agree (triad)","single-output tasks","surface divergence / output ≠ intent"),
 ("H3 Creative-first, then formalize","Creative UST proves it works before Technical UST abstracts it","building a spec from creative intent","structure already fixed","abstract governance with no grounding"),
 ("H4 Promotion surfaces carry the global burden","lift recurring style/persona up so the working sheet stays local","a working surface is overloaded with global explanation","no recurrence to lift","working artifact bloats / loses local control"),
 ("H5 Upshift recurrence, keep local detail granular (FOIL)","shared recurrence belongs one scope up; unique detail stays put","duplicated terms/structures at the edges","recurrence is coincidental not semantic","duplication-bloat OR over-flattening of detail"),
 ("H6 Excellence ratchet — yesterday's best is today's floor","institutional memory of excellence blocks regression","iterative work with a quality standard","deliberately rough divergent drafts (gate comes after)","quality drift / regression to the mean"),
 ("H7 (end state) − (root input) = work; read raw as evidence","the work is the delta, the middle is the value","assessing/reconstructing a dev session","single-turn, non-evolving tasks","summarizing artifacts and missing the work"),
 ("H8 Compile around mutations, not turns; keep the ugly parts","mutations capture what changed; corrections are causal evidence","folding an append-only log into architecture","turns are atomic and non-evolving","losing the 'why' / treating provisional as final"),
 ("H9 Runtime stays primary; artifacts are derived views","the runtime carries the unformalizable flow; specs are projections","preserving a system whose value is partly tacit","system is fully specifiable","the reduction loss (flatten drops flow + corrections)"),
 ("H10 Container-PASS ≠ quality — gate the flow separately","format validation can't see craft","any validated output where craft matters","output is purely structural","green-lighting flow-broken-but-valid output"),
 ("H11 Spill raw clay in, uncompromising gate out","separating freedom (input) from enforcement (output) lets divergence flow","creative generation with a quality standard","input must be constrained (safety-critical)","creative timidity OR quality compromise"),
 ("H12 Sacred Imperfection — govern meaningful failure","perfect-but-dead fails the emotional bar; imperfection carries aliveness","emotional/artistic output","precision-critical output","sterile, average-feeling output that passes format"),
]
def run():
    n, mined = mine()
    spine=[dict(heuristic=h,why=w,when=a,when_not=b,prevents=p) for h,w,a,b,p in SPINE]
    json.dump({"knowledge_spine":spine,"grounding_count":n,"mined_samples":mined[:30]},
              open("/mnt/user-data/outputs/knowledge_spine_v0.1.json","w"),ensure_ascii=False,indent=1)
    print(f"KNOWLEDGE SPINE — portable heuristics   [explicit heuristic lines mined: {n}; {len(mined)} distinct]\n")
    for h,w,a,b,p in SPINE:
        print(f"  {h}")
        print(f"     why {w}  ·  when {a}  ·  NOT {b}  ·  prevents {p}")
    if mined:
        print("\n  mined examples (verbatim):")
        for l in mined[:3]: print(f"    · {l[:120]}")
    print(f"\n-> knowledge_spine_v0.1.json written")
if __name__=="__main__": run()

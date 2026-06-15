#!/usr/bin/env python3
"""
Pass 1 v0.2 — Event Chronology with ADAPTIVE segmentation.

v0.1 baseline kept. Extension: accommodate the formats v0.1 segmented too
coarsely, by adapting to each file's line-length profile:

  - long-line exports (e.g. claude2: one turn per ~650-char line) -> segment
    by line; UI-sidebar chrome is TAGGED (role=ui_chrome), never dropped.
  - sparse/coarse files (admin preview, big definition docs) -> structural
    base segmentation, then sub-split any block > MAXBLK on paragraph breaks.

Invariants unchanged: all files = substrate, full text preserved (coverage
check), stable IDs, human=root / ai=proposal, event-type tags (Pass-2 refines).
"""
import re, os, json, hashlib, statistics

MAXBLK = 2500          # blocks larger than this get paragraph sub-split
LONGLINE = 250         # avg non-blank line length above this => line mode

def signals(t):
    return dict(you=len(re.findall(r'(?m)^\s*You said:', t)),
                gpt=len(re.findall(r'(?m)^\s*ChatGPT said:', t)),
                think=len(re.findall(r'Thought for \d+', t)),
                state=len(re.findall(r'(?m)^\s*(STATE:|MUTATION STATUS:|SEM GATE:)', t)),
                md=len(re.findall(r'(?m)^#{1,4}\s+\S', t)))
def ftype(s):
    if s["you"] >= 3 and s["gpt"] >= 1: return "dialogue"
    if s["state"] >= 2 or s["think"] >= 5: return "session"
    if s["md"] >= 5: return "document"
    return "session"

CHROME = re.compile(r'(?i)^(last message .* ago|start a task|new chat|share|update|'
                    r'create|configure|only me|live|updates pending|show more|pasted|\d+ \w+ ago)\s*$')
def infer_role(line):
    h = line.strip().lower()
    if CHROME.match(line.strip()): return "ui_chrome"
    if h.startswith("you said"): return "human_root"
    if re.match(r'(state:|thought for|stopped thinking|reasoned|chatgpt said|maestro)', h): return "ai_proposal"
    return "segment"

def para_split(role, body):
    if len(body) <= MAXBLK:
        return [(role, body)]
    return [(role, p.strip()) for p in re.split(r'\n\s*\n', body) if p.strip()]

def seg_dialogue(t):
    pat = re.compile(r'(?m)^\s*(You said:|ChatGPT said:)[ \t]*'); ms = list(pat.finditer(t)); out=[]
    if not ms: return para_split("segment", t.strip()) if t.strip() else []
    if t[:ms[0].start()].strip(): out += para_split("context", t[:ms[0].start()].strip())
    for i,m in enumerate(ms):
        role = "human_root" if m.group(1).startswith("You") else "ai_proposal"
        end = ms[i+1].start() if i+1<len(ms) else len(t)
        body = t[m.end():end].strip()
        if body: out += para_split(role, body)
    return out

def seg_session(t):
    bound = re.compile(r'(?m)^\s*(STATE:|Thought for \d+|Stopped thinking|Reasoned|'
                       r'You said:|ChatGPT said:|pasted|Show more)\b')
    idx = [m.start() for m in bound.finditer(t)]
    if not idx:
        return [x for p in re.split(r'\n\s*\n', t) if p.strip() for x in para_split("segment", p.strip())]
    idx = [0]+idx+[len(t)]; out=[]
    for a,b in zip(idx, idx[1:]):
        c = t[a:b].strip()
        if not c: continue
        role = infer_role(c.splitlines()[0] if c.splitlines() else c)
        out += para_split(role, c)
    return out

def seg_document(t):
    pat = re.compile(r'(?m)^(#{1,4}\s+\S.*)$'); ms=list(pat.finditer(t)); out=[]
    if not ms: return para_split("artifact", t.strip()) if t.strip() else []
    if t[:ms[0].start()].strip(): out += para_split("artifact", t[:ms[0].start()].strip())
    for i,m in enumerate(ms):
        end = ms[i+1].start() if i+1<len(ms) else len(t)
        out += para_split("artifact", t[m.start():end].strip())
    return out

def segment(t, typ):
    nb = [l for l in t.splitlines() if l.strip()]
    if nb and statistics.mean(len(l) for l in nb) > LONGLINE:      # long-line export
        return [(infer_role(l), l.strip()) for l in nb]
    return {"dialogue":seg_dialogue,"session":seg_session,"document":seg_document}[typ](t)

SIGS = {
 "reversal":r'DRIFT DETECTED|revert|rolled back|\bundo\b|took it back',
 "failure":r'\bFAIL(ED|URE)?\b|blocked|\berror\b|phantom|broke\b|stuck\b|couldn.?t|didn.?t work|invalidat',
 "validation":r'\bPASS\b|SEM GATE|G-?Card|validation|telemetry|CAP:|LOCKED',
 "test":r'\btest(s|ing)?\b|verif(y|ied)|baseline',
 "artifact_emission":r'```|Creative UST|Technical UST|\bTRIAD\b|Final_Suno|Show Summary|\[Theory\]',
 "correction":r'(?i)\bactually\b|correction|instead\b|should be\b|that.?s wrong|reassess|stop tr',
 "emotional_validation":r'the music is good|love it|nailed it|🔥|😍|🙌'}
def tag(x): return [k for k,p in SIGS.items() if re.search(p,x)]
def fk(f): return re.sub(r'[^A-Za-z0-9]+','_',os.path.splitext(os.path.basename(f))[0]).strip('_').upper()[:38]
ART={'loss_demonstration_v0_1','maestro_month_synthesis_and_rebuild_blueprint_v0_1','maestro_v5_ust_sem_interwoven_v0_1',
 'song_excellence_governance_v0_1','source_lineage_reconciliation_register_v0_1','who_dat_runtime_assessment_v0_1',
 'maestro_version_changelog','open_question_verification_queries_v0_1','v5_corrective_regen_prompt_v0_1','KERNEL'}

def run():
    base,out="/mnt/project","/mnt/user-data/outputs/pass1_v2"; os.makedirs(out,exist_ok=True)
    idx,tally=[],{}
    print(f"{'file':<46}{'type':<10}{'events':>7}{'chrome':>7}{'cover':>7}")
    print("-"*82)
    for f in sorted(os.listdir(base)):
        p=os.path.join(base,f)
        if not os.path.isfile(p) or os.path.splitext(f)[0] in ART or f.endswith(('.yaml','.json','.py')): continue
        t=open(p,encoding='utf-8',errors='replace').read(); typ=ftype(signals(t)); segs=segment(t,typ)
        key=fk(f); ev=[]; cov=0; chrome=0
        for i,(role,body) in enumerate(segs,1):
            ty=tag(body); cov+=len(body); chrome+=(role=="ui_chrome")
            for k in ty: tally[k]=tally.get(k,0)+1
            ev.append(dict(id=f"{key}:E{i:04d}",role=role,types=ty,chars=len(body),
                           sha8=hashlib.sha256(body.encode()).hexdigest()[:8],text=body))
        json.dump(dict(source=f,filekey=key,type=typ,n_events=len(ev),events=ev),
                  open(os.path.join(out,f"{key}.events.json"),"w"),ensure_ascii=False)
        idx += [{k:e[k] for k in ("id","role","types","chars","sha8")} for e in ev]
        nonws=len(re.sub(r'\s','',t)); coverage=min(cov/max(1,nonws),1.0)
        print(f"{f[:46]:<46}{typ:<10}{len(ev):>7}{chrome:>7}{coverage*100:>6.0f}%")
    json.dump(idx,open("/mnt/user-data/outputs/pass1_v2_chronology_index.json","w"),ensure_ascii=False)
    print(f"\nTOTAL events: {len(idx)}   event-type tally: "+", ".join(f"{k}={v}" for k,v in sorted(tally.items(),key=lambda x:-x[1])))

if __name__=="__main__": run()

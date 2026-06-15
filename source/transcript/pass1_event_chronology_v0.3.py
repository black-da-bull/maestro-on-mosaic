#!/usr/bin/env python3
"""
Pass 1 v0.3 — Event Chronology, baseline-preserving adaptive segmentation.

v0.1 baseline behavior is kept for every file that is already well-segmented.
Refinement is applied ONLY to files that come out too coarse (avg event size
above COARSE), and uses a size FLOOR so it groups rather than shatters:
  - long-line exports (claude2) -> line-level, UI chrome tagged not dropped
  - other coarse files -> split oversized base blocks on paragraph breaks,
    grouped up to FLOOR chars
Well-segmented files (dialogues, version chain, worklog, ...) are untouched.
Invariants: all files = substrate, full text preserved (coverage), stable IDs.
"""
import re, os, json, hashlib, statistics
COARSE, REFINE_BLK, FLOOR, LONGLINE = 4000, 1500, 400, 250

def signals(t):
    return dict(you=len(re.findall(r'(?m)^\s*You said:',t)),gpt=len(re.findall(r'(?m)^\s*ChatGPT said:',t)),
                think=len(re.findall(r'Thought for \d+',t)),
                state=len(re.findall(r'(?m)^\s*(STATE:|MUTATION STATUS:|SEM GATE:)',t)),
                md=len(re.findall(r'(?m)^#{1,4}\s+\S',t)))
def ftype(s):
    if s["you"]>=3 and s["gpt"]>=1: return "dialogue"
    if s["state"]>=2 or s["think"]>=5: return "session"
    if s["md"]>=5: return "document"
    return "session"

CHROME=re.compile(r'(?i)^(last message .* ago|start a task|new chat|share|update|create|configure|'
                  r'only me|live|updates pending|show more|pasted|\d+ \w+ ago)\s*$')
def role_of(line):
    h=line.strip().lower()
    if CHROME.match(line.strip()): return "ui_chrome"
    if h.startswith("you said"): return "human_root"
    if re.match(r'(state:|thought for|stopped thinking|reasoned|chatgpt said|maestro)',h): return "ai_proposal"
    return "segment"

# ---- baseline segmenters (v0.1: NO sub-splitting) ----
def base_dialogue(t):
    pat=re.compile(r'(?m)^\s*(You said:|ChatGPT said:)[ \t]*'); ms=list(pat.finditer(t)); out=[]
    if not ms: return [("segment",t.strip())] if t.strip() else []
    if t[:ms[0].start()].strip(): out.append(("context",t[:ms[0].start()].strip()))
    for i,m in enumerate(ms):
        r="human_root" if m.group(1).startswith("You") else "ai_proposal"
        e=ms[i+1].start() if i+1<len(ms) else len(t); b=t[m.end():e].strip()
        if b: out.append((r,b))
    return out
def base_session(t):
    bd=re.compile(r'(?m)^\s*(STATE:|Thought for \d+|Stopped thinking|Reasoned|You said:|ChatGPT said:|pasted|Show more)\b')
    idx=[m.start() for m in bd.finditer(t)]
    if not idx: return [("segment",p.strip()) for p in re.split(r'\n\s*\n',t) if p.strip()]
    idx=[0]+idx+[len(t)]; out=[]
    for a,b in zip(idx,idx[1:]):
        c=t[a:b].strip()
        if c: out.append((role_of(c.splitlines()[0] if c.splitlines() else c),c))
    return out
def base_document(t):
    pat=re.compile(r'(?m)^(#{1,4}\s+\S.*)$'); ms=list(pat.finditer(t)); out=[]
    if not ms: return [("artifact",t.strip())] if t.strip() else []
    if t[:ms[0].start()].strip(): out.append(("artifact",t[:ms[0].start()].strip()))
    for i,m in enumerate(ms):
        e=ms[i+1].start() if i+1<len(ms) else len(t); out.append(("artifact",t[m.start():e].strip()))
    return out
BASE={"dialogue":base_dialogue,"session":base_session,"document":base_document}

def split_floor(text):
    out,buf=[],""
    for p in re.split(r'\n\s*\n',text):
        p=p.strip()
        if not p: continue
        buf=(buf+"\n\n"+p) if buf else p
        if len(buf)>=FLOOR: out.append(buf); buf=""
    if buf:
        if out: out[-1]+="\n\n"+buf
        else: out.append(buf)
    return out

def refine(segs,t):
    nb=[l for l in t.splitlines() if l.strip()]
    if nb and statistics.mean(len(l) for l in nb)>LONGLINE:        # long-line export
        return [(role_of(l),l.strip()) for l in nb]
    out=[]
    for r,b in segs:
        out += [(r,c) for c in split_floor(b)] if len(b)>REFINE_BLK else [(r,b)]
    return out

SIGS={"reversal":r'DRIFT DETECTED|revert|rolled back|\bundo\b|took it back',
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
    base,out="/mnt/project","/mnt/user-data/outputs/pass1_final"; os.makedirs(out,exist_ok=True)
    idx,tally=[],{}
    print(f"{'file':<46}{'type':<10}{'base':>6}{'final':>7}{'mode':>9}{'cov':>6}")
    print("-"*84)
    for f in sorted(os.listdir(base)):
        p=os.path.join(base,f)
        if not os.path.isfile(p) or os.path.splitext(f)[0] in ART or f.endswith(('.yaml','.json','.py')): continue
        t=open(p,encoding='utf-8',errors='replace').read(); typ=ftype(signals(t))
        segs=BASE[typ](t); nbase=len(segs); avg=sum(len(b) for _,b in segs)/max(1,nbase)
        mode="baseline"
        if avg>COARSE: segs=refine(segs,t); mode="refined"
        key=fk(f); ev=[]; cov=0
        for i,(r,b) in enumerate(segs,1):
            ty=tag(b); cov+=len(b)
            for k in ty: tally[k]=tally.get(k,0)+1
            ev.append(dict(id=f"{key}:E{i:04d}",role=r,types=ty,chars=len(b),
                           sha8=hashlib.sha256(b.encode()).hexdigest()[:8],text=b))
        json.dump(dict(source=f,filekey=key,type=typ,mode=mode,n_events=len(ev),events=ev),
                  open(os.path.join(out,f"{key}.events.json"),"w"),ensure_ascii=False)
        idx += [{k:e[k] for k in ("id","role","types","chars","sha8")} for e in ev]
        cv=min(cov/max(1,len(re.sub(r'\s','',t))),1.0)
        print(f"{f[:46]:<46}{typ:<10}{nbase:>6}{len(ev):>7}{mode:>9}{cv*100:>5.0f}%")
    json.dump(idx,open("/mnt/user-data/outputs/pass1_final_chronology_index.json","w"),ensure_ascii=False)
    print(f"\nTOTAL events: {len(idx)}   tally: "+", ".join(f"{k}={v}" for k,v in sorted(tally.items(),key=lambda x:-x[1])))
if __name__=="__main__": run()

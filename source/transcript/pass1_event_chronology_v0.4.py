#!/usr/bin/env python3
"""
Pass 1 v0.4 — adds structured_yaml (hybrid) as a 4th type and REASSESSES the
corpus under the new understanding:
  - .yaml files (previously skipped) are now in scope -> structured_yaml/hybrid
  - YAML-ish .txt (high key:value, no md headers) re-types to structured_yaml
  - exclusion narrowed to ONLY this-session derived artifacts (avoid circularity)
v0.3 baseline-preserving behavior is unchanged for dialogue/session/document.
"""
import re, os, json, hashlib, statistics
COARSE, REFINE_BLK, FLOOR, LONGLINE, YFLOOR = 4000, 1500, 400, 250, 300

# this-session derived artifacts (mine) -> excluded to avoid folding outputs as source
MINE = {'song_excellence_governance_v0_1','maestro_v5_ust_sem_interwoven_v0_1',
        'source_lineage_reconciliation_register_v0_1','loss_demonstration_v0_1',
        'who_dat_runtime_assessment_v0_1','maestro_month_synthesis_and_rebuild_blueprint_v0_1'}
# previously excluded but actually prior-work substrate -> now IN scope
PRIOR_CANON = {'maestro_version_changelog','open_question_verification_queries_v0_1',
               'v5_corrective_regen_prompt_v0_1','KERNEL'}

def signals(t):
    nb=[l for l in t.splitlines() if l.strip()]
    return dict(you=len(re.findall(r'(?m)^\s*You said:',t)),gpt=len(re.findall(r'(?m)^\s*ChatGPT said:',t)),
                think=len(re.findall(r'Thought for \d+',t)),
                state=len(re.findall(r'(?m)^\s*(STATE:|MUTATION STATUS:|SEM GATE:)',t)),
                md=len(re.findall(r'(?m)^#{1,4}\s+\S',t)),
                key=len(re.findall(r'(?m)^\s*[A-Za-z_][\w .-]{1,40}:\s',t)), nb=len(nb))
def ftype(s, ext):
    if ext=='.yaml': return "structured_yaml"
    if s["you"]>=3 and s["gpt"]>=1: return "dialogue"
    if s["state"]>=2 or s["think"]>=5: return "session"   # session markers win over YAML heuristic
    if s["md"]==0 and s["think"]==0 and s["key"]>=30 and s["key"]>s["nb"]*0.25: return "structured_yaml"
    if s["md"]>=5: return "document"
    return "session"

CHROME=re.compile(r'(?i)^(last message .* ago|start a task|new chat|share|update|create|configure|'
                  r'only me|live|updates pending|show more|pasted|\d+ \w+ ago)\s*$')
def role_of(l):
    h=l.strip().lower()
    if CHROME.match(l.strip()): return "ui_chrome"
    if h.startswith("you said"): return "human_root"
    if re.match(r'(state:|thought for|stopped thinking|reasoned|chatgpt said|maestro)',h): return "ai_proposal"
    return "segment"

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
def seg_structured(t):
    bound=re.compile(r'^(?:[A-Za-z_][\w.\-]*:|\s*-\s)'); raw,cur=[],[]
    for ln in t.splitlines():
        if bound.match(ln) and cur: raw.append("\n".join(cur)); cur=[ln]
        else: cur.append(ln)
    if cur: raw.append("\n".join(cur))
    out,buf=[],""
    for r in raw:
        if not r.strip(): continue
        buf=(buf+"\n"+r) if buf else r
        if len(buf)>=YFLOOR: out.append(buf); buf=""
    if buf:
        if out: out[-1]+="\n"+buf
        else: out.append(buf)
    return [("artifact",s) for s in out]
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
    if nb and statistics.mean(len(l) for l in nb)>LONGLINE: return [(role_of(l),l.strip()) for l in nb]
    out=[]
    for r,b in segs: out += [(r,c) for c in split_floor(b)] if len(b)>REFINE_BLK else [(r,b)]
    return out

def segment(t,typ):
    if typ=="structured_yaml": return seg_structured(t),"hybrid"
    segs=BASE[typ](t); avg=sum(len(b) for _,b in segs)/max(1,len(segs))
    if avg>COARSE: return refine(segs,t),"refined"
    return segs,"baseline"

SIGS={"reversal":r'DRIFT DETECTED|revert|rolled back|\bundo\b|invalidat',
 "failure":r'\bFAIL(ED|URE)?\b|blocked|\berror\b|phantom|broke\b|stuck\b|couldn.?t|didn.?t work|\bgap|missing|not sufficient',
 "validation":r'\bPASS\b|SEM GATE|G-?Card|validation|telemetry|CAP:|LOCKED|frozen|authoritative',
 "test":r'\btest(s|ing)?\b|verif(y|ied)|baseline',
 "artifact_emission":r'```|Creative UST|Technical UST|\bTRIAD\b|Final_Suno|Show Summary|\[Theory\]|\.yaml|\.md|contract',
 "correction":r'(?i)\bactually\b|correction|instead\b|should be\b|that.?s wrong|reassess|stop tr|not the whole|may not',
 "emotional_validation":r'the music is good|love it|nailed it|🔥|😍|🙌'}
def tag(x): return [k for k,p in SIGS.items() if re.search(p,x)]
def fk(f): return re.sub(r'[^A-Za-z0-9]+','_',os.path.splitext(os.path.basename(f))[0]).strip('_').upper()[:42]

def run():
    base,out="/mnt/project","/mnt/user-data/outputs/pass1_reassessed"; os.makedirs(out,exist_ok=True)
    idx,tally=[],{}; PRIORyaml=set()
    print(f"{'file':<50}{'type':<17}{'mode':>9}{'events':>7}{'cov':>5}  scope")
    print("-"*100)
    for f in sorted(os.listdir(base)):
        p=os.path.join(base,f); stem=os.path.splitext(f)[0]
        if not os.path.isfile(p) or stem in MINE or f.endswith(('.json','.py')): continue
        ext=os.path.splitext(f)[1].lower()
        newly = (ext=='.yaml') or (stem in PRIOR_CANON)
        t=open(p,encoding='utf-8',errors='replace').read(); s=signals(t); typ=ftype(s,ext)
        segs,mode=segment(t,typ); key=fk(f); ev=[]; cov=0
        for i,(r,b) in enumerate(segs,1):
            ty=tag(b); cov+=len(b)
            for k in ty: tally[k]=tally.get(k,0)+1
            ev.append(dict(id=f"{key}:E{i:04d}",role=r,types=ty,chars=len(b),
                           sha8=hashlib.sha256(b.encode()).hexdigest()[:8],text=b))
        json.dump(dict(source=f,filekey=key,type=typ,mode=mode,n_events=len(ev),events=ev),
                  open(os.path.join(out,f"{key}.events.json"),"w"),ensure_ascii=False)
        idx += [{k:e[k] for k in ("id","role","types","chars","sha8")} for e in ev]
        cv=min(cov/max(1,len(re.sub(r'\s','',t))),1.0)
        print(f"{f[:50]:<50}{typ:<17}{mode:>9}{len(ev):>7}{cv*100:>4.0f}%  {'NEW' if newly else ''}")
    json.dump(idx,open("/mnt/user-data/outputs/pass1_reassessed_index.json","w"),ensure_ascii=False)
    print(f"\nfiles in scope: (see above)   TOTAL events: {len(idx)}")
    print("tally: "+", ".join(f"{k}={v}" for k,v in sorted(tally.items(),key=lambda x:-x[1])))
if __name__=="__main__": run()

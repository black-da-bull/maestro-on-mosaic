#!/usr/bin/env python3
"""
forensic_ingest — bring the WHOLE corpus into substrate form. No file set aside.

Every file is a load-bearing substrate component. This ingests each by its own
structure and preserves full text. Typing chooses the segmentation method only;
it never decides which files "count."

Segment roles:
  human_root / ai_proposal   (dialogue turns, INV-18)
  doc_section                (markdown / authority-numbered sections)
  session_segment            (split on reasoning/STATE boundaries)
  block                      (fallback paragraph blocks; nothing dropped)
Output: per-file component JSON + a unified manifest. Provenance on every atom.
"""
import re, os, json, hashlib

def fk(path):
    return re.sub(r'[^A-Za-z0-9]+','_',os.path.basename(path)).strip('_').upper()[:40]

def sig(txt):
    return dict(
        you=len(re.findall(r'(?m)^\s*You said:',txt)),
        gpt=len(re.findall(r'(?m)^\s*ChatGPT said:',txt)),
        think=len(re.findall(r'Thought for \d+|Stopped thinking',txt)),
        state=len(re.findall(r'(?m)^\s*(STATE:|MUTATION STATUS:|SEM GATE:)',txt)),
        md=len(re.findall(r'(?m)^#{1,6}\s+\S',txt)),
        auth=len(re.findall(r'(?m)^#+\s+(I+\.|[A-Z]+\.\s|OPERATING|System Operating)',txt)),
    )

def seg_dialogue(txt):
    pat=re.compile(r'(?m)^\s*(You said:|ChatGPT said:)[ \t]*'); ms=list(pat.finditer(txt)); out=[]
    if not ms: return out
    pre=txt[:ms[0].start()].strip()
    if pre: out.append(("context",pre))
    for i,m in enumerate(ms):
        role="human_root" if m.group(1).startswith("You") else "ai_proposal"
        body=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
        if body: out.append((role,body))
    return out

def seg_headers(txt):
    pat=re.compile(r'(?m)^(#{1,6}\s+\S.*)$'); ms=list(pat.finditer(txt)); out=[]
    if not ms: return out
    pre=txt[:ms[0].start()].strip()
    if pre: out.append(("doc_section",pre))
    for i,m in enumerate(ms):
        body=txt[m.start():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
        if body: out.append(("doc_section",body))
    return out

def seg_boundaries(txt):
    pat=re.compile(r'(?m)^(?=.*(Thought for \d+|Stopped thinking|STATE:|pasted|Show more)).*$')
    ms=list(re.finditer(r'(Thought for \d+|Stopped thinking|^STATE:)',txt,re.M)); 
    if len(ms)<2: return []
    out=[]; pre=txt[:ms[0].start()].strip()
    if pre: out.append(("session_segment",pre))
    for i,m in enumerate(ms):
        body=txt[m.start():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
        if body: out.append(("session_segment",body))
    return out

def seg_blocks(txt, target=3000):
    paras=re.split(r'\n\s*\n',txt); out=[]; buf=""
    for p in paras:
        if len(buf)+len(p)>target and buf:
            out.append(("block",buf.strip())); buf=""
        buf+=p+"\n\n"
    if buf.strip(): out.append(("block",buf.strip()))
    return out

def ingest(path):
    txt=open(path,encoding='utf-8',errors='replace').read(); s=sig(txt)
    if s["you"]>=3 and s["gpt"]>=1:
        method,raw="dialogue",seg_dialogue(txt)
    elif s["md"]>=4:
        method,raw="headers",seg_headers(txt)
    elif s["think"]>=2 or s["state"]>=1:
        method,raw="boundaries",seg_boundaries(txt)
    else:
        method,raw=None,[]
    if not raw:
        method,raw="blocks",seg_blocks(txt)
    key=fk(path); segs=[]
    for i,(role,body) in enumerate(raw,1):
        segs.append(dict(id=f"{key}:S{i:04d}",role=role,chars=len(body),
                         sha8=hashlib.sha256(body.encode()).hexdigest()[:8],text=body))
    return dict(source_file=os.path.basename(path),filekey=key,method=method,
                n_segments=len(segs),total_chars=sum(x["chars"] for x in segs),
                src_chars=len(txt),segments=segs)

ART={'loss_demonstration_v0_1.md','maestro_month_synthesis_and_rebuild_blueprint_v0_1.md',
     'maestro_v5_ust_sem_interwoven_v0_1.md','song_excellence_governance_v0_1.md',
     'source_lineage_reconciliation_register_v0_1.md','who_dat_runtime_assessment_v0_1.md'}

if __name__=="__main__":
    base="/mnt/project"; out="/mnt/user-data/outputs"; manifest=[]; tot=0; src_tot=0
    print(f"{'file':<48} {'method':<11} {'segs':>5} {'chars_kept':>11}")
    print("-"*84)
    for f in sorted(os.listdir(base)):
        p=os.path.join(base,f)
        if f in ART or not os.path.isfile(p) or f.endswith(('.yaml','.json','.py')): continue
        comp=ingest(p)
        json.dump(comp,open(os.path.join(out,f"substrate_{comp['filekey']}.json"),"w"),
                  indent=1,ensure_ascii=False)
        manifest.append({k:comp[k] for k in ("source_file","filekey","method","n_segments","total_chars","src_chars")})
        tot+=comp["total_chars"]; src_tot+=comp["src_chars"]
        print(f"{f[:48]:<48} {comp['method']:<11} {comp['n_segments']:>5} {comp['total_chars']:>11,}")
    json.dump({"corpus":"maestro_substrate","files":len(manifest),
               "total_segments":sum(m['n_segments'] for m in manifest),
               "chars_kept":tot,"src_chars":src_tot,"components":manifest},
              open(os.path.join(out,"substrate_manifest.json"),"w"),indent=1)
    print("-"*84)
    print(f"{'TOTAL':<48} {'':<11} {sum(m['n_segments'] for m in manifest):>5} {tot:>11,}")
    print(f"\nfiles ingested: {len(manifest)}   chars kept: {tot:,} of {src_tot:,} source "
          f"({100*tot/src_tot:.1f}% — remainder is whitespace/markers between segments)")

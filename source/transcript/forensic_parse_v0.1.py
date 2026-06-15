#!/usr/bin/env python3
"""
forensic_parse — W0 parse extractor (maestro-forensic-transcript skill).

Tools-first mechanical pass: segment a dev-session transcript into an
append-only event log. AI does NOT read-and-paraphrase here; Python segments,
attributes role, assigns stable IDs, and preserves FULL turn text.

Contract honored:
  - append-only event log (event sourcing); turns are evidence, never rewritten
  - human turns = ROOT, ai turns = PROPOSAL (INV-18)
  - detail-attached: full text preserved per turn (no skeletons)
  - stable IDs: <FILEKEY>:T#### ; content sha8 for dedup/provenance
Output: a JSON event log; nothing is classified or folded at this stage.
"""
import re, json, sys, os, hashlib

ROLE_HUMAN, ROLE_AI = "human_root", "ai_proposal"

def filekey(path):
    base = os.path.basename(path)
    base = re.sub(r'[^A-Za-z0-9]+', '_', base).strip('_').upper()
    return base[:40]

def detect_format(txt):
    you = len(re.findall(r'(?m)^\s*You said:', txt))
    gpt = len(re.findall(r'(?m)^\s*ChatGPT said:', txt))
    maestro = len(re.findall(r'\bMaestro\b', txt))
    if you >= 3 and gpt >= 1:
        return 'chatgpt'
    if maestro >= 5:
        return 'maestro'
    return 'unknown'

def parse_chatgpt(txt):
    """Segment on 'You said:' (human root) / 'ChatGPT said:' (ai proposal)."""
    pat = re.compile(r'(?m)^\s*(You said:|ChatGPT said:)[ \t]*')
    ms = list(pat.finditer(txt))
    turns = []
    if not ms:
        return turns
    pre = txt[:ms[0].start()].strip()
    if pre:
        turns.append(("context", pre))   # title/seed before first marker
    for i, m in enumerate(ms):
        role = ROLE_HUMAN if m.group(1).startswith("You") else ROLE_AI
        start = m.end()
        end = ms[i+1].start() if i+1 < len(ms) else len(txt)
        body = txt[start:end].strip()
        if body:
            turns.append((role, body))
    return turns

def build_log(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    fmt = detect_format(txt)
    if fmt == 'chatgpt':
        raw = parse_chatgpt(txt)
    else:
        raw = []   # maestro/unknown formats handled by a separate variant
    key = filekey(path)
    events = []
    for i, (role, body) in enumerate(raw, 1):
        events.append({
            "id": f"{key}:T{i:04d}",
            "role": role,
            "chars": len(body),
            "sha8": hashlib.sha256(body.encode('utf-8')).hexdigest()[:8],
            "text": body,
        })
    return {
        "source_file": os.path.basename(path),
        "filekey": key,
        "format": fmt,
        "n_events": len(events),
        "n_human_root": sum(1 for e in events if e["role"] == ROLE_HUMAN),
        "n_ai_proposal": sum(1 for e in events if e["role"] == ROLE_AI),
        "n_context": sum(1 for e in events if e["role"] == "context"),
        "total_chars": sum(e["chars"] for e in events),
        "events": events,
    }

def summarize(log, preview=14):
    print(f"\n=== {log['source_file']}  [{log['format']}] ===")
    print(f"events={log['n_events']}  human_root={log['n_human_root']}  "
          f"ai_proposal={log['n_ai_proposal']}  context={log['n_context']}  "
          f"chars_preserved={log['total_chars']:,}")
    print("  id            role          chars  first-line")
    for e in log["events"][:preview]:
        snip = re.sub(r'\s+', ' ', e["text"])[:78]
        print(f"  {e['id']:<13} {e['role']:<12} {e['chars']:>6}  {snip}")
    if log["n_events"] > preview:
        print(f"  … +{log['n_events']-preview} more (full text in JSON)")

if __name__ == "__main__":
    outdir = "/mnt/user-data/outputs"
    for path in sys.argv[1:]:
        log = build_log(path)
        summarize(log)
        if log["format"] == "chatgpt" and log["n_events"]:
            outpath = os.path.join(outdir, f"eventlog_{log['filekey']}.json")
            json.dump(log, open(outpath, "w"), indent=1, ensure_ascii=False)
            print(f"  -> event log saved: {os.path.basename(outpath)}")

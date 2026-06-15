#!/usr/bin/env python3
"""
forensic_classify — types each corpus file so it is parsed by its REAL structure.

The corpus is heterogeneous: clean ChatGPT dialogues, Maestro admin/runtime
sessions, reasoning-heavy worklogs, instruction-corpus pastes (authoring the
GPT), and definition docs. Turn-parsing only fits the dialogue types; the rest
must be segmented structurally or held as reference. Mechanical signals only.
"""
import re, os, json

def signals(txt):
    return {
        "you":   len(re.findall(r'(?m)^\s*You said:', txt)),
        "gpt":   len(re.findall(r'(?m)^\s*ChatGPT said:', txt)),
        "think": len(re.findall(r'Thought for \d+', txt)),
        "state": len(re.findall(r'(?m)^\s*(STATE:|MUTATION STATUS:|SEM GATE:)', txt)),
        "ui":    len(re.findall(r'(?m)^\s*(pasted|Show more|Edit in a page|Preview)\s*$', txt)),
        "youare":len(re.findall(r'(?i)\bYou are \*?\*?(Mo|Maestro|operating|a )', txt)),
        "auth":  len(re.findall(r'(?m)^#+\s+(I+\.|OPERATING AUTHORITY|System Operating)', txt)),
        "md":    len(re.findall(r'(?m)^#{1,3}\s+\S', txt)),
        "chars": len(txt),
        "lines": txt.count("\n"),
    }

def classify(s):
    if s["you"] >= 3 and s["gpt"] >= 1:
        return "dialogue_chatgpt", "high"
    if s["state"] >= 2:
        return "runtime_session", "medium"
    if s["youare"] >= 2 and (s["auth"] >= 1 or s["md"] >= 8) and s["you"] == 0:
        return "instruction_corpus", "reference"
    if s["think"] >= 10 and s["you"] == 0:
        return "worklog_reasoning", "low"
    if s["md"] >= 6 and s["you"] == 0 and s["gpt"] == 0:
        return "definition_doc", "reference"
    if s["think"] >= 1 or s["state"] >= 1:
        return "runtime_session", "low"
    return "unknown", "low"

ART = {'loss_demonstration_v0_1.md','maestro_month_synthesis_and_rebuild_blueprint_v0_1.md',
       'maestro_v5_ust_sem_interwoven_v0_1.md','song_excellence_governance_v0_1.md',
       'source_lineage_reconciliation_register_v0_1.md','who_dat_runtime_assessment_v0_1.md',
       'maestro_version_changelog.md','open_question_verification_queries_v0_1.md',
       'v5_corrective_regen_prompt_v0_1.md','KERNEL.md'}

if __name__ == "__main__":
    base = "/mnt/project"
    rows = []
    for f in sorted(os.listdir(base)):
        p = os.path.join(base, f)
        if f in ART or not os.path.isfile(p): continue
        if f.endswith(('.yaml','.json','.py')): continue
        txt = open(p, encoding='utf-8', errors='replace').read()
        s = signals(txt)
        typ, conf = classify(s)
        rows.append((f, typ, conf, s))
    order = {"dialogue_chatgpt":0,"runtime_session":1,"worklog_reasoning":2,
             "instruction_corpus":3,"definition_doc":4,"unknown":5}
    rows.sort(key=lambda r: (order.get(r[1],9), -r[3]["chars"]))
    print(f"{'file':<50} {'type':<19} {'conf':<9} {'KB':>5}  signals")
    print("-"*120)
    for f, typ, conf, s in rows:
        sig = " ".join(f"{k}={s[k]}" for k in ("you","gpt","think","state","youare","md") if s[k])
        print(f"{f[:50]:<50} {typ:<19} {conf:<9} {s['chars']//1024:>5}  {sig}")
    # tally what is foldable-as-dialogue vs reference
    fold = [r for r in rows if r[1] in ("dialogue_chatgpt","runtime_session","worklog_reasoning")]
    ref  = [r for r in rows if r[1] in ("instruction_corpus","definition_doc")]
    print(f"\nFOLDABLE (dialogue/runtime/worklog): {len(fold)}   REFERENCE (instruction/definition): {len(ref)}")

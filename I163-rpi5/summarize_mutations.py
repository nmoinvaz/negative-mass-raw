#!/usr/bin/env python3
"""mutations_summary.md for #163 from mut_<name>.log/.rc/.time: the 'control' line of each run (fired, SILENT, outside the section, failed
outside the target list), the exit code and the wall time. usage: summarize_mutations.py [raw folder]"""
import os, re, sys
d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
names = "potential printedW matrix planted xmap units tfactor count domain deltaphi cpath background largex centre scale lelimit lefv".split()
rows = []
for n in names:
    f = os.path.join(d, f"mut_{n}.log")
    if not os.path.exists(f):
        rows.append(f"| `{n}` | (no log) | | | | |"); continue
    txt = open(f).read()
    m = re.search(r"^control (\S+): target \[(.*?)\]: fired \[(.*?)\], SILENT \[(.*?)\].*?not in this section \[(.*?)\]; failed outside the target list \[(.*?)\]", txt, re.M)
    rc = open(os.path.join(d, f"mut_{n}.rc")).read().strip() if os.path.exists(os.path.join(d, f"mut_{n}.rc")) else "?"
    tm = ""
    tf = os.path.join(d, f"mut_{n}.time")
    if os.path.exists(tf):
        mm = re.search(r"Elapsed.*?: (\S+)", open(tf).read()); tm = mm.group(1) if mm else ""
    if not m:
        rows.append(f"| `{n}` | no control line (rc {rc}) | | | | {tm} |"); continue
    clean = lambda s: s.replace("'", "") if s else "none"
    rows.append(f"| `{n}` | {clean(m.group(2))} | {clean(m.group(3))} | {clean(m.group(4))} | {clean(m.group(6))} | rc {rc}, {tm} |")
out = ["| mutation | target | fired | SILENT | failed outside the target list | exit, wall |", "|---|---|---|---|---|---|"] + rows
open(os.path.join(d, "mutations_summary.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))

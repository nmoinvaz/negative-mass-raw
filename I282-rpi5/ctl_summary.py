#!/usr/bin/env python3
"""ctl_summary.py PREFIX [--declared FILE]: reads the logs PREFIX_*.log of the control runs in this folder and prints, for each, the
checks that fire (FAIL) and the checks that stay silent (PASS); the nominal run is PREFIX_cnom.log (or PREFIX_exch_nominal.log).
With --declared FILE (JSON {control: [fired ids]}), it compares the fired sets with the declared targets and prints on target / off target."""
import glob
import json
import os
import re
import sys

d = os.path.dirname(os.path.abspath(__file__))
pre = sys.argv[1]
decl = None
if "--declared" in sys.argv:
    decl = json.load(open(sys.argv[sys.argv.index("--declared") + 1]))
rows = {}
for f in sorted(glob.glob(os.path.join(d, pre + "_*.log"))):
    name = os.path.basename(f)[len(pre) + 1:-4]
    fired, silent = [], []
    for line in open(f):
        m = re.match(r"(PASS|FAIL)\s+(\S+):", line)
        if m:
            (fired if m.group(1) == "FAIL" else silent).append(m.group(2))
    rc = open(f[:-4] + ".rc").read().strip() if os.path.exists(f[:-4] + ".rc") else "?"
    rows[name] = (fired, silent, rc)
nom = {k: v for k, v in rows.items() if k in ("cnom", "nominal")}
for name, (fired, silent, rc) in rows.items():
    base = set(nom.get(name, ([], [], ""))[0])
    extra = [x for x in fired if x not in base]
    line = f"{name:28s} rc {rc}  fires: {', '.join(fired) or '-'}"
    if decl is not None and name in decl:
        ok = sorted(fired) == sorted(decl[name])
        line += f"   declared: {', '.join(decl[name]) or '-'}  -> {'on target' if ok else 'OFF TARGET'}"
    print(line)
    if name not in nom:
        print(f"{'':28s} silent: {', '.join(silent) or '-'}")

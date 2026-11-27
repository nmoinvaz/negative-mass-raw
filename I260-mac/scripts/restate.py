#!/usr/bin/env python3
"""restate.py: list the papers in text/ that restate the [BKZ12] verdict on the horizon-at-the-minimum black universe, by a fixed regex
(printed with context). Usage: python3 scripts/restate.py > restatements.txt"""
import os, re
rx = re.compile(r"(stable[^.]{0,140}(horizon (coincid|at the (minimum|throat))|coincid\w* with the (minimum|throat))"
                r"|(horizon (coincid\w* with|at) the (minimum|throat|sphere of minimum)|minimum of the (areal|area|spherical)[^.]{0,30}coincid)[^.]{0,140}(stable|stability)"
                r"|except for a special class of (black universes|solutions)"
                r"|stable for particular values of the constants|stable only (in|when|for)[^.]{0,80}(minimum|horizon))", re.I)
td = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "text")
n = 0
for f in sorted(os.listdir(td)):
    if not f.endswith(".pypdf.txt"): continue
    t = re.sub(r"\s+", " ", re.sub(r"-\n(?=[a-z])", "", open(os.path.join(td, f), errors="replace").read()))
    ms = list(rx.finditer(t))
    if ms:
        n += 1
        print(f"== {f[:-10]}  ({len(ms)})")
        for m in ms[:3]:
            print("   ...", t[max(0, m.start() - 130): m.end() + 110], "...")
print(n, "papers")

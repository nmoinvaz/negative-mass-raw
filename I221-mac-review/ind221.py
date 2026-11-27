#!/usr/bin/env python3
"""ind221: all 16 rows of growth.csv against w2_output.txt's crate column (criteria in README.md)."""
import argparse
import re
import sys

import mpmath as mp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["row4"])
O = ap.parse_args()
mp.mp.dps = 40
wt = "/Users/nathan/Source/negative-mass-r221/notes/wormhole_largeD"
sec = open(f"{wt}/w2_output.txt").read()
sec = sec[sec.index("growth.csv against the crate"):]
crate = {int(m.group(1)): m.group(2) for m in
         re.finditer(r"^\s+(\d+)\s+(?:TS13 Table I|modes_r\.py)\s+[0-9.]+\s+([0-9.]+)", sec, re.M)}
lines = open(f"{wt}/growth.csv").read().splitlines()
bad, ncol = [], {len(l.split(",")) for l in lines}
for l in lines[1:]:
    D, w, src = l.split(",")
    v = mp.mpf(crate[int(D)]) + (mp.mpf("1e-12") if (O.mutate == "row4" and D == "4") else 0)
    want = mp.nstr(v, len(str(int(v))) + 12, strip_zeros=False)
    if w != want or src != "w2_crate qd (#195)":
        bad.append((D, w, want))
ok = not bad and len(lines) == 17 and ncol == {3}
print(f"[{'PASS' if ok else 'FAIL'}] K1: {len(lines) - 1} rows, columns {ncol}; differing: {bad or 'none'}")
print(f"\n1 criteria, {int(ok)} pass; failed: {[] if ok else ['K1']}")
sys.exit(0 if ok else 1)

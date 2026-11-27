#!/usr/bin/env python3
"""ind200: growth.csv's rows against w2_output.txt, and growth_update.md's remainder column (criteria in README.md)."""
import argparse
import csv
import re
import subprocess
import sys

import mpmath as mp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["row", "omega1"])
ap.add_argument("--wt", default="/Users/nathan/Source/negative-mass-r200/notes/wormhole_largeD")
O = ap.parse_args()
mp.mp.dps = 40
R = []


def check(n, ok, d):
    R.append((n, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}", flush=True)


out = open(f"{O.wt}/w2_output.txt").read()
sec = out[out.index("growth.csv against the crate"):]
crate = {}
for m in re.finditer(r"^\s+(\d+)\s+(TS13 Table I|modes_r)\s+[0-9.]+\s+([0-9.]+)", sec, re.M):
    crate.setdefault(int(m.group(1)), m.group(3))
rows = {int(r["D"]): r for r in csv.DictReader(open(f"{O.wt}/growth.csv"))}
main_csv = subprocess.run(["git", "-C", O.wt, "show", "613e866:notes/wormhole_largeD/growth.csv"], capture_output=True,
                          text=True).stdout
main_rows = {int(r["D"]): r for r in csv.DictReader(main_csv.splitlines())}
bad, notes = [], []
for D in sorted(rows):
    if D >= 20:
        v = mp.mpf(crate[D]) + (mp.mpf("1e-12") if (O.mutate == "row" and D == 500) else 0)
        want = mp.nstr(v, len(str(int(v))) + 12, strip_zeros=False)
        ok = rows[D]["W2a2"] == want and rows[D]["source"] == "w2_crate qd (#195)"
    else:
        ok = rows[D] == main_rows[D]
    if not ok:
        bad.append(D)
    notes.append(f"D={D} {'ok' if ok else 'DIFF ' + rows[D]['W2a2']}")
check("K1", not bad and len(rows) == 16, f"{len(rows)} rows; differing: {bad or 'none'}; crate values parsed for {len(crate)} D")
pi, q2 = mp.pi, mp.log(2)
Om1 = 2 * pi**2 / 3 + 8 * q2**2 + (mp.mpf("1e-6") if O.mutate == "omega1" else 0)
want = {200: "72.63", 500: "73.70", 1000: "74.04", 2000: "74.21"}
res, ok2 = [], True
for D, w in want.items():
    s = 2 * (D - 3)
    x = (mp.mpf(rows[D]["W2a2"]) - (s - 4 * q2 + Om1 / s)) * s**2
    got = mp.nstr(x, len(w) - 1, strip_zeros=False)
    ok2 &= got == w
    res.append(f"D={D} {mp.nstr(x, 8)} (printed {w})")
check("K2", ok2, "; ".join(res))
bad = [n for n, ok in R if not ok]
print(f"\n{len(R)} criteria, {len(R) - len(bad)} pass; failed: {bad}")
sys.exit(1 if bad else 0)

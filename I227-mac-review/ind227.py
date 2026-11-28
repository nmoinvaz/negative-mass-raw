#!/usr/bin/env python3
"""ind227: fate monotonicity, the extension slope and the float64 offsets of #227 from its raw files, in mpmath (criteria in README.md).

    python3 ind227.py OUTPUT [--mutate=side-flip|log10|f64-lo]

OUTPUT is extended_bisect_output.txt of branch wip/i227-extended-bisect. Imports nothing from the repository. Exit 1 when a check fails.
"""
import glob
import json
import os
import re
import sys

import mpmath as mp
import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
OUT = [a for a in sys.argv[1:] if not a.startswith("--")][0]
RUNS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "I227-rpi5", "runs")
mp.mp.dps = 40
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def half(s):
    """Half a unit of the last printed digit of a number in e-notation or fixed notation."""
    mant = s.lstrip("+-").split("e")[0]
    exp = int(s.split("e")[1]) if "e" in s else 0
    dec = len(mant.split(".")[1]) if "." in mant else 0
    return 0.5 * 10.0 ** (exp - dec)


txt = open(OUT).read()
ps, pts = {}, {}
k1 = []
for v in ("E", "F"):
    b = json.load(open(os.path.join(RUNS, v, "bisect.json")))
    ps[v] = (mp.mpf(b["lo"]) + mp.mpf(b["hi"])) / 2
    rows = []
    for f in ("series_p_3_20.jsonl", "series_m_3_20.jsonl"):
        rows += [json.loads(line) for line in open(os.path.join(RUNS, v, f)) if line.strip()]
    rows = [r for r in rows if r.get("phase", "series") == "series"]
    pts[v] = rows
    sgn = -1 if MUT == "side-flip" else 1
    good = sum(1 for r in rows if r["fate"] == r["side"] and mp.sign(mp.mpf(r["A"]) - ps[v]) == sgn * r["side"])
    k1.append((v, good, len(rows)))
    print(f"  {v}: p*_h = {mp.nstr(ps[v], 22)}, hi - lo = {mp.nstr(mp.mpf(b['hi']) - mp.mpf(b['lo']), 3)}; {good} of {len(rows)} on their side")
check("K1", all(g == n == 70 for _, g, n in k1), ", ".join(f"{v}: {g} of {n}" for v, g, n in k1))

ll1 = {v: re.search(rf"LL1-{v}: .*?\(([0-9.]+) \+- [0-9.]+ \(OLS\).*?n = (\d+)\)", txt).groups() for v in ("E", "F")}
k2 = []
for v in ("E", "F"):
    sel = []
    for r in pts[v]:
        d = abs(mp.mpf(r["A"]) - ps[v])
        if r["fate"] == r["side"] and mp.mpf("1e-20") * (1 - mp.mpf("1e-6")) <= d <= mp.mpf("1e-12") * (1 + mp.mpf("1e-6")):
            x = float(mp.log10(1 / d)) if MUT == "log10" else float(mp.log(1 / d))
            sel.append((r["side"], x, r["T"]))
    sxy = sxx = 0.0
    for sd in (-1, 1):
        x = np.array([s[1] for s in sel if s[0] == sd]); y = np.array([s[2] for s in sel if s[0] == sd])
        sxy += float(((x - x.mean()) * (y - y.mean())).sum()); sxx += float(((x - x.mean()) ** 2).sum())
    s = sxy / sxx
    k2.append((v, s, len(sel)))
    print(f"  {v}: slope over [1e-20, 1e-12] {s:.6f} (n = {len(sel)}); output LL1 {ll1[v][0]} (n = {ll1[v][1]})")
check("K2", all(abs(s - float(ll1[v][0])) <= 1e-6 and n == int(ll1[v][1]) for v, s, n in k2),
      ", ".join(f"{v}: {s:.6f} against {ll1[v][0]}" for v, s, n in k2) + " (bar 1e-6)")

fs = sorted(glob.glob(os.path.join(RUNS, "f64", "f64_bisect_k*.json")))
p64 = [mp.mpf(json.load(open(f))["lo" if MUT == "f64-lo" else "pstar"]) for f in fs]
ok3 = True
for v in ("E", "F"):
    dev = [x - ps[v] for x in p64]
    mean = sum(dev) / len(dev)
    rms = mp.sqrt(sum(d * d for d in dev) / len(dev))
    mx = max(abs(d) for d in dev)
    pm, pr, px, pk = re.search(rf"A2-{v}: .*?mean ([-+0-9.e]+), rms ([0-9.e-]+), sd [0-9.e-]+, max ([0-9.e-]+), K = (\d+)\)", txt).groups()
    ok = (abs(mean - mp.mpf(pm)) <= half(pm) and abs(rms - mp.mpf(pr)) <= half(pr) and abs(mx - mp.mpf(px)) <= half(px) and len(dev) == int(pk))
    ok3 &= ok
    print(f"  {v}: float64 - binary128 mean {mp.nstr(mean, 6)}, rms {mp.nstr(rms, 6)}, max {mp.nstr(mx, 6)}, K = {len(dev)}; output {pm}, {pr}, {px}, K = {pk} {'ok' if ok else 'OFF'}")
check("K3", ok3, "float64 offsets equal the output's A2 lines to half a unit of the printed digit")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

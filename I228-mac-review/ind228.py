#!/usr/bin/env python3
"""ind228: p*_h order, diagonal slope and drift speed of G at D = 6 from #228's raw files (criteria in README.md beside this file).

    python3 ind228.py [--mutate=order1|no-sides|collapse-only|t-not-tau]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R40 = os.path.join(RAW, "I228-dh610", "runs40")
HS = (0.005, 0.0025, 0.00125)
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


# K1: p*_h, its order, Richardson, and #246's bracket
summ = {h: json.load(open(os.path.join(R40, f"D6_G_h{h:g}", "summary.json"))) for h in HS}
ps = [0.5 * (summ[h]["lo"] + summ[h]["hi"]) for h in HS]
order = math.log2((ps[0] - ps[1]) / (ps[1] - ps[2]))
q = 1.0 if MUT == "order1" else order                                    # A1: observed order, as threshold.py l. 571
rich = ps[2] + (ps[2] - ps[1]) / (2 ** q - 1)
print(f"  fixed-order (q = 2) Richardson p* = {ps[2] + (ps[2] - ps[1]) / 3:.7e} (reported)")
b246 = json.load(open(os.path.join(RAW, "I246-dh610", "runs", "pstar_D6_G_k2.json")))
same = summ[0.00125]["lo"] == b246["lo"] and summ[0.00125]["hi"] == b246["hi"]
print("  p*_h = " + ", ".join(f"{p:.7e}" for p in ps) + f"; hi - lo at 0.00125 = {summ[0.00125]['hi'] - summ[0.00125]['lo']:.2e}")
check("K1", 1.75 <= order <= 2.25 and abs(order - 2.005) <= 0.005 and abs(rich - 1.0567197e-2) <= 1e-9 and same,
      f"order {order:.4f} (note 2.005), observed-order Richardson p* {rich:.7e} (note 1.0567197e-2, bar 1e-9), bracket equal to #246's {same}")


# K2: T = c_side + s ln(1/delta), one intercept per side, by within-side demeaning
def slope(points, pstar):
    rows = [(p["side"], math.log(1.0 / abs(p["A"] - pstar)), p["T"]) for p in points
            if p.get("phase") == "series" and p["T"] is not None and p["fate"] == p["side"]
            and 1e-11 * (1 - 1e-6) <= abs(p["A"] - pstar) <= 1e-3 * (1 + 1e-6)]
    if MUT == "collapse-only":
        rows = [r for r in rows if r[0] == -1]
    if MUT == "no-sides":                                                # A2: cannot fire, both sides share the delta grid
        rows = [(0, x, y) for _, x, y in rows]
    sxy = sxx = 0.0
    for sd in {r[0] for r in rows}:
        x = np.array([r[1] for r in rows if r[0] == sd])
        y = np.array([r[2] for r in rows if r[0] == sd])
        sxy += float(((x - x.mean()) * (y - y.mean())).sum())
        sxx += float(((x - x.mean()) ** 2).sum())
    return sxy / sxx, len(rows)


NOTE_S = (0.990046, 0.994756, 0.996251)
sl = []
for h, p, ns in zip(HS, ps, NOTE_S):
    pts = [json.loads(line) for line in open(os.path.join(R40, f"D6_G_h{h:g}", "points.jsonl"))]
    s, n = slope(pts, p)
    sl.append(s)
    print(f"  h = {h:g}: slope {s:.6f} over {n} points (note {ns:.6f}, difference {s - ns:+.1e})")
ra = abs(sl[2] / sl[1] - 1)
check("K2", all(abs(s - ns) <= 1e-6 for s, ns in zip(sl, NOTE_S)) and ra <= 5e-3,
      f"worst {max(abs(s - ns) for s, ns in zip(sl, NOTE_S)):.1e} (bar 1e-6); finest two differ by {ra:.2e} (bar 5e-3)")

# K3: drift speed at B = 0.1, h = 0.00125 from the pair p*_h -/+ 1e-10
zs = [np.load(os.path.join(RAW, "I228-dh610", "runs", "stall_drift", f"stall_D6_B0.1_h0.00125_d1e-10_side{s}.npz")) for s in (-1, 1)]
com = np.intersect1d(zs[0]["s"], zs[1]["s"])
idx = [np.searchsorted(z["s"], com) for z in zs]
t = 0.5 * (zs[0]["t"][idx[0]] + zs[1]["t"][idx[1]])
tau = 0.5 * (zs[0]["tau"][idx[0]] + zs[1]["tau"][idx[1]])
r = 0.5 * (zs[0]["r"][idx[0]] + zs[1]["r"][idx[1]])
x = t if MUT == "t-not-tau" else tau
NOTE_V = (0.09382, 0.08723, 0.07901)
NOTE_R = (0.35006, 0.51492, 0.66809)
dv, dr = [], []
for tq, nv, nr in zip((8.0, 10.0, 12.0), NOTE_V, NOTE_R):
    xq = float(np.interp(tq, t, x))
    sel = np.abs(x - xq) <= 0.5
    v = np.polyfit(x[sel] - xq, r[sel], 1)[0]
    rq = float(np.interp(tq, t, r)) - 1
    dv.append(abs(v - nv))
    dr.append(abs(rq - nr))
    print(f"  t = {tq:g}: tau {np.interp(tq, t, tau):.3f}, r_th - 1 = {rq:.5f} (note {nr:.5f}), rdot {v:.5f} (note {nv:.5f}) over {sel.sum()} slices")
check("K3", max(dv) <= 5e-4 and max(dr) <= 1e-4, f"rdot worst {max(dv):.1e} (bar 5e-4); r_th - 1 worst {max(dr):.1e} (bar 1e-4)")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

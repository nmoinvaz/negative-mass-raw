#!/usr/bin/env python3
"""ind267: an independent reading of #267's raw runs (criteria in README.md beside this file).

    python3 ind267.py [--mutate=eps-1e-2|b-scale|plat-half|rth-side]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R267 = os.path.join(RAW, "I267-mac", "runs", "G_B0.1", "h0.005")
R266 = os.path.join(RAW, "I266-mac", "runs")
EPS = 1e-2 if MUT == "eps-1e-2" else 1e-3
WIN = 0.5 if MUT == "plat-half" else 1.0
RKEY = "r_th_a" if MUT == "rth-side" else "r_th"
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def t_departure(loc):
    sa, sb = loc["s_a"], loc["s_b"]
    common = sorted(set(sa.tolist()) & set(sb.tolist()))
    ia = {s: i for i, s in enumerate(sa.tolist())}
    ib = {s: i for i, s in enumerate(sb.tolist())}
    t = np.array([loc["t_a"][ia[s]] for s in common])
    ra = np.array([loc["r_a"][ia[s]] for s in common])
    rb = np.array([loc["r_b"][ib[s]] for s in common])
    q = np.abs(rb - ra) / (ra + rb)          # |odd| / mean = |rb - ra| / 2 / ((ra + rb) / 2)
    for k in range(len(t)):
        if t[k] >= 6.0 and q[k] >= EPS:
            if k == 0 or t[k - 1] < 6.0:
                return float(t[k])
            return float(t[k - 1] + (EPS - q[k - 1]) / (q[k] - q[k - 1]) * (t[k] - t[k - 1]))
    return float("nan")


def member(d):
    loc = np.load(os.path.join(d, "member", "locus.npz"))
    rows = json.load(open(os.path.join(d, "member", "member.json")))["rows"]
    td = t_departure(loc)
    for r0, r1 in zip(rows, rows[1:]):
        if r0["t"] <= td <= r1["t"]:
            w = (td - r0["t"]) / (r1["t"] - r0["t"])
            rth = r0[RKEY] + w * (r1[RKEY] - r0[RKEY])
            s = r0["s_m"] + w * (r1["s_m"] - r0["s_m"])
            return td, rth, s / math.sqrt(1 - s * s)
    raise RuntimeError(f"t_dep {td} outside the slices of {d}")


def plateau(d):
    z = np.load(os.path.join(d, "chain", "series.npz"))
    xp, M = z["xp"], z["M"]
    sel = xp >= xp.max() - WIN
    return float(M[sel].mean())


# the note's table (h = 0.005): delta exponent -> t_dep, r_th, gamma_1, M, M - predicted
NOTE = {7: (11.610, 1.003370, 0.048511, 0.235198, -5.21e-4), 8: (13.615, 1.002878, 0.048316, 0.235548, 5e-7),
        9: (15.618, 1.003477, 0.048159, 0.235991, 3.48e-4), 10: (17.624, 1.004787, 0.048013, 0.236497, 5.87e-4),
        11: (19.628, 1.006583, 0.047870, 0.237051, 7.61e-4), 12: (21.613, 1.008642, 0.047732, 0.237622, 8.88e-4)}

# K2: #266's relation from its four B
M0 = plateau(os.path.join(R266, "O", "h0.005"))
pts = []
for B in ("0.025", "0.05", "0.1", "0.125"):
    d = os.path.join(R266, f"G_B{B}", "h0.005")
    _, rth, g1 = member(d)
    pts.append((g1, rth, plateau(d)))
A = np.array([[g, g * g] for g, _, _ in pts])
y = np.array([M / r - M0 for g, r, M in pts])
(a, b), *_ = np.linalg.lstsq(A, y, rcond=None)
print(f"  #266's four B: " + ", ".join(f"(g1 {g:.6f}, r_th {r:.6f}, M {M:.6f})" for g, r, M in pts))
check("K2", abs(a - 0.2027) <= 1e-3 and abs(b - 0.8534) <= 1e-2 and abs(M0 - 0.223086) <= 2e-6,
      f"a = {a:.5f}, b = {b:.4f}, M0 = {M0:.6f} (note: 0.2027, 0.8534, 0.223086)")
if MUT == "b-scale":
    b *= 1.05

# K1, K3: the six delta
rows, w1, w3 = {}, [], []
for e in sorted(NOTE):
    d = os.path.join(R267, f"e{e}")
    td, rth, g1 = member(d)
    M = plateau(d)
    pred = rth * (M0 + a * g1 + b * g1 * g1)
    rows[e] = (td, rth, g1, M, pred)
    n = NOTE[e]
    w1.append((abs(td - n[0]), abs(rth - n[1]), abs(g1 - n[2]), abs(M - n[3])))
    w3.append(abs((M - pred) - n[4]))
    print(f"  delta 1e-{e}: t_dep {td:.3f}, r_th {rth:.6f}, g1 {g1:.6f}, M {M:.6f}, predicted {pred:.6f}, M - predicted {M - pred:+.3e}"
          f"  (note {n[4]:+.2e})")
W1 = np.max(np.array(w1), axis=0)
check("K1", W1[0] <= 1e-3 and W1[1] <= 1e-6 and W1[2] <= 1e-5 and W1[3] <= 2e-6,
      f"largest differences from the note's table: t_dep {W1[0]:.1e}, r_th {W1[1]:.1e}, g1 {W1[2]:.1e}, M {W1[3]:.1e} (bars 1e-3, 1e-6, 1e-5, 2e-6)")
worst_late = max(abs(rows[e][3] - rows[e][4]) for e in (9, 10, 11, 12))
check("K3", max(w3) <= 1e-5 and worst_late > 6e-5,
      f"M - predicted against the note's column: worst {max(w3):.1e} (bar 1e-5); largest |M - predicted| at 1e-9 ... 1e-12 {worst_late:.2e} (> 6e-5: PRED not met)")

# K4: the rise from 1e-8 to 1e-12
dM = rows[12][3] - rows[8][3]
dP = rows[12][4] - rows[8][4]
check("K4", abs(dM - 2.074e-3) <= 1e-5 and abs(dP - 1.186e-3) <= 2e-5, f"dM {dM:+.4e} (note +2.074e-3), predicted {dP:+.4e} (note +1.186e-3)")

# K5: the excess between neighbouring decades
exc = []
for e in range(7, 12):
    _, r0, _, M0e, _ = rows[e]
    _, r1, _, M1e, _ = rows[e + 1]
    exc.append((M1e - M0e) - (M0e / r0) * (r1 - r0))
ratios = [exc[k + 1] / exc[k] for k in range(len(exc) - 1)]
want = (0.649, 0.653, 0.669, 0.650)
check("K5", all(abs(r - w) <= 0.02 for r, w in zip(ratios, want)),
      "excess " + ", ".join(f"{x:+.3e}" for x in exc) + "; ratios " + ", ".join(f"{r:.3f}" for r in ratios) + " (note 0.649, 0.653, 0.669, 0.650)")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

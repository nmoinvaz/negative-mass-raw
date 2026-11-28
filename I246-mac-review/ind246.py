#!/usr/bin/env python3
"""ind246: the settled threshold mass at D = 5, 6 from #246's raw series (criteria in README.md beside this file).

    python3 ind246.py [--mutate=last-half|order1|ball]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RUNS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "I246-dh610", "runs")
WIN = 0.5 if MUT == "last-half" else 1.0
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def series(tag):
    return np.load(os.path.join(RUNS, tag, "series.npz"))


def plateau(tag):
    z = series(tag)
    return float(z["M"][z["xp"] >= z["xp"].max() - WIN].mean())


def vball(k):
    return math.pi ** (k / 2) / math.gamma(k / 2 + (0 if MUT == "ball" else 1))


P = {}
for D in (5, 6):
    for fam in ("S", "G"):
        for d in ("1e-8", "1e-6"):
            P[(D, fam, d)] = [plateau(f"D{D}_{fam}_k{k}_d{d}") for k in range(3)]
print("  case            k0          k1          k2          Richardson   order")
RICH, ORD = {}, {}
for key, (m0, m1, m2) in sorted(P.items()):
    rich = 2 * m2 - m1 if MUT == "order1" else (4 * m2 - m1) / 3
    order = math.log2((m0 - m1) / (m1 - m2)) if (m1 - m2) != 0 and (m0 - m1) / (m1 - m2) > 0 else float("nan")
    RICH[key], ORD[key] = rich, order
    print(f"  D{key[0]} {key[1]} {key[2]:5s}   {m0:.7f}   {m1:.7f}   {m2:.7f}   {rich:.7f}    {order:.2f}")

NOTE1 = {(5, "S", "1e-8"): 0.145859, (5, "G", "1e-8"): 0.263924, (6, "S", "1e-8"): 0.107793, (6, "G", "1e-8"): 0.862180,
         (5, "G", "1e-6"): 0.234978, (6, "G", "1e-6"): 0.567448}
w1 = max(abs(P[k][2] - v) for k, v in NOTE1.items())
check("K1", w1 <= 2e-6, f"finest-h plateaus against the note's six: worst {w1:.1e} (bar 2e-6)")

NOTE2 = {(5, "S", "1e-8"): 0.145866, (5, "G", "1e-8"): 0.263951, (6, "S", "1e-8"): 0.107920, (6, "G", "1e-8"): 0.862862}
w2 = max(abs(RICH[k] - v) for k, v in NOTE2.items())
oS = [ORD[(5, "S", "1e-8")], ORD[(6, "S", "1e-8")]]
check("K2", w2 <= 5e-6 and all(1.5 <= o <= 2.5 for o in oS), f"Richardson against the note's four: worst {w2:.1e} (bar 5e-6); S orders {oS[0]:.2f}, {oS[1]:.2f}")

ratio = {}
for D in (5, 6):
    n = D - 2
    cD = n * vball(n)
    ratio[D] = cD * RICH[(D, "S", "1e-8")] / (cD * 0.5)
check("K3", f"{ratio[5]:.4f}" == "0.2917" and f"{ratio[6]:.4f}" == "0.2158", f"E/E_throat = {ratio[5]:.4f} (D = 5), {ratio[6]:.4f} (D = 6); the note: 0.2917, 0.2158")

pref = []
for D in (5, 6):
    for fam in ("S", "G"):
        base = f"D{D}_{fam}_k0_d1e-8"
        if not os.path.isdir(os.path.join(RUNS, base + "_K20")):
            continue
        z = series(base)
        for K in ("K20", "K24"):
            p = series(f"{base}_{K}")
            n = len(p["M"])
            same = n <= len(z["M"]) and all(np.array_equal(p[k], z[k][:n]) for k in p.files if k in z.files)
            pref.append((f"{base}_{K}", n, len(z["M"]), same))
for t, n, nz, s in pref:
    print(f"  prefix {t}: {n} of {nz} cells, bit-identical {s}")
check("K4", len(pref) >= 4 and all(p[3] for p in pref), f"{sum(p[3] for p in pref)} of {len(pref)} prefix series bit-identical")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

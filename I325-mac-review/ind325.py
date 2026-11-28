#!/usr/bin/env python3
"""ind325: local exponents of the D = 6 throat speed rdot(8) over nine B from the raw pairs (criteria in README.md).

    python3 ind325.py [--mutate=t-not-tau|h-coarse]

Imports nothing from the repository; the reader is ind228's K3. Exit 1 when a check fails.
"""
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []
BS = (0.01, 0.014, 0.02, 0.03, 0.04, 0.07, 0.1, 0.15, 0.2)


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def path(B, h, s):
    f = f"stall_D6_B{B:g}_h{h:g}_d1e-10_side{s}.npz"
    for d in ("I325-dh610", "I228-dh610"):
        p = os.path.join(RAW, d, "runs", "stall_drift", f)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f)


def rdot8(B, h):
    zs = [np.load(path(B, h, s)) for s in (-1, 1)]
    com = np.intersect1d(zs[0]["s"], zs[1]["s"])
    idx = [np.searchsorted(z["s"], com) for z in zs]
    t = 0.5 * (zs[0]["t"][idx[0]] + zs[1]["t"][idx[1]])
    tau = 0.5 * (zs[0]["tau"][idx[0]] + zs[1]["tau"][idx[1]])
    r = 0.5 * (zs[0]["r"][idx[0]] + zs[1]["r"][idx[1]])
    x = t if MUT == "t-not-tau" else tau
    xq = float(np.interp(8.0, t, x))
    sel = np.abs(x - xq) <= 0.5
    return float(np.polyfit(x[sel] - xq, r[sel], 1)[0])


def hfin(B1, B2):
    return 0.0025 if (MUT == "h-coarse" or max(B1, B2) > 0.1) else 0.00125


NOTE = (2.250, 2.272, 2.415, 2.617, 2.724, 2.220, 1.365, 0.757)
al = []
for (B1, B2), na in zip(zip(BS, BS[1:]), NOTE):
    h = hfin(B1, B2)
    v1, v2 = rdot8(B1, h), rdot8(B2, h)
    a = math.log(v2 / v1) / math.log(B2 / B1)
    al.append(a)
    print(f"  {B1:g} -> {B2:g} (h = {h:g}): rdot(8) {v1:.6f}, {v2:.6f}; alpha {a:.3f} (#325 {na})")
check("K1", all(abs(a - n) <= 0.01 for a, n in zip(al, NOTE)), f"worst |alpha - #325| {max(abs(a - n) for a, n in zip(al, NOTE)):.3f} (bar 0.01)")
sat = [rdot8(0.1, 0.00125), rdot8(0.15, 0.0025), rdot8(0.2, 0.0025)]
check("K2", all(abs(s - n) <= 1e-3 for s, n in zip(sat, (0.094, 0.163, 0.203))), "rdot(8) at B = 0.1, 0.15, 0.2: " + ", ".join(f"{s:.4f}" for s in sat))
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

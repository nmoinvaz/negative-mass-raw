#!/usr/bin/env python3
"""ind318: the second-order part of the reading at seven members against B = 0's, from #318's raw pairs (criteria in README.md).

    python3 ind318.py [--mutate=swap|same-eps]

Imports nothing from the repository; the reader is that of I317-mac-review/ind317.py. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def pair(loc):
    sa, sb = loc["s_a"].tolist(), loc["s_b"].tolist()
    ia, ib = {s: i for i, s in enumerate(sa)}, {s: i for i, s in enumerate(sb)}
    com = sorted(set(sa) & set(sb))
    A = np.array([ia[s] for s in com]); B = np.array([ib[s] for s in com])
    t = 0.5 * (loc["t_a"][A] + loc["t_b"][B])
    tau = 0.5 * (loc["tau_a"][A] + loc["tau_b"][B])
    r = 0.5 * (loc["r_a"][A] + loc["r_b"][B])
    q = np.abs(loc["r_b"][B] - loc["r_a"][A]) / (loc["r_a"][A] + loc["r_b"][B])
    return t, tau, r, q


def read(d, eps):
    loc = np.load(os.path.join(d, "member", "locus.npz"))
    rows = json.load(open(os.path.join(d, "member", "member.json")))["rows"]
    t, tau, r, q = pair(loc)
    td = float("nan")
    for k in range(len(t)):
        if t[k] >= 6.0 and q[k] >= eps:
            td = float(t[k]) if (k == 0 or t[k - 1] < 6.0) else float(t[k - 1] + (eps - q[k - 1]) / (q[k] - q[k - 1]) * (t[k] - t[k - 1]))
            break
    for r0, r1 in zip(rows, rows[1:]):
        if r0["t"] <= td <= r1["t"]:
            w = (td - r0["t"]) / (r1["t"] - r0["t"])
            rth = r0["r_th"] + w * (r1["r_th"] - r0["r_th"])
            break
    tau_d = float(np.interp(td, t, tau))
    sel = np.abs(tau - tau_d) <= 0.5
    c2, c1, _ = np.polyfit(tau[sel] - tau_d, r[sel], 2)
    return dict(td=td, rth=rth, rdot=float(c1))


E2, E3 = 1e-2, (1e-2 if MUT == "same-eps" else 1e-3)
STORED = {"X1": ("I305-mac", "R_B0.09112_xc4_w1.5"), "X2": ("I305-mac", "R_B0.1695_xc4_w1.5"), "X3": ("I305-mac", "R_B0.2044_xc4_w1.5"),
          "W3": ("I283-mac", "R_B0.1909_xc3_w1"), "C3": ("I283-mac", "R_B0.09576_xc4_w0.5"), "N3": ("I295-mac", "R_B0.136_xc3.5_w0.75"),
          "B0.125": ("I266-mac", "G_B0.125")}
NOTE_V = {"X1": 1.002, "X2": 1.006, "X3": 1.009, "W3": 1.009, "C3": 1.002, "N3": 1.005, "B0.125": 1.003}
NOTE_RA = {"X1": 0.954, "X2": 0.960, "X3": 0.891, "W3": 0.965, "C3": 0.905, "N3": 0.920, "B0.125": 0.920}
b0d = os.path.join(RAW, "I266-mac", "runs", "G_B0", "h0.005")
b2, b3 = read(b0d, 1e-2), read(b0d, 1e-3)
db_r, db_v = b2["rth"] - b3["rth"], b2["rdot"] - b3["rdot"]
print(f"  B = 0: r_th part {db_r:+.4e}, rdot_th part {db_v:+.4e} (reading at 1e-2 minus at 1e-3)")
dt, dv, dr = [], [], []
for k, (raw, f) in STORED.items():
    a = read(os.path.join(RAW, raw, "runs", f, "h0.005"), E2)
    b = read(os.path.join(RAW, "I318-mac", "runs", k, "h0.005", "e9"), E3)
    rv = (a["rdot"] - b["rdot"]) / db_v
    rr = (a["rth"] - b["rth"]) / (db_v if MUT == "swap" else db_r)
    dt.append(abs(a["td"] - b["td"])); dv.append((k, rv)); dr.append((k, rr))
    print(f"  {k:7s}: t_dep {a['td']:.4f} (e8, 1e-2) {b['td']:.4f} (e9, 1e-3); rho_rdot {rv:.4f} (#318 {NOTE_V[k]}), rho_r {rr:.4f} (#318 A {NOTE_RA[k]})")
check("K0", max(dt) <= 0.01, f"same moment: worst |dt_dep| {max(dt):.2e} (bar 0.01)")
check("K1", all(abs(v - NOTE_V[k]) <= 0.02 for k, v in dv) and all(v < 1.1 for k, v in dv if k.startswith("X")),
      f"rho_rdot within 0.02 of #318's: worst {max(abs(v - NOTE_V[k]) for k, v in dv):.3f}; at X1-X3 " + ", ".join(f"{v:.3f}" for k, v in dv if k.startswith("X")) + " (needed 1.19, 1.41, 1.44)")
check("K2", all(abs(v - NOTE_RA[k]) <= 0.02 for k, v in dr), f"rho_r within 0.02 of #318's reader A: worst {max(abs(v - NOTE_RA[k]) for k, v in dr):.3f}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

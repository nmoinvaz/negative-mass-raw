#!/usr/bin/env python3
"""ind283: an independent reading of #283's six route points (criteria in README.md beside this file).

    python3 ind283.py [--mutate=eps-1e-2|no-speed|swap]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPS = 1e-2 if MUT == "eps-1e-2" else 1e-3
P3C = (0.2300, 0.2724, 0.0 if MUT == "no-speed" else 0.7835)
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


def read(d):
    loc = np.load(os.path.join(d, "member", "locus.npz"))
    rows = json.load(open(os.path.join(d, "member", "member.json")))["rows"]
    t, tau, r, q = pair(loc)
    td = float("nan")
    for k in range(len(t)):
        if t[k] >= 6.0 and q[k] >= EPS:
            td = float(t[k]) if (k == 0 or t[k - 1] < 6.0) else float(t[k - 1] + (EPS - q[k - 1]) / (q[k] - q[k - 1]) * (t[k] - t[k - 1]))
            break
    for r0, r1 in zip(rows, rows[1:]):
        if r0["t"] <= td <= r1["t"]:
            w = (td - r0["t"]) / (r1["t"] - r0["t"])
            rth = r0["r_th"] + w * (r1["r_th"] - r0["r_th"])
            s = r0["s_m"] + w * (r1["s_m"] - r0["s_m"])
            break
    g1 = s / math.sqrt(1 - s * s)
    tau_d = float(np.interp(td, t, tau))
    sel = np.abs(tau - tau_d) <= 0.5
    c2, c1, _ = np.polyfit(tau[sel] - tau_d, r[sel], 2)
    z = np.load(os.path.join(d, "chain", "series.npz"))
    M = float(z["M"][z["xp"] >= z["xp"].max() - 1.0].mean())
    return dict(td=td, g1=g1, rth=rth, rdot=float(c1), M=M)


I266 = os.path.join(RAW, "I266-mac", "runs")
fam = {0.0: read(os.path.join(I266, "O", "h0.005"))}
for B in (0.025, 0.05, 0.1, 0.125):
    fam[B] = read(os.path.join(I266, f"G_B{B:g}", "h0.005"))
M0 = fam[0.0]["M"]
G = np.array([fam[B]["g1"] for B in (0.025, 0.05, 0.1, 0.125)])
Y = np.array([fam[B]["M"] / fam[B]["rth"] - M0 for B in (0.025, 0.05, 0.1, 0.125)])
(a2, b2), *_ = np.linalg.lstsq(np.stack([G, G * G], 1), Y, rcond=None)
print(f"  P2: M0 {M0:.6f}, (a, b) = ({a2:.5f}, {b2:.5f}); P3: {P3C}")

R283 = os.path.join(RAW, "I283-mac", "runs")
PTS = {"W1": "R_B0.07905_xc3_w1", "W2": "R_B0.1543_xc3_w1", "W3": "R_B0.1909_xc3_w1",
       "C1": "R_B0.0393_xc4_w0.5", "C2": "R_B0.07726_xc4_w0.5", "C3": "R_B0.09576_xc4_w0.5"}
if MUT == "swap":
    PTS = {k: PTS[{"W1": "C1", "W2": "C2", "W3": "C3", "C1": "W1", "C2": "W2", "C3": "W3"}[k]] for k in PTS}
NOTE = {  # t_dep, gamma_1, r_th, rdot, M, M - P2, M - P3, SEP r_th
    "W1": (13.348, 0.012003, 0.994956, -5.05e-4, 0.224367, -1.37e-4, +1.41e-5, -3.4e-3),
    "W2": (13.568, 0.047982, 0.989179, -6.65e-4, 0.231740, -4.96e-4, +4.72e-5, -1.4e-2),
    "W3": (13.776, 0.075022, 0.993634, +4.99e-4, 0.240794, -7.55e-4, +7.11e-5, -2.2e-2),
    "C1": (13.365, 0.011989, 0.999623, -3.89e-4, 0.225489, -6.46e-5, -3.81e-6, +1.3e-3),
    "C2": (13.640, 0.048006, 1.006321, -2.92e-4, 0.235995, -2.72e-4, -1.36e-5, +3.5e-3),
    "C3": (13.891, 0.074833, 1.019366, +9.95e-4, 0.247278, -4.62e-4, -2.24e-5, +3.8e-3),
}
gB = np.array([fam[B]["g1"] for B in (0.0, 0.025, 0.05, 0.1, 0.125)])
rB = np.array([fam[B]["rth"] for B in (0.0, 0.025, 0.05, 0.1, 0.125)])
o = np.argsort(gB)
w1 = [0, 0, 0, 0]; w2 = 0.0; w3 = [0.0, 0.0]; p2size = []; sep_ok = []
print("  pt   t_dep    gamma_1   r_th      rdot        M         M-P2       M-P3       SEP r_th")
for k, f in PTS.items():
    v = read(os.path.join(R283, f, "h0.005"))
    n = NOTE[k]
    p2 = v["rth"] * (M0 + a2 * v["g1"] + b2 * v["g1"] ** 2)
    p3 = v["rth"] * (M0 + P3C[0] * v["g1"] + P3C[1] * v["g1"] ** 2 + P3C[2] * v["rdot"])
    sep = v["rth"] - float(np.interp(v["g1"], gB[o], rB[o]))
    print(f"  {k}   {v['td']:.3f}  {v['g1']:.6f}  {v['rth']:.6f}  {v['rdot']:+.4e}  {v['M']:.6f}  {v['M'] - p2:+.3e}  {v['M'] - p3:+.3e}  {sep:+.2e}")
    w1 = [max(w1[0], abs(v["td"] - n[0])), max(w1[1], abs(v["g1"] - n[1])), max(w1[2], abs(v["rth"] - n[2])), max(w1[3], abs(v["M"] - n[4]))]
    w2 = max(w2, abs((v["M"] - p2) - n[5]))
    p2size.append(abs(v["M"] - p2))
    w3 = [max(w3[0], abs(v["rdot"] - n[3])), max(w3[1], abs((v["M"] - p3) - n[6]))]
    if k == "W3":
        w3res = v["M"] - p3
    sep_ok.append(np.sign(sep) == np.sign(n[7]) and abs(sep / n[7] - 1) <= 0.15)

check("K1", w1[0] <= 1e-3 and w1[1] <= 1e-5 and w1[2] <= 1e-6 and w1[3] <= 2e-6,
      f"against the note: t_dep {w1[0]:.1e}, gamma_1 {w1[1]:.1e}, r_th {w1[2]:.1e}, M {w1[3]:.1e} (bars 1e-3, 1e-5, 1e-6, 2e-6)")
check("K2", w2 <= 3e-6 and min(p2size) > 6e-5, f"M - P2 within {w2:.1e} of the note's (bar 3e-6); smallest |M - P2| {min(p2size):.2e} (> 6e-5: P2 fails at all six)")
check("K3", w3[0] <= 3e-6 and w3[1] <= 5e-6, f"rdot_th within {w3[0]:.1e} (bar 3e-6); M - P3 within {w3[1]:.1e} (bar 5e-6). "
      f"W3 with this estimator: M - P3 = {w3res:+.3e} ({'exceeds' if abs(w3res) > 6e-5 else 'within'} 6e-5)")
check("K4", all(sep_ok), f"SEP sign and size within 15 % at {sum(sep_ok)} of 6")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

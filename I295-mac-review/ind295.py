#!/usr/bin/env python3
"""ind295: the fifteen-point refit and the third route with the coordinator's own readings (criteria in README.md beside this file).

    python3 ind295.py [--mutate=no-speed|drop-routes]

Imports nothing from the repository; the reader is copied from ind283.py. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPS = 1e-3
M0 = 0.223086
FROZEN = (0.2296318924, 0.2834170383, 0.7657657062)
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



P = {}
for B in (0.025, 0.05, 0.1, 0.125):
    P[f"B{B:g}"] = read(os.path.join(RAW, "I266-mac", "runs", f"G_B{B:g}", "h0.005"))
for e in (7, 9, 10, 11, 12):
    P[f"d{e}"] = read(os.path.join(RAW, "I267-mac", "runs", "G_B0.1", "h0.005", f"e{e}"))
if MUT != "drop-routes":
    for k, f in {"W1": "R_B0.07905_xc3_w1", "W2": "R_B0.1543_xc3_w1", "W3": "R_B0.1909_xc3_w1",
                 "C1": "R_B0.0393_xc4_w0.5", "C2": "R_B0.07726_xc4_w0.5", "C3": "R_B0.09576_xc4_w0.5"}.items():
        P[k] = read(os.path.join(RAW, "I283-mac", "runs", f, "h0.005"))
NEW = {"N1": "R_B0.05648_xc3.5_w0.75", "N2": "R_B0.1101_xc3.5_w0.75", "N3": "R_B0.136_xc3.5_w0.75"}
NOTE = {"N1": -4.77e-07, "N2": -2.15e-06, "N3": +1.21e-06}
Q = {k: read(os.path.join(RAW, "I295-mac", "runs", f, "h0.005")) for k, f in NEW.items()}

X = np.array([[v["g1"], v["g1"] ** 2, v["rdot"]] for v in P.values()])
Y = np.array([v["M"] / v["rth"] - M0 for v in P.values()])
own, *_ = np.linalg.lstsq(X, Y, rcond=None)
print(f"  {len(P)} fitted points; own (a, b, c) = ({own[0]:.6f}, {own[1]:.6f}, {own[2]:.6f}); frozen {FROZEN}")
d = [abs(own[i] - FROZEN[i]) for i in range(3)]
check("K1", d[0] <= 2e-3 and d[1] <= 2e-2 and d[2] <= 2e-2, f"own fit against the frozen: differences {d[0]:.1e}, {d[1]:.1e}, {d[2]:.1e} (bars 2e-3, 2e-2, 2e-2)")


def pred(v, co):
    c = 0.0 if MUT == "no-speed" else co[2]
    return v["rth"] * (M0 + co[0] * v["g1"] + co[1] * v["g1"] ** 2 + c * v["rdot"])


rf = {k: v["M"] - pred(v, FROZEN) for k, v in Q.items()}
ro = {k: v["M"] - pred(v, own) for k, v in Q.items()}
for k, v in Q.items():
    print(f"  {k}: gamma_1 {v['g1']:.6f}, r_th {v['rth']:.6f}, rdot {v['rdot']:+.4e}, M {v['M']:.6f}; M - frozen {rf[k]:+.2e} (note {NOTE[k]:+.2e}); M - own {ro[k]:+.2e}")
check("K2", all(abs(x) <= 6e-5 for x in rf.values()) and all(abs(rf[k] - NOTE[k]) <= 5e-6 for k in rf),
      "frozen refit with own readings: max |M - predicted| " + f"{max(abs(x) for x in rf.values()):.2e} (bar 6e-5); max difference from the note's {max(abs(rf[k] - NOTE[k]) for k in rf):.1e} (bar 5e-6)")
check("K3", all(abs(x) <= 6e-5 for x in ro.values()), f"own refit: max |M - predicted| {max(abs(x) for x in ro.values()):.2e} (bar 6e-5)")

# K4: where the new points sit relative to the fitted ones (reported)
F = np.array([[v["g1"], v["rth"], v["rdot"]] for v in P.values()])
scale = F.max(0) - F.min(0)
for k, v in Q.items():
    q = np.array([v["g1"], v["rth"], v["rdot"]])
    lo, hi = F.min(0), F.max(0)
    inside = bool(np.all(q >= lo) and np.all(q <= hi))
    dist = float(np.min(np.linalg.norm((F - q) / scale, axis=1)))
    print(f"  {k}: inside the fitted points' bounding box {inside}; nearest fitted point at {dist:.3f} (box-scaled units)")
check("K4", True, "reported above (not gated)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

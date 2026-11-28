#!/usr/bin/env python3
"""ind313: the frozen refit on #313's moderate-leverage route with the coordinator's own readings (criteria in README.md beside this file).

    python3 ind313.py [--mutate=old-coef|no-speed]

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
NEW = {"Y1": "R_B0.0394_xc5_w0.7", "Y2": "R_B0.0768_xc5_w0.7", "Y3": "R_B0.09431_xc5_w0.7"}
NOTE_RES = {"Y1": 2.9e-05, "Y2": 5.3e-05, "Y3": 1.8e-05}
NOTE_LEV = {"Y1": 0.10, "Y2": 0.52, "Y3": 0.77}
NOTE_RD = {"X1": -1.130e-3, "X2": -2.733e-3, "X3": -2.439e-3}
Q = {k: read(os.path.join(RAW, "I313-mac", "runs", f, "h0.005")) for k, f in NEW.items()}
CO = (0.2300, 0.2724, 0.7835) if MUT == "old-coef" else FROZEN
X = np.array([[v["g1"], v["g1"] ** 2, v["rdot"]] for v in P.values()])
G = np.linalg.inv(X.T @ X)
levf = max(float(x @ G @ x) for x in X)


def pred(v, co):
    c = 0.0 if MUT == "no-speed" else co[2]
    return v["rth"] * (M0 + co[0] * v["g1"] + co[1] * v["g1"] ** 2 + c * v["rdot"])


res, lev = {}, {}
for k, v in Q.items():
    res[k] = v["M"] - pred(v, CO)
    xv = np.array([v["g1"], v["g1"] ** 2, v["rdot"]])
    lev[k] = float(xv @ G @ xv)
    print(f"  {k}: gamma_1 {v['g1']:.6f}, r_th {v['rth']:.6f}, rdot {v['rdot']:+.4e}, M {v['M']:.6f}; M - P4 {res[k]:+.3e} (note {NOTE_RES[k]:+.2e}); leverage {lev[k]:.3f} (note {NOTE_LEV[k]})")
print(f"  largest fitted leverage {levf:.4f}")
check("K1", all(abs(res[k] - NOTE_RES[k]) <= 5e-6 and abs(res[k]) <= 6e-5 for k in res),
      "M - P4 " + ", ".join(f"{res[k]:+.2e}" for k in res) + " against the note's within 5e-6, each within 6e-5")
check("K2", all(abs(lev[k] - NOTE_LEV[k]) <= max(0.02 * NOTE_LEV[k], 0.006) for k in lev) and abs(levf - 0.393) <= 0.005,
      "leverage " + ", ".join(f"{lev[k]:.3f}" for k in lev) + f"; fitted maximum {levf:.4f}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

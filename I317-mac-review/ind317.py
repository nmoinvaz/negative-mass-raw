#!/usr/bin/env python3
"""ind317: #296's V3 reading at eps = 1e-2, refitted over the fourteen and predicting #305's X1-X3 (criteria in README.md beside this file).

    python3 ind317.py [--mutate=no-sub|eps-1e-3]

Imports nothing from the repository; the reader is copied from I296-mac-review/ind296.py. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M0 = 0.223086
EPS = 1e-3 if MUT == "eps-1e-3" else 1e-2
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


TRAIN = {f"B{B:g}": os.path.join(RAW, "I266-mac", "runs", f"G_B{B:g}", "h0.005") for B in (0.025, 0.05, 0.1, 0.125)}
TRAIN.update({f"d{e}": os.path.join(RAW, "I267-mac", "runs", "G_B0.1", "h0.005", f"e{e}") for e in (7, 9, 10, 11)})
TRAIN.update({k: os.path.join(RAW, "I283-mac", "runs", f, "h0.005") for k, f in {"W1": "R_B0.07905_xc3_w1", "W2": "R_B0.1543_xc3_w1",
              "W3": "R_B0.1909_xc3_w1", "C1": "R_B0.0393_xc4_w0.5", "C2": "R_B0.07726_xc4_w0.5", "C3": "R_B0.09576_xc4_w0.5"}.items()})
NN = {k: os.path.join(RAW, "I295-mac", "runs", f, "h0.005") for k, f in {"N1": "R_B0.05648_xc3.5_w0.75", "N2": "R_B0.1101_xc3.5_w0.75",
      "N3": "R_B0.136_xc3.5_w0.75"}.items()}
XX = {k: os.path.join(RAW, "I305-mac", "runs", f, "h0.005") for k, f in {"X1": "R_B0.09112_xc4_w1.5", "X2": "R_B0.1695_xc4_w1.5",
      "X3": "R_B0.2044_xc4_w1.5"}.items()}

ref = read(os.path.join(RAW, "I266-mac", "runs", "G_B0", "h0.005"))
dr, dv = (0.0, 0.0) if MUT == "no-sub" else (ref["rth"] - 1.0, ref["rdot"])
print(f"  B = 0 at eps = {EPS:g}: r_th - 1 = {ref['rth'] - 1:+.3e}, rdot_th = {ref['rdot']:+.3e} (#296: -1.41 eps^2 = {-1.41 * EPS ** 2:+.2e}, -3.24 eps^2 = {-3.24 * EPS ** 2:+.2e})")
P = {k: read(d) for k, d in {**TRAIN, **NN, **XX}.items()}
for v in P.values():
    v["rth"] -= dr
    v["rdot"] -= dv
X = np.array([[P[k]["g1"], P[k]["g1"] ** 2, P[k]["rdot"]] for k in TRAIN])
Y = np.array([P[k]["M"] / P[k]["rth"] - M0 for k in TRAIN])
co = np.linalg.lstsq(X, Y, rcond=None)[0]
res = {k: P[k]["M"] - P[k]["rth"] * (M0 + co[0] * P[k]["g1"] + co[1] * P[k]["g1"] ** 2 + co[2] * P[k]["rdot"]) for k in list(NN) + list(XX)}
print(f"  fit over {len(TRAIN)}: (a, b, c) = ({co[0]:.6f}, {co[1]:.6f}, {co[2]:.6f}); #317's V3: (0.229606, 0.131549, 0.558734)")
print("  residuals M - predicted: " + ", ".join(f"{k} {v:+.3e}" for k, v in res.items()))
NOTE = {"X1": 3.35e-5, "X2": 7.32e-5, "X3": 7.73e-5}
d1 = max(abs(res[k] - v) for k, v in NOTE.items())
verdict = abs(res["X1"]) <= 6e-5 and abs(res["X2"]) > 6e-5 and abs(res["X3"]) > 6e-5
check("K1", d1 <= 1e-5 and verdict, f"X against #317's +3.35e-5, +7.32e-5, +7.73e-5: worst {d1:.2e} (bar 1e-5); X1 inside, X2 and X3 outside 6e-5: {verdict}")
nmax = max(abs(res[k]) for k in NN)
check("K2", nmax <= 6e-5, f"N1-N3 largest |M - predicted| {nmax:.2e} (bar 6e-5)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

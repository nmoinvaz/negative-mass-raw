#!/usr/bin/env python3
"""ind296: the settled-mass relation with the member read at departure eps = 1e-2 (criteria in README.md beside this file).

    python3 ind296.py [--mutate=eps-1e-3|no-speed]

Imports nothing from the repository; the reader is copied from ind283.py. Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M0 = 0.223086
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



NINE = {f"B{B:g}": os.path.join(RAW, "I266-mac", "runs", f"G_B{B:g}", "h0.005") for B in (0.025, 0.05, 0.1, 0.125)}
NINE.update({f"d{e}": os.path.join(RAW, "I267-mac", "runs", "G_B0.1", "h0.005", f"e{e}") for e in (7, 9, 10, 11, 12)})
SIX = {k: os.path.join(RAW, "I283-mac", "runs", f, "h0.005") for k, f in {"W1": "R_B0.07905_xc3_w1", "W2": "R_B0.1543_xc3_w1",
       "W3": "R_B0.1909_xc3_w1", "C1": "R_B0.0393_xc4_w0.5", "C2": "R_B0.07726_xc4_w0.5", "C3": "R_B0.09576_xc4_w0.5"}.items()}
THREE = {k: os.path.join(RAW, "I295-mac", "runs", f, "h0.005") for k, f in {"N1": "R_B0.05648_xc3.5_w0.75", "N2": "R_B0.1101_xc3.5_w0.75",
         "N3": "R_B0.136_xc3.5_w0.75"}.items()}


def readall(eps):
    global EPS
    EPS = eps
    return {k: read(d) for k, d in {**NINE, **SIX, **THREE}.items()}


def fit(P, keys):
    X = np.array([[P[k]["g1"], P[k]["g1"] ** 2, 0.0 if MUT == "no-speed" else P[k]["rdot"]] for k in keys])
    Y = np.array([P[k]["M"] / P[k]["rth"] - M0 for k in keys])
    return np.linalg.lstsq(X, Y, rcond=None)[0]


def res(P, k, co):
    v = P[k]
    return v["M"] - v["rth"] * (M0 + co[0] * v["g1"] + co[1] * v["g1"] ** 2 + co[2] * (0.0 if MUT == "no-speed" else v["rdot"]))


eps_test = 1e-3 if MUT == "eps-1e-3" else 1e-2
P = readall(eps_test)
c9 = fit(P, list(NINE))
t1 = {k: res(P, k, c9) for k in SIX}
c15 = fit(P, list(NINE) + list(SIX))
t2 = {k: res(P, k, c15) for k in THREE}
print(f"  eps = {eps_test}: nine-point fit {np.round(c9, 5)}; residuals on the six " + ", ".join(f"{k} {v:+.2e}" for k, v in t1.items()))
print(f"  fifteen-point fit {np.round(c15, 5)}; residuals on the three " + ", ".join(f"{k} {v:+.2e}" for k, v in t2.items()))
m1, m2 = max(abs(v) for v in t1.values()), max(abs(v) for v in t2.values())
check("K1", abs(m1 - 1.29e-4) <= 1e-5 and m1 > 6e-5, f"T1 largest |M - P| {m1:.3e} (note 1.29e-4; bar 6e-5)")
check("K2", abs(m2 - 9.3e-5) <= 1e-5 and m2 > 6e-5, f"T2 largest |M - P| {m2:.3e} (note 9.3e-5; bar 6e-5)")
Q = readall(1e-3)
FROZEN = (0.2296318924, 0.2834170383, 0.7657657062)
P3 = (0.2300, 0.2724, 0.7835)
w3 = res(Q, "W3", P3)
n_max = max(abs(res(Q, k, FROZEN)) for k in THREE)
check("K3", abs(w3 - 7.11e-5) <= 2e-6 and abs(n_max - 2.15e-6) <= 2e-6, f"eps = 1e-3: #283's W3 {w3:+.3e} (7.11e-5), #295's largest {n_max:.2e} (2.15e-6)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""ind323: the settled-mass refit at four departure eps with V3, over the fifteen and the fourteen (criteria in README.md).

    python3 ind323.py OUTPUT [--mutate=no-sub|one-eps]

Imports nothing from the repository; the reader is that of I317-mac-review/ind317.py. Exit 1 when a check fails.
"""
import json
import math
import os
import re
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
OUT = [a for a in sys.argv[1:] if not a.startswith("--")][0]
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
            s = r0["s_m"] + w * (r1["s_m"] - r0["s_m"])
            break
    g1 = s / math.sqrt(1 - s * s)
    tau_d = float(np.interp(td, t, tau))
    sel = np.abs(tau - tau_d) <= 0.5
    c2, c1, _ = np.polyfit(tau[sel] - tau_d, r[sel], 2)
    z = np.load(os.path.join(d, "chain", "series.npz"))
    M = float(z["M"][z["xp"] >= z["xp"].max() - 1.0].mean())
    return dict(g1=g1, rth=rth, rdot=float(c1), M=M)


P = lambda *a: os.path.join(RAW, *a)  # noqa: E731
TRAIN = {f"B{B:g}": P("I266-mac", "runs", f"G_B{B:g}", "h0.005") for B in (0.025, 0.05, 0.1, 0.125)}
TRAIN.update({f"e{e}": P("I267-mac", "runs", "G_B0.1", "h0.005", f"e{e}") for e in (7, 9, 10, 11, 12)})
TRAIN.update({k: P("I283-mac", "runs", f, "h0.005") for k, f in {"W1": "R_B0.07905_xc3_w1", "W2": "R_B0.1543_xc3_w1", "W3": "R_B0.1909_xc3_w1",
              "C1": "R_B0.0393_xc4_w0.5", "C2": "R_B0.07726_xc4_w0.5", "C3": "R_B0.09576_xc4_w0.5"}.items()})
HELD = {k: P("I295-mac", "runs", f, "h0.005") for k, f in {"N1": "R_B0.05648_xc3.5_w0.75", "N2": "R_B0.1101_xc3.5_w0.75", "N3": "R_B0.136_xc3.5_w0.75"}.items()}
HELD.update({k: P("I305-mac", "runs", f, "h0.005") for k, f in {"X1": "R_B0.09112_xc4_w1.5", "X2": "R_B0.1695_xc4_w1.5", "X3": "R_B0.2044_xc4_w1.5"}.items()})
HELD.update({k: P("I313-mac", "runs", f, "h0.005") for k, f in {"Y1": "R_B0.0394_xc5_w0.7", "Y2": "R_B0.0768_xc5_w0.7", "Y3": "R_B0.09431_xc5_w0.7"}.items()})
txt = open(OUT).read()
EPS = ("1e-3", "2e-3", "5e-3", "1e-2")
NOTE = {}
for e in EPS:                                                    # the output's row: eps, reading, a, b, c, in-sample, LOO | N | X | Y
    m = re.search(rf"^\s+{float(e):g}\s+REF-V3\s+(?:[-+0-9.e]+\s+){{5}}\|\s+" + r"\s+\|\s+".join([r"\s+".join([r"([-+0-9.e]+)"] * 3)] * 3), txt, re.M)
    NOTE[e] = dict(zip(["N1", "N2", "N3", "X1", "X2", "X3", "Y1", "Y2", "Y3"], map(float, m.groups())))


def run(eps, keys):
    ee = 1e-3 if MUT == "one-eps" else eps
    ref = read(P("I266-mac", "runs", "G_B0", "h0.005"), ee)
    dr, dv = (0.0, 0.0) if MUT == "no-sub" else (ref["rth"] - 1.0, ref["rdot"])
    R = {k: read(d, ee) for k, d in {**{k: TRAIN[k] for k in keys}, **HELD}.items()}
    for v in R.values():
        v["rth"] -= dr; v["rdot"] -= dv
    X = np.array([[R[k]["g1"], R[k]["g1"] ** 2, R[k]["rdot"]] for k in keys])
    Y = np.array([R[k]["M"] / R[k]["rth"] - M0 for k in keys])
    co = np.linalg.lstsq(X, Y, rcond=None)[0]
    return {k: R[k]["M"] - R[k]["rth"] * (M0 + co[0] * R[k]["g1"] + co[1] * R[k]["g1"] ** 2 + co[2] * R[k]["rdot"]) for k in HELD}


k15 = list(TRAIN)
k14 = [k for k in TRAIN if k != "e12"]
w1, beyond, k2max, k3 = 0.0, True, 0.0, None
for e in EPS:
    r15, r14 = run(float(e), k15), run(float(e), k14)
    d = max(abs(r15[k] - NOTE[e][k]) for k in ("X1", "X2", "X3"))
    w1 = max(w1, d)
    beyond &= abs(r15["X2"]) > 6e-5 and abs(r15["X3"]) > 6e-5
    k2max = max(k2max, max(abs(r15[k]) for k in ("N1", "N2", "N3", "Y1", "Y2", "Y3")))
    if e == "1e-2":
        k3 = max(abs(r14[k] - v) for k, v in {"X1": 3.35e-5, "X2": 7.32e-5, "X3": 7.73e-5}.items())
    print(f"  eps {e}: fifteen X " + ", ".join(f"{r15[k]:+.2e}" for k in ("X1", "X2", "X3")) + f" (#323 " + ", ".join(f"{NOTE[e][k]:+.2e}" for k in ("X1", "X2", "X3"))
          + "); N, Y max " + f"{max(abs(r15[k]) for k in ('N1', 'N2', 'N3', 'Y1', 'Y2', 'Y3')):.2e}; fourteen X " + ", ".join(f"{r14[k]:+.2e}" for k in ("X1", "X2", "X3")))
check("K1", w1 <= 1e-5 and beyond, f"fifteen, V3: X against #323's REF-V3 rows, worst {w1:.2e} (bar 1e-5); X2 and X3 beyond 6e-5 at every eps: {beyond}")
check("K2", k2max <= 6e-5, f"fifteen, V3: N and Y largest {k2max:.2e} over four eps (bar 6e-5)")
check("K3", k3 is not None and k3 <= 1e-5, f"fourteen at eps = 1e-2: X against #317's, worst {k3:.2e} (bar 1e-5)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

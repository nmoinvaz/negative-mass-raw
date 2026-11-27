#!/usr/bin/env python3
"""ind226: the coordinator's independent check of #226 (criteria in README.md beside this file, committed before the first run).

The half-domain double-null march of notes/wormhole_evolution/threshold_check.py (the coordinator's code, no line of dn.py), with
its own ray data (RK4 at h/16), its own C_++ by centered differences along a row, relative noise in r injected as a node is
computed, and the noise model derived in the README. Static Ellis member only.

    python3 ind226.py [--mutate=csign|model-exp|noise-sq] [--only=K0,K1,K2,K3]
"""
import argparse
import math
import sys
import time

import numba as nb
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["csign", "model-exp", "noise-sq"])
ap.add_argument("--only", default="K0,K1,K2,K3")
OPT = ap.parse_args()
MUT = OPT.mutate
ONLY = OPT.only.split(",")
SQ2 = math.sqrt(2.0)
EPS = 2.0 ** -52
BAND = (0.5, 2.0, 3.5, 4.0)          # l_lo, l_hi, t_lo, t_hi
ORDER_BAND = (3.364, 4.757)
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def ray_data(n, N, h, sub=16):
    """Static Ellis member on the ray x- = 0 from the throat: rb'' = (n-1)/(2 rb^(2n-1)), phi' = q/(sqrt2 rb^n), by RK4 at h/sub."""
    q = math.sqrt(n * (n - 1.0))

    def rhs(y):
        rb, rbs, _ = y
        return np.array([rbs, (n - 1.0) / (2.0 * rb ** (2 * n - 1)), q / (SQ2 * rb ** n)])
    y = np.array([1.0, 0.0, 0.0])
    r = np.empty(N + 1)
    p = np.empty(N + 1)
    r[0], p[0] = 1.0, 0.0
    dt = h / sub
    for k in range(1, N + 1):
        for _ in range(sub):
            k1 = rhs(y)
            k2 = rhs(y + 0.5 * dt * k1)
            k3 = rhs(y + 0.5 * dt * k2)
            k4 = rhs(y + dt * k3)
            y = y + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        r[k], p[k] = y[0], y[2]
    return r, p


@nb.njit(cache=False)
def march(n, h, r0, p0, Sc, a, seed, csgn, band, store, a_model, mexp, var):
    """Rows j = 1 .. Sc/2 of the half domain x+ >= x-, nodes i <= Sc - j + 1. Returns the slab max of |C_++| (rows j >= 1,
    j + 1 <= i <= Sc - j), and, if store, C and the model rms at the band's nodes in a fixed order."""
    np.random.seed(seed)
    N = r0.shape[0] - 1
    pr = r0.copy()
    pf = np.zeros(N + 1)
    pp = p0.copy()
    cr = np.zeros(N + 1)
    cf = np.zeros(N + 1)
    cp = np.zeros(N + 1)
    scol = np.zeros(N + 1)                       # sum over rows j' <= j of r(i, j')^(2 n + mexp)
    for i in range(N + 1):
        scol[i] = pr[i] ** (2.0 * n + mexp)
    nn = float(n)
    c1 = nn - 1.0
    h2 = h * h
    ih = 0.5 / h
    cmax = 0.0
    nb_max = 4000000
    cs = np.zeros(nb_max)
    ms = np.zeros(nb_max)
    cnt = 0
    l_lo, l_hi, t_lo, t_hi = band[0], band[1], band[2], band[3]
    for j in range(1, Sc // 2 + 1):
        iend = min(N, Sc - j + 1)
        for i in range(j, iend + 1):
            rE = pr[i]
            fE = pf[i]
            qE = pp[i]
            rS = pr[i - 1]
            fS = pf[i - 1]
            qS = pp[i - 1]
            if i == j:
                rW = rE
                fW = fE
                qW = -qE
            else:
                rW = cr[i - 1]
                fW = cf[i - 1]
                qW = cp[i - 1]
            rN = rE + rW - rS
            fN = fE + fW - fS
            qN = qE + qW - qS
            for it in range(3):
                rc = 0.25 * (rN + rE + rW + rS)
                fc = 0.25 * (fN + fE + fW + fS)
                rp = (rN - rW + rE - rS) * ih
                rm = (rN - rE + rW - rS) * ih
                qp = (qN - qW + qE - qS) * ih
                qm = (qN - qE + qW - qS) * ih
                ruv = -c1 * (rp * rm + 0.5 * math.exp(-fc)) / rc
                fuv = (nn / rc) * ruv - qp * qm
                quv = -nn * (rp * qm + rm * qp) / (2.0 * rc)
                rN = rE + rW - rS + h2 * ruv
                fN = fE + fW - fS + h2 * fuv
                qN = qE + qW - qS + h2 * quv
            if a > 0.0:
                rN = rN * (1.0 + a * EPS_NB * (2.0 * np.random.random() - 1.0))
            cr[i] = rN
            cf[i] = fN
            cp[i] = qN
        for i in range(j, iend + 1):
            scol[i] += cr[i] ** (2.0 * nn + mexp)
        for i in range(j + 1, min(iend - 1, Sc - j) + 1):
            rpp = (cr[i + 1] - 2.0 * cr[i] + cr[i - 1]) / h2
            rpl = (cr[i + 1] - cr[i - 1]) * ih
            fpl = (cf[i + 1] - cf[i - 1]) * ih
            qpl = (cp[i + 1] - cp[i - 1]) * ih
            C = rpp + fpl * rpl - csgn * (cr[i] / nn) * qpl * qpl
            if abs(C) > cmax:
                cmax = abs(C)
            if store:
                l = (i - j) * h / SQRT2_NB
                t = (i + j) * h / SQRT2_NB
                if l_lo <= l <= l_hi and t_lo <= t <= t_hi and cnt < nb_max:
                    cs[cnt] = C
                    ms[cnt] = math.sqrt(2.0 * var) * a_model * EPS_NB / h2 * cr[i] ** (-(nn - 1.0) - mexp / 2.0) * math.sqrt(scol[i])
                    cnt += 1
        for i in range(j, iend + 1):
            pr[i] = cr[i]
            pf[i] = cf[i]
            pp[i] = cp[i]
    return cmax, cs[:cnt], ms[:cnt]


EPS_NB = EPS
SQRT2_NB = SQ2


def run(D, h, Tc=4.0, a=0.0, seed=1, store=False, a_model=0.0):
    n = D - 2
    Sc = int(math.floor(Tc * SQ2 / h + 1e-9))
    N = Sc + 2
    r0, p0 = ray_data(n, N, h)
    csgn = -1.0 if MUT == "csign" else 1.0
    mexp = 2.0 if MUT == "model-exp" else 0.0
    var = 1.0 if MUT == "noise-sq" else 1.0 / 3.0
    t0 = time.time()
    cmax, cs, ms = march(n, h, r0, p0, Sc, a, seed, csgn, np.array(BAND), store, a_model, mexp, var)
    return cmax, cs, ms, time.time() - t0


t00 = time.time()
if "K0" in ONLY:
    m, _, _, dt = run(6, 0.005)
    check("K0", m < 1e-3, f"static D = 6, h = 0.005, t <= 4: max |C_++| = {m:.4e} ({dt:.1f} s); bar 1e-3")

if "K1" in ONLY or "K2" in ONLY:
    resp = {}
    for D, h in ((5, 0.0025 / SQ2), (6, 0.00125)):
        _, c0, m0, _ = run(D, h, store=True, a_model=256.0)
        for a in ((256.0, 1024.0) if D == 6 else (256.0,)):
            _, ca, _, dt = run(D, h, a=a, seed=7, store=True, a_model=a)
            dC = ca - c0
            rms_obs = math.sqrt(np.mean(dC * dC))
            rms_mod = math.sqrt(np.mean(m0 * m0)) * (a / 256.0)
            resp[(D, a)] = (rms_obs, rms_mod, len(dC))
            print(f"  D = {D}, h = {h:.6g}, a = {a:g}: rms dC {rms_obs:.4e}, model {rms_mod:.4e}, ratio {rms_obs / rms_mod:.4f}, "
                  f"{len(dC)} nodes ({dt:.1f} s)", flush=True)
    if "K1" in ONLY:
        rs = {D: resp[(D, 256.0)][0] / resp[(D, 256.0)][1] for D in (5, 6)}
        check("K1", all(0.7 <= x <= 1.4 for x in rs.values()), f"rms dC / model at a = 256: D = 5 {rs[5]:.4f}, D = 6 {rs[6]:.4f}; band [0.7, 1.4]")
    if "K2" in ONLY:
        q = resp[(6, 1024.0)][0] / resp[(6, 256.0)][0]
        check("K2", 3.8 <= q <= 4.2, f"rms dC(1024) / rms dC(256) at D = 6, h = 0.00125: {q:.4f}; band [3.8, 4.2]")

if "K3" in ONLY:
    hs = (0.005, 0.0025, 0.00125, 0.000625)
    ms_ = []
    for h in hs:
        m, _, _, dt = run(6, h)
        ms_.append(m)
        print(f"  static D = 6, h = {h}: max |C_++| = {m:.4e} ({dt:.1f} s)", flush=True)
    rat = [ms_[k] / ms_[k + 1] for k in range(3)]
    ok = ORDER_BAND[0] <= rat[0] <= ORDER_BAND[1] and rat[2] < ORDER_BAND[0]
    check("K3", ok, f"ratios {', '.join(f'{x:.3f}' for x in rat)}; first in [3.364, 4.757], last below 3.364")

bad = [nm for nm, o in RESULTS if not o]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t00:.0f} s", flush=True)
sys.exit(1 if bad else 0)

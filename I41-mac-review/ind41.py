#!/usr/bin/env python3
"""ind41 (built on ind213.py's march): the symmetric expanding branch of #213 by the coordinator's own double-null code (criteria in README.md beside
this file). The march is the one of notes/wormhole_evolution/threshold_check.py (the review of #40), copied and extended:
no stop at r = 2, and the throat series r, f, r_+ and phi_+ recorded.

    python3 ind213.py [--mutate=coord-time|rho-factor|tuned-offset] [--only=K1,K2,K3,D5] [--hs=0.02,0.01]
"""
import argparse
import math
import sys
import time

import numba as nb
import numpy as np
from scipy.integrate import solve_ivp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["M-factor", "side"])
ap.add_argument("--hs", default="0.005,0.0025")
OPT = ap.parse_args()
MUT = OPT.mutate
HS = [float(x) for x in OPT.hs.split(",")]

SQ2 = math.sqrt(2.0)
XC, WP = 3.0, 0.5
W2 = {4: 1.39705243433350684, 5: 2.98495893035176025}
RESULTS = []

def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def ray_data(n, N, h, p):
    q = math.sqrt(n * (n - 1.0))
    g0 = math.exp(-(XC / WP) ** 2)

    def rhs(s, y):
        rb, rbs, _, r, rs = y
        g = math.exp(-((s - XC) / WP) ** 2)
        phbs = q / (SQ2 * rb ** n)
        phs = phbs + p * (-2.0 * (s - XC) / WP ** 2) * g
        return [rbs, (n - 1.0) / (2.0 * rb ** (2 * n - 1)), phbs, rs, (phs * phs / n) * r]
    s = np.arange(N + 1) * h
    sol = solve_ivp(rhs, [0.0, s[-1]], [1.0, 0.0, 0.0, 1.0, 0.0], method="DOP853", rtol=1e-13, atol=1e-14, t_eval=s)
    if not sol.success:
        raise RuntimeError(sol.message)
    _, _, phb, r, _ = sol.y
    phi = phb + p * (np.exp(-((s - XC) / WP) ** 2) - g0)
    return np.ascontiguousarray(r), np.ascontiguousarray(phi)


@nb.njit(cache=False)
def march(n, h, r0, p0, rlo, rhi, stop):
    """Half domain x+ >= x- of the symmetric member, row by row in x-. Records on the diagonal r, f, r_+ and phi_+
    (centred across the diagonal: r(j-1, j) = r(j, j-1), phi(j-1, j) = -phi(j, j-1)). With stop, ends at r <= rlo or
    r >= rhi on the diagonal (fate -1, +1)."""
    N = r0.shape[0] - 1
    pr = r0.copy()
    pf = np.zeros(N + 1)
    pp = p0.copy()
    cr = np.zeros(N + 1)
    cf = np.zeros(N + 1)
    cp = np.zeros(N + 1)
    dr = np.zeros(N + 1)
    df = np.zeros(N + 1)
    drp = np.zeros(N + 1)
    dpp = np.zeros(N + 1)
    dr[0] = pr[0]
    drp[0] = (pr[1] - pr[0]) / h * 0.0
    dpp[0] = (pp[1] + pp[0]) / (2 * h) * 0.0
    nn = float(n)
    c1 = n - 1.0
    h2 = h * h
    ih = 0.5 / h
    cut = N + 1
    fate = 0
    jend = 0
    for j in range(1, N + 1):
        newcut = cut
        for i in range(j, cut):
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
            if not (np.isfinite(rN) and np.isfinite(fN) and np.isfinite(qN)) or rN < 0.05 or fN < -18.42:
                newcut = i
                break
            cr[i] = rN
            cf[i] = fN
            cp[i] = qN
        jend = j
        if newcut <= j + 1:
            fate = 0
            break
        dr[j] = cr[j]
        df[j] = cf[j]
        drp[j] = (cr[j + 1] - pr[j]) * ih
        dpp[j] = (cp[j + 1] + pp[j]) * ih
        if stop and cr[j] <= rlo:
            fate = -1
            break
        if stop and cr[j] >= rhi:
            fate = 1
            break
        cut = newcut
        for i in range(j, cut):
            pr[i] = cr[i]
            pf[i] = cf[i]
            pp[i] = cp[i]
    return dr[:jend], df[:jend], drp[:jend], dpp[:jend], fate, jend


def fate_of(n, h, X, p):
    r0, p0 = ray_data(n, int(round(X / h)), h, p)
    return march(n, h, r0, p0, 0.5, 2.0, True)[4]


def bisect(n, h, X, lo=-0.01, hi=0.01, tol=1e-14):
    if fate_of(n, h, X, lo) != -1 or fate_of(n, h, X, hi) != 1:
        raise RuntimeError("bracket does not straddle")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        f = fate_of(n, h, X, mid)
        if f == 1:
            hi = mid
        elif f == -1:
            lo = mid
        else:
            raise RuntimeError(f"no event at {mid!r}")
    return 0.5 * (lo + hi)


def throat(n, h, X, p):
    r0, p0 = ray_data(n, int(round(X / h)), h, p)
    dr, df, drp, dpp, _, jend = march(n, h, r0, p0, 0.5, 2.0, False)
    lap_all = np.ones_like(df) if MUT == "coord-time" else np.exp(-0.5 * df)
    tau_all = np.concatenate([[0.0], np.cumsum(0.5 * (lap_all[1:] + lap_all[:-1]) * SQ2 * h)])   # from the corner, t = 0
    k = np.arange(1, len(dr))                       # the corner row 0 has no centred derivative
    r, f, rp, pp = dr[k], df[k], drp[k], dpp[k]
    t = SQ2 * h * k
    lap, tau = lap_all[k], tau_all[k]
    H = SQ2 * rp / lap / r
    rho = np.exp(f) * pp * pp * (2.0 if MUT == "rho-factor" else 1.0)
    return dict(t=t, tau=tau, r=r, H=H, rho=rho, f=f, jend=jend)


def analyse(th, W):
    r, H, tau = th["r"], th["H"], th["tau"]
    sel = r >= r[-1] / math.e
    sl, b = np.polyfit(tau[sel], 1.0 / H[sel], 1)
    k = -1.0 / sl
    tau_s = -b / sl
    q = np.polyfit(np.log(tau_s - tau[sel]), np.log(r[sel]), 1)[0]
    hw = []
    for ra in (10, 25, 50):
        idx = np.nonzero(r >= ra)[0]
        hw.append(H[idx[0]] / W if len(idx) else float("nan"))
    return dict(k=k, tau_s=tau_s, rhoH2=th["rho"][-1] / H[-1] ** 2, hw=hw, q=q, r_end=r[-1], tau_end=tau[-1], n=int(sel.sum()))




@nb.njit(cache=False)
def march_ah(n, h, r0, p0):
    """As march, without a stop, recording on each row the right apparent horizon: the first i > j with r_+ >= 0 after
    a cell with r_+ < 0 and r_- < 0; r and f linear in r_+ between the two cells. Returns (j, x+, r_AH, f_AH) arrays."""
    N = r0.shape[0] - 1
    pr = r0.copy(); pf = np.zeros(N + 1); pp = p0.copy()
    cr = np.zeros(N + 1); cf = np.zeros(N + 1); cp = np.zeros(N + 1)
    oj = np.zeros(N + 1); oxp = np.zeros(N + 1); orr = np.zeros(N + 1); off = np.zeros(N + 1)
    no = 0
    nn = float(n); c1 = n - 1.0; h2 = h * h; ih = 0.5 / h
    cut = N + 1
    for j in range(1, N + 1):
        newcut = cut
        for i in range(j, cut):
            rE = pr[i]; fE = pf[i]; qE = pp[i]
            rS = pr[i - 1]; fS = pf[i - 1]; qS = pp[i - 1]
            if i == j:
                rW = rE; fW = fE; qW = -qE
            else:
                rW = cr[i - 1]; fW = cf[i - 1]; qW = cp[i - 1]
            rN = rE + rW - rS; fN = fE + fW - fS; qN = qE + qW - qS
            for it in range(3):
                rc = 0.25 * (rN + rE + rW + rS); fc = 0.25 * (fN + fE + fW + fS)
                rp = (rN - rW + rE - rS) * ih; rm = (rN - rE + rW - rS) * ih
                qp = (qN - qW + qE - qS) * ih; qm = (qN - qE + qW - qS) * ih
                ruv = -c1 * (rp * rm + 0.5 * math.exp(-fc)) / rc
                fuv = (nn / rc) * ruv - qp * qm
                quv = -nn * (rp * qm + rm * qp) / (2.0 * rc)
                rN = rE + rW - rS + h2 * ruv; fN = fE + fW - fS + h2 * fuv; qN = qE + qW - qS + h2 * quv
            if not (np.isfinite(rN) and np.isfinite(fN) and np.isfinite(qN)) or rN < 0.05 or fN < -18.42:
                newcut = i
                break
            cr[i] = rN; cf[i] = fN; cp[i] = qN
        if newcut <= j + 2:
            break
        # the right apparent horizon on this row
        trapped = False
        prev_rp = 0.0
        for i in range(j + 1, newcut - 1):
            rpl = (cr[i + 1] - cr[i - 1]) * ih
            rmi = (cr[i] - pr[i]) / h if i < cut else 0.0           # one-sided in x-, sign only
            if rpl < 0.0 and rmi < 0.0:
                trapped = True
            elif trapped and rpl >= 0.0:
                s = -prev_rp / (rpl - prev_rp)
                oj[no] = j; oxp[no] = (i - 1 + s) * h
                orr[no] = cr[i - 1] + s * (cr[i] - cr[i - 1]); off[no] = cf[i - 1] + s * (cf[i] - cf[i - 1])
                no += 1
                break
            prev_rp = rpl
        cut = newcut
        for i in range(j, cut):
            pr[i] = cr[i]; pf[i] = cf[i]; pp[i] = cp[i]
    return oj[:no], oxp[:no], orr[:no], off[:no]


REF_F = (1.335, 1.936, 4.074, 11.96)
REF_M = (0.43732, 0.37800, 0.30314, 0.24998)
t0 = time.time()
out = {}
for h in HS:
    ps = bisect(2, h, 28.0)
    p = ps + (1e-6 if MUT == "side" else -1e-6)
    r0, p0 = ray_data(2, int(round(12.0 / h)), h, p)
    oj, oxp, orr, off = march_ah(2, h, r0, p0)
    xm = oj * h
    F = np.exp(-off)
    M = orr * (1.0 if MUT == "M-factor" else 0.5)
    out[h] = (F, M, xm)
    print(f"  h={h:g}: p*_h {ps:.12e}; {len(F)} horizon rows; e^-f from {F.min() if len(F) else float('nan'):.3f} to "
          f"{F.max() if len(F) else float('nan'):.3f}; first M {M[0] if len(M) else float('nan'):.5f} ({time.time() - t0:.0f} s)", flush=True)


def at(h, Fv):
    F, M, xm = out[h]
    if len(F) < 2 or not (F.min() <= Fv <= F.max()):
        return float("nan"), float("nan"), 0
    o = np.argsort(F)
    return float(np.interp(Fv, F[o], M[o])), float(np.interp(Fv, F[o], xm[o])), int(np.sum(np.abs(np.log(F / Fv)) < 0.05))


ok1, notes = True, []
for Fv, Mref in zip(REF_F, REF_M):
    m2, x2, n2 = at(0.0025, Fv)
    m1, _, _ = at(0.005, Fv)
    okp = abs(m2 - Mref) <= 1e-3 and abs(m1 - m2) <= 1e-3
    ok1 &= okp
    notes.append(f"e^-f {Fv}: M {m2:.5f} (h = 0.005: {m1:.5f}) against {Mref} ({m2 - Mref:+.1e})")
check("K1", ok1, "; ".join(notes))
_, x2, _ = at(0.0025, 11.96)
check("K2", abs(x2 - 9.39779) <= 5e-3, f"horizon x- at e^-f = 11.96: {x2:.5f} against 9.39779 ({x2 - 9.39779:+.1e})")
m, x, nrow = at(0.0025, 36.23)
print(f"  reported: at e^-f = 36.23, M {m:.5f} (runner 0.22930), x- {x:.5f}, {nrow} rows within 5 % of that e^-f", flush=True)
bad = [nm for nm, o in RESULTS if not o]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)

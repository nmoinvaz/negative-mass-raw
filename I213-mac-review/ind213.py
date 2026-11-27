#!/usr/bin/env python3
"""ind213: the symmetric expanding branch of #213 by the coordinator's own double-null code (criteria in README.md beside
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
ap.add_argument("--mutate", default=None, choices=["coord-time", "rho-factor", "tuned-offset"])
ap.add_argument("--only", default="K1,K2,K3,D5")
ap.add_argument("--hs", default="0.02,0.01")
OPT = ap.parse_args()
MUT = OPT.mutate
ONLY = OPT.only.split(",")
HS = [float(x) for x in OPT.hs.split(",")]

SQ2 = math.sqrt(2.0)
XC, WP = 3.0, 0.5
W2 = {4: 1.39705243433350684, 5: 2.98495893035176025}
RESULTS = []

# the runner's values (expansion_output.txt at 94d89f7), by h
REF_HW = {0.02: (1.231, 1.946, 2.752), 0.01: (1.230, 1.946, 2.752)}
REF_TS = {0.02: {"tuned": 17.89018, 0.01: 10.05900, 0.05: 8.43404, 0.2: 6.16920},
          0.01: {"tuned": 17.89022, 0.01: 10.05589, 0.05: 8.43337, 0.2: 6.16898}}


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


RUNS = {}
t0 = time.time()
if any(k in ONLY for k in ("K1", "K2", "K3")):
    W = math.sqrt(W2[4])
    for h in HS:
        ps = bisect(2, h, 28.0)
        off = 1e-3 if MUT == "tuned-offset" else 1e-6
        for mem in ("tuned", 0.01, 0.05, 0.2):
            p = ps + off if mem == "tuned" else mem
            th = throat(2, h, 200.0, p)
            a = analyse(th, W)
            RUNS[(h, mem)] = a
            print(f"  D=4 h={h:g} {mem!s:>6} (A = {p:.6e}; p*_h {ps:.6e}): k {a['k']:.5f}, tau_s {a['tau_s']:.5f}, |rho|/H^2 end "
                  f"{a['rhoH2']:.5f}, H/W at r/a 10, 25, 50: {a['hw'][0]:.4f} {a['hw'][1]:.4f} {a['hw'][2]:.4f}; exponent of r "
                  f"{-a['q']:.4f}; r_end {a['r_end']:.1f}, tau_end {a['tau_end']:.4f}, {a['n']} pts ({time.time() - t0:.0f} s)", flush=True)

if "K1" in ONLY:
    bad = [(h, m) for (h, m), a in RUNS.items() if not (abs(a["k"] - 2) <= 1e-3 and abs(a["rhoH2"] - 4) <= 1e-3)]
    check("K1", not bad and len(RUNS) == 8, "k " + ", ".join(f"{a['k']:.5f}" for a in RUNS.values()) + "; |rho|/H^2 "
          + ", ".join(f"{a['rhoH2']:.5f}" for a in RUNS.values()) + (f"; outside: {bad}" if bad else ""))
if "K2" in ONLY:
    ok, notes = True, []
    for h in HS:
        a = RUNS[(h, "tuned")]
        rel = [a["hw"][i] / REF_HW[h][i] - 1 for i in range(3)]
        ok &= all(abs(x) <= 3e-3 for x in rel)
        notes.append(f"h={h:g}: " + ", ".join(f"{a['hw'][i]:.4f} against {REF_HW[h][i]} ({rel[i]:+.1e})" for i in range(3)))
    check("K2", ok, "; ".join(notes))
if "K3" in ONLY:
    ok, notes = True, []
    for h in HS:
        for mem in ("tuned", 0.01, 0.05, 0.2):
            ts, ref = RUNS[(h, mem)]["tau_s"], REF_TS[h][mem]
            ok &= abs(ts / ref - 1) <= 2e-3
            notes.append(f"h={h:g} {mem}: {ts:.5f} against {ref} ({ts / ref - 1:+.1e})")
    check("K3", ok, "; ".join(notes))
if "D5" in ONLY:
    W = math.sqrt(W2[5])
    h = 0.01 / SQ2
    ps = bisect(3, h, 18.0)
    for mem in ("tuned", 0.05):
        p = ps + 1e-6 if mem == "tuned" else mem
        a = analyse(throat(3, h, 100.0, p), W)
        print(f"  D=5 h={h:.6g} {mem!s:>6} (A = {p:.6e}): k {a['k']:.4f}, tau_s {a['tau_s']:.5f}, |rho|/H^2 end {a['rhoH2']:.4f}, "
              f"H/W at r/a 10, 25, 50: {a['hw'][0]:.4f} {a['hw'][1]:.4f} {a['hw'][2]:.4f}; exponent of r {-a['q']:.4f}; "
              f"r_end {a['r_end']:.1f} (reported) ({time.time() - t0:.0f} s)", flush=True)

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

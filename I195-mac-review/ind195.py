#!/usr/bin/env python3
"""ind195: the coordinator's independent check of #195 (criteria in README.md beside this file).

    python3 ind195.py [--mutate=NAME] [--only=K1,K2,K3,K4]
"""
import argparse
import json
import os
import re
import sys
import time

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["k1-B", "k2-eps", "k3-omega1"])
ap.add_argument("--only", default="K1,K2,K3,K4")
A_ = ap.parse_args()
MUT, ONLY = A_.mutate, A_.only.split(",")
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def crate_values(log):
    out = {}
    for ln in open(os.path.join(HERE, log)):
        m = re.match(r"RESULT (\{.*\})", ln)
        if m:
            r = json.loads(m.group(1))
            if r.get("kind") == "w2":
                out[int(r["D"])] = r["W2"]
    return out


# ---------------- K1: E2 in the variable ell, by sympy ----------------
if "K1" in ONLY:
    l, n, W2 = sp.symbols("l n W2", positive=True)
    rr = sp.Function("r")(l)
    Yf = sp.Function("Y")(l)
    # E2 of master.py: Y'' - (2 r''/r' + n r'/r) Y' + (n r'^2/r^2 + r''/r) Y = W^2 Y (proper distance l)
    E2 = (Yf.diff(l, 2) - (2 * rr.diff(l, 2) / rr.diff(l) + n * rr.diff(l) / rr) * Yf.diff(l)
          + (n * rr.diff(l)**2 / rr**2 + rr.diff(l, 2) / rr) * Yf - W2 * Yf)
    # change to ell = s ln r, w = dY/d ln r: Y' = w r'/r, w' = w_ell s r'/r
    s = 2 * (n - 1)
    w, wl, Y, rp, rpp, r0 = sp.symbols("w w_ell Y rp rpp r0")
    Yp = w * rp / r0
    Ypp = wl * s * rp**2 / r0**2 + w * (rpp / r0 - rp**2 / r0**2)
    expr = E2.subs({Yf.diff(l, 2): Ypp, Yf.diff(l): Yp}).subs({rr.diff(l, 2): rpp, rr.diff(l): rp, rr: r0, Yf: Y})
    # background: r'^2 = F, r r'' = (n-1) e^{-ell} with e^{-ell} = r^{-2(n-1)}; W^2 = s + Omega, r^2 = e^{2 eps ell}
    ell, Om = sp.symbols("ell Omega")
    E = sp.exp(-ell)
    F = 1 - E
    eps = 1 / s
    sub = {rpp: (n - 1) * E / r0, rp: sp.sqrt(F), W2: s + Om}
    wl_sol = sp.solve(sp.Eq(expr.subs(sub), 0), wl)[0]
    r2 = sp.exp(2 * eps * ell)
    wl_sol = wl_sol.subs(r0**2, r2).subs(r0, sp.sqrt(r2))
    Aexp = (1 + eps * Om) * r2 - (sp.Rational(1, 2) + eps) * F - E / 2
    Bexp = ((sp.Rational(1, 2) + (eps if MUT == "k1-B" else 2 * eps)) * F + E / 2)
    res = sp.simplify(sp.expand(wl_sol * F - (Aexp * Y + Bexp * w)))
    check("K1", res == 0, f"residual of F w_ell - (A Y + B w): {res}")

# ---------------- K2: an independent W^2 by outward/inward Taylor stepping, matched at ell_m = 3 ----------------
if "K2" in ONLY:
    mp.mp.dps = 50
    ORD = 60

    def jets(lc, eps, Om):
        """Taylor coefficients about lc of a = A/F and b = B/F"""
        e1 = [mp.exp(2 * eps * lc) * (2 * eps)**k / mp.factorial(k) for k in range(ORD + 1)]
        e2 = [mp.exp(-lc) * (-1)**k / mp.factorial(k) for k in range(ORD + 1)]
        Fj = [(1 if k == 0 else 0) - e2[k] for k in range(ORD + 1)]
        Aj = [(1 + eps * Om) * e1[k] - (mp.mpf(1) / 2 + eps) * Fj[k] - e2[k] / 2 for k in range(ORD + 1)]
        Bj = [(mp.mpf(1) / 2 + 2 * eps) * Fj[k] + e2[k] / 2 for k in range(ORD + 1)]

        def div(N):
            q = []
            for k in range(ORD + 1):
                q.append((N[k] - mp.fsum(Fj[j] * q[k - j] for j in range(1, k + 1))) / Fj[0])
            return q
        return div(Aj), div(Bj)

    def step(lc, h, Y0, w0, eps, Om):
        a, b = jets(lc, eps, Om)
        Y, w = [Y0], [w0]
        for k in range(ORD):
            Y.append(eps * w[k] / (k + 1))
            w.append(mp.fsum(a[j] * Y[k - j] + b[j] * w[k - j] for j in range(k + 1)) / (k + 1))
        hh = mp.mpf(h)
        return mp.polyval(Y[::-1], hh), mp.polyval(w[::-1], hh)

    def throat(eps, Om, l0, M=90):
        """the even (analytic) solution's series at the throat, Y(0) = 1, summed at l0"""
        Fj = [mp.mpf(0)] + [(-1)**(j + 1) / mp.factorial(j) for j in range(1, M + 2)]
        Aj = [(1 + eps * Om) * (2 * eps)**i / mp.factorial(i) - (mp.mpf(1) / 2 + eps) * Fj[i] - (-1)**i / (2 * mp.factorial(i))
              for i in range(M + 1)]
        Bj = [(mp.mpf(1) / 2 + 2 * eps) * Fj[i] + (-1)**i / (2 * mp.factorial(i)) for i in range(M + 1)]
        Y, w = [mp.mpf(1)], [-2 * Aj[0]]
        for m in range(1, M + 1):
            Y.append(eps * w[m - 1] / m)
            rhs = Aj[0] * Y[m] + mp.fsum(Aj[i] * Y[m - i] + Bj[i] * w[m - i] for i in range(1, m + 1))
            rhs -= mp.fsum(Fj[j] * (m - j + 1) * w[m - j + 1] for j in range(2, m + 1))
            w.append(rhs / (m - mp.mpf(1) / 2))
        return mp.polyval(Y[::-1], l0), mp.polyval(w[::-1], l0)

    def M(Om, D):
        eps = mp.mpf(1) / (2 * (D - 3))
        if MUT == "k2-eps":
            eps *= 1 + mp.mpf("1e-8")
        l0, lm, linf = mp.mpf(1) / 2, mp.mpf(3), mp.mpf(180)
        Y, w = throat(eps, Om, l0)
        lc = l0
        while lc < lm:
            h = min(mp.mpf(1) / 4, lc / 5, lm - lc)
            Y, w = step(lc, h, Y, w, eps, Om)
            lc += h
        Yo, wo = Y, w
        # far side: the decaying eigenvector of the frozen matrix [[0, eps], [a, b]] at linf
        a, b = jets(linf, eps, Om)
        lam = (b[0] - mp.sqrt(b[0]**2 + 4 * eps * a[0])) / 2
        Y, w = mp.mpf(1), lam / eps
        lc = linf
        while lc > lm:
            h = min(mp.mpf(1) / 2, lc / 5, lc - lm)
            Y, w = step(lc, -h, Y, w, eps, Om)
            lc -= h
            nrm = abs(Y) + abs(w)
            Y, w = Y / nrm, w / nrm
        return (Yo * w - wo * Y) / (abs(Yo) + abs(wo))

    crate = crate_values("rerun_run_02_w2_qd_growth.log")
    ok2, notes = True, []
    for D in (50, 1000):
        t0 = time.time()
        eps = mp.mpf(1) / (2 * (D - 3))
        O1c = 2 * mp.pi**2 / 3 + 8 * mp.log(2)**2
        Oa = -4 * mp.log(2) + O1c * eps + 73 * eps**2
        Ob = Oa + mp.mpf("1e-3")
        fa, fb = M(Oa, D), M(Ob, D)
        for it in range(30):
            Oc = Ob - fb * (Ob - Oa) / (fb - fa)
            Oa, fa, Ob, fb = Ob, fb, Oc, M(Oc, D)
            if abs(Ob - Oa) < mp.mpf("1e-46"):
                break
        W2i = 2 * (D - 3) + Ob
        W2c = mp.mpf(crate[D])
        rel = abs(W2i - W2c) / W2c
        ok2 &= rel <= mp.mpf("1e-35")
        notes.append(f"D={D}: W2_ind {mp.nstr(W2i, 40)}, crate {mp.nstr(W2c, 40)}, rel {mp.nstr(rel, 3)} "
                     f"({it + 1} secant steps, {time.time() - t0:.0f} s)")
        print("  " + notes[-1], flush=True)
    check("K2", ok2, "; ".join(notes))

# ---------------- K3 and K4: Omega1, Omega2 by Neville extrapolation; PSLQ ----------------
if "K3" in ONLY or "K4" in ONLY:
    mp.mp.dps = 100
    vals = crate_values("rerun_run_03_w2_qd_Dlist.log")
    Ds = sorted(vals, reverse=True)
    O1c = 2 * mp.pi**2 / 3 + 8 * mp.log(2)**2
    O2c = 80 * mp.zeta(3) - mp.mpf(8) / 3 * mp.pi**2 * mp.log(2) - mp.mpf(32) / 3 * mp.log(2)**3

    def neville(xs, ys):
        p = list(ys)
        nn = len(xs)
        for k in range(1, nn):
            for i in range(nn - k):
                p[i] = ((0 - xs[i + k]) * p[i] + (xs[i] - 0) * p[i + 1]) / (xs[i] - xs[i + k])
        return p[0]

    O1s, O2s = {}, {}
    O1sub = O1c + (mp.mpf("1e-20") if MUT == "k3-omega1" else 0)
    for N in (16, 20, 24):
        sel = Ds[:N]
        es = [mp.mpf(1) / (2 * (D - 3)) for D in sel]
        gs = [mp.mpf(vals[D]) - 2 * (D - 3) + 4 * mp.log(2) for D in sel]
        O1s[N] = neville(es, [g / e for g, e in zip(gs, es)])
        O2s[N] = neville(es, [(g / e - O1sub) / e for g, e in zip(gs, es)])
    d1 = {N: abs(O1s[N] - O1c) for N in O1s}
    d2 = {N: abs(O2s[N] - O2c) for N in O2s}
    spread = max(O2s.values()) - min(O2s.values())
    if "K3" in ONLY:
        ok3 = all(v <= mp.mpf("1e-30") for v in d1.values()) and all(v <= mp.mpf("1e-20") for v in d2.values()) \
            and spread <= mp.mpf("1e-20")
        check("K3", ok3, "; ".join(f"N={N}: |Ω1 − closed| {mp.nstr(d1[N], 3)}, Ω2 {mp.nstr(O2s[N], 30)}, "
                                   f"|Ω2 − closed| {mp.nstr(d2[N], 3)}" for N in O1s)
              + f"; spread of Ω2 over N {mp.nstr(spread, 3)}")
    if "K4" in ONLY:
        mp.mp.dps = 60
        x = O2s[20]
        rel = mp.pslq([x, mp.zeta(3), mp.pi**2 * mp.log(2), mp.log(2)**3], tol=mp.mpf("1e-18"), maxcoeff=1000,
                      maxsteps=10**6)
        good = rel is not None and all(abs(r * 3 - e * rel[0]) == 0 for r, e in zip(rel, [3, -240, 8, 32])) \
            and rel[0] != 0
        ctl = mp.pslq([x, mp.zeta(3) + mp.mpf("1e-12"), mp.pi**2 * mp.log(2), mp.log(2)**3], tol=mp.mpf("1e-18"),
                      maxcoeff=1000, maxsteps=10**6)
        check("K4", good and ctl is None, f"relation {rel}; perturbed basis: {ctl}")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)

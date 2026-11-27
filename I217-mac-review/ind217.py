#!/usr/bin/env python3
"""ind217: #217's double-null equations with the potential, derived again by a brute-force Ricci tensor, against the code
under test (evolve.F_np) and on the closed-form static member (criteria in README.md beside this file).

    python3 ind217.py [--mutate=V-sign|code-Vp] [--wt=WORKTREE/notes/black_universe]
"""
import argparse
import math
import os
import random
import sys
import time

import mpmath as mp
import numpy as np
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["V-sign", "code-Vp"])
ap.add_argument("--wt", default=os.path.expanduser("~/Source/negative-mass-r217/notes/black_universe"))
OPT = ap.parse_args()
MUT = OPT.mutate
sys.path.insert(0, OPT.wt)
sys.argv = [sys.argv[0]]
import evolve  # noqa: E402  (the code under test)
import evolve_potential as ep  # noqa: E402  (the potential, shared)

RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def ricci(g, X):
    dim = len(X)
    gi = sp.simplify(g.inv())
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                             for d in range(dim)) / 2) for c in range(dim)] for b in range(dim)] for a in range(dim)]
    R = sp.zeros(dim, dim)
    for b in range(dim):
        for d in range(b, dim):
            e = sum(sp.diff(Gam[a][b][d], X[a]) - sp.diff(Gam[a][b][a], X[d]) for a in range(dim))
            e += sum(Gam[a][a][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][a] for a in range(dim) for k in range(dim))
            R[b, d] = R[d, b] = sp.simplify(e)
    return R, gi


t0 = time.time()
u, v, th1, th2 = sp.symbols("u v th1 th2")
X = [u, v, th1, th2]
r, f, ph = sp.Function("r")(u, v), sp.Function("f")(u, v), sp.Function("ph")(u, v)
Vf = sp.Function("V")
eps = -1
sV = -1 if MUT == "V-sign" else 1
g = sp.zeros(4, 4)
g[0, 1] = g[1, 0] = -sp.exp(-f)
g[2, 2] = r ** 2
g[3, 3] = r ** 2 * sp.sin(th1) ** 2
R, gi = ricci(g, X)
E = lambda a, b: (R[a, b] - eps * sp.diff(ph, X[a]) * sp.diff(ph, X[b]) - sV * Vf(ph) * g[a, b]).doit()  # noqa: E731
sq = sp.sqrt(-g.det())
box = sp.simplify(sum(sp.diff(sq * gi[a, b] * sp.diff(ph, X[b]), X[a]) for a in range(4) for b in range(4)) / sq)
scal = eps * box - sV * sp.diff(Vf(ph), ph)                  # eps box phi = V'(phi)
ruv, fuv, puv = sp.diff(r, u, v), sp.diff(f, u, v), sp.diff(ph, u, v)
sol_r = sp.solve(sp.Eq(E(2, 2), 0), ruv)[0]
sol_f = sp.solve(sp.Eq(E(0, 1).subs(ruv, sol_r), 0), fuv)[0]
sol_p = sp.solve(sp.Eq(scal, 0), puv)[0]
ru, rv, fu, fv, pu, pv = (sp.diff(r, u), sp.diff(r, v), sp.diff(f, u), sp.diff(f, v), sp.diff(ph, u), sp.diff(ph, v))
Vs = Vf(ph)
# evolution_design.md section 1, as printed (n = 2):
pr_r = -(ru * rv + sp.exp(-f) / 2) / r + sp.Rational(1, 2) * Vs * r * sp.exp(-f)
pr_f = (2 / r) * pr_r + eps * pu * pv - Vs * sp.exp(-f)
pr_p = -(ru * pv + rv * pu) / r - sp.Rational(eps, 2) * sp.exp(-f) * sp.diff(Vf(ph), ph)
res = [sp.simplify(sol_r - pr_r), sp.simplify(sol_f - pr_f), sp.simplify(sol_p - pr_p)]
sym_ok = all(x == 0 for x in res)
print(f"  derivation done ({time.time() - t0:.0f} s); residuals against the printed forms: {[str(x)[:60] for x in res]}", flush=True)

# numerical comparison with evolve.F_np
syms = sp.symbols("R F P Ru Rv Fu Fv Pu Pv V0 V1")
Rs, Fs, Ps, Rus, Rvs, Fus, Fvs, Pus, Pvs, V0s, V1s = syms
sub = {ru: Rus, rv: Rvs, fu: Fus, fv: Fvs, pu: Pus, pv: Pvs}
sub2 = {r: Rs, f: Fs, ph: Ps}
def lam(e):  # noqa: E302
    e = e.subs(sp.diff(Vf(ph), ph), V1s).subs(Vf(ph), V0s)
    return e.subs(sub).subs(sub2)
fn = sp.lambdify(syms, [lam(sol_r), lam(sol_f), lam(sol_p)], "math")
evolve.MUT = "Vp_sign" if MUT == "code-Vp" else None
worst = 0.0
for c in (-0.3, -1.5, -1.0):
    mem = ep.Member(c)
    par = evolve.params(mem)
    rng = random.Random(int(1000 * -c))
    for _ in range(20):
        st = [rng.uniform(0.5, 3.0), rng.uniform(-1, 1), rng.uniform(-2.0, 2.0)] + [rng.uniform(-1, 1) for _ in range(6)]
        V0, V1 = ep.pot(st[2], mem.c, mem.K)
        mine = fn(*st, V0, V1)
        cc = np.array([[st[0]], [st[1]], [st[2]]])
        up = np.array([[st[3]], [st[5]], [st[7]]])
        um = np.array([[st[4]], [st[6]], [st[8]]])
        got = evolve.F_np(cc, up, um, par, np.array([-1.0]))[:, 0]
        worst = max(worst, max(abs(a - b) / max(1.0, abs(a)) for a, b in zip(mine, got)))
evolve.MUT = None
check("K1", sym_ok and worst <= 1e-12, f"symbolic residuals {['0' if x == 0 else 'nonzero' for x in res]}; evolve.F_np worst rel diff {worst:.1e} at 60 states")

# K2: the static member in the tortoise null gauge, at 30 digits, with the coordinator's own expressions
mp.mp.dps = 30
Rsym, Asym, Phsym = sp.symbols("Rr A Ph")
worst2 = mp.mpf(0)
for c in (-0.3, -1.5, -1.0):
    cm = mp.mpf(c)
    K = -2 * cm / mp.pi
    A = lambda x: 1 + cm * (x * x + 1) + K * (x + (x * x + 1) * mp.atan(x))  # noqa: E731
    Rf = lambda x: mp.sqrt(x * x + 1)  # noqa: E731
    phf = lambda x: mp.sqrt(2) * mp.atan(x)  # noqa: E731
    mem = ep.Member(c)
    rh = mem.rh
    for k in range(10):
        rho = mp.mpf(rh) + mp.mpf(0.05) + mp.mpf(k) * mp.mpf(0.4)
        # functions of x through rho: d/dx = A d/drho; on the member d+ = (1/sqrt2) d/dx, d- = -(1/sqrt2) d/dx
        Ax = A(rho)
        d = lambda F, x=rho: mp.diff(F, x)  # noqa: E731
        Rx = Ax * d(Rf)
        Rxx = Ax * mp.diff(lambda y: A(y) * mp.diff(Rf, y), rho)
        Px = Ax * d(phf)
        Pxx = Ax * mp.diff(lambda y: A(y) * mp.diff(phf, y), rho)
        fval = -mp.log(Ax)                                           # e^{-f} = A
        fx = -d(A)                                                    # f_x = A d(-ln A)/drho = -A'
        fxx = -Ax * mp.diff(A, rho, 2)                                # f_xx = A d(-A')/drho
        sq2 = mp.sqrt(2)
        rp, rm_ = Rx / sq2, -Rx / sq2
        pp, pm = Px / sq2, -Px / sq2
        fp_, fm_ = fx / sq2, -fx / sq2
        ruv_m, fuv_m, puv_m = -Rxx / 2, -fxx / 2, -Pxx / 2           # d+d- = -(1/2) d_xx on a function of x
        Vpsi = lambda ps: -cm * (3 - 2 * mp.cos(ps) ** 2) - K * (3 * mp.sin(ps) * mp.cos(ps) + ps * (3 - 2 * mp.cos(ps) ** 2))  # noqa: E731
        ps = phf(rho) / sq2
        V0 = sV * Vpsi(ps)
        V1 = sV * mp.diff(Vpsi, ps) / sq2
        emf = mp.e ** (-fval)
        e1 = ruv_m - (-(rp * rm_ + emf / 2) / Rf(rho) + V0 * Rf(rho) * emf / 2)
        e2 = fuv_m - ((2 / Rf(rho)) * (-(rp * rm_ + emf / 2) / Rf(rho) + V0 * Rf(rho) * emf / 2) + eps * pp * pm - V0 * emf)
        e3 = puv_m - (-(rp * pm + rm_ * pp) / Rf(rho) - mp.mpf(eps) / 2 * emf * V1)
        # null constraints C++ = r++ + f+ r+ + (r/2) eps phi+^2 with d+d+ = (1/2) d_xx
        cpp = Rxx / 2 + fp_ * rp + Rf(rho) / 2 * eps * pp ** 2
        cmm = Rxx / 2 + fm_ * rm_ + Rf(rho) / 2 * eps * pm ** 2
        worst2 = max(worst2, *[abs(e) for e in (e1, e2, e3, cpp, cmm)])
check("K2", worst2 <= mp.mpf("1e-25"), f"largest residual on the member {mp.nstr(worst2, 3)} at 30 points (c = -0.3, -1.5, -1)")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""ind220: ind208 carried to order 6: the order equations of #220 derived again from the l-system, and Omega0..Omega4 by the
coordinator's Taylor stepper (criteria in README.md beside this file).

    python3 ind220.py [--mutate=NAME] [--wt=WORKTREE_NOTES_DIR]
"""
import argparse
import os
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["short-V", "drop-z5"])
ap.add_argument("--wt", default="/Users/nathan/Source/negative-mass-r220/notes/wormhole_largeD")
A_ = ap.parse_args()
MUT = A_.mutate

saved, sys.argv = sys.argv, ["order6.py"]
sys.path.insert(0, A_.wt)
import order6 as o5  # noqa: E402  (the object under test: hk, Fsum)
sys.argv = saved

RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


# ---------------- K1: the order equations from the l-system ----------------
t0 = time.time()
eps, l, R = sp.symbols("epsilon l R", positive=True)
Om = sp.symbols("Omega0:6")
Ys, Ls = sp.symbols("Y0:7"), sp.symbols("L0:7")
half = sp.Rational(1, 2)
F = 1 - 1 / R
Oser = sum(Om[i] * eps**i for i in range(6))
A = (1 + eps * Oser) * sp.exp(2 * eps * l) - (half + eps) * F - 1 / (2 * R)       # e^{-l} = 1/R
B = (half + 2 * eps) * F + 1 / (2 * R)

# w = e^{eps l} L: F w_l = A Y + B w becomes (R - 1) L_R - L/2 = A e^{-eps l} Y + (B - 1/2 - eps F) L,
# since F L_l = (1 - 1/R) R L_R = (R - 1) L_R.  Check the transformation itself on a generic L(l), Y:
x = sp.symbols("x", positive=True)
Lf, Yv = sp.Function("Lf")(x), sp.symbols("Yv")
Fx, Ax, Bx = (F.subs(R, sp.exp(x)), A.subs({R: sp.exp(x), l: x}), B.subs(R, sp.exp(x)))
w = sp.exp(eps * x) * Lf
lhs = (Fx * sp.diff(w, x) - Ax * Yv - Bx * w) * sp.exp(-eps * x)
new = (Fx * sp.diff(Lf, x) - Lf / 2) - (Ax * sp.exp(-eps * x) * Yv + (Bx - half - eps * Fx) * Lf)
res_T = sp.simplify(sp.expand(lhs - new))

Ae = sp.expand(sp.series(A * sp.exp(-eps * l), eps, 0, 7).removeO())
Bm = sp.expand(B - half - eps * F)
Yser = sum(Ys[k] * eps**k for k in range(7))
Lser = sum(Ls[k] * eps**k for k in range(7))
rhsL = sp.expand(sp.series(Ae * Yser + Bm * Lser, eps, 0, 7).removeO())
rhsY = sp.expand(sp.series(eps * sp.exp(eps * l) * Lser, eps, 0, 7).removeO())
res = []
for k in range(7):
    res.append(sp.simplify(rhsL.coeff(eps, k) - o5.hk(k, Om, l, R, Ys, Ls)))
    if k >= 1:
        res.append(sp.simplify(rhsY.coeff(eps, k) - o5.Fsum(k, Ls, l)))
bad = [str(r_) for r_ in res if r_ != 0]
check("K1", res_T == 0 and not bad,
      f"transformation residual {res_T}; h_k (k = 0..6) and dY_k/dl (k = 1..6) against order6.py: "
      f"{'residual 0' if not bad else bad[:3]} ({time.time() - t0:.1f} s)")

# ---------------- K2: Taylor jets in v = sqrt(l), C_k integrated from the throat outward ----------------
mp.mp.dps = 70
N = 40
V = 9 if MUT == "short-V" else 17
Rinv = sp.symbols("Rinv")


def terms(expr):
    """expr polynomial in l, 1/R and Omega_i (degree <= 1 in them): [(coef, a, b, i or None)] for coef l^a Rinv^b (Omega_i)"""
    p = sp.Poly(sp.expand(expr.subs(R, 1 / Rinv)), l, Rinv, *Om)
    out = []
    for mon, c in p.terms():
        a, b, oms = mon[0], mon[1], mon[2:]
        assert sum(oms) <= 1
        out.append((mp.mpf(sp.Rational(c).p) / sp.Rational(c).q, a, b, oms.index(1) if sum(oms) else None))
    return out


CT = [terms(Ae.coeff(eps, m)) for m in range(7)]            # c_m, m = 0 (= 1/2) .. 6
BT = [terms(Bm.coeff(eps, m)) for m in range(7)]            # the L coefficient, by order
assert not BT[0] or all(c == 0 for c, *_ in BT[0])
AMAX = max(5, *[a for t in CT + BT for _, a, _, _ in t])
BMAX = max(0, *[b for t in CT + BT for _, _, b, _ in t])


def jmul(a, b):
    return [mp.fsum(a[j] * b[k - j] for j in range(k + 1)) for k in range(N + 1)]


def jadd(*xs):
    return [mp.fsum(z[k] for z in xs) for k in range(N + 1)]


def jscale(c, a):
    return [c * z for z in a]


def jexp(p):
    e = [mp.exp(p[0])] + [mp.mpf(0)] * N
    for k in range(1, N + 1):
        e[k] = mp.fsum(j * p[j] * e[k - j] for j in range(1, k + 1)) / k
    return e


def jsqrt(a):
    s = [mp.sqrt(a[0])] + [mp.mpf(0)] * N
    for k in range(1, N + 1):
        s[k] = (a[k] - mp.fsum(s[j] * s[k - j] for j in range(1, k))) / (2 * s[0])
    return s


def jdiv(n, d):
    q = []
    for k in range(N + 1):
        q.append((n[k] - mp.fsum(d[j] * q[k - j] for j in range(1, k + 1))) / d[0])
    return q


def jshift(a, m):
    """a / t^m when a's first m coefficients vanish analytically (dropped), padded with 0"""
    return a[m:] + [mp.mpf(0)] * m


def jint(a, c0):
    return [c0] + [a[k] / (k + 1) for k in range(N)]


def jeval(a, h):
    return mp.polyval(a[::-1], h)


def const(c):
    return [mp.mpf(c)] + [mp.mpf(0)] * N


def steps():
    v, out = mp.mpf(0), []
    while v < V:
        h = mp.mpf(1) / 8 if v < 3 else 1 / (2 * v)
        h = min(h, V - v)
        out.append((v, h))
        v += h
    return out


def precompute():
    pre = []
    for v0, h in steps():
        vj = [v0, mp.mpf(1)] + [mp.mpf(0)] * (N - 1)
        lj = jmul(vj, vj)
        E = jexp(lj)
        lp = [const(1)]
        for a in range(1, AMAX + 1):
            lp.append(jmul(lp[-1], lj))
        rp = [const(1)] + [jexp(jscale(-b, lj)) for b in range(1, BMAX + 1)]

        def mono(a, b):
            return jmul(lp[a], rp[b]) if b else lp[a]
        cj = [[(c, mono(a, b), i) for c, a, b, i in CT[m]] for m in range(7)]
        bj = [[(c, mono(a, b), i) for c, a, b, i in BT[m]] for m in range(7)]
        Em1 = jadd(E, const(-1))
        if v0 == 0:
            sig = jsqrt(jshift(Em1, 2))                          # sqrt((E - 1)/v^2)
            s = [mp.mpf(0)] + sig[:N]                            # v sig
            wfac = jdiv(jscale(2, E), jmul(sig, jmul(sig, sig)))  # times (h - h1)/v^2
        else:
            s = jsqrt(Em1)
            wfac = jdiv(jscale(2, jmul(vj, E)), jmul(s, jmul(s, s)))
        lfac = [jscale(1 / mp.factorial(j), lp[j]) for j in range(7)]
        pre.append((v0, h, vj, s, wfac, cj, bj, lfac))
    return pre


def jet_of(table, Oms):
    acc = [mp.mpf(0)] * (N + 1)
    for c, mj, i in table:
        f = c if i is None else c * Oms[i]
        if f != 0:
            acc = [acc[k] + f * mj[k] for k in range(N + 1)]
    return acc


def run(pre, Oms, kmax):
    Yv = [mp.mpf(1)] + [mp.mpf(0)] * kmax
    Cv = [mp.mpf(0)] * (kmax + 1)
    h1 = [None] * (kmax + 1)
    for v0, h, vj, s, wfac, cj, bj, lfac in pre:
        c = [jet_of(cj[m], Oms) for m in range(kmax + 1)]
        b = [jet_of(bj[m], Oms) for m in range(kmax + 1)]
        Yj, Lj, Cj = [const(1)], [], []
        for k in range(kmax + 1):
            if k >= 1:
                Fk1 = jadd(*[jmul(Lj[k - 1 - j], lfac[j]) for j in range(k)])
                Yj.append(jint(jscale(2, jmul(vj, Fk1)), Yv[k]))
            hk = jadd(*[jmul(c[k - j], Yj[j]) for j in range(k + 1)], *[jmul(b[m], Lj[k - m]) for m in range(1, k + 1)])
            if h1[k] is None:
                h1[k] = hk[0]
            q = jadd(hk, const(-h1[k]))
            integrand = jmul(wfac, jshift(q, 2) if v0 == 0 else q)
            Cj.append(jint(integrand, Cv[k]))
            Lj.append(jadd(const(-2 * h1[k]), jmul(s, Cj[k])))
        Yv = [jeval(Yj[k], h) for k in range(kmax + 1)]
        Cv = [jeval(Cj[k], h) for k in range(kmax + 1)]
    return Cv, h1


t0 = time.time()
pre = precompute()
print(f"K2: {len(pre)} steps to V = {V}, order {N}, {mp.mp.dps} digits; precompute {time.time() - t0:.1f} s", flush=True)
q2, pi, z3, z5 = mp.log(2), mp.pi, mp.zeta(3), mp.zeta(5)
Oms = [mp.mpf(0)] * 6
for k in (2, 3, 4, 5, 6):
    t1 = time.time()
    o = list(Oms)
    o[k - 2] = mp.mpf(0)
    g0 = run(pre, o, k)[0][k]
    o[k - 2] = mp.mpf(1)
    g1 = run(pre, o, k)[0][k]
    Oms[k - 2] = -g0 / (g1 - g0)
    print(f"  order {k}: G_{k}(0) = {mp.nstr(g0, 30)}, slope {mp.nstr(g1 - g0, 30)}, Omega{k - 2} = {mp.nstr(Oms[k - 2], 45)} ({time.time() - t1:.1f} s)", flush=True)
O0c = -4 * q2
O1c = 2 * pi**2 / 3 + 8 * q2**2
O2c = 80 * z3 - mp.mpf(8) / 3 * pi**2 * q2 - mp.mpf(32) / 3 * q2**3
O3c = 22 * pi**4 / 45 + mp.mpf(16) / 3 * pi**2 * q2**2 + mp.mpf(32) / 3 * q2**4 - 320 * z3 * q2 - 384 * z3
O4c = (-(0 if MUT == "drop-z5" else 10432 * z5) - 160 * pi**2 * z3 + 640 * q2**2 * z3 - mp.mpf(64) / 9 * pi**2 * q2**3
       - mp.mpf(88) / 45 * pi**4 * q2 - mp.mpf(128) / 15 * q2**5 - mp.mpf(2432) / 45 * pi**4 + 1536 * q2 * z3 + 3072 * z3)
d = [abs(Oms[0] - O0c), abs(Oms[1] - O1c), abs(Oms[2] - O2c), abs(Oms[3] - O3c)]
r4 = abs(Oms[4] - O4c) / abs(O4c)
check("K2", d[0] <= mp.mpf("1e-35") and d[1] <= mp.mpf("1e-33") and d[2] <= mp.mpf("1e-30") and d[3] <= mp.mpf("1e-30") and r4 <= mp.mpf("1e-25"),
      f"Omega0..Omega3 - closed: {', '.join(mp.nstr(x, 3) for x in d)}; Omega4 = {mp.nstr(Oms[4], 40)}, closed form {mp.nstr(O4c, 40)}, relative {mp.nstr(r4, 3)}")
FIT = mp.mpf("-12794.49986002")
check("K3", abs(O4c - FIT) <= mp.mpf("5e-10"), f"closed form minus #195's fit {FIT}: {mp.nstr(O4c - FIT, 3)}")
FIT14 = mp.mpf("-12794.499860023")                                   # A1: the 14-digit fit
check("K3b", abs(O4c - FIT14) <= mp.mpf("5e-10"), f"closed form minus #195's 14-digit fit {FIT14}: {mp.nstr(O4c - FIT14, 3)}")
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)

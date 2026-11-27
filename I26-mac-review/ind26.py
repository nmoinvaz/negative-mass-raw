#!/usr/bin/env python3
"""ind26: the order equations of #26 derived again from the l-system, and Omega0..Omega2 by a third evaluation
(criteria in README.md beside this file).

    python3 ind26.py [--mutate=NAME] [--wt=WORKTREE_NOTES_DIR]
"""
import argparse
import os
import re
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["k1-B", "short-V", "clausen"])
ap.add_argument("--wt", default="/Users/nathan/Source/negative-mass-r26/notes/wormhole_largeD")
A_ = ap.parse_args()
MUT = A_.mutate

saved, sys.argv = sys.argv, ["order4.py"]
sys.path.insert(0, A_.wt)
import order4 as o4  # noqa: E402  (the object under test: hk, cc, Fsum)
sys.argv = saved

RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


# ---------------- K1: the order equations from the l-system ----------------
t0 = time.time()
eps, l, R = sp.symbols("epsilon l R", positive=True)
Om = sp.symbols("Omega0:4")
Ys, Ls = sp.symbols("Y0:5"), sp.symbols("L0:5")
half = sp.Rational(1, 2)
F = 1 - 1 / R
Oser = sum(Om[i] * eps**i for i in range(4))
A = (1 + eps * Oser) * sp.exp(2 * eps * l) - (half + eps) * F - 1 / (2 * R)       # e^{-l} = 1/R
B = (half + (eps if MUT == "k1-B" else 2 * eps)) * F + 1 / (2 * R)

# w = e^{eps l} L: F w_l = A Y + B w becomes (R - 1) L_R - L/2 = A e^{-eps l} Y + (B - 1/2 - eps F) L,
# since F L_l = (1 - 1/R) R L_R = (R - 1) L_R.  Check the transformation itself on a generic L(l), Y:
x = sp.symbols("x", positive=True)
Lf, Yv = sp.Function("Lf")(x), sp.symbols("Yv")
Fx, Ax, Bx = (F.subs(R, sp.exp(x)), A.subs({R: sp.exp(x), l: x}), B.subs(R, sp.exp(x)))
w = sp.exp(eps * x) * Lf
lhs = (Fx * sp.diff(w, x) - Ax * Yv - Bx * w) * sp.exp(-eps * x)
new = (Fx * sp.diff(Lf, x) - Lf / 2) - (Ax * sp.exp(-eps * x) * Yv + (Bx - half - eps * Fx) * Lf)
res_T = sp.simplify(sp.expand(lhs - new))

Ae = sp.expand(sp.series(A * sp.exp(-eps * l), eps, 0, 5).removeO())
Bm = sp.expand(B - half - eps * F)
Yser = sum(Ys[k] * eps**k for k in range(5))
Lser = sum(Ls[k] * eps**k for k in range(5))
rhsL = sp.expand(sp.series(Ae * Yser + Bm * Lser, eps, 0, 5).removeO())
rhsY = sp.expand(sp.series(eps * sp.exp(eps * l) * Lser, eps, 0, 5).removeO())
res = []
for k in range(5):
    res.append(sp.simplify(rhsL.coeff(eps, k) - o4.hk(k, Om, l, R, Ys, Ls)))
    if k >= 1:
        res.append(sp.simplify(rhsY.coeff(eps, k) - o4.Fsum(k, Ls, l)))
bad = [str(r_) for r_ in res if r_ != 0]
check("K1", res_T == 0 and not bad,
      f"transformation residual {res_T}; h_k (k = 0..4) and dY_k/dl (k = 1..4) against order4.py: "
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


CT = [terms(Ae.coeff(eps, m)) for m in range(5)]            # c_m, m = 0 (= 1/2) .. 4
BT = [terms(Bm.coeff(eps, m)) for m in range(5)]            # the L coefficient, by order
assert not BT[0] or all(c == 0 for c, *_ in BT[0])
AMAX = max(4, *[a for t in CT + BT for _, a, _, _ in t])
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
        cj = [[(c, mono(a, b), i) for c, a, b, i in CT[m]] for m in range(5)]
        bj = [[(c, mono(a, b), i) for c, a, b, i in BT[m]] for m in range(5)]
        Em1 = jadd(E, const(-1))
        if v0 == 0:
            sig = jsqrt(jshift(Em1, 2))                          # sqrt((E - 1)/v^2)
            s = [mp.mpf(0)] + sig[:N]                            # v sig
            wfac = jdiv(jscale(2, E), jmul(sig, jmul(sig, sig)))  # times (h - h1)/v^2
        else:
            s = jsqrt(Em1)
            wfac = jdiv(jscale(2, jmul(vj, E)), jmul(s, jmul(s, s)))
        lfac = [jscale(1 / mp.factorial(j), lp[j]) for j in range(5)]
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
q2, pi, z3 = mp.log(2), mp.pi, mp.zeta(3)
Oms, G0, slope = [mp.mpf(0)] * 4, {}, {}
for k in (2, 3, 4):
    t1 = time.time()
    o = list(Oms)
    o[k - 2] = mp.mpf(0)
    g0 = run(pre, o, k)[0][k]
    o[k - 2] = mp.mpf(1)
    g1 = run(pre, o, k)[0][k]
    G0[k], slope[k] = g0, g1 - g0
    Oms[k - 2] = -g0 / (g1 - g0)
    print(f"  order {k}: G_{k}(0) = {mp.nstr(g0, 30)}, slope {mp.nstr(g1 - g0, 30)}, "
          f"Omega{k - 2} = {mp.nstr(Oms[k - 2], 45)} ({time.time() - t1:.1f} s)", flush=True)

O0c = -4 * q2
O1c = 2 * pi**2 / 3 + 8 * q2**2
O2c = 80 * z3 - mp.mpf(8) / 3 * pi**2 * q2 - mp.mpf(32) / 3 * q2**3
out = open(os.path.join(A_.wt, "order4_output.txt")).read()
A70 = mp.mpf(re.search(r"X1: Omega2 \(A70\) = ([0-9.]+)", out).group(1))
d0, d1, d2, d2a = (abs(Oms[0] - O0c), abs(Oms[1] - O1c), abs(Oms[2] - O2c), abs(Oms[2] - A70))
check("K2", d0 <= mp.mpf("1e-35") and d1 <= mp.mpf("1e-33") and d2 <= mp.mpf("1e-30") and d2a <= mp.mpf("1e-30"),
      f"Omega0 - (-4 ln 2) = {mp.nstr(d0, 3)}, Omega1 - closed = {mp.nstr(d1, 3)}, Omega2 - closed = {mp.nstr(d2, 3)}, "
      f"Omega2 - A70 = {mp.nstr(d2a, 3)} (A70 printed to {len(str(A70).split('.')[1])} decimals)")

# ---------------- K3: the derivation's statements against K2, and the Clausen integral ----------------
rel = lambda a, b: abs(a - b) / abs(b)  # noqa: E731
sl = {k: rel(slope[k], -4 * pi) for k in (2, 3, 4)}
G3c = 4 * pi / 3 * (-3 * Oms[0]**2 - 12 * Oms[0] * q2 + 24 * q2**2 + 2 * pi**2)
G4c = pi * (320 * z3 - mp.mpf(128) / 3 * q2**3 - mp.mpf(32) / 3 * pi**2 * q2)
r3, r4 = rel(G0[3], G3c), rel(G0[4], G4c)
mp.mp.dps = 60
cl = mp.quad(lambda xx: mp.cot(xx) * mp.clsin(2, 2 * xx), [0, mp.pi / 4, mp.pi / 2])   # x = pi/2 - theta
target = mp.pi**3 / 12 * (1 + (mp.mpf("1e-35") if MUT == "clausen" else 0))
dc = abs(cl - target)
check("K3", all(v <= mp.mpf("1e-30") for v in sl.values()) and r3 <= mp.mpf("1e-30") and r4 <= mp.mpf("1e-30")
      and dc <= mp.mpf("1e-40"),
      f"(a) slopes vs -4 pi, relative: {', '.join(f'k={k} {mp.nstr(v, 3)}' for k, v in sl.items())}; "
      f"(b) G3(Omega1=0) vs closed {mp.nstr(r3, 3)}, G4(Omega2=0) = {mp.nstr(G0[4], 25)} vs closed {mp.nstr(r4, 3)}; "
      f"(c) int tan Cl2(pi - 2 th) = {mp.nstr(cl, 25)}, minus pi^3/12: {mp.nstr(dc, 3)}")

bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)

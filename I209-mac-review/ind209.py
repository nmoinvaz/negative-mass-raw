#!/usr/bin/env python3
"""ind209: #209's exchange identities E1, E2, E3 evaluated on the coordinator's own Taylor-jet hierarchy (ind26, ind208),
which shares no code with method B (criteria in README.md beside this file).

    python3 ind209.py [--mutate=e1-factor|e2-weight|e3-Om0|k4-off]
"""
import argparse
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["e1-factor", "e2-weight", "e3-Om0", "k4-off"])
MUT = ap.parse_args().mutate
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


mp.mp.dps = 70
N = 40
V = 17
eps, l, R = sp.symbols("epsilon l R", positive=True)
Om = sp.symbols("Omega0:5")
Ys, Ls = sp.symbols("Y0:6"), sp.symbols("L0:6")
half = sp.Rational(1, 2)
F = 1 - 1 / R
Oser = sum(Om[i] * eps**i for i in range(5))
A = (1 + eps * Oser) * sp.exp(2 * eps * l) - (half + eps) * F - 1 / (2 * R)       # e^{-l} = 1/R
B = (half + 2 * eps) * F + 1 / (2 * R)

Ae = sp.expand(sp.series(A * sp.exp(-eps * l), eps, 0, 6).removeO())
Bm = sp.expand(B - half - eps * F)
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


CT = [terms(Ae.coeff(eps, m)) for m in range(6)]            # c_m, m = 0 (= 1/2) .. 5
BT = [terms(Bm.coeff(eps, m)) for m in range(6)]            # the L coefficient, by order
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
    """per step: v, h, jets of v, s, the C_k weight, c_m, the L coefficients, l^j/j!, dtheta/dv, ell, and 1/S (or its v = 0 form)"""
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
        cj = [[(c, mono(a, b), i) for c, a, b, i in CT[m]] for m in range(6)]
        bj = [[(c, mono(a, b), i) for c, a, b, i in BT[m]] for m in range(6)]
        Em1 = jadd(E, const(-1))
        ell = jscale(mp.mpf(-1) / 2, lj)                            # ln cos theta = -l/2
        if v0 == 0:
            sig = jsqrt(jshift(Em1, 2))                             # sqrt((E - 1)/v^2)
            s = [mp.mpf(0)] + sig[:N]
            wfac = jdiv(jscale(2, E), jmul(sig, jmul(sig, sig)))
            dth = jdiv(const(1), sig)                               # v/s = 1/sig
            invS = jdiv(E, jmul(sig, sig))                          # times (numerator)/v^2: 1/S = E/(v^2 sig^2)
        else:
            s = jsqrt(Em1)
            wfac = jdiv(jscale(2, jmul(vj, E)), jmul(s, jmul(s, s)))
            dth = jdiv(vj, s)
            invS = jdiv(E, Em1)
        lfac = [jscale(1 / mp.factorial(j), lp[j]) for j in range(6)]
        pre.append((v0, h, vj, s, wfac, cj, bj, lfac, dth, ell, invS))
    return pre


def jet_of(table, Oms):
    acc = [mp.mpf(0)] * (N + 1)
    for c, mj, i in table:
        f = c if i is None else c * Oms[i]
        if f != 0:
            acc = [acc[k] + f * mj[k] for k in range(N + 1)]
    return acc




def over_S(num, v0, invS):
    """num/sin^2 theta; at v0 = 0 num must vanish to order v^2"""
    return jmul(jshift(num, 2) if v0 == 0 else num, invS)


def run(pre, Oms, kmax):
    """the hierarchy (as ind208) plus the theta-integrals of E1 (k = 3..kmax), E2 and E3 (m = 2..kmax-1), to V"""
    Yv = [mp.mpf(1)] + [mp.mpf(0)] * kmax
    Cv = [mp.mpf(0)] * (kmax + 1)
    h1 = [None] * (kmax + 1)
    names = [f"E1a{k}" for k in range(3, kmax + 1)] + [f"E1b{k}" for k in range(3, kmax + 1)] + \
            [f"E1c{k}" for k in range(3, kmax + 1)] + [f"E2l{m}" for m in range(2, kmax)] + [f"E2r{m}" for m in range(2, kmax)] + \
            [f"E3l{m}" for m in range(2, kmax)] + [f"E3r{m}" for m in range(2, kmax)]
    I = {nm: mp.mpf(0) for nm in names}
    O0 = Oms[0] if MUT != "e3-Om0" else mp.mpf(0)
    shift = mp.ln2 if MUT == "e2-weight" else 0
    for v0, h, vj, s, wfac, cj, bj, lfac, dth, ell, invS in pre:
        c = [jet_of(cj[m], Oms) for m in range(kmax + 1)]
        b = [jet_of(bj[m], Oms) for m in range(kmax + 1)]
        Yj, Lj, Cj, Hj, Sj, Fj = [const(1)], [], [], [], [], [None]
        for k in range(kmax + 1):
            if k >= 1:
                Fk1 = jadd(*[jmul(Lj[k - 1 - j], lfac[j]) for j in range(k)])
                Fj.append(Fk1)
                Yj.append(jint(jscale(2, jmul(vj, Fk1)), Yv[k]))
            Sk = jadd(*[jmul(c[k - j], Yj[j]) for j in range(k)]) if k >= 1 else const(0)
            hk = jadd(Sk, jmul(c[0], Yj[k]), *[jmul(b[m], Lj[k - m]) for m in range(1, k + 1)])
            if h1[k] is None:
                h1[k] = hk[0]
            q = jadd(hk, const(-h1[k]))
            Cj.append(jint(jmul(wfac, jshift(q, 2) if v0 == 0 else q), Cv[k]))
            Lj.append(jadd(const(-2 * h1[k]), jmul(s, Cj[k])))
            Hj.append(hk)
            Sj.append(Sk)
        integ = {}
        for k in range(3, kmax + 1):
            integ[f"E1a{k}"] = Lj[k - 1]
            integ[f"E1b{k}"] = jadd(Fj[k], jscale(-1, Lj[k - 1]))          # F_{k-1} - L_{k-1}
            integ[f"E1c{k}"] = over_S(jadd(Sj[k], const(-Oms[k - 1])), v0, invS)
        for m in range(2, kmax):
            integ[f"E2l{m}"] = Lj[m]
            integ[f"E2r{m}"] = over_S(jmul(Hj[m], jadd(ell, const(shift))), v0, invS) if shift == 0 else \
                jadd(over_S(jmul(Hj[m], ell), v0, invS), jscale(shift, jmul(Hj[m], invS if v0 != 0 else const(0))))
            integ[f"E3l{m}"] = jadd(over_S(jmul(Yj[m], jadd(ell, const(-O0))), v0, invS), Yj[m])
            integ[f"E3r{m}"] = jmul(jadd(ell, const(-O0)), Fj[m])            # F_{m-1}
        for nm in names:
            I[nm] += jeval(jint(jmul(integ[nm], dth), mp.mpf(0)), h)
        Yv = [jeval(Yj[k], h) for k in range(kmax + 1)]
        Cv = [jeval(Cj[k], h) for k in range(kmax + 1)]
    return Cv, I


def agree(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1)


t0 = time.time()
pre = precompute()
q2, pi, z3 = mp.log(2), mp.pi, mp.zeta(3)
OM = [-4 * q2, 2 * pi**2 / 3 + 8 * q2**2, 80 * z3 - mp.mpf(8) / 3 * pi**2 * q2 - mp.mpf(32) / 3 * q2**3,
      22 * pi**4 / 45 + mp.mpf(16) / 3 * pi**2 * q2**2 + mp.mpf(32) / 3 * q2**4 - 320 * z3 * q2 - 384 * z3, mp.mpf(0)]
G, I = run(pre, OM, 5)
print(f"hierarchy to k = 5 with the closed-form Omegas: G_2..G_5 = {[mp.nstr(G[k], 3) for k in range(2, 6)]} ({time.time() - t0:.0f} s)",
      flush=True)
d1 = {}
for k in (3, 4, 5):
    rhs = (2 if MUT == "e1-factor" else 4) * I[f"E1a{k}"] + 2 * I[f"E1b{k}"] + 2 * I[f"E1c{k}"]
    d1[k] = agree(G[k], rhs)
for k in (3, 4, 5):                                          # off the root: Omega_{k-2} + 1/10, G_k != 0
    o = list(OM)
    o[k - 2] = o[k - 2] + mp.mpf(1) / 10
    Gk, Ik = run(pre, o, k)
    rhs = (2 if MUT == "e1-factor" else 4) * Ik[f"E1a{k}"] + 2 * Ik[f"E1b{k}"] + 2 * Ik[f"E1c{k}"]
    d1[f"{k} off"] = agree(Gk[k], rhs)
    print(f"  E1 off the root, k = {k}: G_k = {mp.nstr(Gk[k], 20)}, right side {mp.nstr(rhs, 20)}", flush=True)
check("K1", all(d <= mp.mpf("1e-30") for d in d1.values()),
      "E1: G_k against its right side: " + ", ".join(f"k={k} {mp.nstr(d, 3)}" for k, d in d1.items()))
d2 = {m: agree(I[f"E2l{m}"], 2 * I[f"E2r{m}"]) for m in (2, 3, 4)}
check("K2", all(d <= mp.mpf("1e-30") for d in d2.values()),
      "E2: " + ", ".join(f"m={m} {mp.nstr(I[f'E2l{m}'], 12)} vs {mp.nstr(2 * I[f'E2r{m}'], 12)} ({mp.nstr(d, 3)})" for m, d in d2.items()))
d3 = {m: agree(I[f"E3l{m}"], 2 * I[f"E3r{m}"]) for m in (2, 3, 4)}
check("K3", all(d <= mp.mpf("1e-30") for d in d3.values()),
      "E3: " + ", ".join(f"m={m} {mp.nstr(d, 3)}" for m, d in d3.items()))
OMs = list(OM)
if MUT != "k4-off":
    OMs[0] = OMs[0] + mp.mpf("1e-3")
Gs, Is = run(pre, OMs, 3)
d4 = agree(Is["E2l2"], 2 * Is["E2r2"])
check("K4", d4 > mp.mpf("1e-6"), f"with Omega0 + 1e-3 (G_2 = {mp.nstr(Gs[2], 4)}): E2 at m = 2 off by {mp.nstr(d4, 3)}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}  ({time.time() - t0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)

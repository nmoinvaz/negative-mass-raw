#!/usr/bin/env python3
"""ind171: the coordinator's independent check of #171 (criteria in README.md beside this file). Own Christoffel symbols,
Ricci and Einstein tensors; imports nothing from the negative-mass repository.

    python3 ind171.py [--mutate=NAME]
"""
import argparse
import sys
import time

import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["alpha-11", "phantom-sign", "uniq-claim", "p1-V"])
MUT = ap.parse_args().mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def einstein(g, X):
    gi = sp.simplify(g.inv())
    n = len(X)
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, c], X[b]) + sp.diff(g[d, b], X[c]) - sp.diff(g[b, c], X[d]))
                             for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]
    R = sp.zeros(n, n)
    for b in range(n):
        for d in range(b, n):
            e = 0
            for a in range(n):
                e += sp.diff(Gam[a][b][d], X[a]) - sp.diff(Gam[a][b][a], X[d])
                for k in range(n):
                    e += Gam[a][a][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][a]
            R[b, d] = R[d, b] = sp.simplify(e)
    Rs = sp.simplify(sum(gi[a, b] * R[a, b] for a in range(n) for b in range(n)))
    return (R - Rs * g / 2).applyfunc(sp.simplify), gi


def stress(g, gi, X, fields, V):
    """fields: list of (phi, sign) with sign +1 normal, -1 phantom."""
    n = len(X)
    T = sp.zeros(n, n)
    kin = 0
    for phi, s in fields:
        d = [sp.diff(phi, x) for x in X]
        kin += s * sum(gi[a, b] * d[a] * d[b] for a in range(n) for b in range(n)) / 2
        for a in range(n):
            for b in range(n):
                T[a, b] += s * d[a] * d[b]
    return T - g * (kin + V)


p, q, y, z = sp.symbols("p q y z", real=True)
c = sp.Symbol("c", nonzero=True, real=True)
H, J = sp.Function("H")(p), sp.Function("J")(q)
Xpq = (p, q, y, z)
gpq = sp.zeros(4, 4)
gpq[0, 1] = gpq[1, 0] = -sp.exp(2 * H * J)
gpq[2, 2] = gpq[3, 3] = 1
Gpq, gipq = einstein(gpq, Xpq)


def m1():
    al = 1 / (4 * sp.sqrt(2 * sp.pi))
    a1 = al * (sp.Rational(11, 10) if MUT == "alpha-11" else 1)
    s2 = 1 if MUT == "phantom-sign" else -1
    T = stress(gpq, gipq, Xpq, [(a1 * (c * H - 4 * J / c), 1), (al * (c * H + 4 * J / c), s2)], 0)
    res = (Gpq - 8 * sp.pi * T).applyfunc(lambda e: sp.simplify(sp.expand(e)))
    ok = res == sp.zeros(4, 4)
    nz = [(i, j) for i in range(4) for j in range(4) if res[i, j] != 0]
    check("M1", ok, f"G - 8 pi T = 0 for undefined H, J and symbolic c: {ok}" + ("" if ok else f"; nonzero {nz}")
          + f"; G is nonzero: {Gpq != sp.zeros(4, 4)}")


def m2():
    A1, A2, V = sp.symbols("A1 A2 V")
    s1, s2_ = sp.Symbol("s1", positive=True), sp.Symbol("s2", positive=True)  # alpha_i, with A_i = alpha_i^2
    T = stress(gpq, gipq, Xpq, [(s1 * (c * H - 4 * J / c), 1), (s2_ * (c * H + 4 * J / c), -1)], V)
    res = (Gpq - 8 * sp.pi * T)
    vals = {sp.Derivative(H, p, 2): 2, sp.Derivative(H, p): sp.Rational(1, 3), sp.Derivative(J, q, 2): 3,
            sp.Derivative(J, q): sp.Rational(-1, 5)}
    eqs = []
    for i in range(4):
        for j in range(i, 4):
            e = res[i, j].subs(vals).subs({H: sp.Rational(1, 2), J: 2, c: sp.Rational(3, 2)})
            e = sp.expand(e.subs({s1**2: A1, s2_**2: A2}))
            if e != 0:
                eqs.append(e)
    sol = sp.solve(eqs, [A1, A2, V], dict=True)
    want = sp.Rational(1, 16) / sp.pi if MUT == "uniq-claim" else sp.Rational(1, 32) / sp.pi
    ok = len(sol) == 1 and sp.simplify(sol[0].get(A1, A1) - want) == 0 and \
        sp.simplify(sol[0].get(A2, A2) - sp.Rational(1, 32) / sp.pi) == 0 and sp.simplify(sol[0].get(V, V)) == 0
    check("M2", ok, f"{len(eqs)} nonzero component equations; solutions {sol}; unique (1/(32 pi), 1/(32 pi), 0): {ok}")


def m3():
    tau, zz, R, Th = sp.symbols("tau z R Theta", positive=True)
    X = (tau, zz, R, Th)
    g = sp.diag(-1 / zz**2, 1 / zz**2, 1, R**2)
    G, gi = einstein(g, X)
    V = (1 if MUT == "p1-V" else -1) / (8 * sp.pi)
    f1, f2 = R * sp.cos(Th) / sp.sqrt(8 * sp.pi), R * sp.sin(Th) / sp.sqrt(8 * sp.pi)
    T = stress(g, gi, X, [(f1, 1), (f2, 1)], V)
    res = (G - 8 * sp.pi * T).applyfunc(sp.simplify)
    ok = res == sp.zeros(4, 4)
    check("M3", ok, f"#78's P1 with two normal scalars and V = {V}: G - 8 pi T = 0: {ok}")


print(f"ind171.py  mutate={MUT}", flush=True)
for fn in (m1, m2, m3):
    t1 = time.time()
    fn()
    print(f"[info] {fn.__name__} done in {time.time() - t1:.0f} s", flush=True)
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)

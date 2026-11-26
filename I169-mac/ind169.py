#!/usr/bin/env python3
"""ind169: the coordinator's independent check of #169 (criteria in README.md beside this file).

Own E = 8D for u = X1 R1 + X2 R2 + v from the jets, own coefficient matrices and ranks, own Groebner calls. Imports
nothing from the negative-mass repository.

    python3 ind169.py [--mutate=NAME]
"""
import argparse
import sys
import time
from fractions import Fraction

import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None,
                choices=["j1-v0", "j2-sign", "j3-claim", "j4-iota", "j5-factor", "j6-undivided", "j7-freq"])
MUT = ap.parse_args().mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def info(text):
    print(f"[info] {text} ({time.time() - T0:.0f} s)", flush=True)


A0, A1, A2, B0, B1, B2 = sp.symbols("A0 A1 A2 B0 B1 B2")
a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")
v = sp.Symbol("v")
XJ = (A0, A1, A2, B0, B1, B2)
RJ = (a0, a1, a2, b0, b1, b2)


def D_of(u, ux, uxx, ur, uxr, lap):
    """#65's D for a static or traveling shift, from u and its jets (lap = u_rr + u_r/rho)."""
    P = -(ux**2 + u * uxx)
    Q = -lap / 2
    Z = uxr / 2
    Y = ux * ur + u * uxr / 2
    h = ur**2 / 2
    return h * (h**2 - P**2 - Q**2 + Y**2 + Z**2) - P * (Y**2 - Z**2) + 2 * Q * Y * Z


def E_of(vv=v):
    u = A0 * a0 + B0 * b0 + vv
    return sp.expand(8 * D_of(u, A1 * a0 + B1 * b0, A2 * a0 + B2 * b0, A0 * a1 + B0 * b1, A1 * a1 + B1 * b1,
                              A0 * a2 + B0 * b2))


E = E_of(0 if MUT == "j1-v0" else v)
info("E built")


def j1():
    n = len(sp.Poly(E, *XJ, *RJ, v).terms())
    E1 = sp.expand(E.subs({B0: 0, B1: 0, B2: 0}))
    q, r = sp.div(sp.Poly(E1, *XJ, *RJ, v), sp.Poly(a1**2, *XJ, *RJ, v))
    ok = n == 376 and r.is_zero
    check("J1", ok, f"E has {n} terms (376: {n == 376}); E at X2 = 0 divisible by a1^2: {r.is_zero}")


def j2():
    P, Q, Z, Y, h = sp.symbols("P Q Z Y h")
    D = h * (h**2 - P**2 - Q**2 + Y**2 + Z**2) - P * (Y**2 - Z**2) + 2 * Q * Y * Z
    Aq = 2 * h * P + Y**2 - Z**2
    Bq = 2 * h * Q + (2 if MUT == "j2-sign" else -2) * Y * Z
    Cq = Y**2 + Z**2 + 2 * h**2
    ok = sp.expand(4 * h * D - (Cq**2 - Aq**2 - Bq**2)) == 0
    check("J2", ok, f"4hD = C^2 - A^2 - B^2 identically: {ok}")


def sep_rank(Ev):
    p = sp.Poly(Ev, *XJ, *RJ)
    rows, cols, ent = {}, {}, {}
    for mon, c in p.terms():
        xm, rm = mon[:6], mon[6:]
        i = rows.setdefault(xm, len(rows))
        j = cols.setdefault(rm, len(cols))
        ent[(i, j)] = c
    M = sp.zeros(len(rows), len(cols))
    for (i, j), c in ent.items():
        M[i, j] = c
    return M.rank(), M.shape


def j3():
    r0, s0 = sep_rank(sp.expand(E.subs(v, 0)))
    r3, s3 = sep_rank(sp.expand(E.subs(v, sp.Rational(1, 3))))
    want3 = 59 if MUT == "j3-claim" else 93
    ok = r0 == 59 and r3 == want3
    check("J3", ok, f"rank at v = 0: {r0} ({s0[0]} x {s0[1]}), want 59; rank at v = 1/3: {r3} ({s3[0]} x {s3[1]}), "
          f"want {want3}")


def j4():
    gam, dl, io = sp.symbols("gamma delta iota")
    fac = gam if MUT == "j4-iota" else gam + io
    Ek = sp.expand(E.subs({a2: fac * a1 + dl * a0, b2: fac * b1 + dl * b0}))
    p = sp.Poly(Ek, io)
    deg = p.degree()
    c2 = p.coeff_monomial(io**2)
    ur = A0 * a1 + B0 * b1
    ok = deg == 2 and sp.expand(c2 + ur**4) == 0
    check("J4", ok, f"degree in iota {deg} (2: {deg == 2}); iota^2 coefficient = -u_rho^4: {sp.expand(c2 + ur**4) == 0}")


def j5():
    k1, z1 = sp.symbols("k1 z1")
    Ez = sp.expand(E.subs({A0: z1, A1: k1 * z1, A2: k1**2 * z1, B0: 0, B1: 0, B2: 0}))
    c6 = sp.Poly(Ez, z1).coeff_monomial(z1**6)
    want = a1**2 * (a1**2 + 4 * k1**2 * a0**2) * ((a1**2 + 4 * k1**2 * a0**2) if MUT == "j5-factor"
                                                 else (a1**2 + 5 * k1**2 * a0**2))
    ok = sp.expand(c6 - want) == 0
    check("J5", ok, f"z1^6 coefficient = {sp.factor(c6)}; equals the claim: {ok}")


def j6():
    k1, k2, z1, z2, c1, t = sp.symbols("k1 k2 z1 z2 c1 t")
    Ez = sp.expand(E.subs({a0: c1, a1: 0, a2: 0, A0: z1, A1: k1 * z1, A2: k1**2 * z1,
                           B0: z2, B1: k2 * z2, B2: k2**2 * z2}))
    gens_all = (z1, z2, b0, b1, b2, c1, k1, k2, v)
    q, r = sp.div(sp.Poly(Ez, *gens_all), sp.Poly(z2**2 * b1**2, *gens_all))
    ok_div = r.is_zero
    Epp = q.as_expr()
    src = Ez if MUT == "j6-undivided" else Epp
    pz = sp.Poly(src, z1, z2)
    coeffs = {m: c for m, c in pz.terms()}
    ring_vars = (t, b0, b1, b2, c1, k1, k2, v)
    gens = list(coeffs.values())
    if MUT != "j6-undivided":
        gens.append(t * c1 * k1 * k2 * (k1 - k2) * b1 - 1)
    G = sp.groebner(gens, *ring_vars, order="grevlex", domain=sp.QQ)
    ok_a = list(G.exprs) == [1]
    info(f"J6 (a): {len(coeffs)} coefficients, basis {'[1]' if ok_a else str(len(G.exprs)) + ' elements'}")
    mons = list(sp.Poly(Epp, z1, z2).monoms())
    res = set()
    for (i, j) in mons:
        for (i2, j2) in mons:
            if i != i2:
                qq = Fraction(j2 - j, i - i2)
                if abs(qq) >= 1 and qq != 1:
                    res.add(qq)
    want = {Fraction(-2), Fraction(-1), Fraction(4, 3), Fraction(3, 2), Fraction(2), Fraction(3), Fraction(4)}
    ok_b = res == want
    ok_c, notes = True, []
    pE = sp.Poly(Epp, z1, z2)
    for qq in sorted(res):
        qs = sp.Rational(qq.numerator, qq.denominator)
        groups = {}
        for (i, j), c in pE.terms():
            f = qs * i + j
            groups[f] = groups.get(f, 0) + c
        gl = [sp.expand(g.subs(k1, qs * k2)) for g in groups.values()]
        gl = [g for g in gl if g != 0]
        gl.append(t * c1 * k2 * b1 - 1)
        Gq = sp.groebner(gl, t, b0, b1, b2, c1, k2, v, order="grevlex", domain=sp.QQ)
        okq = list(Gq.exprs) == [1]
        ok_c &= okq
        notes.append(f"{qq}: {'[1]' if okq else 'not unit'}")
    ok = ok_div and ok_a and ok_b and ok_c
    check("J6", ok, f"E = z2^2 b1^2 E'': {ok_div}; (a) generic unit ideal: {ok_a}; (b) resonant ratios "
          f"{sorted(str(x) for x in res)} = claimed: {ok_b}; (c) " + ", ".join(notes))


def j7():
    x, rho, c, eps, psi, dpsi = sp.symbols("x rho c epsilon psi dpsi")
    k = 1 if MUT == "j7-freq" else 2
    ddpsi = -dpsi / rho - k * c**2 * psi

    def jets(pert):
        g1 = -eps * dpsi / psi + (rho / 5 if pert else 0)
        g2 = -eps * (ddpsi / psi - dpsi**2 / psi**2) + (sp.Rational(1, 5) if pert else 0)
        return {A0: x, A1: 1, A2: 0, a0: c, a1: 0, a2: 0, B0: 1, B1: 0, B2: 0,
                b0: sp.Symbol("g0"), b1: g1, b2: g2 + g1 / rho}

    ok0 = True
    for e in (1, -1):
        val = sp.simplify(sp.together(E.subs(jets(False)).subs(eps, e)))
        ok0 &= val == 0
    pt = {c: sp.Rational(1, 2), eps: 1, psi: 1, dpsi: sp.Rational(1, 3), rho: 2}
    valp = sp.nsimplify(E.subs(jets(True)).subs(pt))
    ok1 = valp != 0
    check("J7", ok0 and ok1, f"additive u = cx + g, g = -eps ln psi on the Bessel equation: E = 0 for eps = +-1: {ok0}; "
          f"g + rho^2/10 at the exact point: E = {valp} (nonzero: {ok1})")


print(f"ind169.py  mutate={MUT}", flush=True)
for fn in (j1, j2, j3, j4, j5, j6, j7):
    t1 = time.time()
    fn()
    info(f"{fn.__name__} done in {time.time() - t1:.0f} s")
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)

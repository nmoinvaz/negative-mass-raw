#!/usr/bin/env python3
"""ind162: the coordinator's independent check of #162 (closure fails for the Bessel shift family).

Criteria R0-R4 in negative-mass-raw I162-mac/README.md. Imports nothing from the repository: own Ricci routine, own
Frobenius coefficient in coordinates, own elimination for Theorem 2.
"""
import argparse
import sys
import time

import sympy as sp

MUTS = ['pg', 'bsign', 'frob', 'poly', 'jet']
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.0f} s)", flush=True)
    if not ok:
        FAIL.append(name)


def christoffel_ricci(g, gi, D, simp=sp.cancel):
    n = g.shape[0]
    dg = [[[D[k](g[i, j]) for k in range(n)] for j in range(n)] for i in range(n)]
    G = [[[simp(sum(gi[a, d] * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d]) for d in range(n)) / 2)
           for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(b, n):
            e = sum(D[a](G[a][b][c]) - D[c](G[a][b][a]) for a in range(n))
            e += sum(G[a][a][d] * G[d][b][c] - G[a][c][d] * G[d][b][a] for a in range(n) for d in range(n))
            Ric[b, c] = Ric[c, b] = simp(e)
    return Ric


# R0 -------------------------------------------------------------------------------------------------------------
print("== R0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
bpg = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + bpg**2, bpg, 0, 0], [bpg, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify),
                        [lambda e, y=y: sp.diff(e, y) for y in (t_, rr, th_, ph_)], sp.simplify)
check('R0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# setup ------------------------------------------------------------------------------------------------------------
t, x = sp.symbols('t x', real=True)
rho = sp.Symbol('rho', positive=True)
phi = sp.Symbol('phi', real=True)
c = sp.Symbol('c', real=True, nonzero=True)
XS = [t, x, rho, phi]
gF = sp.Function('g')(rho)
u = c * x + gF
gp = sp.diff(gF, rho)
W = sp.sqrt(gp**2 + 2 * c**2)
G_, Ws = sp.symbols('G Ws')


def on_ode(e, eps):
    return e.subs(sp.Derivative(gF, (rho, 2)), eps * (gp**2 + 2 * c**2) - gp / rho)


def reduceW(e):
    """Replace g' by G and sqrt(G^2 + 2c^2) by Ws, then reduce Ws^2 = G^2 + 2c^2 in the numerator."""
    e = e.subs(gp, G_)
    e = e.subs(sp.sqrt(G_**2 + 2 * c**2), Ws)
    num, den = sp.fraction(sp.together(sp.expand(e)))
    num = sp.rem(sp.Poly(sp.expand(num), Ws), sp.Poly(Ws**2 - G_**2 - 2 * c**2, Ws)).as_expr()
    return sp.expand(num), den


# R1 -------------------------------------------------------------------------------------------------------------
print("\n== R1: R = a a - b b on the ODE ==", flush=True)
g = sp.Matrix([[-1 + u**2, u, 0, 0], [u, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, rho**2]])
gi = sp.Matrix([[-1, u, 0, 0], [u, 1 - u**2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho**2]])
R = christoffel_ricci(g, gi, [lambda e, v_=v_: sp.diff(e, v_) for v_ in XS], lambda e: sp.expand(sp.cancel(e)))


def covectors(eps):
    a = sp.Matrix([2 * c * u, 2 * c, gp, 0]) / sp.sqrt(2)
    nu = sp.Matrix([1 + (-1 if MUT == 'bsign' else 1) * eps * u, (-1 if MUT == 'bsign' else 1) * eps, 0, 0])
    b = W * nu / sp.sqrt(2)
    return a, b


r1 = []
for eps in (1, -1):
    a, b = covectors(eps)
    M = (a * a.T - b * b.T).applyfunc(sp.expand)
    ok = all(sp.simplify(on_ode(R[i, j], eps) - M[i, j]) == 0 for i in range(4) for j in range(4))
    r1.append(ok)
check('R1', all(r1), f"own Ricci on the ODE equals a a - b b for eps = +1, -1: {r1}")

# R2 -------------------------------------------------------------------------------------------------------------
print("\n== R2: the Frobenius coefficients ==", flush=True)


def frob(k):
    """coefficient of k ^ dk on dt ^ dx ^ drho for k = (k_t, k_x, k_rho, k_phi)."""
    d = lambda f, v_: sp.diff(f, v_)
    sgn = -1 if MUT == 'frob' else 1
    return (k[0] * (d(k[2], x) - d(k[1], rho)) + k[1] * (d(k[0], rho) - d(k[2], t))
            + sgn * k[2] * (d(k[1], t) - d(k[0], x)))


r_ = sp.Symbol('r')  # r = 1/rho in the closed forms
r2 = []
own = {}
for eps in (1, -1):
    a, b = covectors(eps)
    kt, mt = sp.sqrt(2) * (a + b), sp.sqrt(2) * (a - b)
    Fk, Fm = frob(kt), frob(mt)
    sumok = sp.simplify(Fk + Fm - 2 * gp * (gp**2 + 4 * c**2)) == 0
    Ok = gp * (gp**2 + 4 * c**2 + 5 * c * eps * W - 2 * c * gp / (rho * W))
    Om = gp * (gp**2 + 4 * c**2 - 5 * c * eps * W + 2 * c * gp / (rho * W))
    dk = reduceW(on_ode(Fk, eps) - Ok)[0]
    dm = reduceW(on_ode(Fm, eps) - Om)[0]
    own[eps] = (on_ode(Fk, eps), on_ode(Fm, eps))
    r2.append((sp.simplify(dk) == 0, sp.simplify(dm) == 0, sumok))
gpp0 = [sp.simplify((eps * (gp**2 + 2 * c**2) - gp / rho).subs(gp, 0) - 2 * eps * c**2) == 0 for eps in (1, -1)]
pl = [frob(sp.Matrix(v)) for v in ([0, 0, 1, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 0, x, 0])]
plok = pl[:3] == [0, 0, 0] and abs(pl[3]) == 1
r2ok = all(all(z) for z in r2) and all(gpp0) and plok
check('R2', r2ok, f"(O_k as printed, O_m as printed, sum = 2g'(g'^2+4c^2) without the ODE) for eps = +1, -1: {r2}; "
      f"g'' = 2 eps c^2 at g' = 0: {gpp0}; planted dr, dt, d(t+x), dt + x dr: {pl}: {plok}")

# R3 -------------------------------------------------------------------------------------------------------------
print("\n== R3: Theorem 2's elimination ==", flush=True)
ep = sp.Symbol('eps')
Pprinted = (G_**12 - (20 if MUT == 'poly' else 21) * c**2 * G_**10 - 78 * c**4 * G_**8 + 720 * c**6 * G_**6
            + 5936 * c**8 * G_**4 + 13056 * c**10 * G_**2 + 8704 * c**12)
r3 = []
for which in ('k', 'm'):
    for epsv in (1, -1):
        s = 1 if which == 'k' else -1
        H = (G_**2 + 4 * c**2) * Ws + s * 5 * c * epsv * Ws**2 - s * 2 * c * G_ * r_
        rstar = sp.solve(H, r_)[0]
        Gd = epsv * Ws**2 - G_ * r_
        rd = -r_**2
        Wd = G_ * Gd / Ws
        LH = sp.diff(H, G_) * Gd + sp.diff(H, r_) * rd + sp.diff(H, Ws) * Wd
        LH = sp.together(LH.subs(r_, rstar))
        num = sp.numer(LH)
        num = sp.rem(sp.Poly(sp.expand(num), Ws), sp.Poly(Ws**2 - G_**2 - 2 * c**2, Ws)).as_expr()
        pW = sp.Poly(sp.expand(num), Ws)
        p1 = pW.coeff_monomial(Ws)
        p0 = pW.coeff_monomial(1)
        N = sp.expand(p0**2 - p1**2 * (G_**2 + 2 * c**2))
        quo = sp.cancel(N / ((G_**2 + 2 * c**2) * Pprinted))
        qp = sp.Poly(quo, G_, c) if quo.is_polynomial(G_, c) else None
        ok = N != 0 and qp is not None and len(qp.terms()) == 1
        r3.append((which, epsv, ok, str(quo)))
check('R3', all(z[2] for z in r3), f"N / ((G^2 + 2c^2) P) is a nonzero monomial: {r3}")

# R4 -------------------------------------------------------------------------------------------------------------
print("\n== R4: exact jets ==", flush=True)


def at(eps, cv, Gv, rv):
    Fk, Fm = own[eps]
    sub = lambda e: sp.nsimplify(sp.simplify(e.subs(gp, Gv).subs({c: cv, rho: rv})))
    return sub(Fk), sub(Fm)


j1 = at(1, -2, 1, sp.Rational(4, 39))
j2 = at(1, 2, 1, sp.Rational(4, 39))
want1 = (0, 33 if MUT == 'jet' else 34)
r4a = tuple(j1) == want1 and tuple(j2) == (34, 0)
six = []
for (cv, Gv) in ((2, 1), (6, 17)):
    for eps in (1, -1):
        v = at(eps, cv, Gv, sp.Rational(5, 7))
        six.append(((cv, Gv, eps), v, v != (0, 0)))
# c = 0: the symbol c is nonzero, so evaluate the Frobenius coefficient afresh with c = 0
for eps in (1, -1):
    a0 = sp.Matrix([0, 0, gp, 0]) / sp.sqrt(2)
    nu0 = sp.Matrix([1 + eps * gF, eps, 0, 0])
    b0 = sp.sqrt(gp**2) * nu0 / sp.sqrt(2)
    Fk0 = frob(sp.sqrt(2) * (a0 + b0)).subs(sp.Derivative(gF, (rho, 2)), eps * gp**2 - gp / rho)
    Fm0 = frob(sp.sqrt(2) * (a0 - b0)).subs(sp.Derivative(gF, (rho, 2)), eps * gp**2 - gp / rho)
    v = (sp.simplify(Fk0.subs(gp, sp.Rational(1, 2))), sp.simplify(Fm0.subs(gp, sp.Rational(1, 2))))
    six.append(((0, sp.Rational(1, 2), eps), v, v == (sp.Rational(1, 8), sp.Rational(1, 8))))
r4b = all(z[2] for z in six)
check('R4', r4a and r4b, f"(-2, 1, 4/39, +1) -> {j1}, (2, 1, 4/39, +1) -> {j2}: {r4a}; #80's six jets: {six}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

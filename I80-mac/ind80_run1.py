#!/usr/bin/env python3
"""ind80: the coordinator's independent check of #80 (shifts with det R_3 = 0 on an open set).

Criteria K0-K9 in negative-mass-raw I80-mac/README.md. Imports nothing from the repository. D is built from #65's formula
D(P, Q, Z, Y, h), which I79-mac/ind79.py (H1) checked against the coordinator's own Ricci routine.
"""
import argparse
import random
import sys
import time

import mpmath as mp
import sympy as sp

MUTS = ['pg', 'ysign', 'travel', 'null', 'bessel', 'addf', 'cone3', 'series', 'far', 'msign']
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
FAIL = []
T0 = time.time()
mp.mp.dps = 60


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


def zero(e):
    return sp.expand(sp.cancel(sp.together(e))) == 0


t, x, rho, v, xi = sp.symbols('t x rho v xi', real=True)


def blocks(b):
    bx, br = sp.diff(b, x), sp.diff(b, rho)
    n = lambda f: sp.diff(f, t) - b * sp.diff(f, x)
    P = n(bx) - bx**2
    Q = -(sp.diff(b, rho, 2) + br / rho) / 2
    Z = sp.diff(b, x, rho) / 2
    Y = -n(br) / 2 + bx * br
    h = br**2 / 2
    return P, Q, Z, Y, h


def Dof(P, Q, Z, Y, h):
    return h * (h**2 - P**2 - Q**2 + Y**2 + Z**2) - P * (Y**2 - Z**2) + 2 * Q * Y * Z


def D(b):
    return Dof(*blocks(b))


# K0 -------------------------------------------------------------------------------------------------------------
print("== K0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
beta = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify), [lambda e, y=y: sp.diff(e, y) for y in
                                                                (t_, rr, th_, ph_)], sp.simplify)
check('K0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# K1 -------------------------------------------------------------------------------------------------------------
print("\n== K1: P = a_x, Y = (b_x b_rho - a_rho)/2; planar D = 0 ==", flush=True)
bF = sp.Function('b')(t, x, rho)
P, Q, Z, Y, h = blocks(bF)
a_ = sp.diff(bF, t) - bF * sp.diff(bF, x)
Yexp = (sp.diff(bF, x) * sp.diff(bF, rho) + (1 if MUT == 'ysign' else -1) * sp.diff(a_, rho)) / 2
k1a = zero(P - sp.diff(a_, x)) and zero(Y - Yexp)
bP = sp.Function('b')(t, x)
Pp, Qp, Zp, Yp, hp = blocks(bP)
k1b = all(zero(e) for e in (Qp, Zp, Yp, hp)) and zero(Dof(Pp, Qp, Zp, Yp, hp))
check('K1', k1a and k1b, f"P = a_x and Y as stated: {k1a}; planar h = Q = Z = Y = 0 and D = 0: {k1b}")

# K2 -------------------------------------------------------------------------------------------------------------
print("\n== K2: traveling = static with u = B + v; Galilean covariance ==", flush=True)
B = sp.Function('B')
D1 = D(B(x - v * t, rho)).subs(x, xi + v * t).doit()
D2 = D(B(x, rho) + (0 if MUT == 'travel' else v)).subs(x, xi).doit()
k2a = sp.expand(D1 - D2) == 0
cc = sp.Symbol('c', real=True)
G1 = D(bF.subs(x, x + cc * t) + cc).subs(x, xi - cc * t).doit()
G2 = D(bF).subs(x, xi).doit()
k2b = sp.expand(G1 - G2) == 0
check('K2', k2a and k2b, f"D(B(x - vt, rho)) = D_static(B + v): {k2a}; Galilean: {k2b}")

# K3 -------------------------------------------------------------------------------------------------------------
print("\n== K3: planar static u(x): R = (u u')' g_2, null coordinates, R_pq = -Phi/2 ==", flush=True)
uF = sp.Function('u')(x)
y_, z_ = sp.symbols('y z', real=True)
g4 = sp.Matrix([[-1 + uF**2, uF, 0, 0], [uF, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi4 = sp.Matrix([[-1, uF, 0, 0], [uF, 1 - uF**2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
R4 = christoffel_ricci(g4, gi4, [lambda e, y=y: sp.diff(e, y) for y in (t, x, y_, z_)], lambda e: sp.expand(sp.cancel(e)))
K = sp.diff(uF * sp.diff(uF, x), x)
g2 = g4.copy()
g2[2, 2] = g2[3, 3] = 0
k3a = all(zero(R4[i, j] - K * g2[i, j]) for i in range(4) for j in range(4))
Ap = 1 / (1 + uF) if MUT == 'null' else 1 / (1 - uF)
Bp = 1 / (1 + uF)
dp = sp.Matrix([1, -Ap])
dq = sp.Matrix([1, Bp])
k3b = all(zero(e) for e in (-(1 - uF**2) * (dp * dq.T + dq * dp.T) / 2 - g4[:2, :2]))
Jac = sp.Matrix.hstack(dp, dq).T  # rows dp, dq: d(p, q)/d(t, x)
Vinv = Jac.inv()  # columns d_p, d_q in (t, x)
Rpq = (Vinv[:, 0].T * R4[:2, :2] * Vinv[:, 1])[0, 0]
Phi = K * (1 - uF**2)
k3c = zero(Rpq + Phi / 2) and zero(Ap + Bp - 2 / (1 - uF**2))
check('K3', k3a and k3b and k3c, f"R = (u u')' g_2: {k3a}; -(1 - u^2) dp dq = g_2: {k3b}; R_pq = -Phi/2 and "
      f"s' = 2/(1 - u^2): {k3c}")

# K4 -------------------------------------------------------------------------------------------------------------
print("\n== K4: u = c x + g(rho): factorization, the Bessel reduction, points ==", flush=True)
gF = sp.Function('g')(rho)
u4 = cc * x + gF
D4 = D(u4)
g1, g2_ = sp.diff(gF, rho), sp.diff(gF, rho, 2)
S4 = g2_ + g1 / rho
k4a = zero(D4 - g1**2 * (2 * cc**2 + g1**2 - S4) * (2 * cc**2 + g1**2 + S4) / 8)
psi = sp.Function('psi')(rho)
k4b = True
for eps in (1, -1):
    gg = -eps * sp.log(psi)
    Sg = sp.diff(gg, rho, 2) + sp.diff(gg, rho) / rho
    Sg = Sg.subs(sp.Derivative(psi, (rho, 2)), -sp.diff(psi, rho) / rho - 2 * cc**2 * psi)
    k4b &= zero(Sg - eps * (sp.diff(gg, rho)**2 + 2 * cc**2))
rng = random.Random(8080)
vals = []
for (c0, eps) in ((mp.mpf(1) / 2, 1), (mp.mpf(1) / 2, -1), (mp.mpf(3) / 2, 1), (mp.mpf(3) / 2, -1),
                  (mp.mpf(0), 1), (mp.mpf(0), -1), (mp.mpf(0), 1), (mp.mpf(0), -1)):
    al, be = mp.mpf(rng.randint(1, 9)) / 7, mp.mpf(rng.randint(1, 9)) / 11
    rho0 = mp.mpf(rng.randint(2, 9)) / 7
    kk = c0 if MUT == 'bessel' else mp.sqrt(2) * c0
    if c0 != 0:
        ps = lambda r_: al * mp.besselj(0, kk * r_) + be * mp.bessely(0, kk * r_)
    else:
        ps = lambda r_: al + be * mp.log(r_)
    if ps(rho0) <= 0:
        al, be = abs(al) + 1, abs(be)
    gfun = lambda r_: -eps * mp.log(ps(r_))
    G1v, G2v = mp.diff(gfun, rho0, 1), mp.diff(gfun, rho0, 2)
    Pv, Qv, Zv, Yv, hv = -c0**2, -(G2v + G1v / rho0) / 2, 0, c0 * G1v, G1v**2 / 2
    Dv = hv * (hv**2 - Pv**2 - Qv**2 + Yv**2 + Zv**2) - Pv * (Yv**2 - Zv**2) + 2 * Qv * Yv * Zv
    vals.append(abs(Dv))
k4c = max(vals) < mp.mpf(10) ** -40
check('K4', k4a and k4b and k4c, f"D = g'^2 (2c^2 + g'^2 - S)(2c^2 + g'^2 + S)/8: {k4a}; Bessel reduction: {k4b}; "
      f"largest |D| at 8 points {mp.nstr(max(vals), 3)}")

# K5 -------------------------------------------------------------------------------------------------------------
print("\n== K5: additive u = X(x) + R(rho): D = h E, E = sum f_i g_i ==", flush=True)
XF, RF = sp.Function('X')(x), sp.Function('R')(rho)
P5, Q5, Z5, Y5, h5 = blocks(XF + RF)
X1, X2 = sp.diff(XF, x), sp.diff(XF, x, 2)
E5 = (h5 + X1**2)**2 - ((XF + RF) * X2)**2 - Q5**2
k5a = zero(Dof(P5, Q5, Z5, Y5, h5) - h5 * E5)
R1, R2 = sp.diff(RF, rho), sp.diff(RF, rho, 2)
A5, B5 = R1**2 / 2, (R2 + R1 / rho)**2 / 4
f = [1, X1**2, X2**2, XF * (X2 if MUT == 'addf' else X2**2), X1**4 - XF**2 * X2**2]
gl = [A5**2 - B5, 2 * A5, -RF**2, -2 * RF, 1]
k5b = zero(E5 - sum(fi * gi for fi, gi in zip(f, gl)))
check('K5', k5a and k5b, f"D = h E: {k5a}; E = sum f_i g_i: {k5b}")

# K6 -------------------------------------------------------------------------------------------------------------
print("\n== K6: conical u = F(x/rho): entries, degree-3 and degree-4 parts, k = 2 balance ==", flush=True)
FF = sp.Function('F')
eta = sp.Symbol('eta', real=True)
F0, F1, F2 = sp.symbols('F0 F1 F2', real=True)
u6 = FF(x / rho)
bl6 = blocks(u6)


def to_jets(e):
    e = e.subs(x, eta * rho).doit()
    rep = {}
    for d in e.atoms(sp.Subs):
        rep[d] = d.doit()
    e = e.xreplace(rep).doit()
    e = e.subs({sp.Derivative(FF(eta), (eta, 2)): F2}).subs({sp.Derivative(FF(eta), eta): F1}).subs({FF(eta): F0})
    return sp.expand(e)


blj = [to_jets(sp.expand(rho**2 * e)) for e in bl6]
w = F1 + eta * F2
want6 = [-(F1**2 + F0 * F2), -eta * w / 2, -w / 2, -(eta * F1**2 + F0 * w / 2), eta**2 * F1**2 / 2]
k6a = all(zero(a - b_) for a, b_ in zip(blj, want6)) and not any(e.has(rho) for e in blj)
N = sp.expand(8 * Dof(*blj))
lam = sp.Symbol('lam')
NL = sp.Poly(sp.expand(N.subs({F1: lam * F1, F2: lam * F2})), lam)
low3 = [NL.coeff_monomial(lam**k) for k in range(3)]
c3 = NL.coeff_monomial(lam**3)
want3 = 2 * F0 * w**2 * (((F0**2) if MUT == 'cone3' else (F0**2 - 1)) * F2 - eta * w)
NA = sp.Poly(sp.expand(N.subs({F0: lam * F0, F1: lam * F1, F2: lam * F2})), lam)
low4 = [NA.coeff_monomial(lam**k) for k in range(4)]
c4 = NA.coeff_monomial(lam**4)
want4 = -w**2 * ((eta**2 + 1) * (eta**2 + 2) * F1**2 + 2 * F0 * (eta * w + F2))
k6b = all(zero(e) for e in low3) and zero(c3 - want3) and all(zero(e) for e in low4) and zero(c4 - want4)
Finf, cK, ep = sp.symbols('F_inf c epsilon', real=True)
Fs = Finf + cK * eta**-2
Nk = sp.expand(N.subs({F0: Fs, F1: sp.diff(Fs, eta), F2: sp.diff(Fs, eta, 2)}).subs(eta, 1 / ep))
Pk = sp.Poly(sp.expand(Nk * ep**40), ep)
lead = [m_ for m_ in sorted(Pk.monoms()) if not zero(Pk.coeff_monomial(ep**m_[0]))][0][0]
LC = sp.factor(Pk.coeff_monomial(ep**lead))
k6c = zero(LC.subs(cK, -2 * Finf))
check('K6', k6a and k6b and k6c, f"entries: {k6a}; parts of degree 3 and 4 as printed, lower parts 0: {k6b}; leading "
      f"coefficient at eta^-{lead - 40} is {LC}, zero at c = -2 F_inf: {k6c}")

# K7 -------------------------------------------------------------------------------------------------------------
print("\n== K7: the power series on the branch a_2 = -2 F_inf ==", flush=True)
aa = sp.symbols('a3:7', real=True)
Fser = Finf - 2 * Finf * eta**-2 + sum(aa[k - 3] * eta**-k for k in range(3, 7))
Ns = sp.expand(N.subs({F0: Fser, F1: sp.diff(Fser, eta), F2: sp.diff(Fser, eta, 2)}).subs(eta, 1 / ep))
Ps = sp.Poly(sp.expand(Ns * ep**60), ep)
orders = sorted(set(m_[0] for m_ in Ps.monoms()))
solved, cond, log7 = {}, None, []
started = False
for o in orders:
    co = sp.expand(Ps.coeff_monomial(ep**o).subs(solved))
    if zero(co):
        continue
    free = sorted((s_ for s_ in co.free_symbols if s_ in aa), key=lambda s_: aa.index(s_))
    if not started:
        started = True
        lead7 = o
    if free:
        sol = sp.solve(co, free[0], dict=True)
        if len(sol) != 1:
            log7.append((o - 60, f"several or no solutions for {free[0]}: {sol}"))
            break
        solved[free[0]] = sol[0][free[0]]
        log7.append((o - 60, f"{free[0]} = {sp.factor(solved[free[0]])}"))
    else:
        cond = sp.factor(co)
        log7.append((o - 60, f"condition {cond}"))
        break
want7 = Finf**4 * (Finf**2 + (8 if MUT == 'series' else 7))
k7 = cond is not None and zero(sp.cancel(cond / want7).diff(Finf)) and not zero(cond)
check('K7', k7, f"order by order from eta^-{lead7 - 60}: {log7}; first condition proportional to "
      f"F_inf^4 (F_inf^2 + {'8' if MUT == 'series' else '7'}): {k7}")

# K8 -------------------------------------------------------------------------------------------------------------
print("\n== K8: far field ==", flush=True)
uinf, e8 = sp.symbols('u_inf e', real=True)
wF = sp.Function('w')(x, rho)
D8 = sp.expand(D(uinf + e8 * wF))
P8 = sp.Poly(D8, e8)
lowz = all(zero(P8.coeff_monomial(e8**k)) for k in range(3))
Zw = sp.diff(wF, x, rho) / 2
want8 = (1 if MUT == 'far' else -1) * uinf * Zw**2 * ((1 - uinf**2) * sp.diff(wF, x, 2) + sp.diff(wF, rho, 2)
                                                      + sp.diff(wF, rho) / rho)
k8 = lowz and zero(P8.coeff_monomial(e8**3) - want8)
check('K8', k8, f"e^0, e^1, e^2 vanish: {lowz}; e^3 coefficient as printed: {k8}")

# K9 -------------------------------------------------------------------------------------------------------------
print("\n== K9: the #158 remark, R - K g for a planar static shift ==", flush=True)
M9 = (R4 - K * g4).applyfunc(lambda e: sp.expand(sp.cancel(e)))
want9 = (1 if MUT == 'msign' else -1) * K * sp.diag(0, 0, 1, 1)
k9 = all(zero(M9[i, j] - want9[i, j]) for i in range(4) for j in range(4))
check('K9', k9, f"R - K g = -K (dy^2 + dz^2), so (+,+) iff K < 0: {k9}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

#!/usr/bin/env python3
"""ind158: the coordinator's independent check of #158 (shifts that pass the one-sign stage on an open set).

Criteria K0-K8 in negative-mass-raw I158-mac/README.md. Imports nothing from the repository: own Ricci routine, own
rank test, ideal computations, vector-field brackets and jet-space compatibility test.
"""
import argparse
import random
import sys
import time

import sympy as sp

MUTS = ['pg', 'Ysign', 'lemR', 'brho', 'growth', 'addP', 'multW', 'conEb', 'jet4']
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


def zero(e):
    return sp.expand(sp.cancel(sp.together(e))) == 0


ETA3 = sp.diag(-1, 1, 1)

# K0 -------------------------------------------------------------------------------------------------------------
print("== K0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
bpg = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + bpg**2, bpg, 0, 0], [bpg, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify),
                        [lambda e, y=y: sp.diff(e, y) for y in (t_, rr, th_, ph_)], sp.simplify)
check('K0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# K1 -------------------------------------------------------------------------------------------------------------
print("\n== K1: the block for b(t, x, rho) ==", flush=True)
t, x = sp.symbols('t x', real=True)
rho = sp.Symbol('rho', positive=True)
phi = sp.Symbol('phi', real=True)
XS = [t, x, rho, phi]
bF = sp.Function('b')(t, x, rho)
g = sp.Matrix([[-1 + bF**2, bF, 0, 0], [bF, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, rho**2]])
gi = sp.Matrix([[-1, bF, 0, 0], [bF, 1 - bF**2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho**2]])
simp = lambda e: sp.expand(sp.cancel(e))
R = christoffel_ricci(g, gi, [lambda e, v_=v_: sp.diff(e, v_) for v_ in XS], simp)
E = sp.Matrix([[1, 0, 0, 0], [-bF, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho]])  # columns n, d_x, d_rho, e_phi
RF = (E.T * R * E).applyfunc(simp)


def block(b, X=x, Rho=rho, T=t):
    """Printed entries (P, Q, Z, Y, h) for a shift expression b(T, X, Rho)."""
    n = lambda f: sp.diff(f, T) - b * sp.diff(f, X)
    bx, br = sp.diff(b, X), sp.diff(b, Rho)
    P = n(bx) - bx**2
    Q = -(sp.diff(b, Rho, 2) + br / Rho) / 2
    Z = sp.diff(b, X, Rho) / 2
    Y = (1 if MUT == 'Ysign' else -1) * n(br) / 2 + bx * br
    h = br**2 / 2
    return P, Q, Z, Y, h


def R3_of(P, Q, Z, Y, h):
    return sp.Matrix([[P - h, Q, Z], [Q, -P - h, Y], [Z, Y, h]])


R3p = R3_of(*block(bF))
k1a = all(zero(RF[i, j] - R3p[i, j]) for i in range(3) for j in range(3))
k1b = all(zero(RF[3, j]) for j in range(4))
check('K1', k1a and k1b, f"own frame Ricci equals the printed block: {k1a}; R(e_phi, .) = 0: {k1b}")

# K2 -------------------------------------------------------------------------------------------------------------
print("\n== K2: Lemma R ==", flush=True)
v0, v1, v2, lam = sp.symbols('v0 v1 v2 lambda', real=True)


def vblock(a0, a1, a2):
    P = (1 if MUT == 'lemR' else -1) * (a0**2 + a2**2)
    return P, -a0 * a1, -a0 * a2, -a1 * a2, (a0**2 + a1**2) / 2


Pv, Qv, Zv, Yv, hv = vblock(v0, v1, v2)
vv = sp.Matrix([v0, v1, v2])
k2a = (R3_of(Pv, Qv, Zv, Yv, hv) - (hv + v2**2) * ETA3 + vv * vv.T).applyfunc(sp.expand) == sp.zeros(3, 3)
P, Q, Z, Y, h = sp.symbols('P Q Z Y h', real=True)
A = Q * (Z**2 + Y**2) + 2 * h * Z * Y
B = P * Q * Y - Z * (Q**2 + Y**2)
w0, w1, w2 = -Q * Z / Y, -Q * Y / Z, -Z * Y / Q
k2b1 = zero(h - (w0 + w1) / 2 - A / (2 * Y * Z)) and zero(P + w0 + w2 - B / (Q * Y))
Qsol = sp.solve(A, Q)[0]
k2b2 = zero(Qsol * Y * Z + 2 * h * Y**2 * Z**2 / (Z**2 + Y**2))


def rank1_roots(R3):
    N = R3 - lam * ETA3
    mins = [sp.Poly(sp.expand(N[i, k] * N[j, l] - N[i, l] * N[j, k]), lam) for i in range(3) for j in range(i + 1, 3)
            for k in range(3) for l in range(k + 1, 3)]
    gg = mins[0]
    for m in mins[1:]:
        gg = sp.gcd(gg, m)
    if gg.degree() <= 0:
        return []
    return sorted({r for r in sp.roots(gg).keys() if r != 0})


rng = random.Random(158)
nz = lambda: sp.Rational(rng.choice([-1, 1]) * rng.randint(1, 9), rng.randint(1, 7))
good_v, good_g = 0, 0
for _ in range(30):
    a = (nz(), nz(), nz())
    blk = vblock(*a)
    rts = rank1_roots(R3_of(*blk))
    good_v += rts == [blk[4] + a[2]**2]
for _ in range(30):
    blk = (nz(), nz(), nz(), nz(), abs(nz()))
    good_g += rank1_roots(R3_of(*blk)) == []
check('K2', k2a and k2b1 and k2b2 and good_v == 30 and good_g == 30,
      f"N = -v v^T at h + v2^2: {k2a}; h - (v0^2+v1^2)/2 = A/(2YZ), P + v0^2 + v2^2 = B/(QY): {k2b1}; A = 0 gives "
      f"QYZ = -2h Y^2 Z^2/(Z^2+Y^2) < 0: {k2b2}; v-blocks with the single root h + v2^2: {good_v}/30; generic blocks "
      f"with none: {good_g}/30")

# helpers: kernel of the rank-1 block and involutivity -------------------------------------------------------------


def frame_vec(w, b):
    """Frame components (n, d_x, d_rho) -> coordinate components (t, x, rho, phi)."""
    return sp.Matrix([w[0], -b * w[0] + w[1], w[2], 0])


def bracket(Xv, Yv):
    return sp.Matrix([sum(Xv[m] * sp.diff(Yv[k], XS[m]) - Yv[m] * sp.diff(Xv[k], XS[m]) for m in range(4))
                      for k in range(4)])


def involutive(N, b):
    ker = N.nullspace(simplify=True)
    if len(ker) != 2:
        return None, len(ker)
    K1v, K2v = frame_vec(ker[0], b), frame_vec(ker[1], b)
    br = bracket(K1v, K2v).applyfunc(sp.simplify)
    Mx = sp.Matrix.hstack(K1v, K2v, br).applyfunc(sp.simplify)
    return Mx.rank(simplify=True) == 2, 2


# K3 -------------------------------------------------------------------------------------------------------------
print("\n== K3: b(rho) ==", flush=True)
Cc, b0, cc, dd = sp.symbols('C b0 c d', real=True)
Bf = sp.Function('B')(rho)
Pb, Qb, Zb, Yb, hb = block(Bf)
k3a = Pb == 0 and Zb == 0 and Yb == 0 and zero(Qb + (sp.diff(Bf, rho, 2) + sp.diff(Bf, rho) / rho) / 2)
blog = Cc * sp.log(rho) + b0 + (rho**2 / 10 if MUT == 'brho' else 0)
Pl, Ql, Zl, Yl, hl = block(blog)
k3b = all(zero(e) for e in (Pl, Ql, Zl, Yl))
blog0 = Cc * sp.log(rho) + b0
blk0 = block(blog0)
N3 = (R3_of(*blk0) - blk0[4] * ETA3).applyfunc(sp.simplify)
inv3, kd3 = involutive(N3.subs(Cc, 2), blog0.subs(Cc, 2))
check('K3', k3a and k3b and inv3 is False, f"P = Z = Y = 0, Q = -(b'' + b'/rho)/2: {k3a}; C ln rho + b0 has Q = 0: {k3b}; "
      f"kernel dimension {kd3}, involutive: {inv3}")

# K4 -------------------------------------------------------------------------------------------------------------
print("\n== K4: planar shifts and Theorem P ==", flush=True)
bp = sp.Function('b')(t, x)
Pp, Qp, Zp, Yp, hp = block(bp)
k4a = Qp == 0 and Zp == 0 and Yp == 0 and hp == 0
Ps = sp.Symbol('Ps', nonzero=True)
N4 = R3_of(Ps, 0, 0, 0, 0) - lam * ETA3
mins4 = [sp.Poly(sp.expand(N4[i, k] * N4[j, l] - N4[i, l] * N4[j, k]), lam) for i in range(3) for j in range(i + 1, 3)
         for k in range(3) for l in range(k + 1, 3)]
gg4 = mins4[0]
for m in mins4[1:]:
    gg4 = sp.gcd(gg4, m)
k4b = sp.expand(gg4.as_expr() - (lam + Ps)) == 0 or sp.expand(gg4.as_expr() + (lam + Ps)) == 0
kap, Dl = sp.symbols('kappa Delta', positive=True)
k4c = True
for sgn, hom, xcoef, vcoef in ((1, sp.cosh(kap * t), sp.cosh(kap * Dl), kap * sp.sinh(kap * Dl)),
                               (-1, sp.cos(kap * t), sp.cos(kap * Dl), -kap * sp.sin(kap * Dl))):
    ok_ode = zero(sp.diff(hom, t, 2) - sgn * kap**2 * hom) and hom.subs(t, 0) == 1 and sp.diff(hom, t).subs(t, 0) == 0
    claim_v = kap * sp.cosh(kap * Dl) if (MUT == 'growth' and sgn == 1) else vcoef
    ok_c = zero(hom.subs(t, Dl) - xcoef) and zero(sp.diff(hom, t).subs(t, Dl) - claim_v)
    k4c = k4c and ok_ode and ok_c
check('K4', k4a and k4b and k4c, f"planar block diag(P, -P, 0): {k4a}; rank-1 iff lambda = -P (gcd of minors "
      f"{gg4.as_expr()}): {k4b}; X-coefficients cosh/kappa sinh and cos/-kappa sin: {k4c}")

# K5 -------------------------------------------------------------------------------------------------------------
print("\n== K5: additive shifts ==", flush=True)
vs = sp.Symbol('v', real=True)
Xf, Rf = sp.Function('X')(x), sp.Function('R')(rho)
ua = Xf + Rf + vs
Pa, Qa, Za, Ya, ha = block(ua)
S_ = sp.diff(Rf, rho, 2) + sp.diff(Rf, rho) / rho
X1, X2 = sp.diff(Xf, x), sp.diff(Xf, x, 2)
R1 = sp.diff(Rf, rho)
Pclaim = (-X2 - X1**2) if MUT == 'addP' else (-ua * X2 - X1**2)
k5a = Za == 0 and zero(Ya - X1 * R1) and zero(Qa + S_ / 2) and zero(Pa - Pclaim) and zero(ha - R1**2 / 2)
us, x1, x2, r1, ss, tt, sat = sp.symbols('u x1 x2 r1 S t s')
Pj, Qj, Zj, Yj, hj = -us * x2 - x1**2, -ss / 2, sp.Integer(0), x1 * r1, r1**2 / 2
Irel = [Pj + v0**2 + v2**2, Qj + v0 * v1, Zj + v0 * v2, Yj + v1 * v2, hj - (v0**2 + v1**2) / 2]
gens5 = (tt, sat, v0, v1, v2, us, x1, x2, r1, ss)
k5b = []
for f in (v0, ss, us * x2):
    Gb = sp.groebner(Irel + [1 - sat * x1 * r1 * v2, 1 - tt * f], *gens5, order='grevlex')
    k5b.append(Gb.exprs == [1])
k5c_vals = {}
for Cv, cv in ((2, sp.Rational(3, 2)), (3, 1), (0, sp.Rational(3, 2))):
    ub = cv * x + Cv * sp.log(rho) + dd
    blk = block(ub)
    lamv = blk[4] + cv**2 if Cv != 0 else -blk[0]
    Nk = (R3_of(*blk) - lamv * ETA3).applyfunc(sp.simplify)
    k5c_vals[(Cv, str(cv))] = involutive(Nk, ub)
k5c = (k5c_vals[(2, '3/2')][0] is False and k5c_vals[(3, '1')][0] is False and k5c_vals[(0, '3/2')][0] is True)
check('K5', k5a and all(k5b) and k5c, f"additive block: {k5a}; v0, S, u X'' in the radical (saturated by X'R'v2): "
      f"{k5b}; involutive (kernel dim): {k5c_vals}")

# K6 -------------------------------------------------------------------------------------------------------------
print("\n== K6: multiplicative shifts ==", flush=True)
um = Xf * Rf + vs
Pm, Qm, Zm, Ym, hm = block(um)
Fm = Qm * (Zm**2 + Ym**2) + 2 * hm * Zm * Ym
Wm = (2 if MUT == 'multW' else 3) * Xf * Rf + vs
Fclaim = -Xf * X1**2 * R1**2 * (S_ * (1 + Wm**2) - 2 * Xf * R1**2 * Wm) / 8
k6a = zero(Fm - Fclaim)
Xs, Rs, R1s, Ss = sp.symbols('Xs Rs R1s Ss')
quad = sp.Poly(sp.expand(Ss * (1 + (3 * Xs * Rs + vs)**2) - 2 * Xs * R1s**2 * (3 * Xs * Rs + vs)), Xs)
coeffs = quad.all_coeffs()
Gm = sp.groebner(coeffs + [1 - tt * Rs * R1s], tt, Rs, R1s, Ss, vs, order='grevlex')
k6b = Gm.exprs == [1]
check('K6', k6a and k6b, f"F identity: {k6a}; quadratic coefficients with 1 - t R R' generate the unit ideal: {k6b}")

# K7 -------------------------------------------------------------------------------------------------------------
print("\n== K7: conical shifts ==", flush=True)
eta = sp.Symbol('eta', real=True)
Fc = sp.Function('F')
uc = Fc(x / rho) + vs
blkc = block(uc)
Uu, Gg, Hh = sp.symbols('U G H', real=True)


ww = Gg + eta * Hh
printed = (-(Gg**2 + Uu * Hh), -eta * ww / 2, -ww / 2, -(eta * Gg**2 + Uu * ww / 2), eta**2 * Gg**2 / 2)
k7a = True
for e, pv in zip(blkc, printed):
    e2 = (rho**2 * e).subs(x, eta * rho)
    e2 = e2.doit()
    e2 = e2.subs({sp.Derivative(Fc(eta), (eta, 2)): Hh, sp.Derivative(Fc(eta), eta): Gg}).subs(Fc(eta), Uu - vs)
    k7a = k7a and zero(e2 - pv)
p_, q_, z_, y_, h_ = printed
I7 = [p_ + v0**2 + v2**2, q_ + v0 * v1, z_ + v0 * v2, y_ + v1 * v2, h_ - (v0**2 + v1**2) / 2]
G7 = sp.groebner(I7, v0, v1, v2, Hh, Gg, Uu, eta, order='grevlex')
gsat = eta * Gg * Uu * ww * v0
Ea = ww * (1 + Uu**2) + 2 * eta * Uu * Gg**2
Eb = (eta**2 + 1) * eta * Hh + ((eta**2 + 1) if MUT == 'conEb' else (eta**2 - 1)) * Gg
kmem = []
for Ex in (Ea, Eb):
    found = None
    for k in range(0, 7):
        if G7.reduce(sp.expand(gsat**k * Ex))[1] == 0:
            found = k
            break
    kmem.append(found)
Cs = sp.Symbol('C', nonzero=True)
Gsol = Cs * eta / (eta**2 + 1)
Hsol = sp.diff(Gsol, eta)
Eb_at = Eb.subs({Gg: Gsol, Hh: Hsol})
Ea_at = Ea.subs({Gg: Gsol, Hh: Hsol})
k7c = zero(Eb_at) and zero(Ea_at - (2 * Gsol / (eta**2 + 1)) * (1 + Uu**2 + Cs * eta**2 * Uu))
Ust = -Cs * eta**2 / (2 * (eta**2 + 2))
k7d = zero(sp.diff(Ust, eta) - Gsol + Cs * eta * (eta**4 + 6 * eta**2 + 6) / ((eta**2 + 1) * (eta**2 + 2)**2))
k7 = k7a and None not in kmem and k7c and k7d
check('K7', k7, f"scaled entries as printed: {k7a}; E_a, E_b in the saturation (power of the saturating product "
      f"needed): {kmem}; G = C eta/(eta^2+1) solves E_b and factors E_a: {k7c}; F' - G at the critical F as printed: {k7d}")

# K8 -------------------------------------------------------------------------------------------------------------
print("\n== K8: static u_x rho != 0, jet compatibility ==", flush=True)
ORD = 4
J = {(i, j): sp.Symbol(f'u{i}{j}') for i in range(ORD + 1) for j in range(ORD + 1 - i)}
r_ = sp.Symbol('r', positive=True)


def Dx(e):
    return sum(sp.diff(e, J[(i, j)]) * J[(i + 1, j)] for (i, j) in J if i + j < ORD and sp.diff(e, J[(i, j)]) != 0)


def Dr(e):
    return sp.diff(e, r_) + sum(sp.diff(e, J[(i, j)]) * J[(i, j + 1)] for (i, j) in J
                                if i + j < ORD and sp.diff(e, J[(i, j)]) != 0)


def jet_test(e1, e2, pt, drop=False):
    """pt: values of r, u00, u10, u01, u11. Returns (n second-order solutions, third-order det, rank coef, rank aug)."""
    sub = {r_: pt[0], J[(0, 0)]: pt[1], J[(1, 0)]: pt[2], J[(0, 1)]: pt[3], J[(1, 1)]: pt[4]}
    sol2 = sp.solve([e1.subs(sub), e2.subs(sub)], [J[(2, 0)], J[(0, 2)]], dict=True)
    if len(sol2) != 1:
        return len(sol2), None, None, None
    sub.update(sol2[0])
    eq3 = [Dx(e1), Dr(e1), Dx(e2), Dr(e2)]
    un3 = [J[(3, 0)], J[(2, 1)], J[(1, 2)], J[(0, 3)]]
    M3 = sp.Matrix([[sp.diff(e, u_).subs(sub) for u_ in un3] for e in eq3])
    rhs3 = sp.Matrix([-(e.subs({u_: 0 for u_ in un3})).subs(sub) for e in eq3])
    det3 = sp.simplify(M3.det())
    if det3 == 0:
        return 1, det3, None, None
    s3 = M3.LUsolve(rhs3)
    sub.update({u_: sp.nsimplify(sp.simplify(s3[k])) for k, u_ in enumerate(un3)})
    eq4 = [Dx(Dx(e1)), Dx(Dr(e1)), Dr(Dr(e1)), Dx(Dx(e2)), Dx(Dr(e2)), Dr(Dr(e2))]
    if drop:
        eq4 = eq4[:3] + eq4[4:]
    un4 = [J[(4, 0)], J[(3, 1)], J[(2, 2)], J[(1, 3)], J[(0, 4)]]
    M4 = sp.Matrix([[sp.simplify(sp.diff(e, u_).subs(sub)) for u_ in un4] for e in eq4])
    rhs4 = sp.Matrix([sp.simplify(-(e.subs({u_: 0 for u_ in un4})).subs(sub)) for e in eq4])
    return 1, det3, M4.rank(), M4.row_join(rhs4).rank()


u00, u10, u01, u11, u20, u02 = (J[(0, 0)], J[(1, 0)], J[(0, 1)], J[(1, 1)], J[(2, 0)], J[(0, 2)])
Ps_ = -u00 * u20 - u10**2
Qs_ = -(u02 + u01 / r_) / 2
Zs_ = u11 / 2
Ys_ = u00 * u11 / 2 + u10 * u01
hs_ = u01**2 / 2
Aj = sp.expand(Qs_ * (Zs_**2 + Ys_**2) + 2 * hs_ * Zs_ * Ys_)
Bj = sp.expand(Ps_ * Qs_ * Ys_ - Zs_ * (Qs_**2 + Ys_**2))
drop = MUT == 'jet4'
PTS8 = [(1, 2, sp.Rational(1, 3), sp.Rational(3, 2), sp.Rational(5, 7)), (2, -1, 2, sp.Rational(1, 2), 3),
        (sp.Rational(3, 2), sp.Rational(1, 2), -1, 2, sp.Rational(1, 4))]
res8 = [jet_test(Aj, Bj, pt, drop) for pt in PTS8]
pl_ok = jet_test(u20, u02 + u01 / r_, (2, 1, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 5)), drop)
pl_bad = jet_test(u20 - u00**2, u02, (2, 1, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 5)), drop)
real_incons = all(rs[0] == 1 and rs[1] not in (None, 0) and rs[2] is not None and rs[3] > rs[2] for rs in res8)
planted = pl_ok[2] is not None and pl_ok[3] == pl_ok[2] and pl_bad[2] is not None and pl_bad[3] > pl_bad[2]
check('K8', real_incons and planted, f"static points (n sol2, det3, rank coef4, rank aug4): {res8}; planted consistent "
      f"{pl_ok}; planted inconsistent {pl_bad}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

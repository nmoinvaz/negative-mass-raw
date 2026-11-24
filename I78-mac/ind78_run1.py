#!/usr/bin/env python3
"""ind78: the coordinator's independent check of #78 (two same-sign scalars on the Alcubierre wall).

Criteria F0-F4 in negative-mass-raw I78-mac/README.md. Imports nothing from the repository. The Ricci routine, the polar
wall route and the Cartesian truncated-Taylor route are the coordinator's, copied from I77-mac/ind77.py. Rank tests by the
gcd and real roots of the 2 x 2 minors of R_3 - lam eta_3; the b(rho) system by sympy.solve.
"""
import argparse
import random
import sys
import time

import mpmath as mp
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.rings import ring

MUTS = ['pg', 'd2lam', 'r00', 'bconst', 'psd', 'accA', 'qh']
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
    """R_bc = d_a G^a_bc - d_c G^a_ba + G^a_ad G^d_bc - G^a_cd G^d_ba; D[k] is the partial derivative along x^k."""
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


def signs_exact(m):
    """(n+, n-, n0) of a real symmetric rational matrix: Descartes on its characteristic polynomial (real roots)."""
    x = sp.Symbol('x')
    p = sp.Poly(sp.Matrix(m).charpoly(x).as_expr(), x)
    n0 = 0
    while p.eval(0) == 0 and p.degree() > 0:
        p = sp.Poly(sp.cancel(p.as_expr() / x), x)
        n0 += 1
    cs = [c for c in p.all_coeffs() if c != 0]
    sc = lambda l: sum(1 for a, b in zip(l, l[1:]) if a * b < 0)
    neg = [c * (-1) ** (p.degree() - k) for k, c in enumerate(p.all_coeffs())]
    return sc(cs), sc([c for c in neg if c != 0]), n0


LAM = sp.Symbol('lam', real=True)
ETA3 = sp.diag(-1, 1, 1)


def minors2(N):
    return [N.extract([i, j], [k, l]).det() for i in range(3) for j in range(i + 1, 3) for k in range(3)
            for l in range(k + 1, 3)]


def common_real_root(R3):
    """Exact: does some real lam make every 2 x 2 minor of R3 - lam eta3 vanish?"""
    ms = [sp.expand(m) for m in minors2(sp.Matrix(R3) - LAM * ETA3)]
    ms = [m for m in ms if m != 0]
    if not ms:
        return True
    gg = ms[0]
    for m in ms[1:]:
        gg = sp.gcd(gg, m)
    gg = sp.Poly(gg, LAM)
    return gg.degree() > 0 and len(sp.real_roots(gg)) > 0


def common_real_root_mp(R3):
    """60 digits: at each real root of N00 N22 - N02^2, is some other minor relatively > 1e-20?"""
    a = [[mp.mpf(R3[i][j]) for j in range(3)] for i in range(3)]
    # N00 = a00 + lam, N22 = a22 - lam, N02 = a02: -lam^2 + (a22 - a00) lam + a00 a22 - a02^2
    co = [-1, a[2][2] - a[0][0], a[0][0] * a[2][2] - a[0][2] ** 2]
    rts = [mp.re(z) for z in mp.polyroots(co, extraprec=200) if abs(mp.im(z)) < mp.mpf(10) ** -40]
    for lam in rts:
        N = mp.matrix(a) - lam * mp.diag([-1, 1, 1])
        sc = max(abs(N[i, j]) for i in range(3) for j in range(3)) ** 2
        mins = [abs(N[i, k] * N[j, l] - N[i, l] * N[j, k]) / sc for i in range(3) for j in range(i + 1, 3)
                for k in range(3) for l in range(k + 1, 3)]
        if max(mins) <= mp.mpf(10) ** -20:
            return True
    return False


# ---------------------------------------------------------------------------------------------------------------
# F0: planted metrics through the own Ricci routine
# ---------------------------------------------------------------------------------------------------------------
print("== F0: planted metrics, own Ricci routine ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
beta = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Xpg = [t_, rr, th_, ph_]
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify), [lambda e, x=x: sp.diff(e, x) for x in Xpg],
                        sp.simplify)
ok_pg = Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4)

ta, zo, Ro, Tho, Xo, Yo = sp.symbols('tau z R Theta X Y', positive=True)
res0 = []
plane = sp.diag(0, 0, 1, Ro**2)  # dX^2 + dY^2 = dR^2 + R^2 dTheta^2
for name, conf, lam, s in (('P1', 1 / zo**2, -1, 1), ('P2', 1 / ta**2, 1, -1)):
    g = sp.diag(-conf, conf, 1, Ro**2)
    X = [ta, zo, Ro, Tho]
    Rc = christoffel_ricci(g, g.inv(), [lambda e, x=x: sp.diff(e, x) for x in X], sp.simplify)
    res0.append((name, (Rc - lam * g - s * plane).applyfunc(sp.simplify) == sp.zeros(4, 4)))
gam = sp.Rational(1, 10)
Ee = 1 + gam * (zo**2 - ta**2)
g = sp.diag(-1, 1, Ee**2, Ee**2)
X = [ta, zo, Xo, Yo]
Rc = christoffel_ricci(g, g.inv(), [lambda e, x=x: sp.diff(e, x) for x in X], sp.simplify)
lamD2 = (-3 if MUT == 'd2lam' else -4) * gam / Ee
res0.append(('D2', (Rc - lamD2 * g - 4 * gam**2 * (ta**2 - zo**2) * sp.diag(0, 0, 1, 1)).applyfunc(sp.simplify)
             == sp.zeros(4, 4)))
check('F0', ok_pg and all(ok for _, ok in res0), f"Painleve-Gullstrand Ricci-flat: {ok_pg}; {res0}")

# ---------------------------------------------------------------------------------------------------------------
# F1: the wall, polar route, generic w: entries, F, B, certificate
# ---------------------------------------------------------------------------------------------------------------
print("\n== F1: the wall, comoving polar coordinates, generic w(r) ==", flush=True)
r, S, C = sp.symbols('r S C', real=True)
W = sp.symbols('W0:7', real=True)
CIRC = S**2 + C**2 - 1


def Dr(e):
    return sp.diff(e, r) + sum(sp.diff(e, W[k]) * W[k + 1] for k in range(6))


def Dth(e):
    return C * sp.diff(e, S) - S * sp.diff(e, C)


def Dzero(e):
    return sp.S.Zero


def red(e):
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    num = sp.expand(sp.rem(sp.expand(num), CIRC, S))
    return num / den


w0 = W[0]
gW = sp.Matrix([[-1 + w0**2, w0 * C, -w0 * r * S, 0], [w0 * C, 1, 0, 0], [-w0 * r * S, 0, r**2, 0],
                [0, 0, 0, r**2 * S**2]])
giW = sp.Matrix([[-1, w0 * C, -w0 * S / r, 0], [w0 * C, 1 - w0**2 * C**2, w0**2 * C * S / r, 0],
                 [-w0 * S / r, w0**2 * C * S / r, (1 - w0**2 * S**2) / r**2, 0], [0, 0, 0, 1 / (r**2 * S**2)]])
RW = christoffel_ricci(gW, giW, [Dzero, Dr, Dth, Dzero], simp=red)
E = sp.Matrix([[1, 0, 0], [-w0 * C, C, S], [w0 * S / r, -S / r, C / r], [0, 0, 0]])  # columns n, d_x, d_rho
R3 = (E.T * RW * E).applyfunc(red)

W0, W1, W2 = W[:3]
u_ = r * W2 - W1
V_ = W0 * u_ + 2 * r * W1**2
z_ = 2 * W1 + u_ * S**2


def typed_entries(A=0):
    R00 = -(2 * W0 * W1 + (-2 if MUT == 'r00' else 2) * W0 * u_ * C**2 + r * W1**2 * (1 + C**2)) / (2 * r)
    if MUT != 'accA':
        R00 += A * W1 * C
    Rrr = W1**2 * S**2 / 2
    return sp.Matrix([[R00, -z_ / (2 * r), u_ * S * C / (2 * r)],
                      [-z_ / (2 * r), -R00 - 2 * Rrr, S * (V_ * C - A * r * W1) / (2 * r)],
                      [u_ * S * C / (2 * r), S * (V_ * C - A * r * W1) / (2 * r), Rrr]])


ent = typed_entries()
ent_ok = all(red(R3[i, j] - ent[i, j]) == 0 for i in range(3) for j in range(i, 3))
Fown = R3[0, 1] * (R3[0, 2]**2 + R3[1, 2]**2) + 2 * R3[2, 2] * R3[0, 2] * R3[1, 2]
Bt = -z_ * (u_**2 + V_**2) + 2 * r * u_ * V_ * W1**2 * (1 if MUT == 'bconst' else S**2)
F_ok = red(Fown - S**2 * C**2 * Bt / (8 * r**3)) == 0
Bp = sp.Poly(sp.expand(Bt), S)
affine = all(k[0] in (0, 2) for k in Bp.monoms())
const_ok = sp.expand(Bt.subs(S, 0) + 2 * W1 * (u_**2 + V_**2)) == 0
a00, a01, a0r, a1r, arr = sp.symbols('a00 a01 a0r a1r arr', real=True)
Ng = sp.Matrix([[a00, a01, a0r], [a01, -a00 - 2 * arr, a1r], [a0r, a1r, arr]]) - LAM * ETA3
md = Ng[0, 0] * Ng[1, 2] - Ng[0, 1] * Ng[0, 2]
me = Ng[1, 1] * Ng[0, 2] - Ng[0, 1] * Ng[1, 2]
Fg = a01 * (a0r**2 + a1r**2) + 2 * arr * a0r * a1r
cert_ok = sp.expand(a0r * md + a1r * me + Fg) == 0
check('F1', ent_ok and F_ok and affine and const_ok and cert_ok,
      f"entries as printed: {ent_ok}; F = s^2 c^2 B/(8 r^3): {F_ok}; B affine in s^2: {affine}; constant term "
      f"-2 w' (u^2 + V^2): {const_ok}; certificate R_0rho m_d + R_1rho m_e + F = 0: {cert_ok}")

# ---------------------------------------------------------------------------------------------------------------
# F2: re-solve at exact and 60-digit points of the wall
# ---------------------------------------------------------------------------------------------------------------
print("\n== F2: wall points: R_3 indefinite, no lam with rank(R_3 - lam eta_3) <= 1 ==", flush=True)
xr = sp.Symbol('xr', positive=True)
bump = (1 - xr**2 / 4)**3
ftanh = (sp.tanh(8 * (xr + 1)) - sp.tanh(8 * (xr - 1))) / (2 * sp.tanh(8))


def R3_exact(r0, s0, c0, Wj):
    return sp.Matrix(3, 3, lambda i, j: sp.cancel(R3[i, j].subs({r: r0, S: s0, C: c0, W0: Wj[0], W1: Wj[1], W2: Wj[2]})))


def jets_poly(fexpr, r0, v):
    return [v * (1 - fexpr.subs(xr, r0))] + [-v * sp.diff(fexpr, xr, k).subs(xr, r0) for k in (1, 2)]


EX = []
for (x0, y0, z0, r0) in [(4, 3, 0, 5), (-3, 0, 4, 5), (0, 3, 4, 5)]:
    c0, s0 = sp.Rational(x0, r0), sp.sqrt(sp.Rational(y0**2 + z0**2, r0**2))
    EX.append(('bump', 1, s0, c0, jets_poly(bump, 1, sp.Rational(7, 4))))
for vv in (1, sp.Rational(1, 2), sp.Rational(7, 4)):
    for r0 in (sp.Integer(1), sp.Rational(3, 2)):
        for (c0, s0) in ((sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(5, 13), sp.Rational(12, 13)),
                         (sp.Rational(-4, 5), sp.Rational(3, 5))):
            EX.append(('explicit', r0, s0, c0, jets_poly(bump, r0, vv)))
random.seed(2026)
for r0, (c0, s0) in zip((1, sp.Rational(3, 2), sp.Rational(2, 3), sp.Rational(5, 4)),
                        ((sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(-5, 13), sp.Rational(12, 13)),
                         (sp.Rational(8, 17), sp.Rational(15, 17)), (sp.Integer(0), sp.Integer(1)))):
    jets = [sp.Rational(random.randint(-9, 9), random.randint(1, 9)) for _ in range(5)]
    EX.append(('random', sp.S(r0), s0, c0, jets[:3]))
rows2, ok2 = [], True
for k, (lab, r0, s0, c0, Wj) in enumerate(EX):
    M3 = R3_exact(r0, s0, c0, Wj)
    if MUT == 'psd' and k == 0:
        n_ = sp.Matrix([1, 2, 1])
        wn = n_[0]**2 + n_[1]**2 + 2 * n_[2]**2
        M3 = -1 * ETA3 + sp.Rational(2) / wn * n_ * n_.T
    npos, nneg, _ = signs_exact(M3)
    crr = common_real_root(M3)
    ok = npos >= 1 and nneg >= 1 and not crr
    ok2 &= ok
    rows2.append((lab, ok))
for (x0, y0, z0, r0) in [(12, 3, 4, 13), (-12, 4, 3, 13), (0, 5, 12, 13), (5, 12, 0, 13), (-5, 0, 12, 13),
                         (9, 12, 0, 15)]:
    c0 = mp.mpf(x0) / r0
    s0 = mp.sqrt(mp.mpf(y0**2 + z0**2)) / r0
    for vv in (1, mp.mpf(1) / 2, 3):
        fk = [mp.mpf(sp.N(sp.diff(ftanh, xr, k).subs(xr, 1), 80)) for k in range(3)]
        Wj = [vv * (1 - fk[0]), -vv * fk[1], -vv * fk[2]]
        M3 = [[mp.mpf(sp.N(R3[i, j].subs({r: 1, S: s0, C: c0, W0: Wj[0], W1: Wj[1], W2: Wj[2]}), 70))
               for j in range(3)] for i in range(3)]
        ev = mp.eigsy(mp.matrix(M3))[0]
        ok = any(e > 0 for e in ev) and any(e < 0 for e in ev) and not common_real_root_mp(M3)
        ok2 &= ok
        rows2.append(('tanh', ok))
summ = {}
for lab, ok in rows2:
    summ.setdefault(lab, [0, 0])
    summ[lab][0] += 1
    summ[lab][1] += int(ok)
check('F2', ok2, "R_3 indefinite and no real lam with rank(R_3 - lam eta_3) <= 1: "
      + ", ".join(f"{lab} {v[1]} of {v[0]}" for lab, v in summ.items()))

# ---------------------------------------------------------------------------------------------------------------
# F3: the accelerating bubble, Cartesian route
# ---------------------------------------------------------------------------------------------------------------
print("\n== F3: accelerating bubble, Cartesian route: entries with A, rank, v_s = 0 block ==", flush=True)
Rg, Tg, Xg, Yg, Zg = ring('T X Y Z', QQ)
GENS = [Tg, Xg, Yg, Zg]


def trunc(p, n):
    return Rg.from_dict({m_: c for m_, c in p.items() if sum(m_) <= n})


def cart_R(vs, xs, t0, x0, y0):
    """Frame block R(E_a, E_b) on (n, d_x, d_y) at (t0, x0, y0, 0) of b = -v_s(t) (1 - Q/4)^3, exact."""
    tt = Rg(t0) + Tg
    Vt = sum((Rg(c) * tt**k for k, c in enumerate(vs)), Rg(0))
    Xs = sum((Rg(c) * tt**k for k, c in enumerate(xs)), Rg(0))
    Q = (Rg(x0) + Xg - Xs)**2 + Yg**2 + Rg(y0)**2 + 2 * Rg(y0) * Yg + Zg**2
    b = trunc(-Vt * (1 - Q * QQ(1, 4))**3, 2)
    b2 = trunc(b * b, 2)
    one, zero = Rg(1), Rg(0)
    g = [[b2 - one, b, zero, zero], [b, one, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    gi = [[-one, b, zero, zero], [b, one - b2, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    n = 4
    dg = [[[g[i][j].diff(GENS[k]) for k in range(n)] for j in range(n)] for i in range(n)]
    G = [[[trunc(sum((gi[a][d] * (dg[d][c][bb] + dg[d][bb][c] - dg[bb][c][d]) for d in range(n)), zero) * QQ(1, 2),
                 1) for c in range(n)] for bb in range(n)] for a in range(n)]
    co = lambda p: sp.Rational(str(dict(p).get((0, 0, 0, 0), QQ(0))))
    Ric = sp.zeros(4, 4)
    for bb in range(n):
        for c in range(n):
            e = sum((G[a][bb][c].diff(GENS[a]) - G[a][bb][a].diff(GENS[c]) for a in range(n)), zero)
            e += sum((G[a][a][d] * G[d][bb][c] - G[a][c][d] * G[d][bb][a] for a in range(n) for d in range(n)), zero)
            Ric[bb, c] = co(e)
    b0 = co(b)
    Ef = sp.Matrix([[1, 0, 0], [-b0, 1, 0], [0, 0, 1], [0, 0, 0]])
    return Ef.T * Ric * Ef, [Ric[3, m_] for m_ in range(4)]


def poly_at(cs, t0, k=0):
    p = sum(sp.Rational(str(c)) * xr**j for j, c in enumerate(cs))
    return sp.diff(p, xr, k).subs(xr, sp.Rational(str(t0)))


VS = [QQ(1), QQ(1, 2), QQ(1, 3)]
XSs = [QQ(0), QQ(1), QQ(1, 4), QQ(1, 5)]
ok3, rows3 = True, []
for (t0, x0, y0) in ((QQ(0), QQ(-5, 13), QQ(12, 13)), (QQ(0), QQ(9, 10), QQ(6, 5)), (QQ(1, 2), QQ(19, 16), QQ(4, 5))):
    R3c, rz = cart_R(VS, XSs, t0, x0, y0)
    xsv, vsv, dvs = poly_at(XSs, t0), poly_at(VS, t0), poly_at(VS, t0, 1)
    dx, yv = sp.Rational(str(x0)) - xsv, sp.Rational(str(y0))
    r0 = sp.sqrt(dx**2 + yv**2)
    wt = poly_at(XSs, t0, 1) - vsv * bump
    Wj = [wt.subs(xr, r0), sp.diff(wt, xr).subs(xr, r0), sp.diff(wt, xr, 2).subs(xr, r0)]
    A = dvs / vsv
    ty = typed_entries(A).subs({r: r0, S: yv / r0, C: dx / r0, W0: Wj[0], W1: Wj[1], W2: Wj[2]})
    eq = (R3c - ty).applyfunc(sp.simplify) == sp.zeros(3, 3)
    crr = common_real_root(R3c)
    ok = eq and all(x == 0 for x in rz) and not crr
    ok3 &= ok
    rows3.append(((str(t0), str(x0), str(y0)), r0, eq, crr))
vs0 = []
for (x0, y0) in ((QQ(3, 5), QQ(4, 5)), (QQ(-5, 13), QQ(12, 13))):
    R3c, _ = cart_R([QQ(0), QQ(1)], [QQ(0), QQ(0), QQ(1, 2)], QQ(0), x0, y0)
    r0 = sp.sqrt(sp.Rational(str(x0))**2 + sp.Rational(str(y0))**2)
    c0, s0 = sp.Rational(str(x0)) / r0, sp.Rational(str(y0)) / r0
    k = sp.diff(bump, xr).subs(xr, r0)  # v_s' = 1
    want = sp.Matrix([[-k * c0, 0, 0], [0, k * c0, k * s0 / 2], [0, k * s0 / 2, 0]])
    vs0.append((R3c - want).applyfunc(sp.simplify) == sp.zeros(3, 3))
check('F3', ok3 and all(vs0), f"3 points (t, x, y): entries as printed with A = v_s'/v_s {[x[2] for x in rows3]}, "
      f"a common real root of the minors {[x[3] for x in rows3]}; v_s = 0 block as printed at 2 points: {vs0}")

# ---------------------------------------------------------------------------------------------------------------
# F4: a shift b(rho)
# ---------------------------------------------------------------------------------------------------------------
print("\n== F4: shift b(rho): R_3, the rank-1 set, D3 = 2 ln rho ==", flush=True)
tt_, xx_, rho, phi = sp.symbols('t x rho phi', positive=True)
bf = sp.Function('b')(rho)
gb = sp.Matrix([[-1 + bf**2, bf, 0, 0], [bf, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, rho**2]])
gib = sp.Matrix([[-1, bf, 0, 0], [bf, 1 - bf**2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho**2]])
Xb = [tt_, xx_, rho, phi]
Rb = christoffel_ricci(gb, gib, [lambda e, x=x: sp.diff(e, x) for x in Xb], sp.simplify)
E4 = sp.Matrix([[1, 0, 0, 0], [-bf, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho]])  # n, d_x, d_rho, d_phi/rho
R4b = (E4.T * Rb * E4).applyfunc(sp.simplify)
hb = sp.diff(bf, rho)**2 / 2
Qb = -(sp.diff(bf, rho, 2) + sp.diff(bf, rho) / rho) / 2
form_ok = (R4b[:3, :3] - sp.Matrix([[-hb, Qb, 0], [Qb, -hb, 0], [0, 0, hb]])).applyfunc(sp.simplify) == sp.zeros(3, 3)
phi_ok = all(sp.simplify(R4b[3, m_]) == 0 for m_ in range(4))
hs = sp.Symbol('h', nonzero=True)
Qs = sp.Symbol('Q')
Ns = sp.Matrix([[-hs, Qs, 0], [Qs, -hs, 0], [0, 0, hs]]) - LAM * ETA3
sols = sp.solve([sp.expand(m) for m in minors2(Ns) if sp.expand(m) != 0], [LAM, Qs], dict=True)
want = [{LAM: hs, Qs: hs if MUT == 'qh' else 0}]
solve_ok = sols == want
d3 = []
bD3 = 2 * sp.log(rho)
R4d = R4b.subs(bf, bD3).doit().applyfunc(sp.simplify)
for r0 in (sp.Integer(2), sp.Rational(1, 2), sp.Integer(3)):
    hv = sp.Rational(2) / r0**2
    M4 = (R4d - hv * sp.diag(-1, 1, 1, 1)).subs(rho, r0).applyfunc(sp.simplify)
    npos, nneg, n0 = signs_exact(M4)
    K1 = sp.Matrix([1, -bD3, 0, 0])
    K2 = sp.Matrix([0, 0, 1, 0])
    br = sp.Matrix([sum(K1[a] * sp.diff(K2[m_], Xb[a]) - K2[a] * sp.diff(K1[m_], Xb[a]) for a in range(4))
                    for m_ in range(4)])
    Mc = (Rb.subs(bf, bD3).doit() - hv * gb.subs(bf, bD3)).subs(rho, r0).applyfunc(sp.simplify)
    kern = all(sp.simplify(x) == 0 for x in list(Mc * K1.subs(rho, r0)) + list(Mc * K2))
    rank3 = sp.Matrix.hstack(K1, K2, br).subs(rho, r0).rank(simplify=True) == 3
    d3.append((npos, nneg, n0) == (0, 2, 2) and kern and rank3)
check('F4', form_ok and solve_ok and all(d3),  # R(e_phi, .) = 0 is printed, not a criterion
      f"R_3 = [[-h, Q, 0], [Q, -h, 0], [0, 0, h]]: {form_ok}; R(e_phi, .) = 0 (printed): {phi_ok}; solve: {sols} "
      f"(expected {want}); D3 at 3 points, inertia (0, 2), kernel span(n, d_rho), bracket outside it: {d3}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

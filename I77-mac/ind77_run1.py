#!/usr/bin/env python3
"""ind77: the coordinator's independent check of #77 (three mixed-sign scalars on the Alcubierre wall).

Criteria B0-B5 in negative-mass-raw I77-mac/README.md. Imports nothing from the repository: own Christoffel and Ricci
routine (coordinates), own 3D Ricci from values and derivatives, own L_K M (Jacobi's formula for d lam, a bordered
system for dK), and a Cartesian route with truncated Taylor series for the accelerating bubble.
"""
import argparse
import os
import random
import re
import sys
import time

import mpmath as mp
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.rings import ring
from sympy.printing.lambdarepr import LambdaPrinter

MUTS = ['pg', 'p2lam', 'sph', 'd2shell', 'qtyped', 'flat', 'nodk', 'refl', 'xcheck', 'accflat']
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []
T0 = time.time()
mp.mp.dps = 60
TINY = mp.mpf(10) ** -30   # "= 0" for a relative size
SMALL = mp.mpf(10) ** -8   # "!= 0" for a relative size


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


def inv3(h):
    """Inverse of a 3 x 3 matrix (nested lists), any field."""
    a = h
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
           + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    cof = [[(a[(j + 1) % 3][(i + 1) % 3] * a[(j + 2) % 3][(i + 2) % 3]
             - a[(j + 1) % 3][(i + 2) % 3] * a[(j + 2) % 3][(i + 1) % 3]) for j in range(3)] for i in range(3)]
    return [[cof[i][j] / det for j in range(3)] for i in range(3)], det


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def ric3(h, dh, ddh):
    """Ricci tensor of a 3D metric at a point from h, dh[k] = d_k h, ddh[m][k] = d_m d_k h (nested lists)."""
    n = 3
    hi, _ = inv3(h)
    dhi = [[[-x for x in row] for row in mm(mm(hi, dh[k]), hi)] for k in range(n)]
    G = [[[sum(hi[a][d] * (dh[b][d][c] + dh[c][d][b] - dh[d][b][c]) for d in range(n)) / 2
           for c in range(n)] for b in range(n)] for a in range(n)]
    dG = [[[[sum(dhi[m][a][d] * (dh[b][d][c] + dh[c][d][b] - dh[d][b][c])
                 + hi[a][d] * (ddh[m][b][d][c] + ddh[m][c][d][b] - ddh[m][d][b][c]) for d in range(n)) / 2
             for c in range(n)] for b in range(n)] for a in range(n)] for m in range(n)]
    return [[sum(dG[a][a][b][c] - dG[c][a][b][a] for a in range(n))
             + sum(G[a][a][d] * G[d][b][c] - G[a][c][d] * G[d][b][a] for a in range(n) for d in range(n))
             for c in range(n)] for b in range(n)], hi


def amax(M):
    return max(abs(x) for row in M for x in row)


def inertia_exact(h):
    """(n+, n-) of a symmetric rational 3 x 3 matrix by Descartes on its characteristic polynomial (all roots real)."""
    m = sp.Matrix(h)
    p = [sp.Integer(1), -m.trace(), sum(m.extract([i, j], [i, j]).det() for i in range(3) for j in range(i + 1, 3)),
         -m.det()]
    sc = lambda cs: sum(1 for a, b in zip([x for x in cs if x != 0], [x for x in cs if x != 0][1:]) if a * b < 0)
    return sc(p), sc([p[0], -p[1], p[2], -p[3]])


# ---------------------------------------------------------------------------------------------------------------
# B0: planted metrics through the own Ricci routine
# ---------------------------------------------------------------------------------------------------------------
print("== B0: planted metrics, own Ricci routine ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
beta = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Xpg = [t_, rr, th_, ph_]
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify), [lambda e, x=x: sp.diff(e, x) for x in Xpg],
                        sp.simplify)
ok_pg = Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4)

T, Rr, Th, L = sp.symbols('T R Th L', real=True)
XS = [T, Rr, Th, L]
DS = [lambda e, x=x: sp.diff(e, x) for x in XS]


def sheared(a, fib=None):
    """dL^2 + a(L)^2 (-dt^2 + dR^2 + F(R) dTheta^2), t = T + L/3, Theta = Th + L/5; returns g, the fiber 1-forms."""
    F = Rr**2 if fib is None else fib
    dt = sp.Matrix([1, 0, 0, sp.Rational(1, 3)])
    dR = sp.Matrix([0, 1, 0, 0])
    dTh = sp.Matrix([0, 0, 1, sp.Rational(1, 5)])
    dL = sp.Matrix([0, 0, 0, 1])
    g = dL * dL.T + a**2 * (-dt * dt.T + dR * dR.T + F * dTh * dTh.T)
    Theta = Th + L / 5
    tt = T + L / 3
    X = [tt, Rr * sp.cos(Theta), Rr * sp.sin(Theta)]
    dX = [sp.Matrix([sp.diff(Xi, x) for x in XS]) for Xi in X]
    return g, dX


def ricci_sheared(g):
    return christoffel_ricci(g, g.inv().applyfunc(sp.simplify), DS, sp.simplify)


def zero_ex(e):
    d = sp.simplify(e)
    return d == 0 or sp.simplify(d.rewrite(sp.exp)) == 0


res0 = []
for name, a, lam, k2, sg in (('P1', L, 0, 2, (1, -1, -1)), ('P2', sp.cosh(L) / sp.sqrt(2), -3, 1, (-1, 1, 1))):
    if MUT == 'p2lam' and name == 'P2':
        lam = -2
    g, dX = sheared(a)
    Rs = ricci_sheared(g)
    target = lam * g + k2 * sum((sg[i] * dX[i] * dX[i].T for i in range(3)), sp.zeros(4, 4))
    res0.append((name, all(zero_ex(e) for e in (Rs - target))))
check('B0', ok_pg and all(ok for _, ok in res0),
      f"Painleve-Gullstrand Ricci-flat: {ok_pg}; R = lam g + kappa^2 sum s_I dX dX exactly: {res0}")

# ---------------------------------------------------------------------------------------------------------------
# B1: planted 3D Ricci and L_K M
# ---------------------------------------------------------------------------------------------------------------
print("\n== B1: planted 3D Ricci and L_K M ==", flush=True)


def ric3_symbolic(hs, X, pt, exact=True):
    """Ric of a symbolic 3D metric hs in coordinates X at the point pt, through ric3 (values and derivatives only)."""
    ev = (lambda e: sp.nsimplify(e.subs(pt)) if exact else mp.mpf(sp.N(e.subs(pt), 70)))
    h = [[ev(hs[i, j]) for j in range(3)] for i in range(3)]
    dh = [[[ev(sp.diff(hs[i, j], X[k])) for j in range(3)] for i in range(3)] for k in range(3)]
    ddh = [[[[ev(sp.diff(hs[i, j], X[m], X[k])) for j in range(3)] for i in range(3)] for k in range(3)]
           for m in range(3)]
    return ric3(h, dh, ddh)[0]


a3 = sp.symbols('a3', real=True)
ok1 = []
Ric = ric3_symbolic(sp.diag(-1, 1, Rr**2), [T, Rr, Th], {Rr: sp.Rational(3, 2)})
ok1.append(('flat polar', all(x == 0 for row in Ric for x in row)))
Ric = ric3_symbolic(sp.diag(-1, 1, sp.sin(Th)**2), [T, Rr, Th], {Th: sp.acos(sp.Rational(3, 5))})
want = [[0, 0, 0], [0, 2 if MUT == 'sph' else 1, 0], [0, 0, sp.Rational(16, 25)]]
ok1.append(('sphere x time', all(sp.simplify(Ric[i][j] - want[i][j]) == 0 for i in range(3) for j in range(3))))
PTS_S = [{T: 0, Rr: 1, Th: 0, L: sp.Rational(1, 2)}, {T: sp.Rational(1, 3), Rr: 2, Th: sp.Rational(1, 5), L: 1},
         {T: -1, Rr: sp.Rational(1, 2), Th: 1, L: sp.Rational(3, 2)}]
for name, a, lam, fib, expect_flat in (('P1', L, 0, None, True), ('P2', sp.cosh(L) / sp.sqrt(2), -3, None, True),
                                       ('D1', L, 0, Rr**2 * (1 + Rr**2 / 10), False)):
    g, _ = sheared(a, fib)
    Ms = (ricci_sheared(g) - lam * g).applyfunc(sp.simplify)
    hs = Ms.extract([1, 2, 3], [1, 2, 3])  # slice T = const, coordinates (R, Th, L)
    flats = []
    for p in PTS_S:
        Rc = ric3_symbolic(hs, [Rr, Th, L], p, exact=False)
        rel = amax(Rc) / max(amax([[mp.mpf(sp.N(hs[i, j].subs(p), 70)) for j in range(3)] for i in range(3)]), 1)
        flats.append(rel < TINY)
    ok1.append((f"{name} block flat at 3 points = {expect_flat}", all(f == expect_flat for f in flats)))


def lie_KM(Rv, gv, dR, dg, lam, nodk=False):
    """L_K M of M = R - lam(x) g along its kernel field K, at a point, from values and first derivatives (mp).
    d lam from Jacobi's formula, dK from the bordered system (dN) K + N dK = 0, K^T dK = 0."""
    n = 4
    N = Rv - lam * gv
    adj = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            minor = mp.matrix([[N[a, b] for b in range(n) if b != i] for a in range(n) if a != j])
            adj[i, j] = (-1) ** (i + j) * mp.det(minor)
    cols = [[adj[i, j] for i in range(n)] for j in range(n)]
    K = mp.matrix(max(cols, key=lambda col: sum(x * x for x in col)))
    K = K / mp.norm(K)
    tr = lambda A, B: sum(A[i, j] * B[j, i] for i in range(n) for j in range(n))
    Plam = -tr(adj, gv)
    dlam = [-tr(adj, dR[k] - lam * dg[k]) / Plam for k in range(n)]
    dN = [dR[k] - lam * dg[k] - dlam[k] * gv for k in range(n)]
    A = mp.matrix(n + 1, n)
    for i in range(n):
        for j in range(n):
            A[i, j] = N[i, j]
    for j in range(n):
        A[n, j] = K[j]
    dK, resid = [], mp.mpf(0)
    for k in range(n):
        rhs = mp.matrix(n + 1, 1)
        v_ = -(dN[k] * K)
        for i in range(n):
            rhs[i] = v_[i]
        x = mp.lu_solve(A.T * A, A.T * rhs)
        resid = max(resid, mp.norm(A * x - rhs))
        dK.append(x)
    LKM = mp.matrix(n, n)
    scale = mp.mpf(0)
    for m_ in range(n):
        for v2 in range(n):
            t1 = sum(K[a] * dN[a][m_, v2] for a in range(n))
            t2 = sum(N[a, v2] * dK[m_][a] for a in range(n))
            t3 = sum(N[m_, a] * dK[v2][a] for a in range(n))
            LKM[m_, v2] = t1 if nodk else t1 + t2 + t3
            scale = max(scale, abs(t1) + abs(t2) + abs(t3))
    rel = max(abs(LKM[i, j]) for i in range(n) for j in range(n)) / scale
    ident = mp.norm(LKM * K) / scale
    Klam = sum(K[a] * dlam[a] for a in range(n))
    dl = max(abs(x) for x in dlam)
    relK = abs(Klam) / dl if dl > 0 else mp.mpf(0)
    nullK = mp.norm(N * K) / max(abs(N[i, j]) for i in range(n) for j in range(n))
    return dict(rel=rel, ident=ident, relK=relK, resid=resid, nullK=nullK, K=K)


def sym_point(Rs, gs, X, p):
    ev = lambda e: mp.mpf(sp.N(e.subs(p), 70))
    Rv = mp.matrix([[ev(Rs[i, j]) for j in range(4)] for i in range(4)])
    gv = mp.matrix([[ev(gs[i, j]) for j in range(4)] for i in range(4)])
    dR = [mp.matrix([[ev(sp.diff(Rs[i, j], x)) for j in range(4)] for i in range(4)]) for x in X]
    dg = [mp.matrix([[ev(sp.diff(gs[i, j], x)) for j in range(4)] for i in range(4)]) for x in X]
    return Rv, gv, dR, dg


def real_roots_pencil(Rv, gv):
    """Real roots of det(R - lam g) (degree 4) from 5 values and a Vandermonde solve."""
    xs = [mp.mpf(k) for k in range(5)]
    ys = [mp.det(Rv - x * gv) for x in xs]
    V = mp.matrix([[x ** (4 - j) for j in range(5)] for x in xs])
    co = mp.lu_solve(V, mp.matrix(ys))
    rts = mp.polyroots([co[i] for i in range(5)], maxsteps=400, extraprec=400)
    return [mp.re(z) for z in rts if abs(mp.im(z)) < mp.mpf(10) ** -40 * (1 + abs(z))]


p_lk = {T: 0, Rr: 1, Th: 0, L: sp.Rational(1, 2)}
for name, a, want_zero in (('P2', sp.cosh(L) / sp.sqrt(2), True),
                           ("D2'", sp.cosh(L) / sp.sqrt(2) if MUT == 'd2shell' else 1 + L**2 / 2, False)):
    g, _ = sheared(a)
    Rs = ricci_sheared(g)
    Rv, gv, dR, dg = sym_point(Rs, g, XS, p_lk)
    lam_exp = mp.mpf(sp.N((-3 * sp.diff(a, L, 2) / a).subs(p_lk), 70))
    lam0 = min(real_roots_pencil(Rv, gv), key=lambda x: abs(x - lam_exp))
    out = lie_KM(Rv, gv, dR, dg, lam0, nodk=(MUT == 'nodk'))
    ok = (out['rel'] < TINY) if want_zero else (out['rel'] > SMALL)
    ok1.append((f"{name}: lam = {mp.nstr(lam0, 8)}, L_K M rel {mp.nstr(out['rel'], 3)}, (L_K M)(K,.) rel "
                f"{mp.nstr(out['ident'], 3)}", ok and out['ident'] < TINY and abs(lam0 - lam_exp) < TINY))
check('B1', all(ok for _, ok in ok1), "; ".join(f"{n_}: {ok}" for n_, ok in ok1))

# ---------------------------------------------------------------------------------------------------------------
# B2: the wall in comoving polar coordinates, own route; D against the printed q
# ---------------------------------------------------------------------------------------------------------------
print("\n== B2: the wall, comoving polar coordinates (t, r, theta, phi), generic w(r) ==", flush=True)
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
    """Reduce mod S^2 + C^2 - 1 (numerator), keep a rational function."""
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    num = sp.expand(sp.rem(sp.expand(num), CIRC, S))
    return num / den


w0 = W[0]
gW = sp.Matrix([[-1 + w0**2, w0 * C, -w0 * r * S, 0], [w0 * C, 1, 0, 0], [-w0 * r * S, 0, r**2, 0],
                [0, 0, 0, r**2 * S**2]])
giW = sp.Matrix([[-1, w0 * C, -w0 * S / r, 0], [w0 * C, 1 - w0**2 * C**2, w0**2 * C * S / r, 0],
                 [-w0 * S / r, w0**2 * C * S / r, (1 - w0**2 * S**2) / r**2, 0], [0, 0, 0, 1 / (r**2 * S**2)]])
ginv_ok = all(red(x) == 0 for x in (gW * giW - sp.eye(4)))
RW = christoffel_ricci(gW, giW, [Dzero, Dr, Dth, Dzero], simp=red)
print(f"  own Ricci in {time.time() - T0:.0f} s; g g^-1 = 1: {ginv_ok}", flush=True)
phi_zero = all(red(RW[3, m_]) == 0 for m_ in range(4))
E = sp.Matrix([[1, 0, 0], [-w0 * C, C, S], [w0 * S / r, -S / r, C / r], [0, 0, 0]])  # columns E0, E1, E_rho
R3 = (E.T * RW * E).applyfunc(red)
I2 = red(R3[0, 0] + R3[1, 1] + 2 * R3[2, 2])
txt = open(os.path.join(HERE, 'rpi5_output.txt')).read()
qs = re.search(r"q\(c\^2\) with q = (.*?); no odd terms", txt).group(1)
q = sp.sympify(qs, locals={'W0': W[0], 'W1': W[1], 'W2': W[2], 'c': C, 'r': r})
if MUT == 'qtyped':
    q = q + W[0]**3 * W[1]**3 * C**4
D16 = red(16 * r**3 * R3.det(method='berkowitz'))
dD = red(D16 - (1 - C**2) * q)
check('B2', ginv_ok and phi_zero and I2 == 0 and dD == 0,
      f"R_phi,mu = 0: {phi_zero}; R_00 + R_11 + 2 R_rho,rho = {I2}; 16 r^3 det R_3 - (1 - c^2) q(c^2) = 0 mod the "
      f"circle: {dD == 0} (q has {len(sp.Add.make_args(sp.expand(q)))} terms)")

# ---------------------------------------------------------------------------------------------------------------
# Point evaluation of the wall: R, g, dR, dg, h, dh, ddh (exact or 60 digits)
# ---------------------------------------------------------------------------------------------------------------
ARGS = [r, S, C] + list(W[:5])
hS = RW.extract([0, 1, 2], [0, 1, 2])
Dc = [Dzero, Dr, Dth]
exprs = {
    'R': [RW[i, j] for i in range(4) for j in range(4)],
    'g': [gW[i, j] for i in range(4) for j in range(4)],
    'dR': [Dk(RW[i, j]) for Dk in (Dr, Dth) for i in range(4) for j in range(4)],
    'dg': [Dk(gW[i, j]) for Dk in (Dr, Dth) for i in range(4) for j in range(4)],
    'dh': [Dk(hS[i, j]) for Dk in (Dr, Dth) for i in range(3) for j in range(3)],
    'ddh': [Dm(Dk(hS[i, j])) for Dm in (Dr, Dth) for Dk in (Dr, Dth) for i in range(3) for j in range(3)],
    'D16': [D16],
}
print(f"  derivatives built in {time.time() - T0:.0f} s", flush=True)
class ExactPrinter(LambdaPrinter):
    def _print_Rational(self, e):
        return f"Rational({e.p}, {e.q})"
    _print_Half = _print_Rational


F_ex = {k: sp.lambdify(ARGS, v, modules=[{'Rational': sp.Rational}, 'sympy'], printer=ExactPrinter)
        for k, v in exprs.items()}
F_mp = {k: sp.lambdify(ARGS, v, modules='mpmath') for k, v in exprs.items()}


def wall_at(pt, exact, mut=True):
    r0, s0, c0, Wj = pt
    F = F_ex if exact else F_mp
    a = [r0, s0, c0] + list(Wj[:5])
    v = {k: F[k](*a) for k in F}
    z3 = [[0] * 3 for _ in range(3)]
    h = [[v['R'][4 * i + j] for j in range(3)] for i in range(3)]
    dh = [z3] + [[[v['dh'][9 * k + 3 * i + j] for j in range(3)] for i in range(3)] for k in range(2)]
    ddh = [[z3, z3, z3]] + [[z3] + [[[v['ddh'][18 * m_ + 9 * k + 3 * i + j] for j in range(3)] for i in range(3)]
                                    for k in range(2)] for m_ in range(2)]
    if MUT == 'flat' and mut:
        h = [[-1, 0, 0], [0, 1, 0], [0, 0, r0**2]]
        dh = [z3, [[0, 0, 0], [0, 0, 0], [0, 0, 2 * r0]], z3]
        ddh = [[z3, z3, z3], [z3, [[0, 0, 0], [0, 0, 0], [0, 0, 2]], z3], [z3, z3, z3]]
    return v, h, dh, ddh


def jets_poly(fexpr, x, r0, v, n=5):
    """w = v (1 - f) and its derivatives at r0, exact."""
    return [v * (1 - fexpr.subs(x, r0))] + [-v * sp.diff(fexpr, x, k).subs(x, r0) for k in range(1, n)]


xr = sp.Symbol('xr', positive=True)
bump = (1 - xr**2 / 4)**3
sig, Rb = 8, 1
ftanh = (sp.tanh(sig * (xr + Rb)) - sp.tanh(sig * (xr - Rb))) / (2 * sp.tanh(sig * Rb))
tanh_d = [sp.diff(ftanh, xr, k) for k in range(5)]


def jets_tanh(r0, v):
    fk = [mp.mpf(sp.N(tanh_d[k].subs(xr, r0), 80)) for k in range(5)]
    return [v * (1 - fk[0])] + [-v * fk[k] for k in range(1, 5)]


def to_cs(x0, y0, z0, r0):
    return sp.Rational(x0, r0), sp.sqrt(sp.Rational(y0**2 + z0**2, r0**2))


PTS = []  # (label, (r0, s0, c0, jets), exact, eq)
for (x0, y0, z0, r0) in [(4, 3, 0, 5), (-3, 0, 4, 5), (0, 3, 4, 5)]:
    c0, s0 = to_cs(x0, y0, z0, r0)
    PTS.append(('bump', (sp.Integer(1), s0, c0, jets_poly(bump, xr, 1, sp.Rational(7, 4))), True, c0 == 0))
for (x0, y0, z0, r0) in [(12, 3, 4, 13), (-12, 4, 3, 13), (0, 5, 12, 13), (5, 12, 0, 13), (-5, 0, 12, 13),
                         (9, 12, 0, 15)]:
    c0, s0 = to_cs(x0, y0, z0, r0)
    for vv in (1, sp.Rational(1, 2), 3):
        PTS.append(('tanh', (mp.mpf(1), mp.mpf(sp.N(s0, 70)), mp.mpf(sp.N(c0, 70)), jets_tanh(1, vv)), False,
                    c0 == 0))

# ---------------------------------------------------------------------------------------------------------------
# B3: lam = 0, kernel d_phi, pattern by sign D, Ric(h) != 0
# ---------------------------------------------------------------------------------------------------------------
print("\n== B3: lam = 0 at the off-axis points: kernel, pattern, Ric(h) ==", flush=True)
EXPL = []
for vv in (1, sp.Rational(1, 2), sp.Rational(7, 4)):
    for r0 in (sp.Integer(1), sp.Rational(3, 2)):
        for (c0, s0) in ((sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(5, 13), sp.Rational(12, 13)),
                         (sp.Rational(-4, 5), sp.Rational(3, 5))):
            EXPL.append(('explicit', (r0, s0, c0, jets_poly(bump, xr, r0, vv)), True, False))
random.seed(2026)
RND = []
for r0, (c0, s0) in zip((1, sp.Rational(3, 2), sp.Rational(2, 3), sp.Rational(5, 4)),
                        ((sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(-5, 13), sp.Rational(12, 13)),
                         (sp.Rational(8, 17), sp.Rational(15, 17)), (sp.Integer(0), sp.Integer(1)))):
    jets = [sp.Rational(random.randint(-9, 9), random.randint(1, 9)) for _ in range(5)]
    RND.append(('random', (sp.Integer(r0), s0, c0, jets), True, False))

rows3, ok3 = [], True
for lab, pt, exact, eq in PTS + EXPL + RND:
    v, h, dh, ddh = wall_at(pt, exact)
    Ric, hi = ric3(h, dh, ddh)
    D16v = v['D16'][0]
    if exact:
        dh_ = sp.Matrix(h).det()
        npos, nneg = inertia_exact(h)
        nz = any(x != 0 for row in Ric for x in row)
        rel = None
    else:
        dh_ = mp.det(mp.matrix(h))
        ev = mp.eigsy(mp.matrix(h))[0]
        npos, nneg = sum(1 for e in ev if e > 0), sum(1 for e in ev if e < 0)
        rel = amax(Ric) / max(amax(h), amax([row for k in range(3) for row in dh[k]]))
        nz = rel > SMALL
    pat = 'A' if (npos, nneg) == (2, 1) else ('B' if (npos, nneg) == (1, 2) else '?')
    pat_ok = (pat == 'A' and D16v < 0) or (pat == 'B' and D16v > 0)
    want = {'bump': 'A', 'tanh': 'B'}.get(lab)
    ok = dh_ != 0 and pat_ok and nz and (want is None or pat == want)
    ok3 &= bool(ok)
    rows3.append((lab, pat, nz, ok))
summ = {}
for lab, pat, nz, ok in rows3:
    s_ = summ.setdefault(lab, [0, 0, set(), 0])
    s_[0] += 1
    s_[1] += int(nz)
    s_[2].add(pat)
    s_[3] += int(ok)
for lab, (n_, nnz, pats, nok) in summ.items():
    print(f"  {lab:>8}: {n_} points, patterns {sorted(pats)}, Ric(h) != 0 at {nnz}, all conditions at {nok}")
check('B3', ok3, f"{len(rows3)} points: lam = 0 kernel d_phi with h nondegenerate, pattern by sign of 16 r^3 det R_3 "
      f"(bump A, tanh B), Ric(h) != 0 at {sum(1 for x in rows3 if x[2])} of {len(rows3)}")

# ---------------------------------------------------------------------------------------------------------------
# B4: lam != 0 at the 21 non-random points
# ---------------------------------------------------------------------------------------------------------------
print("\n== B4: lam != 0 roots: count, sign by pattern, L_K M, K(lam) ==", flush=True)
B4pts = PTS
if MUT == 'refl':
    B4pts = [(lab, (pt[0], sp.Rational(4, 5) if exact else mp.mpf(4) / 5,
                    sp.Rational(3, 5) if exact else mp.mpf(3) / 5, pt[3]), exact, eq) if eq else (lab, pt, exact, eq)
             for lab, pt, exact, eq in PTS]
counts, ok4, rows4 = [], True, []
for lab, pt, exact, eq in B4pts:
    v, *_ = wall_at(pt, exact)
    cvt = (lambda x: mp.mpf(sp.N(x, 70))) if exact else (lambda x: mp.mpf(x))
    Rv = mp.matrix([[cvt(v['R'][4 * i + j]) for j in range(4)] for i in range(4)])
    for m_ in range(4):
        Rv[3, m_] = Rv[m_, 3] = 0  # R_phi,mu = 0 identically (B2)
    gv = mp.matrix([[cvt(v['g'][4 * i + j]) for j in range(4)] for i in range(4)])
    z4 = mp.zeros(4, 4)
    dR = [z4] + [mp.matrix([[cvt(v['dR'][16 * k + 4 * i + j]) for j in range(4)] for i in range(4)])
                 for k in range(2)] + [z4]
    for k in (1, 2):
        for m_ in range(4):
            dR[k][3, m_] = dR[k][m_, 3] = 0
    dg = [z4] + [mp.matrix([[cvt(v['dg'][16 * k + 4 * i + j]) for j in range(4)] for i in range(4)])
                 for k in range(2)] + [z4]
    scale_l = max(abs(Rv[i, j]) for i in range(4) for j in range(4))
    roots = [x for x in real_roots_pencil(Rv, gv) if abs(x) > mp.mpf(10) ** -40 * scale_l]
    nadm = 0
    for lam in roots:
        ev = mp.eigsy(Rv - lam * gv)[0]
        sc = max(abs(e) for e in ev)
        nz = [e for e in ev if abs(e) > mp.mpf(10) ** -40 * sc]
        if len(nz) != 3:
            continue
        npos = sum(1 for e in nz if e > 0)
        pat = {2: 'A', 1: 'B'}.get(npos)
        if pat is None:
            continue
        nadm += 1
        out = lie_KM(Rv, gv, dR, dg, lam, nodk=(MUT == 'nodk'))
        sign_ok = (pat == 'A' and lam < 0) or (pat == 'B' and lam > 0)
        klam_ok = (out['relK'] < TINY) if eq else (out['relK'] > SMALL)
        ok = sign_ok and out['rel'] > SMALL and out['ident'] < TINY and klam_ok
        ok4 &= ok
        rows4.append((lab, eq, pat, lam, out, ok))
    counts.append(nadm)
    ok4 &= nadm == 1
for lab, eq, pat, lam, out, ok in rows4:
    print(f"  {lab:>5} {'c = 0' if eq else 'c != 0'}: pattern {pat}, lam = {mp.nstr(lam, 10):>14}, L_K M rel "
          f"{mp.nstr(out['rel'], 3):>8}, (L_K M)(K,.) {mp.nstr(out['ident'], 2):>8}, K(lam) rel "
          f"{mp.nstr(out['relK'], 3):>8}, bordered residual {mp.nstr(out['resid'], 2)}, ok {ok}")
neq = sum(1 for x in rows4 if x[1])
check('B4', ok4 and sum(counts) == 21,
      f"admissible rank-3 roots lam != 0 per point {counts} (sum {sum(counts)}); L_K M != 0 at "
      f"{sum(1 for x in rows4 if x[4]['rel'] > SMALL)} of {len(rows4)}; K(lam) = 0 at the {neq} roots with c = 0: "
      f"{all(x[4]['relK'] < TINY for x in rows4 if x[1])}; K(lam) != 0 at the other "
      f"{sum(1 for x in rows4 if not x[1] and x[4]['relK'] > SMALL)} of {len(rows4) - neq}")

# ---------------------------------------------------------------------------------------------------------------
# B5: the accelerating bubble, Cartesian route with truncated Taylor series
# ---------------------------------------------------------------------------------------------------------------
print("\n== B5: Cartesian route: accelerating bubble and the cross-check of the two routes ==", flush=True)
Rg, Tg, Xg, Yg, Zg = ring('T X Y Z', QQ)
GENS = [Tg, Xg, Yg, Zg]


def trunc(p, n):
    return Rg.from_dict({m_: c for m_, c in p.items() if sum(m_) <= n})


def cart_block(vs, xs, t0, x0, y0):
    """3D block h on z = 0 of the Ricci tensor of b = -v_s(t) (1 - Q/4)^3 at (t0, x0, y0, 0), with derivatives."""
    tt = Rg(t0) + Tg
    V = sum((Rg(c) * tt**k for k, c in enumerate(vs)), Rg(0))
    Xs = sum((Rg(c) * tt**k for k, c in enumerate(xs)), Rg(0))
    Q = (Rg(x0) + Xg - Xs)**2 + (Rg(y0) + Yg)**2 + Zg**2
    b = trunc(-V * (1 - Q * QQ(1, 4))**3, 4)
    b2 = trunc(b * b, 4)
    one, zero = Rg(1), Rg(0)
    g = [[b2 - one, b, zero, zero], [b, one, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    gi = [[-one, b, zero, zero], [b, one - b2, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    n = 4
    eye_ok = all(trunc(sum((g[i][k] * gi[k][j] for k in range(n)), zero), 4) == (one if i == j else zero)
                 for i in range(n) for j in range(n))
    dg = [[[g[i][j].diff(GENS[k]) for k in range(n)] for j in range(n)] for i in range(n)]
    G = [[[trunc(sum((gi[a][d] * (dg[d][c][bb] + dg[d][bb][c] - dg[bb][c][d]) for d in range(n)), zero) * QQ(1, 2),
                 3) for c in range(n)] for bb in range(n)] for a in range(n)]
    Ric = [[None] * n for _ in range(n)]
    for bb in range(n):
        for c in range(n):
            e = sum((G[a][bb][c].diff(GENS[a]) - G[a][bb][a].diff(GENS[c]) for a in range(n)), zero)
            e += sum((G[a][a][d] * G[d][bb][c] - G[a][c][d] * G[d][bb][a] for a in range(n) for d in range(n)), zero)
            Ric[bb][c] = trunc(e, 2)
    co = lambda p, m_: sp.Rational(str(dict(p).get(m_, QQ(0))))
    e_ = lambda k: tuple(1 if i == k else 0 for i in range(4))
    rz = [co(Ric[3][m_], (0, 0, 0, 0)) for m_ in range(4)]
    h = [[co(Ric[i][j], (0, 0, 0, 0)) for j in range(3)] for i in range(3)]
    dh = [[[co(Ric[i][j], e_(k)) for j in range(3)] for i in range(3)] for k in range(3)]
    ddh = [[[[co(Ric[i][j], tuple(a + b_ for a, b_ in zip(e_(m_), e_(k)))) * (2 if m_ == k else 1)
              for j in range(3)] for i in range(3)] for k in range(3)] for m_ in range(3)]
    return eye_ok, rz, h, dh, ddh


VS = [QQ(1), QQ(1, 2), QQ(1, 3)]
XSs = [QQ(0), QQ(1), QQ(1, 4), QQ(1, 5)]
ok5, rows5 = True, []
for (t0, x0, y0) in ((QQ(0), QQ(1, 2), QQ(1, 2)), (QQ(0), QQ(-1, 3), QQ(1)), (QQ(1, 2), QQ(1), QQ(2, 3))):
    eye_ok, rz, h, dh, ddh = cart_block(VS, XSs, t0, x0, y0)
    if MUT == 'accflat':
        z3 = [[0] * 3 for _ in range(3)]
        h, dh, ddh = [[-1, 0, 0], [0, 1, 0], [0, 0, 1]], [z3] * 3, [[z3] * 3] * 3
    Ric, _ = ric3(h, dh, ddh)
    nz = any(x != 0 for row in Ric for x in row)
    ok = eye_ok and all(x == 0 for x in rz) and sp.Matrix(h).det() != 0 and nz
    ok5 &= ok
    rows5.append(((t0, x0, y0), nz, ok))
# cross-check at constant speed: Cartesian (0, 3/5, 4/5, 0) against polar r = 1, (c, s) = (3/5, 4/5), bump at v = 1
xc = QQ(3, 5) + (QQ(1, 50) if MUT == 'xcheck' else QQ(0))
_, _, hC, dhC, ddhC = cart_block([QQ(1)], [QQ(0), QQ(1)], QQ(0), xc, QQ(4, 5))
RicC, hiC = ric3(hC, dhC, ddhC)
scalC = sp.nsimplify(sum(hiC[i][j] * RicC[i][j] for i in range(3) for j in range(3)))
_, hP, dhP, ddhP = wall_at((sp.Integer(1), sp.Rational(4, 5), sp.Rational(3, 5), jets_poly(bump, xr, 1, 1)), True,
                           mut=False)  # B3's mutation does not reach the cross-check
RicP, hiP = ric3(hP, dhP, ddhP)
scalP = sp.nsimplify(sum(hiP[i][j] * RicP[i][j] for i in range(3) for j in range(3)))
xok = sp.simplify(scalC - scalP) == 0
check('B5', ok5 and xok,
      f"accelerating: R_z,mu = 0, h nondegenerate and Ric(h) != 0 at {sum(1 for x in rows5 if x[1])} of {len(rows5)} "
      f"points {[tuple(str(c) for c in x[0]) for x in rows5]}; scalar curvature of h, Cartesian {scalC} vs polar "
      f"{scalP}: equal {xok}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

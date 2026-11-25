#!/usr/bin/env python3
"""ind79: the coordinator's independent check of #79 (the review of #65's two-scalar result).

Criteria H0-H6 in negative-mass-raw I79-mac/README.md. Imports nothing from the repository. The Ricci routine, the polar
wall route and the Cartesian route are the coordinator's (I77-mac/ind77.py, I78-mac/ind78.py). #79's cofactors are read
as data from rpi5_ideals_certs_output.txt and multiplied into the coordinator's own coefficients.
"""
import argparse
import os
import random
import re
import sys
import time

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.rings import ring

MUTS = ['pg', 'qsign', 'c3', 'cof', 'ode', 'accY', 'acccof', 'omega', 'h2']
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
HERE = os.path.dirname(os.path.abspath(__file__))
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


# ---------------------------------------------------------------------------------------------------------------
# H0
# ---------------------------------------------------------------------------------------------------------------
print("== H0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
beta = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify), [lambda e, x=x: sp.diff(e, x) for x in
                                                                (t_, rr, th_, ph_)], sp.simplify)
check('H0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# ---------------------------------------------------------------------------------------------------------------
# H1: generic axisymmetric b(t, x, rho)
# ---------------------------------------------------------------------------------------------------------------
print("\n== H1: b(t, x, rho) generic: the block and D ==", flush=True)
tt, xx, rho, phi = sp.symbols('t x rho phi', positive=True)
b = sp.Function('b')(tt, xx, rho)
gb = sp.Matrix([[-1 + b**2, b, 0, 0], [b, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, rho**2]])
gib = sp.Matrix([[-1, b, 0, 0], [b, 1 - b**2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho**2]])
XB = [tt, xx, rho, phi]
simpB = lambda e: sp.expand(sp.cancel(e))
RB = christoffel_ricci(gb, gib, [lambda e, x=x: sp.diff(e, x) for x in XB], simpB)
E4 = sp.Matrix([[1, 0, 0, 0], [-b, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1 / rho]])
RF = (E4.T * RB * E4).applyfunc(simpB)
nder = lambda f: sp.diff(f, tt) - b * sp.diff(f, xx)
bx, br = sp.diff(b, xx), sp.diff(b, rho)
P = nder(bx) - bx**2
Q = (1 if MUT == 'qsign' else -1) * (sp.diff(b, rho, 2) + br / rho) / 2
Z = sp.diff(b, xx, rho) / 2
Y = -nder(br) / 2 + bx * br
h = br**2 / 2
blk = sp.Matrix([[P - h, Q, Z], [Q, -P - h, Y], [Z, Y, h]])
phi0 = all(zero(RF[3, m]) for m in range(4))
blk_ok = all(zero(RF[i, j] - blk[i, j]) for i in range(3) for j in range(i, 3))
Dpr = h * (h**2 - P**2 - Q**2 + Y**2 + Z**2) - P * (Y**2 - Z**2) + 2 * Q * Y * Z
det_ok = zero(RF[:3, :3].det(method='berkowitz') - Dpr)
check('H1', phi0 and blk_ok and det_ok, f"R(e_phi, .) = 0: {phi0}; block as printed: {blk_ok}; det = D: {det_ok}")

# ---------------------------------------------------------------------------------------------------------------
# H2: constant speed, own polar route; coefficients; ideal membership; #79's cofactors
# ---------------------------------------------------------------------------------------------------------------
print("\n== H2: constant speed: coefficients and the certificates ==", flush=True)
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
E = sp.Matrix([[1, 0, 0], [-w0 * C, C, S], [w0 * S / r, -S / r, C / r], [0, 0, 0]])
R3 = (E.T * RW * E).applyfunc(red)
W0, W1, W2 = W[:3]


def coeffs_in_c(M3):
    D16 = red(16 * r**3 * M3.det(method='berkowitz'))
    num, den = sp.fraction(sp.cancel(D16))
    assert not den.has(C) and not den.has(S) and not num.has(S), "16 r^3 D not a polynomial in c"
    p = sp.Poly(sp.expand(num), C)
    return [sp.cancel(p.coeff_monomial(C**k) / den) for k in range(p.degree() + 1)], p.degree()


cc, deg = coeffs_in_c(R3)
odd0 = all(zero(cc[k]) for k in range(1, len(cc), 2))
c0p = 2 * r * W1**2 * (r**2 * W1**4 - 4 * W0**2 * W1**2 - (W1 + r * W2)**2)
c3p = -2 * (r * W0 * W2 + r * W1**2 - W0 * W1)**2 * (2 * r * W0 * W2 + r * W1**2 + (2 if MUT == 'c3' else -2) * W0 * W1)
ck = [cc[2 * k] for k in range(4)]
pr_ok = deg == 6 and odd0 and zero(ck[0] - c0p) and zero(ck[3] - c3p)
A_, B_ = sp.symbols('A B', real=True)
sub_AB = {W0: (A_ + r * W1) / 2, W2: (B_ - W1) / r}
ckAB = [sp.expand(sp.cancel(c.subs(sub_AB, simultaneous=True))) for c in ck]
memb = []
for c in ckAB:
    num, den = sp.fraction(sp.cancel(c))
    pp = sp.Poly(sp.expand(num), A_, B_)
    memb.append(all(i >= 1 or j >= 2 for (i, j) in pp.monoms()) and not den.has(A_) and not den.has(B_))
txt = open(os.path.join(HERE, 'rpi5_ideals_certs_output.txt')).read()
loc = {'r': r, 'w1': W1, 'A': A_, 'B': B_, 'w': W0, 'aa': sp.Symbol('aa', real=True),
       'omega': sp.Symbol('omega', real=True)}
const_part = txt.split('CERTIFICATES (constant speed)')[1].split('== 4.')[0]
certs = {}
cur = None
for line in const_part.splitlines():
    m_ = re.match(r'\s*target (\S+):', line)
    if m_:
        cur = m_.group(1)
        certs[cur] = []
        continue
    m_ = re.match(r'\s*\(k=(\d+), A\^(\d+) B\^(\d+)\): (.*)$', line)
    if m_ and cur:
        certs[cur].append((int(m_.group(1)), int(m_.group(2)), int(m_.group(3)), sp.sympify(m_.group(4), locals=loc)))
if MUT == 'cof':
    k0, i0, j0, e0 = certs['A'][0]
    certs['A'][0] = (k0, i0, j0, 2 * e0)
targets = {'A': A_, 'B^2': B_**2}
cert_ok = {nm: zero(sum(e * A_**i * B_**j * ckAB[k] for (k, i, j, e) in lst) - targets[nm])
           for nm, lst in certs.items()}
check('H2', pr_ok and all(memb) and len(certs) == 2 and all(cert_ok.values()),
      f"degree {deg} in c, odd powers 0: {odd0}; c_0, c_3 as printed: {pr_ok}; each c_k in (A, B^2): {memb}; "
      f"#79's cofactors ({ {k: len(v) for k, v in certs.items()} } terms) give the targets: {cert_ok}")

# ---------------------------------------------------------------------------------------------------------------
# H3: the no-open-set step
# ---------------------------------------------------------------------------------------------------------------
print("\n== H3: 2w = r w', w' + r w'' = 0 force w' = 0 ==", flush=True)
rx = sp.Symbol('r', positive=True)
wf = sp.Function('w')
sol = sp.dsolve(2 * wf(rx) - rx * wf(rx).diff(rx), wf(rx))
second = (wf(rx).diff(rx) + (-1 if MUT == 'ode' else 1) * rx * wf(rx).diff(rx, 2))
expr = sp.simplify(second.subs(wf(rx), sol.rhs).doit())
C1 = [s_ for s_ in sol.rhs.free_symbols if s_ != rx]
ok3 = expr != 0 and len(C1) == 1 and sp.solve(sp.Poly(expr, rx).coeffs(), C1[0]) in ({C1[0]: 0}, [0], [{C1[0]: 0}])
check('H3', ok3, f"w = {sol.rhs}; w' + r w'' = {expr}; forces the constant to 0: {ok3}")

# ---------------------------------------------------------------------------------------------------------------
# H4: accelerating bubble
# ---------------------------------------------------------------------------------------------------------------
print("\n== H4: accelerating bubble: entries at 3 points (Cartesian), coefficients, #79's certificate ==", flush=True)
aa, om = loc['aa'], loc['omega']
shift = sp.Matrix([[aa * W1 * C, 0, 0], [0, -aa * W1 * C, (1 if MUT == 'accY' else -1) * aa * W1 * S / 2],
                   [0, (1 if MUT == 'accY' else -1) * aa * W1 * S / 2, 0]])
R3A = R3 + shift
Rg, Tg, Xg, Yg, Zg = ring('T X Y Z', QQ)
GENS = [Tg, Xg, Yg, Zg]


def trunc(p, n):
    return Rg.from_dict({m_: c for m_, c in p.items() if sum(m_) <= n})


def cart_R(vs, xs, t0, x0, y0):
    t1 = Rg(t0) + Tg
    Vt = sum((Rg(c) * t1**k for k, c in enumerate(vs)), Rg(0))
    Xs = sum((Rg(c) * t1**k for k, c in enumerate(xs)), Rg(0))
    Qr = (Rg(x0) + Xg - Xs)**2 + (Rg(y0) + Yg)**2 + Zg**2
    bb_ = trunc(-Vt * (1 - Qr * QQ(1, 4))**3, 2)
    b2 = trunc(bb_ * bb_, 2)
    one, zr = Rg(1), Rg(0)
    g = [[b2 - one, bb_, zr, zr], [bb_, one, zr, zr], [zr, zr, one, zr], [zr, zr, zr, one]]
    gi = [[-one, bb_, zr, zr], [bb_, one - b2, zr, zr], [zr, zr, one, zr], [zr, zr, zr, one]]
    n = 4
    dg = [[[g[i][j].diff(GENS[k]) for k in range(n)] for j in range(n)] for i in range(n)]
    G = [[[trunc(sum((gi[a][d] * (dg[d][c][q] + dg[d][q][c] - dg[q][c][d]) for d in range(n)), zr) * QQ(1, 2), 1)
           for c in range(n)] for q in range(n)] for a in range(n)]
    co = lambda p: sp.Rational(str(dict(p).get((0, 0, 0, 0), QQ(0))))
    Ric = sp.zeros(4, 4)
    for q in range(n):
        for c in range(n):
            e = sum((G[a][q][c].diff(GENS[a]) - G[a][q][a].diff(GENS[c]) for a in range(n)), zr)
            e += sum((G[a][a][d] * G[d][q][c] - G[a][c][d] * G[d][q][a] for a in range(n) for d in range(n)), zr)
            Ric[q, c] = co(e)
    b0 = co(bb_)
    Ef = sp.Matrix([[1, 0, 0], [-b0, 1, 0], [0, 0, 1], [0, 0, 0]])
    return Ef.T * Ric * Ef


xr = sp.Symbol('xr', positive=True)
bump = (1 - xr**2 / 4)**3
VS = [QQ(1), QQ(1, 2), QQ(1, 3)]
XSs = [QQ(0), QQ(1), QQ(1, 4), QQ(1, 5)]
poly_at = lambda cs, t0, k=0: sp.diff(sum(sp.Rational(str(c)) * xr**j for j, c in enumerate(cs)), xr, k).subs(
    xr, sp.Rational(str(t0)))
pts_ok = []
for (t0, x0, y0) in ((QQ(0), QQ(3, 5), QQ(4, 5)), (QQ(1, 4), QQ(-17, 32), QQ(3, 5)),
                     (QQ(-1, 2), QQ(119, 1040), QQ(18, 13))):
    Rc = cart_R(VS, XSs, t0, x0, y0)
    dx, yv = sp.Rational(str(x0)) - poly_at(XSs, t0), sp.Rational(str(y0))
    r0 = sp.sqrt(dx**2 + yv**2)
    wt = poly_at(XSs, t0, 1) - poly_at(VS, t0) * bump
    sub = {r: r0, S: yv / r0, C: dx / r0, W0: wt.subs(xr, r0), W1: sp.diff(wt, xr).subs(xr, r0),
           W2: sp.diff(wt, xr, 2).subs(xr, r0), aa: poly_at(VS, t0, 1) / poly_at(VS, t0)}
    pts_ok.append(all(zero(Rc[i, j] - R3A[i, j].subs(sub)) for i in range(3) for j in range(3)) and r0.is_rational)
ccA, degA = coeffs_in_c(R3A)
oddA = [sp.cancel(ccA[k] / (4 * aa * r * W1)) for k in (1, 3, 5)]
div_ok = all(sp.fraction(sp.cancel(e))[1].free_symbols <= set() or sp.fraction(sp.cancel(e))[1] == 1 for e in oddA)
eA = [ccA[k] if k % 2 == 0 else ccA[k] / (4 * aa * r * W1) for k in range(7)]
subw = {W2: W1 / r - om * W1**2}
eA = [sp.cancel(e.subs(subw)) for e in eA]
acc_part = txt.split('CERTIFICATE (accelerating bubble)')[1].split('chain:')[0]
accc = []
for line in acc_part.splitlines():
    m_ = re.match(r'\s*\(k=(\d+), w\^(\d+) omega\^(\d+)\): (.*)$', line)
    if m_:
        accc.append((int(m_.group(1)), int(m_.group(2)), int(m_.group(3)), sp.sympify(m_.group(4), locals=loc)))
if MUT == 'acccof':
    k0, i0, j0, e0 = accc[0]
    accc[0] = (k0, i0, j0, 2 * e0)
acc_cert = zero(sum(e * W0**i * om**j * eA[k] for (k, i, j, e) in accc) - 1)
check('H4', all(pts_ok) and degA == 6 and div_ok and acc_cert,
      f"entries at 3 points: {pts_ok}; degree {degA} in c; odd coefficients divisible by 4 A r w': {div_ok}; "
      f"#79's {len(accc)} cofactors give 1: {acc_cert}")

# ---------------------------------------------------------------------------------------------------------------
# H5: the omega formula
# ---------------------------------------------------------------------------------------------------------------
print("\n== H5: omega = dm(K, M) k + iota_K dk ==", flush=True)
rng = random.Random(7979)
rq = lambda: sp.Rational(rng.randint(-9, 9), rng.randint(1, 5))
wedge = lambda a, c: sp.Matrix(4, 4, lambda i, j: a[i] * c[j] - a[j] * c[i])
ok5 = []
for _ in range(6):
    while True:
        k = sp.Matrix([rq() for _ in range(4)])
        m = sp.Matrix([rq() for _ in range(4)])
        Lm = sp.Matrix.vstack(k.T, m.T)
        if Lm.rank() == 2:
            break
    KM = Lm.T * (Lm * Lm.T).inv()
    K, M = KM[:, 0], KM[:, 1]
    om0 = sp.Matrix([rq() for _ in range(4)])
    dk, dm = -wedge(om0, k), wedge(om0, m)
    sgn = -1 if MUT == 'omega' else 1
    cand = (K.T * dm * M)[0, 0] * k + sgn * sp.Matrix([sum(K[i] * dk[i, j] for i in range(4)) for j in range(4)])
    lin = sp.Matrix([[wedge(sp.eye(4)[:, q], k)[i, j] for q in range(4)] for i in range(4) for j in range(i + 1, 4)] +
                    [[wedge(sp.eye(4)[:, q], m)[i, j] for q in range(4)] for i in range(4) for j in range(i + 1, 4)])
    dk_bad = sp.Matrix(4, 4, lambda i, j: 0)
    for i in range(4):
        for j in range(i + 1, 4):
            v_ = rq()
            dk_bad[i, j], dk_bad[j, i] = v_, -v_
    cand_bad = (K.T * dm * M)[0, 0] * k + sp.Matrix([sum(K[i] * dk_bad[i, j] for i in range(4)) for j in range(4)])
    viol = wedge(cand_bad, k) + dk_bad != sp.zeros(4, 4)
    ok5.append(cand == om0 and lin.rank() == 4 and viol)
check('H5', all(ok5), f"6 instances: candidate = omega_0, rank 4, a random dk violated: {ok5}")

# ---------------------------------------------------------------------------------------------------------------
# H6: b(rho)
# ---------------------------------------------------------------------------------------------------------------
print("\n== H6: b(rho) with b'' + b'/rho = eps b'^2 ==", flush=True)
bfun = sp.Function('b')(rho)
g6 = gb.subs(b, bfun)
gi6 = gib.subs(b, bfun)
R6 = christoffel_ricci(g6, gi6, [lambda e, x=x: sp.diff(e, x) for x in XB], simpB)
ok6 = []
for eps in (1, -1):
    bpp = eps * sp.diff(bfun, rho)**2 - sp.diff(bfun, rho) / rho
    R6e = R6.subs(sp.Derivative(bfun, (rho, 2)), bpp)
    hh = (2 if MUT == 'h2' else 1) * sp.diff(bfun, rho)**2 / 2
    nu = sp.Matrix([1 + eps * bfun, eps, 0, 0])
    er = sp.Matrix([0, 0, 1, 0])
    want = hh * (er * er.T - nu * nu.T)
    t_ok = all(zero(R6e[i, j] - want[i, j]) for i in range(4) for j in range(4))
    nuv = sp.Matrix([1 + eps * bfun, eps, 1, 0])
    dnu = sp.Matrix(4, 4, lambda i, j: sp.diff(nuv[j], XB[i]) - sp.diff(nuv[i], XB[j]))
    i_, j_, k_ = 0, 1, 2
    three = nuv[i_] * dnu[j_, k_] + nuv[j_] * dnu[k_, i_] + nuv[k_] * dnu[i_, j_]
    ok6.append(t_ok and zero(three - sp.diff(bfun, rho)))
check('H6', all(ok6), f"R = h((d rho)^2 - nu'^2) and (nu ^ d nu)_(t x rho) = b' for eps = +1, -1: {ok6}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

#!/usr/bin/env python3
"""ind73: the coordinator's independent check of #73 (Hawking-Ellis type of the accelerating bubble).

Criteria A0-A5 in negative-mass-raw I73-mac/README.md. Imports nothing from the repository: own Christoffel and Ricci,
own chain rule for the 2-jets of b = -v_s(t) f(r_s), sympy's charpoly and discriminant, numpy's eigenvalues for the map.
"""
import argparse
import sys
import time

import numpy as np
import sympy as sp
from scipy.optimize import brentq
from sympy.polys.domains import QQ
from sympy.polys.rings import ring

ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.0f} s)", flush=True)
    if not ok:
        FAIL.append(name)


def christoffel_ricci(g, X):
    """R_bc = d_a G^a_bc - d_c G^a_ba + G^a_ad G^d_bc - G^a_cd G^d_ba, G^a_bc = g^ad (d_b g_dc + d_c g_db - d_d g_bc)/2."""
    n = len(X)
    gi = g.inv().applyfunc(sp.cancel)
    dg = [[[sp.diff(g[i, j], X[k]) for k in range(n)] for j in range(n)] for i in range(n)]
    G = [[[sp.cancel(sum(gi[a, d] * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d]) for d in range(n)) / 2)
           for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(b, n):
            e = sum(sp.diff(G[a][b][c], X[a]) - sp.diff(G[a][b][a], X[c]) for a in range(n))
            e += sum(G[a][a][d] * G[d][b][c] - G[a][c][d] * G[d][b][a] for a in range(n) for d in range(n))
            Ric[b, c] = Ric[c, b] = e
    return Ric


# ---------------------------------------------------------------------------------------------------------------
# A0: planted metrics
# ---------------------------------------------------------------------------------------------------------------
t, rr, th, ph, M, H = sp.symbols('t r theta phi M H', positive=True)
beta_pg = sp.sqrt(2 * M) / rr if MUT == 'pg' else sp.sqrt(2 * M / rr)
gpg = sp.diag(-1 + beta_pg**2, 1, rr**2, rr**2 * sp.sin(th)**2)
gpg[0, 1] = gpg[1, 0] = beta_pg
Rpg = christoffel_ricci(gpg, [t, rr, th, ph]).applyfunc(sp.simplify)
x, y, z = sp.symbols('x y z', real=True)
gds = sp.diag(-1, sp.exp(2 * H * t), sp.exp(2 * H * t), sp.exp(2 * H * t))
Rds = christoffel_ricci(gds, [t, x, y, z])
ok_ds = all(sp.simplify(Rds[i, j] - 3 * H**2 * gds[i, j]) == 0 for i in range(4) for j in range(4))
check('A0', Rpg == sp.zeros(4, 4) and ok_ds,
      f"Painleve-Gullstrand Ricci zero {Rpg == sp.zeros(4, 4)}; de Sitter R = 3H^2 g {ok_ds}")

# ---------------------------------------------------------------------------------------------------------------
# A1: own Ricci of the shift metric, own 2-jets of b, frame block against the printed entries
# ---------------------------------------------------------------------------------------------------------------
v, al, u, be, w, f, f1, f2, r, c, s = sp.symbols('v alpha u beta w f f1 f2 r c s', real=True)
B = sp.Function('B')(t, x, y, z)
g = sp.Matrix([[-1 + B**2, B, 0, 0], [B, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
if MUT == 'w2':
    g[0, 0] = -1
Ric = christoffel_ricci(g, [t, x, y, z])
E = sp.Matrix([[1, -B, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # rows: n, d_x, d_y, d_z
Rf = E * Ric * E.T

# 2-jets of v_s, x_s at t = 0 and of G(Q) = f(sqrt Q) at Q = r^2; x_s(0) = 0 by translation.
Vt = v + al * t + be * t**2 / 2
Xt = u * t + w * t**2 / 2
Q = (x - Xt)**2 + y**2 + z**2
g1 = f1 / (2 * r)
g2 = f2 / (4 * r**2) - f1 / (4 * r**3)
bpoly = -Vt * (f + g1 * (Q - r**2) + g2 * (Q - r**2)**2 / 2)
pt = {t: 0, x: r * c, y: r * s, z: 0}
rep = {B: bpoly.subs(pt)}
for d in Rf.atoms(sp.Derivative):
    rep[d] = sp.diff(bpoly, *d.variables).subs(pt)
Rf = Rf.applyfunc(lambda e: e.xreplace(rep))
CIRC = s**2 + c**2 - 1


def red(e):
    """Rational function with s-degree <= 1 in its numerator, equal to e mod s^2 + c^2 - 1."""
    n_, d_ = sp.fraction(sp.cancel(sp.together(e)))
    return sp.cancel(sp.rem(sp.expand(n_), CIRC, s) / d_)


Rf = Rf.applyfunc(red)

# Printed entries (he_accel.md, "Answer").
Tx = -al * c * f1 + (-1 if MUT == 'tx' else 1) * v * u * (s**2 * f1 / r + c**2 * f2)
Tr = -al * s * f1 + v * u * c * s * (f2 - f1 / r)
A = (v**2 / (2 * r)) * (2 * f * (s**2 * f1 + r * c**2 * f2) + r * (1 + c**2) * f1**2)
Bb = (v**2 * c * s / (2 * r)) * (2 * r * f1**2 + r * f * f2 - f * f1)
q_ = v**2 * s**2 * f1**2
j1_ = v * ((1 + c**2) * f1 + r * s**2 * f2) / (2 * r)
jr_ = v * c * s * (f1 - r * f2) / (2 * r)
P = sp.Matrix([[Tx - A, j1_, jr_], [j1_, A - q_ - Tx, Bb - Tr / 2], [jr_, Bb - Tr / 2, q_ / 2]])
diffs = [red(Rf[i, j] - P[i, j]) for i in range(3) for j in range(3)]
phi = [red(Rf[3, k]) for k in range(4)]
blk_syms = set().union(*[Rf[i, j].free_symbols for i in range(3) for j in range(3)])
ok1 = all(d_ == 0 for d_ in diffs) and all(p_ == 0 for p_ in phi) and not ({be, w} & blk_syms)
check('A1', ok1, f"block - printed, mod s^2: {diffs}; R(e_phi, .) {phi}; symbols of the block {sorted(map(str, blk_syms))}")
i2 = red(Rf[0, 0] + Rf[1, 1] + 2 * Rf[2, 2])
print(f"  (diagnostic) R_00 + R_11 + 2 R_rhorho mod s^2 = {i2}")

# ---------------------------------------------------------------------------------------------------------------
# A2: sympy's discriminant of the charpoly of eta R, generic block with (I2), against the printed D
# ---------------------------------------------------------------------------------------------------------------
lam = sp.Symbol('lambda')
R00, R01, R0r, R1r, Rrr, R11 = sp.symbols('R00 R01 R0r R1r Rrr R11')
j1, jr, q, h, p = sp.symbols('j1 jr q h p')
eta = sp.diag(-1, 1, 1)


def disc_of(Rm):
    return sp.discriminant(sp.Poly((eta * Rm).charpoly(lam).as_expr(), lam))


Dgen6 = sp.expand(disc_of(sp.Matrix([[R00, R01, R0r], [R01, R11, R1r], [R0r, R1r, Rrr]])))
Dg = sp.expand(Dgen6.subs({R11: -R00 - 2 * Rrr}).subs({R00: p - q / 2, Rrr: q / 2, R01: j1, R0r: jr, R1r: h}))
c2 = q - p
c1 = j1**2 + jr**2 - p * q - h**2
c0 = 2 * j1 * jr * h - p * j1**2 + q * jr**2
Dt = 18 * c2 * c1 * c0 - 4 * c2**3 * c0 + c2**2 * c1**2 - 4 * c1**3 - (26 if MUT == 'disc27' else 27) * c0**2
PD = sp.Poly(Dg, j1, jr, q, h, p)
terms = PD.terms()
jdeg = sorted({m[0] + m[1] for m, _ in terms})
tdeg = sorted({sum(m) for m, _ in terms})
part = lambda k: sp.expand(sum(cf * sp.prod([x_**e for x_, e in zip((j1, jr, q, h, p), m)])  # noqa: E731
                               for m, cf in terms if m[0] + m[1] == k))
ok_w6 = sp.expand(part(6) + 4 * (j1**2 + jr**2)**3) == 0
ok_w0 = sp.expand(part(0) - (p * q + h**2)**2 * ((p + q)**2 + 4 * h**2)) == 0
ok_eq = sp.expand(Dg - Dt) == 0
ok2 = ok_eq and len(terms) == 52 and PD.degree(p) == 4 and tdeg == [6] and jdeg == [0, 2, 4, 6] and ok_w6 and ok_w0
check('A2', ok2, f"sympy D = printed D {ok_eq}; {len(terms)} terms, degree {PD.degree(p)} in p, total degrees {tdeg}, "
      f"j-degrees {jdeg}; j^6 part -4|j|^6 {ok_w6}; j^0 part (pq+h^2)^2((p+q)^2+4h^2) {ok_w0}")

# ---------------------------------------------------------------------------------------------------------------
# A3: the bubble's D_b, in a polynomial ring with 1/r as a generator, reduced mod s^2 + c^2 - 1
# ---------------------------------------------------------------------------------------------------------------
ir = sp.Symbol('ir')
K, Ks, Kc, Kv, Kal, Ku, Kf, Ka, Kb, Kir = ring([s, c, v, al, u, f, f1, f2, ir], QQ, order='lex')
G = Ks**2 + Kc**2 - 1


def to_K(e):
    return K.from_expr(sp.expand(sp.together(e).subs(r, 1 / ir)))


ent = {k: to_K(Rf[i, j]) for k, (i, j) in
       dict(R00=(0, 0), R01=(0, 1), R0r=(0, 2), R11=(1, 1), R1r=(1, 2), Rrr=(2, 2)).items()}
P6 = sp.Poly(Dgen6, R00, R01, R0r, R11, R1r, Rrr)
names = ('R00', 'R01', 'R0r', 'R11', 'R1r', 'Rrr')
pw = {nm: [K.one] for nm in names}
for nm in names:
    for _ in range(6):
        pw[nm].append(pw[nm][-1] * ent[nm])
Db = K.zero
for m, cf in P6.terms():
    term = K(QQ(int(cf.p), int(cf.q)))
    for nm, e in zip(names, m):
        term = term * pw[nm][e]
    Db += term
Db = Db.rem(G)
print(f"  (diagnostic) D_b reduced: {len(Db.terms())} terms")
iv, ial, iu, ic, is_ = 2, 3, 4, 1, 0


def subs0(P_, idx, val):
    out = K.zero
    for m, cf in P_.terms():
        out += K({m[:idx] + (0,) + m[idx + 1:]: cf * QQ(val)**m[idx]}) if m[idx] == 0 or val != 0 else K.zero
    return out


# (a) v = 0
Dv0 = subs0(Db, iv, 0)
ok_a = (Dv0 - (Kal**6 * Ka**6 * Ks**4 / 16).rem(G)).rem(G) == 0
# (b) axis c = +-1, s = 0
ok_b = True
for cv in (1, -1):
    sub = lambda P_: subs0(subs0(P_, is_, 0), ic, cv)  # noqa: E731
    j1ax, r00ax = sub(ent['R01']), sub(ent['R00'])
    claim = (4 if MUT == 'axis' else -4) * j1ax**2 * (r00ax**2 + j1ax**2)**2
    ok_b &= sub(Db) == claim and j1ax == Kv * Ka * Kir
# (c) degree 6 in alpha, alpha^6 coefficient
deg_al = max(m[ial] for m, _ in Db.terms())
c6 = K({m[:ial] + (0,) + m[ial + 1:]: cf for m, cf in Db.terms() if m[ial] == 6})
ok_c = deg_al == 6 and (c6 - (Ka**6 * Ks**4 / 16).rem(G)).rem(G) == 0
# (d) monomials in (v, alpha, u)
mons = sorted({(m[iv], m[ial], m[iu]) for m, _ in Db.terms()})
wts = sorted({i_ + k_ + 2 * j_ for i_, j_, k_ in mons})
ok_d = (len(mons) == 50 and wts == [6, 8, 10, 12] and all(k_ <= i_ for i_, _, k_ in mons)
        and max(m[0] for m in mons) == 12 and max(m[1] for m in mons) == 6 and max(m[2] for m in mons) == 6)
# (e) parity alpha -> -alpha, c -> -c
Dpar = K({m: cf * (-1)**(m[ial] + m[ic]) for m, cf in Db.terms()})
ok_e = (Dpar - Db).rem(G) == 0
# (f) equator c = 0, s = 1, alpha = 0
eqs = lambda P_: subs0(subs0(subs0(P_, ic, 0), is_, 1), ial, 0)  # noqa: E731
qe, j1e, pe = 2 * eqs(ent['Rrr']), eqs(ent['R01']), eqs(ent['Rrr']) + eqs(ent['R00'])
ok_f = eqs(Db) == (qe**2 - 4 * j1e**2) * (pe**2 + pe * qe + j1e**2)**2 and \
    qe**2 - 4 * j1e**2 == Kv**2 * (Kv**2 * Ka**4 - (Ka * Kir + Kb)**2)
check('A3', ok_a and ok_b and ok_c and ok_d and ok_e and ok_f,
      f"(a) v = 0 {ok_a}; (b) axis {ok_b}; (c) alpha degree {deg_al}, coefficient {ok_c}; (d) {len(mons)} monomials, "
      f"weights {wts}, k <= i, max powers ({max(m[0] for m in mons)}, {max(m[1] for m in mons)}, "
      f"{max(m[2] for m in mons)}) {ok_d}; (e) parity {ok_e}; (f) equator {ok_f}")

# ---------------------------------------------------------------------------------------------------------------
# A4: the map, numpy eigenvalues of eta R on own grids
# ---------------------------------------------------------------------------------------------------------------
rho_ = sp.Symbol('rho', positive=True)
sg, Rb = sp.symbols('sigma R_b', positive=True)
fexpr = (sp.tanh(sg * (rho_ + Rb)) - sp.tanh(sg * (rho_ - Rb))) / (2 * sp.tanh(sg * Rb))
fj = [sp.lambdify((rho_, sg, Rb), sp.diff(fexpr, rho_, k), 'numpy') for k in range(3)]
args_ = (v, al, u, f, f1, f2, r, c, s)
efn = {(i, j): sp.lambdify(args_, Rf[i, j], 'numpy') for i in range(3) for j in range(i, 3)}
etan = np.array([-1.0, 1.0, 1.0])


def blocks(vv, aa, uu, R_, C_, S_, sig, Rbv):
    F0, F1, F2 = (fj[k](R_, sig, Rbv) for k in range(3))
    Mx = np.empty(R_.shape + (3, 3))
    for i in range(3):
        for j in range(i, 3):
            val = efn[(i, j)](vv, aa, uu, F0, F1, F2, R_, C_, S_) * np.ones_like(R_)
            Mx[..., i, j] = etan[i] * val
            Mx[..., j, i] = etan[j] * val
    return Mx


def frac_I(vv, aa, uu, sig, Rbv, r1, r2, n=1200, chunk=150):
    if MUT == 'map':
        aa = 0.0
    rg = r1 + (r2 - r1) * (np.arange(n) + 0.5) / n
    tg = np.pi * (np.arange(n) + 0.5) / n
    num = den = 0.0
    for k in range(0, n, chunk):
        Rg, Tg = np.meshgrid(rg[k:k + chunk], tg, indexing='ij')
        Mx = blocks(vv, aa, uu, Rg, np.cos(Tg), np.sin(Tg), sig, Rbv)
        ev = np.linalg.eigvals(Mx)
        scale = np.abs(Mx).max(axis=(-2, -1))
        typeI = np.abs(ev.imag).max(axis=-1) <= 1e-8 * scale
        wgt = Rg**2 * np.sin(Tg)
        num += float((wgt * typeI).sum())
        den += float(wgt.sum())
    return 100 * num / den


fle = lambda rv: fj[0](rv, 8, 1)  # noqa: E731
le1, le2 = brentq(lambda rv: fle(rv) - 0.9, 0.5, 1.0, xtol=1e-14), brentq(lambda rv: fle(rv) - 0.1, 1.0, 1.5, xtol=1e-14)
ok_rad = (round(le1, 4), round(le2, 4)) == (0.8627, 1.1373)


def P1(tv):
    vv = 1 / np.cosh(2 * tv)**2
    return vv, -4 * vv * np.tanh(2 * tv), vv


rows = [('Le', 0.5, 0, 0.5, 1.15), ('Le', 0.5, 2, 0.5, 11.99), ('Le', 0.5, -2, 0.5, 11.99), ('Le', 0.5, 32, 0.5, 93.92),
        ('Le', 1, 4, 1, 10.55), ('Le', 2, 8, 2, 15.19), ('Le', 0.5, 0, 0, 2.50), ('Le', 0.5, 0, 2, 19.42),
        ('Le', *P1(-0.6), 8.597), ('Le', *P1(0.9), 10.641), ('Le', P1(0.9)[0], 0.0, P1(0.9)[0], 0.045),
        ('Rodal', 1, 4, 1, 26.24)]
ok4 = ok_rad
print(f"  Le's wall radii [{le1:.6f}, {le2:.6f}], printed [0.8627, 1.1373]: {ok_rad}")
for wall, vv, aa, uu, want in rows:
    sig, Rbv, r1, r2 = (8, 1, le1, le2) if wall == 'Le' else (4, 5, 4.25, 5.75)
    got = frac_I(float(vv), float(aa), float(uu), sig, Rbv, r1, r2)
    ok = abs(got - want) <= 0.10
    ok4 &= ok
    print(f"  {wall:5s} v = {vv:.4f}, alpha = {aa:+.4f}, u = {uu:.4f}: Type I {got:.3f} %, printed {want}, "
          f"|diff| {abs(got - want):.3f} {'ok' if ok else 'OUT'}", flush=True)
check('A4', ok4, f"wall radii {ok_rad}; 12 rows within 0.10 percentage points {ok4}")

# ---------------------------------------------------------------------------------------------------------------
# A5: Rodal's equator, own cubic discriminant from the trace, minors and determinant
# ---------------------------------------------------------------------------------------------------------------


def Deq(rv, aa):
    rv = np.atleast_1d(np.asarray(rv, float))
    Mx = blocks(1.0, aa, 1.0, rv, np.zeros_like(rv), np.ones_like(rv), 4, 5)
    tr = np.trace(Mx, axis1=-2, axis2=-1)
    mn = sum(Mx[..., i, i] * Mx[..., j, j] - Mx[..., i, j] * Mx[..., j, i] for i in range(3) for j in range(i + 1, 3))
    dt = np.linalg.det(Mx)
    b2, b1, b0 = -tr, mn, -dt  # lambda^3 + b2 lambda^2 + b1 lambda + b0
    return 18 * b2 * b1 * b0 - 4 * b2**3 * b0 + b2**2 * b1**2 - 4 * b1**3 - 27 * b0**2


want5 = {0.0: [(4.9458, 5.0660)], 0.5: [(4.9438, 4.9656), (4.9945, 5.0191), (5.0509, 5.0683)], 4.0: [(4.8981, 5.1036)]}
ok5 = True
rgrid = np.linspace(4.25, 5.75, 30001)
for aa, want in want5.items():
    a_use = 0.0 if (MUT == 'rodal' and aa == 4.0) else aa
    dv = Deq(rgrid, a_use)
    pos = dv > 0
    cross = [brentq(lambda rv: float(Deq(rv, a_use)[0]), rgrid[k], rgrid[k + 1], xtol=1e-13)
             for k in np.flatnonzero(np.diff(pos.astype(int)))]
    pts = ([4.25] if pos[0] else []) + cross + ([5.75] if pos[-1] else [])
    ivs = list(zip(pts[0::2], pts[1::2]))
    ok = len(ivs) == len(want) and all(abs(a1 - b1) <= 2e-4 and abs(a2 - b2) <= 2e-4 for (a1, a2), (b1, b2) in zip(ivs, want))
    ok5 &= ok
    print(f"  alpha = {aa}: Type I intervals {[(round(a1, 5), round(a2, 5)) for a1, a2 in ivs]}, printed {want} "
          f"{'ok' if ok else 'OUT'}", flush=True)
check('A5', ok5, f"Rodal's equatorial intervals at alpha = 0, 0.5, 4 within 2e-4 {ok5}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL), f"({time.time() - T0:.0f} s, mutation: {MUT or 'none'})")
sys.exit(1 if FAIL else 0)

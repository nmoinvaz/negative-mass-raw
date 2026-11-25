#!/usr/bin/env python3
"""ind81: the coordinator's independent check of #81 (the scalar form for a sheared warp shift).

Criteria L0-L4 in negative-mass-raw I81-mac/README.md. Imports nothing from the repository: own Ricci routine for a generic
b(t, x, y, z), the sheared shift through 2-jets of F at Q0, the case (B) algebra, and the z-axis point at 60 digits.
"""
import argparse
import sys
import time

import mpmath as mp
import sympy as sp

MUTS = ['pg', 'r1a', 'ident', 'c5', 'zoff']
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


# L0 -------------------------------------------------------------------------------------------------------------
print("== L0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
beta = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify), [lambda e, y=y: sp.diff(e, y) for y in
                                                                (t_, rr, th_, ph_)], sp.simplify)
check('L0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# L1 -------------------------------------------------------------------------------------------------------------
print("\n== L1: generic b(t, x, y, z): the ten frame components ==", flush=True)
t, x, y, z = sp.symbols('t x y z', real=True)
XS = [t, x, y, z]
bF = sp.Function('b')(t, x, y, z)
g = sp.Matrix([[-1 + bF**2, bF, 0, 0], [bF, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi = sp.Matrix([[-1, bF, 0, 0], [bF, 1 - bF**2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
simp = lambda e: sp.expand(sp.cancel(e))
R = christoffel_ricci(g, gi, [lambda e, v_=v_: sp.diff(e, v_) for v_ in XS], simp)
E = sp.Matrix([[1, 0, 0, 0], [-bF, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
RF = (E.T * R * E).applyfunc(simp)


def closed(b):
    d = lambda *a: sp.diff(b, *a)
    bx = d(x)
    grad2 = d(y)**2 + d(z)**2
    Dt = d(t) - b * bx
    T = sp.zeros(4, 4)
    T[0, 0] = -grad2 / 2 - bx**2 + d(x, t) - b * d(x, x)
    T[1, 1] = bx**2 - grad2 / 2 - d(x, t) + b * d(x, x)
    T[0, 1] = T[1, 0] = -(d(y, y) + d(z, z)) / 2
    for i, a in ((2, y), (3, z)):
        T[0, i] = T[i, 0] = sp.diff(bx, a) / 2
        T[1, i] = T[i, 1] = bx * d(a) / 2 - (0 if MUT == 'r1a' else sp.diff(Dt, a) / 2)
        for j, c in ((2, y), (3, z)):
            T[i, j] = d(a) * d(c) / 2
    return T


T1 = closed(bF)
l1 = all(zero(RF[i, j] - T1[i, j]) for i in range(4) for j in range(4))
check('L1', l1, f"own Ricci in the frame equals the printed closed forms: {l1}")

# L2 -------------------------------------------------------------------------------------------------------------
print("\n== L2: the sheared shift b = -v F(q) ==", flush=True)
v, f0, f1, f2, Q0 = sp.symbols('v f0 f1 f2 Q0', real=True)
X = x - v * t
q = X**2 + y**2 + 2 * z**2 + X * y / 2
bS = -v * (f0 + f1 * (q - Q0) + f2 * (q - Q0)**2 / 2)  # exact to second order at q = Q0
TS = closed(bS).applyfunc(lambda e: sp.expand(e.subs(Q0, q)))
Xs = sp.Symbol('X', real=True)
TS = TS.applyfunc(lambda e: sp.expand(e.subs(x, Xs + v * t)))
qX = sp.expand(q.subs(x, Xs + v * t))
qx_, qy_, qz_ = sp.diff(qX, Xs), sp.diff(qX, y), sp.diff(qX, z)
wv = [qy_, qz_]
wp = [-qz_, qy_]
Rv = lambda a, idx: sum(a[k] * TS[2 + k, idx] for k in range(2))  # R(a, E_idx)
Rvv = lambda a, c: sum(a[k] * c[m] * TS[2 + k, 2 + m] for k in range(2) for m in range(2))
res = [Rv(wp, 0), Rv(wp, 1), Rvv(wp, wv), Rvv(wp, wp)]
want = [v * f1 * z, v**2 * f1 * (1 - f0) * z, 0, 0]
i1 = all(zero(a - c) for a, c in zip(res, want))
w2 = qy_**2 + qz_**2
i2 = zero(w2 * (TS[0, 0] + TS[1, 1]) + 2 * Rvv(wv, wv))
bx = sp.diff(bS, x)
cross = sp.expand((sp.diff(bx, y) * sp.diff(bS, z) - sp.diff(bx, z) * sp.diff(bS, y)).subs(Q0, q).subs(x, Xs + v * t))
cr = zero(cross - 2 * v**2 * f1**2 * z)
ident = zero(Rv(wv, 1) - v * (1 - f0) * Rv(wv, 0) - (2 if MUT == 'ident' else 1) * v**2 * f1**2 * qx_ * w2)
rw0 = zero(Rv(wv, 0) + (v / 2) * (f2 * qx_ * w2 + f1 * qy_ / 2))
check('L2', cr and i1 and i2 and ident and rw0, f"cross = 2 v^2 F'^2 z: {cr}; (I1) residues: {i1}; (I2): {i2}; "
      f"identity: {ident}; R(w, E_0): {rw0}")

# L3 -------------------------------------------------------------------------------------------------------------
print("\n== L3: case (B) algebra ==", flush=True)
lam, r0, r1, R00, R11, R01 = sp.symbols('lam r0 r1 R00 R11 R01', real=True)
Rm = sp.Matrix([[R00, R01, 0, r0], [R01, R11, 0, r1], [0, 0, lam, 0], [r0, r1, 0, 0]])
N = Rm - lam * sp.diag(-1, 1, 1, 1)
minors = [N.extract([i, j], [k, l]).det() for i in range(4) for j in range(i + 1, 4) for k in range(4)
          for l in range(k + 1, 4)]
c3 = (R00 + lam) * lam + r0**2
c4 = (R11 - lam) * lam + r1**2
c5 = R01 * lam + r0 * r1
has = [any(zero(m - c) or zero(m + c) for m in minors) for c in (c3, c4, c5)]
sub = {R00: -lam - r0**2 / lam, R11: lam - r1**2 / lam, R01: (1 if MUT == 'c5' else -1) * r0 * r1 / lam}
allzero = all(zero(m.subs(sub)) for m in minors)
check('L3', all(has) and allzero, f"c3, c4, c5 among the minors: {has}; every minor vanishes on the solved forms: "
      f"{allzero}")

# L4 -------------------------------------------------------------------------------------------------------------
print("\n== L4: the z-axis point ==", flush=True)
p = (-32 + mp.sqrt(32**2 + 4 * 32)) / 64
one_f = mp.sqrt(p)
vz, zz = mp.mpf(1), mp.mpf(1) / 2
F0 = 1 - one_f
F1 = -1 / (256 * vz**2 * one_f * zz**2)
F2 = (-one_f / (64 * zz**2) - 6 * F1) / (16 * zz**2)
TSf = sp.lambdify([Xs, y, z, v, f0, f1, f2, t], TS, modules='mpmath')


def minors_at(F2v):
    M = mp.matrix(TSf(0, 0, zz, vz, F0, F1, F2v, 0))
    la = M[3, 3]
    Nn = M - la * mp.diag([-1, 1, 1, 1])
    sc = max(abs(Nn[i, j]) for i in range(4) for j in range(4))
    mx = max(abs(Nn[i, k] * Nn[j, l] - Nn[i, l] * Nn[j, k]) for i in range(4) for j in range(i + 1, 4)
             for k in range(4) for l in range(k + 1, 4))
    return mx, sum(Nn[i, i] for i in range(4)), sc


mx, tr, sc = minors_at(F2 + (mp.mpf(1) / 10 if MUT == 'zoff' else 0))
mxd, _, _ = minors_at(F2 + mp.mpf(1) / 10)
l4 = mx < mp.mpf(10) ** -40 and tr < 0 and mxd > mp.mpf(10) ** -6
check('L4', l4, f"F = {mp.nstr(F0, 11)}, F' = {mp.nstr(F1, 11)}, F'' = {mp.nstr(F2, 11)}; largest minor "
      f"{mp.nstr(mx, 4)}, trace {mp.nstr(tr, 6)}; with F'' + 1/10 largest minor {mp.nstr(mxd, 6)}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

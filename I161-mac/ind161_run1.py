#!/usr/bin/env python3
"""ind161: the coordinator's independent check of #161 (closure for planar shifts that cross |u| = 1 or do not travel).

Criteria Q0-Q5 in negative-mass-raw I161-mac/README.md. Imports nothing from the repository: own Ricci routine, own
d'Alembertian, own RK4 geodesic and Jacobi integrator with Richardson extrapolation, own composite Gauss-Legendre.
"""
import argparse
import math
import sys
import time

import numpy as np
import sympy as sp

MUTS = ['pg', 'null', 'theta', 'alpha', 'rk', 'conv']
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
    return sp.simplify(sp.expand(e)) == 0


def box(f, g, gi, X, sq):
    """d'Alembertian (1/sqrt|g|) d_a (sqrt|g| g^ab d_b f) in 2D; sq = sqrt(-det g), checked below."""
    assert sp.simplify(sq**2 + g.det()) == 0
    return sp.simplify(sum(sp.diff(sq * sum(gi[a, b_] * sp.diff(f, X[b_]) for b_ in range(2)), X[a])
                           for a in range(2)) / sq)


# Q0 -------------------------------------------------------------------------------------------------------------
print("== Q0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
bpg = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + bpg**2, bpg, 0, 0], [bpg, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify),
                        [lambda e, y=y: sp.diff(e, y) for y in (t_, rr, th_, ph_)], sp.simplify)
check('Q0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# Q1 -------------------------------------------------------------------------------------------------------------
print("\n== Q1: the criterion in null coordinates ==", flush=True)
p, q = sp.symbols('p q', real=True)
sig = sp.Function('sigma')(p, q)
gn = sp.Matrix([[0, -sp.exp(2 * sig)], [-sp.exp(2 * sig), 0]])
gni = sp.Matrix([[0, -sp.exp(-2 * sig)], [-sp.exp(-2 * sig), 0]])
Rn = christoffel_ricci(gn, gni, [lambda e: sp.diff(e, p), lambda e: sp.diff(e, q)], sp.simplify)
spq = sp.diff(sig, p, q)
Kn = (1 if MUT == 'null' else 2) * spq * sp.exp(-2 * sig)
q1a = all(zero(Rn[i, j] - Kn * gn[i, j]) for i in range(2) for j in range(2))
fF = sp.Function('f')(p, q)
q1b = zero(box(fF, gn, gni, [p, q], sp.exp(2 * sig)) + 2 * sp.exp(-2 * sig) * sp.diff(fF, p, q))
K2 = 2 * spq * sp.exp(-2 * sig)
lhs = sp.diff(sp.log(2 * spq), p, q)  # ln(-R_pq) with R_pq = -2 sigma_pq
rhs = -(sp.exp(2 * sig) / 2) * (box(sp.log(K2), gn, gni, [p, q], sp.exp(2 * sig)) - 2 * K2)
q1c = zero(lhs - rhs)
check('Q1', q1a and q1b and q1c, f"R = K g with K = 2 sigma_pq e^(-2 sigma): {q1a}; box f = -2 e^(-2 sigma) f_pq: {q1b}; "
      f"d_p d_q ln R_pq = -(e^(2 sigma)/2)(box ln K - 2K): {q1c}")

# Q2 -------------------------------------------------------------------------------------------------------------
print("\n== Q2: the planar PG metric and the static reduction ==", flush=True)
t, x = sp.symbols('t x', real=True)
bF = sp.Function('b')(t, x)
gp = sp.Matrix([[-1 + bF**2, bF], [bF, 1]])
gpi = sp.Matrix([[-1, bF], [bF, 1 - bF**2]])
Rp = christoffel_ricci(gp, gpi, [lambda e: sp.diff(e, t), lambda e: sp.diff(e, x)], sp.simplify)
aF = sp.diff(bF, t) - bF * sp.diff(bF, x)
Kp = -sp.diff(aF, x)
q2a = all(zero(Rp[i, j] - Kp * gp[i, j]) for i in range(2) for j in range(2))
uF = sp.Function('u')(x)
gs = gp.subs(bF, uF)
gsi = gpi.subs(bF, uF)
Ks = sp.diff(uF * sp.diff(uF, x), x)
q2b = zero(Kp.subs(bF, uF).doit() - Ks)
Th = (1 - uF**2) * sp.diff(Ks, x) / Ks + (1 if MUT == 'theta' else -1) * 2 * uF * sp.diff(uF, x)
q2c = zero(box(sp.log(Ks), gs, gsi, [t, x], 1) - 2 * Ks - sp.diff(Th, x))
check('Q2', q2a and q2b and q2c, f"R = K g with K = -a_x: {q2a}; static K = (uu')': {q2b}; box ln K - 2K = Theta': {q2c}")

# Q3 -------------------------------------------------------------------------------------------------------------
print("\n== Q3: the superluminal bubble u_s = 3/(1 + xi^2) and the crossing exponent ==", flush=True)
xi = sp.Symbol('xi', real=True)
us = 3 / (1 + xi**2)
hz = sorted(sp.solve(sp.Eq(us, 1), xi), key=lambda r: float(r))
alphas = [sp.simplify(-(us * sp.diff(us, xi)).subs(xi, h)) for h in hz]
want_alpha = [sp.Integer(2) * sp.sqrt(2) / 3 if MUT == 'alpha' else -2 * sp.sqrt(2) / 3, 2 * sp.sqrt(2) / 3]
q3a = [sp.simplify(h) for h in hz] == [-sp.sqrt(2), sp.sqrt(2)] and all(sp.simplify(a - w) == 0 for a, w in
                                                                         zip(alphas, want_alpha))
Kus = sp.diff(us * sp.diff(us, xi), xi)
sp_ = 2 / (1 - us**2)
Phi = sp.simplify(Kus * (1 - us**2))
comps = [(-sp.oo, -sp.sqrt(2), -2), (-sp.sqrt(2), sp.sqrt(2), 0), (sp.sqrt(2), sp.oo, 2)]
q3b = True
rows = []
for lo, hi, mid in comps:
    sgn = sp.sign(sp_.subs(xi, mid))
    ends = []
    for e_, side in ((lo, '+'), (hi, '-')):
        if e_ in (sp.oo, -sp.oo):
            lim_sp = sp.limit(sp_, xi, e_)
            div = lim_sp != 0 and lim_sp.is_finite
        else:
            res = sp.limit(sp_ * (xi - e_), xi, e_, dir=side)
            div = res != 0 and res.is_finite
        phil = sp.limit(Phi, xi, e_, dir=side) if e_ not in (sp.oo, -sp.oo) else sp.limit(Phi, xi, e_)
        ends.append((bool(div), phil))
    ok = sgn != 0 and all(d for d, _ in ends) and all(pl == 0 for _, pl in ends) and Kus.subs(xi, mid) != 0
    q3b = q3b and ok
    rows.append((str(lo), str(hi), int(sgn), ends))
eta, u1, u2, kap, gam, alp = sp.symbols('eta u1 u2 kappa gamma alpha', nonzero=True)
uu = 1 + u1 * eta + u2 * eta**2
Kc = kap * eta**gam
expr = sp.expand(((1 - uu**2) * sp.diff(Kc, eta) - (2 * alp + 2 * uu * sp.diff(uu, eta)) * Kc) / (kap * eta**gam))
lead = sp.expand(expr).subs(eta, 0)
gsol = sp.solve(lead, gam)
q3c = len(gsol) == 1 and sp.simplify(gsol[0] + (alp + u1) / u1) == 0
check('Q3', q3a and q3b and q3c, f"horizons {hz}, alpha {alphas}: {q3a}; components (sign s', [(s diverges, lim Phi)]): "
      f"{rows}: {q3b}; gamma = {gsol}: {q3c}")

# Q4 -------------------------------------------------------------------------------------------------------------
print("\n== Q4: Theorem E's example, own geodesics and Jacobi field ==", flush=True)
W = (1, 3, 1, 1) if MUT == 'rk' else (1, 2, 2, 1)


def fexp(z):
    return math.exp(-1 / z) if z > 0 else 0.0


def fexp1(z):
    return math.exp(-1 / z) / z**2 if z > 0 else 0.0


def S(z):
    a, b = fexp(z), fexp(1 - z)
    return a / (a + b)


def S1(z):
    a, b = fexp(z), fexp(1 - z)
    return (fexp1(z) * b + a * fexp1(1 - z)) / (a + b)**2


H = lambda z: 1.5 * S(z)
H1 = lambda z: 1.5 * S1(z)


def rhs(y):
    pp, qq, pd, qd, A, Ad = y
    Hp, Jq, H1p, J1q = H(pp), H(qq), H1(pp), H1(qq)
    sp_p, sp_q = H1p * Jq, Hp * J1q
    K = 2 * H1p * J1q * math.exp(-2 * Hp * Jq)
    return (pd, qd, -2 * sp_p * pd * pd, -2 * sp_q * qd * qd, Ad, K * A)


def geodesic(s, dt, T=10.0):
    r2 = math.sqrt(2)
    y = [-1 - s / r2, -1 + s / r2, 1 / r2, 1 / r2, 1.0, 0.0]
    n = int(round(T / dt))
    minA, minAd, maxnorm = 1.0, 0.0, 0.0
    for _ in range(n):
        k1 = rhs(y)
        k2 = rhs([y[i] + dt / 2 * k1[i] for i in range(6)])
        k3 = rhs([y[i] + dt / 2 * k2[i] for i in range(6)])
        k4 = rhs([y[i] + dt * k3[i] for i in range(6)])
        y = [y[i] + dt / 6 * (W[0] * k1[i] + W[1] * k2[i] + W[2] * k3[i] + W[3] * k4[i]) for i in range(6)]
        minA, minAd = min(minA, y[4]), min(minAd, y[5])
        nrm = abs(2 * math.exp(2 * H(y[0]) * H(y[1])) * y[2] * y[3] - 1)
        maxnorm = max(maxnorm, nrm)
    return y[5], minA, minAd, maxnorm


xg, wg = np.polynomial.legendre.leggauss(10)
lo, hi = -1 / math.sqrt(2), 1 / math.sqrt(2)


def Lprime(npan, dt):
    tot, mA, mAd, mn = 0.0, 1.0, 0.0, 0.0
    edges = np.linspace(lo, hi, npan + 1)
    for a, b in zip(edges[:-1], edges[1:]):
        for xn, wn in zip(xg, wg):
            s = (a + b) / 2 + (b - a) / 2 * xn
            Ad, mA_, mAd_, mn_ = geodesic(s, dt)
            tot += (b - a) / 2 * wn * Ad
            mA, mAd, mn = min(mA, mA_), min(mAd, mAd_), max(mn, mn_)
    return tot, mA, mAd, mn


res = {}
for npan in (16, 32):
    for dt in (0.01, 0.005):
        res[(npan, dt)] = Lprime(npan, dt)
rich = {npan: (16 * res[(npan, 0.005)][0] - res[(npan, 0.01)][0]) / 15 for npan in (16, 32)}
Lp = rich[32]
sp_dt = abs(res[(32, 0.005)][0] - res[(32, 0.01)][0]) / 15
sp_pan = abs(rich[32] - rich[16])
minA = min(r[1] for r in res.values())
minAd = min(r[2] for r in res.values())
maxn = max(r[3] for r in res.values())
q4 = abs(Lp - 4.5) < 1e-9 and minA >= 1 - 1e-12 and minAd >= -1e-12 and maxn < 1e-10
check('Q4', q4, f"L'(10) = {Lp:.13f} (|L' - 4.5| = {abs(Lp - 4.5):.1e}); spreads: dt {sp_dt:.1e}, panels {sp_pan:.1e}; "
      f"min A = {minA:.13f}, min A_tau = {minAd:.1e}, normalization {maxn:.1e}")

# Q5 -------------------------------------------------------------------------------------------------------------
print("\n== Q5: linear order and the convolution ==", flush=True)
ep = sp.Symbol('epsilon', positive=True)
Bf = sp.Function('B')(t, x)
bl = ep * Bf
gl = sp.Matrix([[-1 + bl**2, bl], [bl, 1]])
gli = sp.Matrix([[-1, bl], [bl, 1 - bl**2]])
Kl = -sp.diff(sp.diff(bl, t) - bl * sp.diff(bl, x), x)
Kt = sp.expand(Kl / ep)
Cl = box(sp.log(Kt), gl, gli, [t, x], 1) - 2 * ep * Kt  # ln K = ln eps + ln Kt; box(ln eps) = 0
C0 = sp.simplify(Cl.subs(ep, 0))
K1 = -sp.diff(Bf, t, x)
q5a = zero(C0 - (-sp.diff(sp.log(K1), t, 2) + sp.diff(sp.log(K1), x, 2)))
z_, y_ = sp.symbols('z y', real=True)
Fp = lambda w: w * (1 - w) * (1 - 2 * w)


def conv(yv):
    return sp.integrate(Fp(z_) * Fp(yv - z_), (z_, sp.Max(0, yv - 1), sp.Min(1, yv)))


q5b, vals = True, []
for tv in (sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(4, 5)):
    xl, xh = sp.Max(tv - 1, -tv), sp.Min(tv, 1 - tv)
    lhs5 = sp.integrate(Fp(tv - x) * Fp(tv + x), (x, xl, xh))
    rhs5 = conv(tv if MUT == 'conv' else 2 * tv)
    vals.append((str(tv), str(lhs5), str(rhs5)))
    q5b = q5b and sp.simplify(lhs5 - rhs5) == 0
nonzero = conv(sp.Rational(2, 5)) != 0
check('Q5', q5a and q5b and nonzero, f"eps^0 term of C = (-d_t^2 + d_x^2) ln K1: {q5a}; int K1 dx = (F*G)(2t) at t = "
      f"1/5, 1/2, 4/5: {vals}: {q5b}; F*G(2/5) = {conv(sp.Rational(2, 5))} != 0: {nonzero}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

#!/usr/bin/env python3
"""ind151: the coordinator's independent check of #151 (the Ellis family's linear e-folding time at m/a = 1/2).

Criteria E0-E9 in negative-mass-raw I151-mac/README.md. Imports nothing from the repository and no scipy: own Ricci
routine, own linearization in the gauge dPhi = 0, own Numerov, RK4, Cauchy-Frobenius throat crossing and root finder.
"""
import argparse
import math
import sys
import time

import mpmath as mp
import numpy as np
import sympy as sp

MUTS = ['pg', 'ghost', 'gamma0', 'scalar', 'wtyped', 'numerov', 'rho', 'frob', 'match', 'tfac']
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


# E0 -------------------------------------------------------------------------------------------------------------
print("== E0: planted Ricci ==", flush=True)
t_, rr, th_, ph_, Mm = sp.symbols('t r theta phi M', positive=True)
bpg = sp.sqrt(2 * Mm) / rr if MUT == 'pg' else sp.sqrt(2 * Mm / rr)
gpg = sp.Matrix([[-1 + bpg**2, bpg, 0, 0], [bpg, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th_)**2]])
Rpg = christoffel_ricci(gpg, gpg.inv().applyfunc(sp.simplify),
                        [lambda e, y=y: sp.diff(e, y) for y in (t_, rr, th_, ph_)], sp.simplify)
check('E0', Rpg.applyfunc(sp.simplify) == sp.zeros(4, 4), "Painleve-Gullstrand Ricci-flat")

# E1 -------------------------------------------------------------------------------------------------------------
print("\n== E1: the background ==", flush=True)
t, x, th, ph = sp.symbols('t x theta phi', real=True)
g1 = sp.Symbol('gamma1', positive=True)
XS = [t, x, th, ph]
DX = [lambda e, v=v: sp.diff(e, v) for v in XS]
AT = sp.atan(x)
d0, a0, c0 = g1 * AT, -g1 * AT, sp.log(1 + x**2) / 2 - g1 * AT


def diag_metric(dd, aa, cc):
    return sp.diag(-sp.exp(2 * dd), sp.exp(2 * aa), sp.exp(2 * cc), sp.exp(2 * cc) * sp.sin(th)**2)


def diag_inv(g):
    return sp.diag(*[1 / g[i, i] for i in range(4)])


gb = diag_metric(d0, a0, c0)
Rb = christoffel_ricci(gb, diag_inv(gb), DX, sp.simplify)
Phix = 1 / (1 + x**2)  # Phi_x / Phi_1
kp_good = (2 if MUT == 'ghost' else -2) * (1 + g1**2)  # the value tested as passing: kappa Phi_1^2
kp_bad = -kp_good
E_good = [sp.simplify(Rb[i, j] - (kp_good * Phix**2 if (i, j) == (1, 1) else 0)) for i in range(4) for j in range(i, 4)]
E_bad = sp.simplify(Rb[1, 1] - kp_bad * Phix**2)
box_bg = sp.simplify(sp.diff(sp.exp(d0 + a0 + 2 * c0) * sp.exp(-2 * a0) * Phix, x))
e1 = all(e == 0 for e in E_good) and E_bad != 0 and box_bg == 0
check('E1', e1, f"R - kappa dPhi dPhi = 0 at kappa Phi_1^2 = {kp_good}: {all(e == 0 for e in E_good)}; "
      f"nonzero at {kp_bad}: {E_bad != 0}; box Phi = 0: {box_bg == 0}")

# E2 -------------------------------------------------------------------------------------------------------------
print("\n== E2: the map [SN26] -> [GGS09a] ==", flush=True)
a_, m_, r_, xt_ = sp.symbols('a m r xtilde', positive=True)
gam = m_ / a_
u_of_X = lambda X: gam * (sp.atan(X) - sp.pi / 2)
Om = 1 + a_**2 / (4 * r_**2)
rhoE = r_ - a_**2 / (4 * r_)
idA = sp.simplify(sp.diff(rhoE, r_) - Om) == 0  # d rho_E = Omega dr
idB = sp.simplify(Om**2 * r_**2 - (rhoE**2 + a_**2)) == 0  # Omega^2 r^2 = rho_E^2 + a^2
# in the chart (ttilde, xtilde) with rho_E = a xtilde, t = a e^{+-pi gamma} ttilde:
tfac = a_ * sp.exp((-1 if MUT == 'gamma0' else 1) * sp.pi * gam)
u = u_of_X(xt_)
sn = [-sp.exp(2 * u) * tfac**2, sp.exp(-2 * u) * a_**2, sp.exp(-2 * u) * a_**2 * (xt_**2 + 1)]
lam2 = a_**2 * sp.exp(sp.pi * gam)
can = [-sp.exp(2 * gam * sp.atan(xt_)), sp.exp(-2 * gam * sp.atan(xt_)), sp.exp(-2 * gam * sp.atan(xt_)) * (1 + xt_**2)]
hom = [sp.simplify(s - lam2 * c) for s, c in zip(sn, can)]
idC = all(h == 0 for h in hom)
Rar = sp.exp(-u) * a_ * sp.sqrt(xt_**2 + 1)  # areal radius
Mplus = sp.limit(Rar * (1 + (-sp.exp(2 * u))) / 2, xt_, sp.oo)
idD = sp.simplify(Mplus - m_) == 0
dlnR = sp.simplify(sp.diff(sp.log(Rar), xt_))
idE = sp.simplify(dlnR - (xt_ - gam) / (1 + xt_**2)) == 0  # minimum at xtilde = gamma, sign - to +
Rstar = sp.sqrt(a_**2 + m_**2) * sp.exp(gam * sp.atan(a_ / m_))
alth = sp.exp(u.subs(xt_, gam))
bet = sp.Symbol('beta', positive=True)
tau = a_ * sp.exp(sp.pi * gam) / bet
Tid = tau * alth / Rstar - sp.exp(2 * gam * sp.atan(gam)) / (sp.sqrt(1 + gam**2) * bet)
rmin_id = Rar.subs(xt_, gam) - Rstar
sym_closed = {}
for nm, e in (('R(gamma) = R_star', rmin_id), ('T identity', Tid)):
    z = sp.simplify(e)
    if z == 0:
        sym_closed[nm] = 'simplified to 0'
    else:
        worst = max(abs(sp.N(e.subs({a_: av, m_: mv, bet: sp.Rational(17, 10)}), 50))
                    for av, mv in ((2, 1), (1, 3), (sp.Rational(7, 3), sp.Rational(1, 5)), (5, 2), (sp.Rational(1, 2), 4)))
        sym_closed[nm] = f"sympy did not close it; worst at 5 points (50 digits) {sp.N(worst, 3)}"
        if worst > 1e-40:
            sym_closed[nm] += ' FAIL'
num = {a_: 2, m_: 1}
Rs_n = float(sp.N(Rstar.subs(num), 30))
al_n = float(sp.N(alth.subs(num), 30))
idF = abs(Rs_n - 3.8895) <= 5e-5 and abs(al_n - 0.575) <= 5e-4
e2 = idA and idB and idC and idD and idE and all('FAIL' not in v for v in sym_closed.values()) and idF
check('E2', e2, f"d rho_E = Omega dr: {idA}; Omega^2 r^2 = rho_E^2 + a^2: {idB}; homothety a^2 e^(pi gamma): {idC} "
      f"{[str(h) for h in hom] if not idC else ''}; M_+ = m: {idD}; d ln R/dx = (x - gamma)/(1 + x^2): {idE}; "
      f"{sym_closed}; R_star(2, 1) = {Rs_n:.6f}, alpha_th = {al_n:.6f}: {idF}")
ALPHA_OVER_R = al_n / Rs_n

# E3 -------------------------------------------------------------------------------------------------------------
print("\n== E3: linearization in the gauge dPhi = 0 ==", flush=True)
eps = sp.Symbol('epsilon')
beta = sp.Symbol('beta', positive=True)
Cf, Gf = sp.Function('C')(x), sp.Function('G')(x)
ebt = sp.exp(beta * t)
dd_pert = Gf if MUT == 'scalar' else Gf - Cf  # delta d = delta a - 2 delta c (mutation: delta a - delta c)
dP, aP, cP = d0 + eps * dd_pert * ebt, a0 + eps * (Cf + Gf) * ebt, c0 + eps * Cf * ebt
gp = diag_metric(dP, aP, cP)
Rp = christoffel_ricci(gp, diag_inv(gp), DX, lambda e: e)
print(f"   perturbed Ricci built ({time.time() - T0:.0f} s)", flush=True)
lin = lambda e: sp.diff(e, eps).subs(eps, 0)
dE = {'tt': lin(Rp[0, 0]), 'tx': lin(Rp[0, 1]), 'xx': lin(Rp[1, 1]), 'thth': lin(Rp[2, 2])}
sqrtmg = sp.exp(dP + aP + 2 * cP)  # sqrt(-g) / sin(theta)
boxPhi = sp.diff(sqrtmg * sp.exp(-2 * aP) * Phix, x) / sqrtmg  # Phi_t = 0, Phi = atan x
dE['scalar'] = lin(boxPhi)
print(f"   linearized ({time.time() - T0:.0f} s)", flush=True)
Cs, Gs, Gp, G2 = sp.symbols('Cs Gs Gp G2')
dp, cp = sp.diff(d0, x), sp.diff(c0, x)
C1 = dp * Cs + cp * Gs
C2 = sp.diff(dp, x) * Cs + dp * C1 + sp.diff(cp, x) * Gs + cp * Gp


def reduce_(e):
    e = e.subs({t: 0, th: 1})
    e = e.subs({sp.Derivative(Cf, (x, 2)): C2, sp.Derivative(Gf, (x, 2)): G2})
    e = e.subs({sp.Derivative(Cf, x): C1, sp.Derivative(Gf, x): Gp})
    return e.subs({Cf: Cs, Gf: Gs})


red = {k: reduce_(v) for k, v in dE.items()}
th_lin = red['thth']
coefGp = sp.diff(th_lin, Gp)
Gp_expr = -th_lin.subs(Gp, 0) / coefGp
has_G2 = th_lin.has(G2)
G2_expr = sp.diff(Gp_expr, x) + sp.diff(Gp_expr, Cs) * C1 + sp.diff(Gp_expr, Gs) * Gp_expr
PTS = [(sp.Rational(3, 10), sp.Rational(1, 2), sp.Rational(17, 10)), (sp.Rational(-6, 5), sp.Rational(1, 2), sp.Rational(19, 10)),
       (sp.Rational(5, 2), 1, sp.Rational(49, 10)), (sp.Rational(7, 10), sp.Rational(1, 4), sp.Rational(13, 10)),
       (sp.Rational(-2, 5), sp.Rational(3, 2), sp.Rational(31, 10)), (sp.Rational(19, 10), sp.Rational(3, 4), sp.Rational(11, 5))]


def coef_at(e, pt):
    xv, gv, bv = pt
    e = e.subs({x: xv, g1: gv, beta: bv})
    return [abs(sp.N(e.subs({Cs: 1, Gs: 0}), 50)), abs(sp.N(e.subs({Cs: 0, Gs: 1}), 50))]


resid = {}
for k in ('tt', 'tx', 'xx', 'thth', 'scalar'):
    e = red[k].subs(G2, G2_expr).subs(Gp, Gp_expr)
    resid[k] = max(max(coef_at(e, pt)) for pt in PTS)
    print(f"   {k}: largest coefficient {sp.N(resid[k], 3)} ({time.time() - T0:.0f} s)", flush=True)
# #151's printed ODE for method C (ellis_efold.md), typed here
C2run = -(2 * x / (1 + x**2)) * C1 + beta**2 * sp.exp(-4 * g1 * AT) * Cs + (2 / (x - g1)) * (C1 - g1 * Cs / (1 + x**2))
Gp_run = (C2run - sp.diff(dp, x) * Cs - dp * C1 - sp.diff(cp, x) * Gs) / cp
run_diff = max(max(coef_at(Gp_run - Gp_expr, pt)) for pt in PTS)
# P, Q: (x - gamma) G' = P C + Q G, analytic at the throat
Pexpr = (x - g1) * Gp_expr.subs({Cs: 1, Gs: 0})
Qexpr = (x - g1) * Gp_expr.subs({Cs: 0, Gs: 1})
anal = []
for gv in (sp.Rational(1, 2), 1):
    for e in (Pexpr, Qexpr):
        vals = [sp.N(e.subs({g1: gv, beta: sp.Rational(17, 10), x: gv + s * sp.Rational(1, 10**20)}), 50) for s in (1, -1)]
        anal.append(abs(vals[0] - vals[1]) / (1 + abs(vals[0])))
anal_ok = max(anal) < 1e-15
e3 = all(v < 1e-40 for v in resid.values()) and run_diff < 1e-40 and anal_ok and not has_G2
check('E3', e3, f"residuals on the reduced system (largest coefficient at 6 points): "
      f"{ {k: float(sp.N(v, 3)) for k, v in resid.items()} }; #151's printed ODE gives the same G': {float(sp.N(run_diff, 3))}; "
      f"P, Q continuous across the throat (rel jump at 1e-20): {float(max(anal)):.1e}; G'' absent from thth: {not has_G2}")

# numeric forms of P = P0 + beta^2 P2, Q = Q0 + beta^2 Q2
P0s, P2s = Pexpr.subs(beta, 0), sp.diff(Pexpr, beta, 2) / 2
Q0s, Q2s = Qexpr.subs(beta, 0), sp.diff(Qexpr, beta, 2) / 2
poly_chk = max(abs(sp.N((Pexpr - P0s - beta**2 * P2s).subs({x: sp.Rational(9, 10), g1: sp.Rational(1, 2), beta: 3}), 40)),
               abs(sp.N((Qexpr - Q0s - beta**2 * Q2s).subs({x: sp.Rational(9, 10), g1: sp.Rational(1, 2), beta: 3}), 40)))
print(f"   P, Q quadratic in beta: residual {sp.N(poly_chk, 3)}", flush=True)

# E4 -------------------------------------------------------------------------------------------------------------
print("\n== E4: the potential ==", flush=True)
CW = 3 if MUT == 'wtyped' else 2


def W_sym(xx, g):
    at = sp.atan(xx)
    k = g / (1 + g**2)
    F = 1 + k * (1 + g * xx) * at
    Fx = k * ((1 + g * xx) / (1 + xx**2) + g * at)
    return sp.exp(4 * g * at) * (-3 / (1 + xx**2) + 3 * (xx - g)**2 / (1 + xx**2)**2 + CW * (Fx / F)**2
                                 - 4 * g / (1 + xx**2) * Fx / F + 4 * k * (xx - g) / (F * (1 + xx**2)**2))


w0 = sp.simplify(W_sym(x, 0) + 3 / (1 + x**2)**2) == 0
dpar = lambda e: sp.exp(2 * g1 * AT) * sp.diff(e, x)  # the operator partial = e^{2 gamma atan x} d/dx
kPx2 = -2 * (1 + g1**2) * Phix**2  # kappa Phi_x^2
V = sp.exp(2 * (d0 - c0)) - sp.exp(2 * (d0 - a0)) * sp.diff(c0, x)**2 - kPx2 * sp.exp(2 * (d0 - c0)) / sp.diff(c0, x)**2
Fp = 1 + g1 / (1 + g1**2) * (1 + g1 * x) * AT
Psi0 = sp.exp(c0) / (x - g1) * Fp
Wsusy = -V + 2 * (dpar(Psi0) / Psi0)**2
zm = dpar(dpar(Psi0)) - V * Psi0
Wthroat = sp.exp(4 * g1 * sp.atan(g1)) * (-3 / (1 + g1**2) - 2 * g1**2 / (1 + g1**2)**2)
worst_w = worst_z = worst_t = 0
with mp.workdps(40):
    for gv in (sp.Rational(1, 2), 1):
        for xv in (sp.Rational(-37, 10), sp.Rational(-9, 10), sp.Rational(1, 7), sp.Rational(13, 10), sp.Rational(3, 1), sp.Rational(61, 10)):
            sb = {g1: gv, x: xv}
            wt, ws = sp.N(W_sym(x, g1).subs(sb), 40), sp.N(Wsusy.subs(sb), 40)
            worst_w = max(worst_w, abs(wt - ws) / abs(ws))
            worst_z = max(worst_z, abs(sp.N(zm.subs(sb), 40)) / abs(sp.N((V * Psi0).subs(sb), 40)))
        wt = sp.N(W_sym(x, gv).subs(x, gv), 40)
        worst_t = max(worst_t, abs(wt - sp.N(Wthroat.subs(g1, gv), 40)) / abs(wt))
e4 = w0 and worst_w < 1e-30 and worst_z < 1e-30 and worst_t < 1e-30
check('E4', e4, f"W(gamma=0) = -3/(1+x^2)^2: {w0}; typed W vs -V + 2(dPsi0/Psi0)^2: {float(worst_w):.1e}; "
      f"d^2 Psi0 = V Psi0: {float(worst_z):.1e}; W(gamma) printed: {float(worst_t):.1e}")

# numeric helpers ----------------------------------------------------------------------------------------------------


def W_num(xv, g):
    xv = np.asarray(xv, dtype=float)
    at = np.arctan(xv)
    k = g / (1 + g * g)
    F = 1 + k * (1 + g * xv) * at
    Fx = k * ((1 + g * xv) / (1 + xv * xv) + g * at)
    r = Fx / F
    return np.exp(4 * g * at) * (-3 / (1 + xv * xv) + 3 * (xv - g)**2 / (1 + xv * xv)**2 + CW * r * r
                                 - 4 * g / (1 + xv * xv) * r + 4 * k * (xv - g) / (F * (1 + xv * xv)**2))


def x_grid(g, x0, L, h, sgn, mutmap=False):
    """x at rho = rho0 + sgn*j*h, j = 0..N (N = round(L/h)), from x(rho0) = x0, by RK4 of x_rho = e^{2 g atan x}."""
    s = (-2.0 if mutmap else 2.0) * g
    f = lambda v: math.exp(s * math.atan(v))
    N = int(round(L / h))
    xs = [x0]
    xv, hh = x0, sgn * h
    for _ in range(N):
        k1 = f(xv)
        k2 = f(xv + hh / 2 * k1)
        k3 = f(xv + hh / 2 * k2)
        k4 = f(xv + hh * k3)
        xv += hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        xs.append(xv)
    return xs


def roots_scan(fun, lo, hi, n):
    bs = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    vs = [fun(b) for b in bs]
    return [(bs[i], bs[i + 1], vs[i], vs[i + 1]) for i in range(n - 1) if vs[i] * vs[i + 1] < 0]


def refine(fun, a, b, fa=None, fb=None, tol=1e-14):
    fa = fun(a) if fa is None else fa
    fb = fun(b) if fb is None else fb
    side = 0
    for _ in range(200):
        c = (a * fb - b * fa) / (fb - fa)
        fc = fun(c)
        if fc * fb < 0:
            a, fa = b, fb
            b, fb = c, fc
            side = 0
        else:
            b, fb = c, fc
            if side == -1:
                fa /= 2
            side = -1
        if abs(b - a) < tol * abs(b) or fc == 0:
            return c
    return c


# route 1: Numerov ------------------------------------------------------------------------------------------------
C5 = 6.0 if MUT == 'numerov' else 5.0


def numerov_in(Wf, beta_, h, N):
    """Wf: W at rho = j*h, j = N..0 inward (list). Returns chi at the same points (list, far end first)."""
    c = h * h / 12
    b2 = beta_ * beta_
    rN, rN1 = N * h, (N - 1) * h
    chi = [(1 + 1 / (beta_ * rN)), math.exp(beta_ * h) * (1 + 1 / (beta_ * rN1))]
    for j in range(2, len(Wf)):
        q0, q1, q2 = Wf[j - 2] + b2, Wf[j - 1] + b2, Wf[j] + b2
        chi.append((2 * (1 + C5 * c * q1) * chi[j - 1] - (1 - c * q0) * chi[j - 2]) / (1 - c * q2))
    return chi


def route1_D(beta_, Wp, Wm, h):
    """Wp[j] = W at rho = +j h, Wm[j] = W at rho = -j h, j = 0..N; discrete Wronskian at (0, h)."""
    N = len(Wp) - 1
    cR = numerov_in(Wp[::-1], beta_, h, N)  # rho = Nh ... 0
    cL = numerov_in(Wm[::-1] + [Wp[1]], beta_, h, N)  # rho = -Nh ... 0, +h
    R0, R1 = cR[-1], cR[-2]
    L0, L1 = cL[-2], cL[-1]
    return (L0 * R1 - L1 * R0) / (math.hypot(L0, L1) * math.hypot(R0, R1))


def route1_beta(Wfun_p, Wfun_m, h, lo, hi, nscan=40):
    Wp, Wm = Wfun_p(h), Wfun_m(h)
    fun = lambda b: route1_D(b, Wp, Wm, h)
    br = roots_scan(fun, lo, hi, nscan)
    if not br:
        return None, 0
    a, b, fa, fb = br[-1]
    return refine(fun, a, b, fa, fb), len(br)


def richardson(b1, b2):
    return (16 * b2 - b1) / 15, abs(b2 - b1) / 15


# route 2: RK4 + Cauchy-Frobenius ---------------------------------------------------------------------------------


class System2:
    """(x - xt) Y' = M(x) Y for Y = (C, G); rows of M: (x - xt)(a11, a12), (P0 + b^2 P2, Q0 + b^2 Q2); map gamma g."""

    def __init__(self, xt, g, num, mpf):
        self.xt, self.g, self.num, self.mpf = xt, g, num, mpf  # num/mpf: dicts a11 a12 P0 P2 Q0 Q2 -> callables


def cauchy_coeffs(fun, xt, r=0.5, N=64, K=41):
    with mp.workdps(30):
        z = [mp.mpf(xt) + r * mp.expjpi(mp.mpf(2 * k) / N) for k in range(N)]
        v = [fun(zz) for zz in z]
        out = []
        for n in range(K):
            s = mp.fsum(v[k] * mp.expjpi(mp.mpf(-2 * n * k) / N) for k in range(N)) / N / mp.mpf(r)**n
            out.append(mp.re(s))
        return out


def frob_prepare(S, K=41):
    xt = S.xt
    co = {}
    with mp.workdps(30):
        for k in ('a11', 'a12'):
            co[k] = cauchy_coeffs(lambda z, f=S.mpf[k]: (z - xt) * f(z), xt, K=K)
        for k in ('P0', 'P2', 'Q0', 'Q2'):
            co[k] = cauchy_coeffs(S.mpf[k], xt, K=K)
    return co


def frob_basis(co, b2, K=41):
    with mp.workdps(30):
        b2 = mp.mpf(b2)
        M = [[[co['a11'][n], co['a12'][n]], [co['P0'][n] + b2 * co['P2'][n], co['Q0'][n] + b2 * co['Q2'][n]]] for n in range(K)]
        M0 = M[0]
        P0, Q0 = M0[1][0], M0[1][1]
        mv = lambda A, y: [A[0][0] * y[0] + A[0][1] * y[1], A[1][0] * y[0] + A[1][1] * y[1]]

        def solve_n(n, rhs):
            nn = n + 1 if MUT == 'frob' else n
            A = [[nn - M0[0][0], -M0[0][1]], [-M0[1][0], nn - M0[1][1]]]
            det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
            return [(rhs[0] * A[1][1] - A[0][1] * rhs[1]) / det, (A[0][0] * rhs[1] - A[1][0] * rhs[0]) / det]

        ya = [[mp.mpf(1), -P0 / Q0]]
        r1 = mv(M[1], ya[0])
        yc = r1[0] / (1 - M0[0][0])
        nu = r1[1] + M0[1][0] * yc - (1 - Q0) * 0
        nu_rel = abs(nu) / max(abs(r1[0]), abs(r1[1]), mp.mpf(10)**-300)
        ya.append([yc, mp.mpf(0)])
        yb = [[mp.mpf(0), mp.mpf(0)], [mp.mpf(0), mp.mpf(1)]]
        for n in range(2, K):
            for Y in (ya, yb):
                rhs = [mp.mpf(0), mp.mpf(0)]
                for k in range(1, n + 1):
                    t_ = mv(M[k], Y[n - k])
                    rhs = [rhs[0] + t_[0], rhs[1] + t_[1]]
                Y.append(solve_n(n, rhs))

        def basis(epsv):
            e = mp.mpf(epsv)
            sa = [mp.fsum(ya[n][i] * e**n for n in range(K)) for i in (0, 1)]
            sb = [mp.fsum(yb[n][i] * e**n for n in range(K)) for i in (0, 1)]
            return [[float(sa[0]), float(sb[0])], [float(sa[1]), float(sb[1])]]
        return basis, float(nu_rel), float(abs(Q0 - 1)), float(max(abs(M0[0][0]), abs(M0[0][1])))


def side_prep(S, h, L, sgn, delta):
    xs = x_grid(S.g, S.xt + sgn * delta, L, h / 2, sgn)
    xa = np.array(xs)
    f = np.exp(2 * S.g * np.arctan(xa))
    den = xa - S.xt
    arr = {'f': f, 'x': xa,
           'b11': f * S.num['a11'](xa), 'b12': f * S.num['a12'](xa),
           'p0': f * S.num['P0'](xa) / den, 'p2': f * S.num['P2'](xa) / den,
           'q0': f * S.num['Q0'](xa) / den, 'q2': f * S.num['Q2'](xa) / den}
    return arr


def integrate_side(S, arr, beta_, h, sgn):
    b2 = beta_ * beta_
    b11, b12 = arr['b11'].tolist(), arr['b12'].tolist()
    b21 = (arr['p0'] + b2 * arr['p2']).tolist()
    b22 = (arr['q0'] + b2 * arr['q2']).tolist()
    xa = arr['x']
    n2 = len(b11) - 1  # even, 2N
    xf = float(xa[-1])
    ff = float(arr['f'][-1])
    C = 1.0
    Cx = -sgn * beta_ * C / ff
    a11f, a12f = float(S.num['a11'](np.array([xf]))[0]), float(S.num['a12'](np.array([xf]))[0])
    G = (Cx - a11f * C) / a12f
    dr = -sgn * h
    hd = dr / 2
    j = n2
    while j > 0:
        i, m = j, j - 1
        k1c, k1g = b11[i] * C + b12[i] * G, b21[i] * C + b22[i] * G
        yc, yg = C + hd * k1c, G + hd * k1g
        k2c, k2g = b11[m] * yc + b12[m] * yg, b21[m] * yc + b22[m] * yg
        yc, yg = C + hd * k2c, G + hd * k2g
        k3c, k3g = b11[m] * yc + b12[m] * yg, b21[m] * yc + b22[m] * yg
        i = j - 2
        yc, yg = C + dr * k3c, G + dr * k3g
        k4c, k4g = b11[i] * yc + b12[i] * yg, b21[i] * yc + b22[i] * yg
        C += dr / 6 * (k1c + 2 * k2c + 2 * k3c + k4c)
        G += dr / 6 * (k1g + 2 * k2g + 2 * k3g + k4g)
        j -= 2
        if j % 2000 == 0:
            nrm = math.hypot(C, G)
            C, G = C / nrm, G / nrm
    nrm = math.hypot(C, G)
    return C / nrm, G / nrm


def route2_D(S, co, arrp, arrm, beta_, h, delta):
    basis, nu, q0d, m0 = frob_basis(co, beta_ * beta_)
    Yp = integrate_side(S, arrp, beta_, h, +1)
    Ym = integrate_side(S, arrm, beta_, h, -1)
    Pp = np.array(basis(delta))
    Pm = np.array(basis(delta if MUT == 'match' else -delta))
    ap_ = np.linalg.solve(Pp, np.array(Yp))
    am_ = np.linalg.solve(Pm, np.array(Ym))
    ap_ /= np.linalg.norm(ap_)
    am_ /= np.linalg.norm(am_)
    return float(ap_[0] * am_[1] - ap_[1] * am_[0])


def route2_beta(S, co, h, L, delta, lo, hi, nscan, want='largest'):
    arrp, arrm = side_prep(S, h, L, +1, delta), side_prep(S, h, L, -1, delta)
    fun = lambda b: route2_D(S, co, arrp, arrm, b, h, delta)
    br = roots_scan(fun, lo, hi, nscan)
    return br, fun


def route2_refine(S, co, h, L, delta, a, b):
    arrp, arrm = side_prep(S, h, L, +1, delta), side_prep(S, h, L, -1, delta)
    fun = lambda bb: route2_D(S, co, arrp, arrm, bb, h, delta)
    return refine(fun, a, b)


# E5 -------------------------------------------------------------------------------------------------------------
print("\n== E5: planted, route 1 ==", flush=True)
H1, H2 = 0.002, 0.001
e5_msgs, e5_ok = [], True
for ell in (1.3, 2.4):
    L = 45 / ell
    bs = []
    for h in (H1, H2):
        Wpl = lambda hh: [-ell * (ell + 1) / math.cosh(j * hh)**2 for j in range(int(round(L / hh)) + 1)]
        bv, nr = route1_beta(Wpl, Wpl, h, 0.2, ell + 0.45)
        bs.append(bv)
    br, spread = richardson(*bs)
    rel = abs(br / ell - 1)
    e5_ok &= rel < 1e-9
    e5_msgs.append(f"ell = {ell}: beta = {br:.13f}, rel {rel:.1e} (h-spread {spread:.1e}, roots in scan {nr})")
map_worst = 0
for gv in (0.5, 1.0):
    xs = x_grid(gv, 0.0, 10.0, H1, +1, MUT == 'rho') [::1000]
    xs_m = x_grid(gv, 0.0, 10.0, H1, -1, MUT == 'rho')[::1000]
    with mp.workdps(30):
        for sgn, arr in ((1, xs), (-1, xs_m)):
            for j in (1, 3, 5):
                rq = mp.quad(lambda y: mp.exp(-2 * gv * mp.atan(y)), [0, arr[j]])
                map_worst = max(map_worst, abs(float(rq) - sgn * j * 1000 * H1))
e5_ok &= map_worst < 1e-10
check('E5', e5_ok, "; ".join(e5_msgs) + f"; map |rho_quad(x_n) - rho_n| worst {map_worst:.1e}")

# E6 -------------------------------------------------------------------------------------------------------------
print("\n== E6: planted, route 2 ==", flush=True)
MU = 3.5
qpl0_num = lambda v: (1 + v * v) * (2 / np.sinh(v)**2 - MU * (MU + 1) / np.cosh(v)**2 - (2 + 3 * v * v) / (v * v * (1 + v * v)**2))
qpl0_mp = lambda z: (1 + z * z) * (2 / mp.sinh(z)**2 - MU * (MU + 1) / mp.cosh(z)**2 - (2 + 3 * z * z) / (z * z * (1 + z * z)**2))
Spl = System2(0.0, 0.0,
              {'a11': lambda v: 0 * v, 'a12': lambda v: v / (1 + v * v), 'P0': qpl0_num, 'P2': lambda v: 1 + v * v,
               'Q0': lambda v: 1 + 0 * v, 'Q2': lambda v: 0 * v},
              {'a11': lambda z: 0 * z, 'a12': lambda z: z / (1 + z * z), 'P0': qpl0_mp, 'P2': lambda z: 1 + z * z,
               'Q0': lambda z: 1 + 0 * z, 'Q2': lambda z: 0 * z})
DEL = 0.3
co_pl = frob_prepare(Spl)
br_pl, _ = route2_beta(Spl, co_pl, 0.01, 60.0, DEL, 0.2, 5.5, 45)
e6_msgs, e6_ok = [f"sign changes on [0.2, 5.5]: {len(br_pl)} at {[round((a + b) / 2, 2) for a, b, _, _ in br_pl]}"], len(br_pl) == 4
for target in (4.5, 1.5):
    L = 45 / target
    bs = []
    for h in (H1, H2):
        bs.append(route2_refine(Spl, co_pl, h, L, DEL, target - 0.3, target + 0.3))
    bb, spread = richardson(*bs)
    rel = abs(bb / target - 1)
    e6_ok &= rel < 1e-9
    e6_msgs.append(f"beta = {bb:.13f} (exact {target}), rel {rel:.1e}, h-spread {spread:.1e}")
_, nu_pl, q0_pl, _ = frob_basis(co_pl, 4.5**2)
e6_msgs.append(f"no-log residual {nu_pl:.1e}")
check('E6', e6_ok, "; ".join(e6_msgs))

# E7 -------------------------------------------------------------------------------------------------------------
print("\n== E7: route 1, the printed potential ==", flush=True)
RUN = {0.0: 1.181969726488, 0.5: 1.875127511869, 1.0: 5.041327581056}
LS = {0.0: 38.0, 0.5: 24.0, 1.0: 9.0}
B1 = {}
e7_ok, e7_msgs = True, []
for gv in (0.0, 0.5, 1.0):
    L = LS[gv]
    bmax = math.sqrt(-min(W_num(np.linspace(-5, 5, 20001), gv)))
    bs = []
    for h in (H1, H2):
        Wp = lambda hh: W_num(np.array(x_grid(gv, 0.0, L, hh, +1, MUT == 'rho')), gv).tolist()
        Wm = lambda hh: W_num(np.array(x_grid(gv, 0.0, L, hh, -1, MUT == 'rho')), gv).tolist()
        bv, nr = route1_beta(Wp, Wm, h, 0.2, bmax)
        bs.append(bv)
    if None in bs:
        e7_ok = False
        e7_msgs.append(f"gamma = {gv}: no root")
        continue
    bb, spread = richardson(*bs)
    B1[gv] = bb
    rel = abs(bb / RUN[gv] - 1)
    e7_ok &= rel < 1e-9
    e7_msgs.append(f"gamma = {gv}: beta = {bb:.13f}, rel to #151 {rel:.1e}, h-spread {spread:.1e}, roots in scan {nr}")
if 0.0 in B1:
    d2 = abs(B1[0.0]**2 - 1.39705243)
    e7_ok &= d2 < 1e-8
    e7_msgs.append(f"beta^2(0) = {B1[0.0]**2:.11f}, |diff| to 1.39705243 = {d2:.1e}")
check('E7', e7_ok, "; ".join(e7_msgs))

# E8 -------------------------------------------------------------------------------------------------------------
print("\n== E8: route 2, the gauge dPhi = 0, no potential ==", flush=True)
mods = ['numpy']
nf = {k: sp.lambdify((x, g1), e, modules=mods) for k, e in (('P0', P0s), ('P2', P2s), ('Q0', Q0s), ('Q2', Q2s))}
mf = {k: sp.lambdify((x, g1), e, modules='mpmath') for k, e in (('P0', P0s), ('P2', P2s), ('Q0', Q0s), ('Q2', Q2s))}
e8_ok, e8_msgs = True, []
B2 = {}
for gv in (0.0, 0.5, 1.0):
    if gv not in B1:
        e8_ok = False
        continue
    num_d = {'a11': lambda v, g=gv: g / (1 + v * v), 'a12': lambda v, g=gv: (v - g) / (1 + v * v)}
    mp_d = {'a11': lambda z, g=gv: g / (1 + z * z), 'a12': lambda z, g=gv: (z - g) / (1 + z * z)}
    for k in ('P0', 'P2', 'Q0', 'Q2'):
        num_d[k] = (lambda v, f=nf[k], g=gv: f(v, g) + 0 * v)
        mp_d[k] = (lambda z, f=mf[k], g=gv: f(z, mp.mpf(g)))
    S = System2(gv, gv, num_d, mp_d)
    co = frob_prepare(S)
    L = LS[gv]
    br, _ = route2_beta(S, co, 0.004, L, DEL, 0.2, 1.5 * B1[gv], 40)
    if not br:
        e8_ok = False
        e8_msgs.append(f"gamma = {gv}: no sign change")
        continue
    a, b, _, _ = br[-1]
    bs = [route2_refine(S, co, h, L, DEL, a, b) for h in (H1, H2)]
    bb, spread = richardson(*bs)
    B2[gv] = bb
    _, nu_root, q0d, m0 = frob_basis(co, bb * bb)
    _, nu_one, _, _ = frob_basis(co, 1.0)
    rel = abs(bb / B1[gv] - 1)
    ok = rel < 1e-8 and len(br) == 1 and nu_root < 1e-20 and nu_one < 1e-20 and q0d < 1e-25
    e8_ok &= ok
    e8_msgs.append(f"gamma = {gv}: beta = {bb:.13f}, rel to route 1 {rel:.1e}, h-spread {spread:.1e}, sign changes {len(br)}, "
                   f"|Q0 - 1| {q0d:.0e}, first row of M0 {m0:.0e}, no-log residual {nu_root:.0e} (root), {nu_one:.0e} (beta = 1)")
check('E8', e8_ok, "; ".join(e8_msgs))

# E9 -------------------------------------------------------------------------------------------------------------
print("\n== E9: T and the comparisons ==", flush=True)


def T_of(b, g):
    return (1 if MUT == 'tfac' else math.exp(2 * g * math.atan(g))) / (math.sqrt(1 + g * g) * b)


e9_ok, e9_msgs = True, []
if all(g in B1 for g in (0.0, 0.5, 1.0)):
    T = {g: T_of(B1[g], g) for g in (0.0, 0.5, 1.0)}
    tab = {0.0: 0.846, 0.5: 0.758, 1.0: 0.675}
    rnd = {g: round(T[g], 3) == tab[g] for g in T}
    issue = abs(T[0.5] / 0.7584 - 1) <= 0.002
    r4 = round(T[0.5], 4) == 0.7584
    tau_lin = 2 * math.exp(math.pi / 2) / B1[0.5]
    rt = round(tau_lin, 2) == 5.13
    m3 = 100 * (5.12 * ALPHA_OVER_R / T[0.5] - 1)
    m4 = 100 * (5.23 * ALPHA_OVER_R / T[0.5] - 1)
    rm = round(m3, 1) == -0.2 and round(m4, 1) == 1.9
    e9_ok = all(rnd.values()) and issue and r4 and rt and rm
    e9_msgs.append(f"T = {', '.join(f'{T[g]:.9f}' for g in T)} (Table I rounding: {rnd}); T(1/2)/0.7584 - 1 = "
                   f"{100 * (T[0.5] / 0.7584 - 1):+.4f} %: {issue}; rounds to 0.7584: {r4}; tau_lin = {tau_lin:.5f} M: {rt}; "
                   f"measured 5.12, 5.23 -> {m3:+.3f} %, {m4:+.3f} %: {rm}")
else:
    e9_ok = False
    e9_msgs.append("route 1 missing a gamma")
check('E9', e9_ok, "; ".join(e9_msgs))

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

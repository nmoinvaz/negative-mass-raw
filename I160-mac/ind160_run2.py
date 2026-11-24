#!/usr/bin/env python3
"""ind160: the coordinator's independent check of #160 (multiplicative separable shifts with det R3 = 0).

Criteria N0-N7 in negative-mass-raw I160-mac/README.md. Imports nothing from the repository.
"""
import argparse
import sys
import time

import sympy as sp

MUTS = ['Dsign', 'theta', 'trav', 'mob', 'qid', 'pole', 'expo', 'expo2', 'lau']
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


def zero(e):
    return sp.expand(sp.cancel(sp.together(e))) == 0


X0, X1, X2, R0, R1, S0, v = sp.symbols('X0 X1 X2 R0 R1 S0 v')

# N0 -------------------------------------------------------------------------------------------------------------
print("== N0: E = 8D/R'^2 and its sum-of-squares form ==", flush=True)
uu = X0 * R0 + v
ux, ur, uxx, uxr, lap = X1 * R0, X0 * R1, X2 * R0, X1 * R1, X0 * S0
P = -uu * uxx - ux**2
Q = -lap / 2
Z = uxr / 2
Y = uu * uxr / 2 + (-1 if MUT == 'Dsign' else 1) * ux * ur
h = ur**2 / 2
D = h * (h**2 - P**2 - Q**2 + Y**2 + Z**2) - P * (Y**2 - Z**2) + 2 * Q * Y * Z
E = sp.expand(8 * D / R1**2)
m_ = X1**2 / X0**2
be_ = X2 / X0 - X1**2 / X0**2
c_ = R1**2 / R0**2
s2_ = S0 / R0
U_ = X0 * R0
W_ = 3 * U_ + v
s_ = U_**2 * c_ + m_ * (W_**2 + 1) / 2
d_ = 2 * uu * U_ * (be_ + m_) + m_ * (4 * U_**2 + 1 - W_**2) / 2
t_ = U_ * s2_ + m_ * W_
n0 = zero(E / X0**2 - (s_**2 - d_**2 - t_**2))
check('N0', n0, f"E/X^2 = s^2 - delta^2 - tau^2: {n0}")

# N1, N2 ---------------------------------------------------------------------------------------------------------
print("\n== N1, N2: the separations ==", flush=True)
mm, bb, cc, ss2, XX, RR = sp.symbols('m beta c s2 X R')
Theta = (19 if MUT == 'theta' else 20) * mm**2 + 2 * mm * bb - 4 * bb**2
Psi = -4 * mm**2 - 2 * mm * bb
f = [XX**2, XX**2 * mm, XX**2 * Theta, mm, Psi, 1]
g = [RR**2 * cc**2, 9 * RR**2 * cc, RR**2, cc - 6 * ss2, 1, -ss2**2]
to_jets = {mm: m_, bb: be_, cc: c_, ss2: s2_, XX: X0, RR: R0}
sumfg = sum(a * b for a, b in zip(f, g))
n1a = zero(E.subs(v, 0) - R0**2 * X0**4 * sumfg.subs(to_jets))
lam = sp.Symbol('lambda', nonzero=True)
kfg = sp.expand(sumfg.subs({mm: lam**2, bb: 0}))
n1b = zero(kfg.coeff(XX, 2) - RR**2 * (cc + 4 * lam**2) * (cc + 5 * lam**2)) and zero(kfg.coeff(XX, 1))
check('N1', n1a and n1b, f"E(v=0) = R^2 X^4 sum f_i g_i: {n1a}; Lemma K coefficient R^2(c+4l^2)(c+5l^2): {n1b}")
Phi2 = -4 * v**2 * bb**2 + (6 * v**2 - 2) * bb * mm + (12 * v**2 - 4) * mm**2
Phi3 = -4 * bb**2 + 3 * bb * mm + 13 * mm**2
Theta20 = 20 * mm**2 + 2 * mm * bb - 4 * bb**2
F = [-2 * v * (1 - v**2) * XX * mm * (bb + mm), -2 * v * XX * mm, XX**2 * Phi2, (2 if MUT == 'trav' else 1) * XX**2 * mm,
     XX**2, 2 * v * XX**3 * Phi3, 6 * v * XX**3 * mm, XX**4, XX**4 * mm, XX**4 * Theta20]
G = [RR, RR * ss2, RR**2, RR**2 * ((v**2 + 1) * cc - 6 * ss2), -RR**2 * ss2**2, RR**3, RR**3 * cc, RR**4 * cc**2,
     9 * RR**4 * cc, RR**4]
sumFG = sum(a * b for a, b in zip(F, G))
n2 = zero(E / X0**2 - sumFG.subs(to_jets))
check('N2', n2, f"E/X^2 = sum_(i<=10) F_i G_i for symbolic v: {n2}")

# N3 -------------------------------------------------------------------------------------------------------------
print("\n== N3: Lemma X ==", flush=True)
a, b, c, d, al0, al1, al2, t = sp.symbols('a b c d al0 al1 al2 t')
rho_m = (a * mm + b) / (c * mm + d)
beta_m = sp.cancel(rho_m / sp.diff(rho_m, mm))
n3a = zero(beta_m - (a * mm + b) * (c * mm + d) / (a * d - b * c))
Psi_m = -4 * mm**2 - 2 * mm * beta_m
eq = sp.expand(sp.cancel((Psi_m * (c * mm + d) - (al0 + al1 * mm) * (c * mm + d) - al2) * (a * d - b * c)))
coeffs = sp.Poly(eq, mm).all_coeffs()
Gb = sp.groebner(coeffs + [1 - t * c * (a * d - b * c)], a, b, c, d, al0, al1, al2, t, order='grevlex')
n3b = Gb.exprs == [1]
rho0 = (a * mm + b) / d
beta0 = sp.cancel(rho0 / sp.diff(rho0, mm))
th0 = sp.expand(rho0 * (20 * mm**2 + 2 * mm * beta0 - 4 * beta0**2))
n3c = zero(sp.Poly(th0, mm).coeff_monomial(mm**3) - (17 if MUT == 'mob' else 18) * a / d) and sp.Poly(th0, mm).degree() == 3
check('N3', n3a and n3b and n3c, f"beta = (am+b)(cm+d)/(ad-bc): {n3a}; Psi not in span{{1, m, 1/(cm+d)}} (unit ideal): "
      f"{n3b}; c = 0: rho Theta cubic with m^3 coefficient 18a/d: {n3c}")

# N4 -------------------------------------------------------------------------------------------------------------
print("\n== N4: the consistency identity (step 2) ==", flush=True)
Rp, rh, PR = sp.symbols('Rp rh PR', nonzero=True)
Pp = Rp**2
qq = Rp / rh
qR = (PR / 2 / rh - Rp / rh**2) / Rp  # dq/dR = (dq/drho)/R', with R'' = P_R/2
sgnq = -1 if MUT == 'qid' else 1
n4a = zero(qq**2 - (PR / 2) * qq + sgnq * Pp * qR)
Rv, a1, a2, s1, s2c = sp.symbols('Rv a1 a2 s1 s2c')
Pv = a1 * Rv + a2 * Rv**2
Sv = s1 * Rv + s2c * Rv**2
qv = Sv - sp.diff(Pv, Rv) / 2
ident = sp.expand(qv**2 - sp.diff(Pv, Rv) / 2 * qv + Pv * sp.diff(qv, Rv))
sols = sp.solve(sp.Poly(ident, Rv).all_coeffs(), [a1, a2, s1, s2c], dict=True)
n4b = len(sols) > 0 and all(sp.expand(qv.subs(so)) == 0 for so in sols)
check('N4', n4a and n4b, f"q^2 - (P_R/2) q + P q_R = 0 by the chain rule: {n4a}; polynomial P, S force q = 0 "
      f"({len(sols)} solution families): {n4b}")

# N5 -------------------------------------------------------------------------------------------------------------
print("\n== N5: pole order (step 4) ==", flush=True)
x = sp.Symbol('x')
Xf = sp.Function('X')(x)
mf = (sp.diff(Xf, x) / Xf)**2
bf = sp.diff(sp.log(Xf), x, 2)
n5a = zero(bf - Xf * (sp.diff(mf, x) / sp.diff(Xf, x)) / 2)
mu, X1s, r0, r1, ep = sp.symbols('mu X1s r0 r1 epsilon', nonzero=True)
n5b = True
lead = []
for k in range(1, 5):
    Xv = X1s + ep
    mk = mu * ep**(-k) + r0 + r1 * ep
    bk = Xv * sp.diff(mk, ep) / 2
    Th = 20 * mk**2 + 2 * mk * bk - 4 * bk**2
    e2 = sp.expand(Th * ep**(2 * k + 2))
    ok_poly = all(term.as_coeff_exponent(ep)[1] >= 0 for term in sp.Add.make_args(e2))
    lc = sp.expand(e2.subs(ep, 0))
    want = (1 if MUT == 'pole' else -1) * k**2 * X1s**2 * mu**2
    lead.append(lc)
    n5b = n5b and ok_poly and sp.expand(lc - want) == 0
check('N5', n5a and n5b, f"beta = X m_X/2: {n5a}; leading pole coefficients for k = 1..4: {lead}: {n5b}")

# N6 -------------------------------------------------------------------------------------------------------------
print("\n== N6: robust exponent count (step 5) ==", flush=True)
kap = sp.Symbol('kappa_b', nonzero=True)
vv = sp.Symbol('v', nonzero=True)


def exps(e):
    """[(exponent, leading coefficient)] of F5, F8, F6, F10 for m = kappa X^e (top at infinity, bottom at 0)."""
    mlead = kap
    blead = sp.Rational(e, 2) * kap  # beta = X m_X / 2
    ph3 = -4 * blead**2 + 3 * blead * mlead + 13 * mlead**2
    th = 20 * mlead**2 + 2 * mlead * blead - 4 * blead**2
    e10 = 4 + (e if MUT == 'expo' else 2 * e)
    return [(2, sp.Integer(1)), (4, sp.Integer(1)), (3 + 2 * e, sp.expand(2 * vv * ph3)), (e10, sp.expand(th))]


def admissible(e):
    allowed = set(range(e + 1, e + 5))
    out = {ex for ex, co in exps(e) if co != 0 and ex not in allowed}
    return len(out) <= (2 if MUT == 'expo2' else 1)  # expo2: added in run 2, after expo was silent


top = [b_ for b_ in range(-15, 16) if admissible(b_)]
bottom = [a_ for a_ in range(-15, 16) if admissible(a_)]
n6 = top == [-2, -1, 0, 1] and bottom == [-2, -1, 0, 1]
check('N6', n6, f"admissible top exponents b: {top}; bottom exponents a: {bottom}")

# N7 -------------------------------------------------------------------------------------------------------------
print("\n== N7: the Laurent step (step 6) ==", flush=True)
Xs = sp.Symbol('Xs', positive=True)
km2, km1, k0, k1, Rs, cs, s2s = sp.symbols('km2 km1 k0 k1 Rs cs s2s')
mL = km2 / Xs**2 + km1 / Xs + k0 + k1 * Xs
bL = Xs * sp.diff(mL, Xs) / 2
UL = Xs * Rs
uL = UL + v
WL = 3 * UL + v
sL = UL**2 * cs + mL * (WL**2 + 1) / 2
dL = 2 * uL * UL * (bL + mL) + mL * (4 * UL**2 + 1 - WL**2) / 2
tL = UL * s2s + mL * WL
EL = sp.expand((sL**2 - dL**2 - tL**2) * Xs**4)
PL = sp.Poly(EL, Xs)
c6 = sp.expand(PL.coeff_monomial(Xs**10))
n7a = sp.expand(c6 - (10 if MUT == 'lau' else 20) * Rs**4 * k1**2) == 0
EL0 = sp.expand(EL.subs(k1, 0))
c4 = sp.expand(sp.Poly(EL0, Xs).coeff_monomial(Xs**8))
n7b = sp.expand(c4 - Rs**4 * (cs + 4 * k0) * (cs + 5 * k0)) == 0
Yv, wv, kp, aa, tt = sp.symbols('Y w kp aa tt')
unit = []
for k0v in (-kp**2 / 4, -kp**2 / 5):
    Eb = sp.expand(EL0.subs({k0: k0v, cs: kp**2, s2s: kp**2 + kp * wv, Rs: aa * Yv}))
    cfs = [cf for cf in sp.Poly(Eb, Xs, Yv, wv).coeffs()]
    Gl = sp.groebner(cfs + [1 - tt * kp * aa * v], km2, km1, kp, aa, v, tt, order='grevlex')
    unit.append(Gl.exprs == [1])
check('N7', n7a and n7b and all(unit), f"X^6 coefficient 20 R^4 k1^2: {n7a}; with k1 = 0 the X^4 coefficient "
      f"R^4(c+4k0)(c+5k0): {n7b}; unit ideal in the branches k0 = -kappa^2/4, -kappa^2/5: {unit}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)

#!/usr/bin/env python3
"""DG06 (gr-qc/0604021): the ODE's own regularity relation at r_s and the paper's explicit unstable mode.

Run: ~/Source/negative-mass-venv314/bin/python -I dg06_check.py [--mutate=exp_sign|rw24a_k]
Exit 0: every check PASS. Exit 1: a check FAILED.

Formulas are typed from DG06 v2 = I149-rpi5/dg06_v2/nakedsingularity2.tex (sha256 4da32b56...; line numbers below)
and, for E1, equal in v1 = dg06_v1/naked01.tex (sha256 92e4d33b...; (AppB2) 276-283... see quotes.md).
  (AppB2)  v2 340-348      (exp) v2 363-374, v1 824-836      (nv1) v2 289-300      (cz) v2 316-320
  (AppC4)  v2 ~705-710     (AppC5) v2 ~716      (RW24a) v2 ~725-728      (RW2), (RW2a) v2 168-181
"""
import sys
import sympy as sp

MUT = ""
for a in sys.argv[1:]:
    if a.startswith("--mutate="):
        MUT = a.split("=", 1)[1]
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" : " + detail) if detail else ""))
    if not ok:
        fails.append(name)


r, lam, mu, w, rho, t, n, s = sp.symbols("r lambda mu omega rho t n s")

# ---- E1: (AppB2) at r_s ------------------------------------------------------------------------
# chi'' = A chi' + B chi,  zeta = exp(i w t) chi
A = (4 * lam * r**2 + 6 * lam * r * mu - 3 * mu**2) / ((2 * lam * r - 3 * mu) * (r + mu) * r)
B = (4 * lam**2 * r**2 - 6 * lam * r * mu + 3 * mu**2) / ((2 * lam * r - 3 * mu) * (r + mu) * r**2) \
    - r**2 / (r + mu) ** 2 * w**2
r_s = 3 * mu / (2 * lam)


def laurent(expr, order):
    e = sp.together(expr.subs(r, r_s + rho))
    return sp.series(e, rho, 0, order).removeO()


LA = sp.expand(laurent(A, 2))
LB = sp.expand(laurent(B, 2))
# printed (exp): 0 = chi'' + (-2/rho - 4 lam^2/(3 mu (3+2 lam)) + 16 (3+lam) lam^3 rho/(9 mu^2 (3+2 lam)^2)) chi'
#                        + (-4 lam^2/(3 mu (3+2 lam) rho) - (16 lam^4 - 81 w^2 mu^2)/(9 mu^2 (3+2 lam)^2)
#                           + 8 lam^2 (4 lam^3 + 27 w^2 mu^2) rho/(9 mu^3 (3+2 lam)^3)) chi
b1_sign = -1 if MUT == "exp_sign" else 1
exp_chi1 = -2 / rho - 4 * lam**2 / (3 * mu * (3 + 2 * lam)) + 16 * (3 + lam) * lam**3 * rho / (9 * mu**2 * (3 + 2 * lam) ** 2)
exp_chi0 = b1_sign * (-4 * lam**2 / (3 * mu * (3 + 2 * lam) * rho)) \
    - (16 * lam**4 - 81 * w**2 * mu**2) / (9 * mu**2 * (3 + 2 * lam) ** 2) \
    + 8 * lam**2 * (4 * lam**3 + 27 * w**2 * mu**2) * rho / (9 * mu**3 * (3 + 2 * lam) ** 3)
dA = sp.simplify(sp.expand(-LA) - exp_chi1)
dB = sp.simplify(sp.expand(-LB) - exp_chi0)
check("E1a printed (exp) 1/rho and higher terms agree with (AppB2) through rho^1 (all printed terms)", dA == 0 and dB == 0)
# analytic chi: chi'' finite  =>  2 chi'(r_s) + Bres chi(r_s) = 0
Ares = sp.simplify(sp.limit(A.subs(r, r_s + rho) * rho, rho, 0))
Bres = sp.simplify(sp.limit(B.subs(r, r_s + rho) * rho, rho, 0))
print("residues of A, B at r_s:", sp.factor(Ares), "|", sp.factor(Bres))
check("E1a0 residues are A = 2, B = 4 lam^2/(3 mu (2 lam+3)) (nonzero)",
      sp.simplify(Ares - 2) == 0 and sp.simplify(Bres - 4 * lam**2 / (3 * mu * (2 * lam + 3))) == 0)
c_ode = sp.simplify(-Bres / Ares)
print("chi'/chi at r_s forced by (AppB2) (any omega):", sp.factor(c_ode))
cz_printed = 2 * lam**2 / (3 * mu * (2 * lam + 3))                 # (cz), v2 317-319
check("E1c (AppB2)'s relation = -2 lam^2/(3 mu (2 lam+3)), independent of omega",
      sp.simplify(c_ode + 2 * lam**2 / (3 * mu * (2 * lam + 3))) == 0)
check("E1d v2's printed (cz) = - (AppB2)'s relation", sp.simplify(cz_printed + c_ode) == 0)

# ---- X1: the explicit unstable mode through the printed and the derived map ------------------
# zeta = r u(r) e^{kt}, u = (r+mu)^n e^{-k r}, so u' = u (n/(r+mu) - k); k = n/mu; n = k mu = 2 lam (lam+1)/3 by (AppC4).
# (v2: (AppC5) zeta = C1 r e^{-kr} (r+mu)^{k mu} e^{kt}, C1 = 1.)  Working with u keeps every expression rational.
k = n / mu
nsol = 2 * lam * (lam + 1) / 3
u = sp.Function("u")(r)
ULOG = n / (r + mu) - k


def Dr(e):
    return sp.diff(e, r).subs(sp.Derivative(u, r), u * ULOG)


z = r * u * sp.exp(k * t)
zr = Dr(z)
zrr = Dr(zr)
zt = sp.diff(z, t)
ztr = Dr(zt)
D = 2 * lam * r - 3 * mu
# printed (nv1), v2 289-300
Kp = ((mu + r) * r * zr + (lam * r - mu) * z) / (r**2 * D)
H1p = (2 * r * (mu + r) * ztr + mu * zt) / (r * (r + mu) * D)
H2p = (r + mu) / D * zrr - (4 * lam * r**2 + 6 * lam * mu * r - 3 * mu**2) / (2 * r * D**2) * zr \
    + (3 * mu**2 - 6 * lam * mu * r + 4 * lam**2 * r**2) / (2 * r**2 * D**2) * z
# derived: (RW2), (RW2a) of DG06 (v2 168-181) with psi = zeta/(2 lam r - 3 mu), M = -mu/2
M = -mu / 2
f_ = (lam * (lam + 1) * r**2 + 3 * lam * M * r + 6 * M**2) / (r**2 * (lam * r + 3 * M))
h_ = (lam * r**2 - 3 * lam * r * M - 3 * M**2) / ((r - 2 * M) * (lam * r + 3 * M))
psi = z / D
Kd = f_ * psi + (1 - 2 * M / r) * Dr(psi)
H1d = h_ * sp.diff(psi, t) + r * Dr(sp.diff(psi, t))
H2d = Dr((1 - 2 * M / r) * (h_ * psi + r * Dr(psi))) - Kd
# (RW24a), v2 725-728, written with u: K = -(lam+1) u e^{kt}/(3 mu);  H1 = -H2 = -lam (lam+1)[2(lam+1) r + 3 mu] r u e^{kt}/(9 mu^2 (r+mu))
kk = -1 if MUT == "rw24a_k" else 1
E_ = sp.exp(k * t)
K24 = kk * (-(lam + 1) * u * E_ / (3 * mu))
H124 = -lam * (lam + 1) * (2 * (lam + 1) * r + 3 * mu) * r * u * E_ / (9 * mu**2 * (r + mu))
H224 = -H124


def ratio(X, Y):
    return sp.simplify(sp.simplify(X / Y).subs(n, nsol))


RKd, RH1d, RH2d = ratio(Kd, K24), ratio(H1d, H124), ratio(H2d, H224)
RKp, RH1p, RH2p = ratio(Kp, K24), ratio(H1p, H124), ratio(H2p, H224)
print("derived  K, H1, H2 over (RW24a):", RKd, "|", RH1d, "|", RH2d)
print("printed  K, H1, H2 over (RW24a):", RKp, "|", RH1p, "|", RH2p)
check("X1.0 K of (nv1) printed = K derived", sp.simplify(sp.simplify(Kp - Kd) / (u * E_)) == 0)
check("X1.K  K derived / (RW24a) K is a constant (independent of r, t)", not RKd.has(r) and not RKd.has(t),
      "= %s" % RKd)
check("X1.H1d H1 derived / (RW24a) H1 = same constant as K", sp.simplify(RH1d - RKd) == 0)
check("X1.H2d H2 derived / (RW24a) H2 = same constant as K", sp.simplify(RH2d - RKd) == 0)
# the predicted discrepancies of the printed (nv1), stated as checks that PASS when the discrepancy is exactly as predicted
check("X1.H1p printed H1 = (2/r) x derived H1", sp.simplify(sp.simplify((H1p - 2 / r * H1d) / (u * E_)).subs(n, nsol)) == 0)
check("X1.H1q printed H1 does NOT reproduce (RW24a) H1 (ratio to K's constant is not 1)", sp.simplify(RH1p - RKd) != 0,
      "printed/RW24a = %s" % RH1p)
zterm = (3 * mu**2 - 6 * lam * mu * r + 4 * lam**2 * r**2) / (r**2 * D**2) * z
check("X1.H2p printed H2 - derived H2 = + (3 mu^2 - 6 lam mu r + 4 lam^2 r^2)/(r^2 D^2) zeta (the zeta term has the opposite sign)",
      sp.simplify(sp.simplify((H2p - H2d - zterm) / (u * E_)).subs(n, nsol)) == 0)
check("X1.H2q printed H2 does NOT reproduce (RW24a) H2", sp.simplify(RH2p - RKd) != 0,
      "printed/RW24a = %s" % RH2p)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all PASS")

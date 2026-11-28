#!/usr/bin/env python3
"""ind262: is Y = R e^{K(t+x)}, K = -2c/pi, an exact linear solution of the black universes? (criteria in README.md beside this file)

The coordinator's double-null forms (ind217), static null coordinates x+- = (t +- x)/sqrt2, e^{-F} = A, gauge dphi = 0, dr = R E,
dF = h E with E = e^{sqrt2 K x+}; h from the linearized phi equation, then the other four equations' residuals at 40 digits.

    python3 ind262.py [--mutate=w-off|r-to-rho|k-kappa]
"""
import sys

import mpmath as mp
import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
mp.mp.dps = 40
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


rho, c = sp.symbols("rho c", real=True)
s2 = sp.sqrt(2)
eps = -1
K = -2 * c / sp.pi
A = 1 + c * (rho ** 2 + 1) + K * (rho + (rho ** 2 + 1) * sp.atan(rho))
R = sp.sqrt(1 + rho ** 2)
P = s2 * sp.atan(rho)
Fb = -sp.log(A)
ph = sp.Symbol("ph")
psi = ph / s2
Vf = -c * (3 - 2 * sp.cos(psi) ** 2) - K * (3 * sp.sin(psi) * sp.cos(psi) + psi * (3 - 2 * sp.cos(psi) ** 2))
Vp = sp.diff(Vf, ph)

# the forms (n = 2): r_+- = pr_r, F_+- = pr_F, phi_+- = pr_p; C_++ = r_++ + F_+ r_+ + (r/2) eps phi_+^2
r_, F_, p_, rP, rM, pP, pM = sp.symbols("r F p rP rM pP pM")
V0, V1 = Vf.subs(ph, p_), Vp.subs(ph, p_)
emF = sp.exp(-F_)
pr_r = -(rP * rM + emF / 2) / r_ + sp.Rational(1, 2) * V0 * r_ * emF
pr_F = (2 / r_) * pr_r + eps * pP * pM - V0 * emF
pr_p = -(rP * pM + rM * pP) / r_ - sp.Rational(eps, 2) * emF * V1
ARGS = (r_, F_, p_, rP, rM, pP, pM)


def dp(g):   # d/dx+ of a function of rho
    return A * sp.diff(g, rho) / s2


def dm(g):
    return -A * sp.diff(g, rho) / s2


bgv = {r_: R, F_: Fb, p_: P, rP: dp(R), rM: dm(R), pP: dp(P), pM: dm(P)}

# K0: the background solves the five equations (the conventions match the member)
bg_res = [dp(dm(R)) - pr_r.subs(bgv), dp(dm(Fb)) - pr_F.subs(bgv), dp(dm(P)) - pr_p.subs(bgv),
          dp(dp(R)) + dp(Fb) * dp(R) + R / 2 * eps * dp(P) ** 2, dm(dm(R)) + dm(Fb) * dm(R) + R / 2 * eps * dm(P) ** 2]

# the perturbation X = f(rho) E, E = e^{sqrt2 Kp x+}: d+ (f E) = E (sqrt2 Kp f + dp f), d- (f E) = E dm f
def Dp(f, Kp):  # noqa: E302
    return s2 * Kp * f + dp(f)


def Dm(f, Kp):
    return dm(f)


def residuals(cval):
    Kp = K * (1 + sp.Rational(1, 1000)) if MUT == "w-off" else K
    if MUT == "k-kappa":
        Kp = sp.Symbol("kap")
    fr = rho if MUT == "r-to-rho" else R
    h = sp.Symbol("h")
    grad = {nm: [sp.diff(e, a).subs(bgv) for a in ARGS] for nm, e in (("r", pr_r), ("F", pr_F), ("p", pr_p))}
    def lin(nm, dr_, dF_, dp_):  # noqa: E306
        pert = (dr_, dF_, dp_, Dp(dr_, Kp), Dm(dr_, Kp), Dp(dp_, Kp), Dm(dp_, Kp))
        return sum(g * q for g, q in zip(grad[nm], pert))
    # phi equation with dphi = 0: 0 - lin_p = 0, linear in h
    eq_p = -lin("p", fr, h, sp.Integer(0))
    hsol = sp.solve(sp.Eq(eq_p, 0), h)[0]
    dr_, dF_ = fr, hsol
    res = {
        "r": Dp(Dm(dr_, Kp), Kp) - lin("r", dr_, dF_, sp.Integer(0)),
        "F": Dp(Dm(dF_, Kp), Kp) - lin("F", dr_, dF_, sp.Integer(0)),
        # C_++: d+d+ dr + F_+ d+ dr + dF_+ r_+ + (dr/2) eps phi_+^2 + r eps phi_+ dphi_+ (dphi = 0)
        "C++": Dp(Dp(dr_, Kp), Kp) + dp(Fb) * Dp(dr_, Kp) + Dp(dF_, Kp) * dp(R) + dr_ / 2 * eps * dp(P) ** 2,
        "C--": Dm(Dm(dr_, Kp), Kp) + dm(Fb) * Dm(dr_, Kp) + Dm(dF_, Kp) * dm(R) + dr_ / 2 * eps * dm(P) ** 2,
    }
    scale = {"r": [Dp(Dm(dr_, Kp), Kp)], "F": [Dp(Dm(dF_, Kp), Kp)], "C++": [Dp(Dp(dr_, Kp), Kp)], "C--": [Dm(Dm(dr_, Kp), Kp)]}
    return res, scale


def evaluate(expr, cval, x, kap=None):
    e = expr.subs(c, cval)
    if kap is not None:
        e = e.subs(sp.Symbol("kap"), kap)
    f = sp.lambdify(rho, e, "mpmath")
    return f(mp.mpf(x))


def kappa_of(cval):
    cm = mp.mpf(cval)
    Kc = -2 * cm / mp.pi
    Af = lambda y: 1 + cm * (y * y + 1) + Kc * (y + (y * y + 1) * mp.atan(y))  # noqa: E731
    rh = mp.findroot(Af, mp.mpf(0) if cval == -1 else mp.mpf("0.5"))
    return rh, mp.diff(Af, rh) / 2


# K0
worst0 = mp.mpf(0)
for cv in (-1, sp.Rational(-3, 10), sp.Rational(-3, 2), -10):
    rh, _ = kappa_of(float(cv))
    for x in (rh + mp.mpf("0.3"), rh + 1, rh + 3, rh - mp.mpf("0.2") if cv == -1 else rh + 7):
        for e in bg_res:
            worst0 = max(worst0, abs(evaluate(e, cv, x)))
check("K0", worst0 < mp.mpf("1e-30"), f"the background's five residuals at 4 members x 4 points: max {mp.nstr(worst0, 3)}")

# K1 (and K2 = K1 at c = -1)
res_all = {}
cases = (-1, sp.Rational(-3, 10), sp.Rational(-3, 2), -10)
for cv in cases:
    res, scale = residuals(cv)
    rh, kap = kappa_of(float(cv))
    worst, big = mp.mpf(0), mp.mpf(0)
    pts = [rh + mp.mpf(d) for d in ("0.05", "0.2", "0.5", "1", "2", "4", "8", "15")]
    if cv == -1:
        pts += [mp.mpf(d) for d in ("-0.05", "-0.3", "-1", "-3")]
    for x in pts:
        for nm, e in res.items():
            val = evaluate(e, cv, x, kap)
            sc = abs(evaluate(scale[nm][0], cv, x, kap))
            worst = max(worst, abs(val) / max(sc, mp.mpf(1)))
            big = max(big, sc)
    res_all[cv] = (worst, big, len(pts))
    print(f"  c = {cv}: worst relative residual of r_+-, F_+-, C_++, C_-- {mp.nstr(worst, 3)} over {len(pts)} points "
          f"(largest term {mp.nstr(big, 3)}); kappa = {mp.nstr(kap, 12)}, K = {mp.nstr(-2 * mp.mpf(float(cv)) / mp.pi, 12)}", flush=True)
targets = cases if MUT != "k-kappa" else (sp.Rational(-3, 2),)
check("K1", all(res_all[cv][0] < mp.mpf("1e-25") for cv in targets),
      "residuals " + ", ".join(f"c = {cv}: {mp.nstr(res_all[cv][0], 3)}" for cv in cases) + "; bar 1e-25")
check("K2", res_all[-1][0] < mp.mpf("1e-25"), f"c = -1, K = kappa = 2/pi: {mp.nstr(res_all[-1][0], 3)}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

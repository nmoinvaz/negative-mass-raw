#!/usr/bin/env python3
"""ind232: the horizon exponents of #212's master equation at c = -1 and nearby (criteria in README.md beside this file)."""
import sys

import mpmath as mp
import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
rho, W, s, c = sp.symbols("rho W s c", real=True)
K = -2 * c / sp.pi
A = 1 + c * (rho**2 + 1) + K * (rho + (rho**2 + 1) * sp.atan(rho))
R2 = rho**2 + 1
Ap = sp.diff(A, rho)
two_rho = 0 if MUT == "drop-2rho" else 2 / rho
P = two_rho - Ap / A                                  # Y'' = P Y' + Q Y
Q = 1 / R2**2 - Ap / (A * rho * R2) - 2 / (A * R2) + W**2 / A**2
RES = []


def check(name, ok, detail):
    RES.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def indicial(cval, rh):
    """indicial polynomial at the regular singular point rho_h: s(s-1) - p0 s - q0 with p0 = lim (rho-rh) P, q0 = lim (rho-rh)^2 Q"""
    Pc, Qc = P.subs(c, cval), Q.subs(c, cval)
    p0 = sp.limit((rho - rh) * Pc, rho, rh)
    q0 = sp.limit(sp.expand((rho - rh)**2 * Qc), rho, rh)
    return sp.simplify(s * (s - 1) - p0 * s - q0), p0, q0


# K1: c = -1, rho_h = 0
A1 = sp.limit(A.subs(c, -1) / rho, rho, 0)
kap = A1 if MUT == "wrong-kappa" else A1 / 2
poly, p0, q0 = indicial(-1, 0)
roots = sp.solve(sp.Eq(poly, 0), s)
want = {1 - W / A1, 1 + W / A1}
at_kappa = sorted(sp.nsimplify(sp.simplify(r.subs(W, kap))) for r in roots)
ok1 = sp.simplify(A1 - 4 / sp.pi) == 0 and {sp.simplify(r) for r in roots} == {sp.simplify(x) for x in want} and at_kappa == [sp.Rational(1, 2), sp.Rational(3, 2)]
check("K1", ok1, f"A1 = {A1}; indicial roots {[sp.simplify(r) for r in roots]}; at W = kappa {at_kappa}")

# K2: rho^{1/2} e^{kappa t} against e^{kappa (t + x)}, x = int drho / A near rho = 0
x = sp.integrate(sp.series(1 / A.subs(c, -1), rho, 0, 3).removeO(), rho)          # (1/A1) ln rho + a0 + a1 rho + ...
ratio = sp.simplify(sp.exp(kap * x) / sp.sqrt(rho))
lim = sp.limit(ratio, rho, 0, "+")
ok2 = lim.is_finite and lim != 0
check("K2", ok2, f"x = {sp.simplify(x)}; e^(kappa x)/rho^(1/2) -> {lim} as rho -> 0 (finite and nonzero means rho^(1/2) e^(kappa t) = C e^(kappa v)(1 + O(rho)))")

# K3: c = -1.01 and -0.99, rho_h != 0
mp.mp.dps = 30
out, ok3 = [], True
for cv in (sp.Rational(-101, 100), sp.Rational(-99, 100)):
    Af = sp.lambdify(rho, A.subs(c, cv), "mpmath")
    rh = mp.findroot(Af, -0.01 if cv > -1 else 0.01)
    rhs = sp.Float(rh, 30)
    A1c = sp.diff(A.subs(c, cv), rho).subs(rho, rhs).evalf(30)
    Pc, Qc = P.subs(c, cv), Q.subs(c, cv)
    p0n = sp.N(((rho - rhs) * Pc).subs(rho, rhs + sp.Float("1e-14", 30)), 25)
    q0n = sp.N(((rho - rhs)**2 * Qc).subs({W: A1c / 2, rho: rhs + sp.Float("1e-14", 30)}), 25)
    rts = sp.Poly(s * (s - 1) - p0n * s - q0n, s).nroots(n=20)
    rts = sorted(float(sp.re(r)) for r in rts)
    ok3 &= abs(rts[0] + 0.5) <= 1e-12 and abs(rts[1] - 0.5) <= 1e-12
    out.append(f"c = {cv}: rho_h {float(rh):.6g}, roots at W = kappa {rts[0]:.12f}, {rts[1]:.12f}")
check("K3", ok3, "; ".join(out))
print(f"\n{len(RES)} criteria, {sum(RES)} pass; mutation {MUT}")
sys.exit(0 if all(RES) else 1)

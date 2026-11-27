#!/usr/bin/env python3
"""dev_06: is the open-FRW ghost solution an exact solution of dn.py's three evolution equations and the two constraints?
ds^2 = a(eta)^2 (-deta^2 + dchi^2 + sinh^2(chi) dOmega_2), a^2 = cosh(2 eta), phi = sqrt(6) atan(tanh(eta)), ghost eps = -1, 8 pi G = 1, D = 4.
Null coordinates x+ = u = eta + chi, x- = v = eta - chi; -a^2 du dv = -2 e^{-f} dx+ dx-  =>  e^{-f} = a^2/2; r = a sinh(chi)."""
import sympy as sp
u, v = sp.symbols("u v", real=True)
n = 2
eta, chi = (u + v) / 2, (u - v) / 2
a2 = sp.cosh(2 * eta)
a = sp.sqrt(a2)
r = a * sp.sinh(chi)
f = -sp.log(a2 / 2)
phi = sp.sqrt(6) * sp.atan(sp.tanh(eta))
eps = -1
rp, rm = sp.diff(r, u), sp.diff(r, v)
rpm = sp.diff(r, u, v)
eq1 = rpm + (n - 1) * (rp * rm + sp.exp(-f) / 2) / r
eq2 = sp.diff(f, u, v) - (n / r) * rpm - eps * sp.diff(phi, u) * sp.diff(phi, v)
eq3 = sp.diff(phi, u, v) + n * (rp * sp.diff(phi, v) + rm * sp.diff(phi, u)) / (2 * r)
con_p = sp.diff(r, u, 2) + sp.diff(f, u) * rp + (r / n) * eps * sp.diff(phi, u) ** 2
con_m = sp.diff(r, v, 2) + sp.diff(f, v) * rm + (r / n) * eps * sp.diff(phi, v) ** 2
import random
random.seed(1)
for name, e in (("r_+- eq", eq1), ("f_+- eq", eq2), ("phi_+- eq", eq3), ("C++", con_p), ("C--", con_m)):
    fn = sp.lambdify((u, v), e, "mpmath")
    import mpmath as mp
    mp.mp.dps = 30
    vals = [abs(fn(mp.mpf(random.uniform(-1, 3)), mp.mpf(random.uniform(-4, -1)))) for _ in range(6)]
    print(f"{name}: max |residual| over 6 random points {float(max(vals)):.3e}")
# rho, p_perp, w from the field in the comoving (diagonal) frame
rho = sp.exp(f) * eps * (sp.diff(phi, u) ** 2 + sp.diff(phi, v) ** 2) / 2
pperp = sp.exp(f) * eps * sp.diff(phi, u) * sp.diff(phi, v)
for pt in ((0.3, -2.0), (1.5, -1.0)):
    print("point", pt, "rho", sp.N(rho.subs({u: pt[0], v: pt[1]})), "p_perp", sp.N(pperp.subs({u: pt[0], v: pt[1]})), "exact rho -3/cosh^3(2eta):", sp.N((-3 / sp.cosh(2 * eta) ** 3).subs({u: pt[0], v: pt[1]})))
Hx = sp.simplify(sp.diff(a, u) + sp.diff(a, v))
print("H = a'/a^2 =", sp.simplify((sp.diff(a, u) + sp.diff(a, v)) / a2))

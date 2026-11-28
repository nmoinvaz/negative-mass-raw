#!/usr/bin/env python3
"""ind230: #230's late throat state at n = 2 in the coordinator's double-null forms (ind217's, verified against a brute-force Ricci
tensor), with the sphere term e^{-f}/2 dropped in r_uv and V = 0 (massless ghost). Criteria in README.md beside this file.

    python3 ind230.py [--mutate=exp|amp]
"""
import sys
import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
u, v, A, C = sp.symbols("u v A C", positive=True)
eps = -1
r = sp.sqrt(u + v)
phi = A * sp.asin((u - v) / (u + v))
p = sp.Rational(1, 2) - A ** 2 + (sp.Rational(1, 10) if MUT == "exp" else 0)
f = sp.log(C) + A ** 2 * sp.log(u * v) + p * sp.log((u + v) / 2)
if MUT == "amp":
    phi = (A * sp.Rational(101, 100)) * sp.asin((u - v) / (u + v))
ru, rv, pu, pv = sp.diff(r, u), sp.diff(r, v), sp.diff(phi, u), sp.diff(phi, v)
E1 = sp.diff(r, u, v) - (-(ru * rv) / r)                                  # sphere term dropped
E2 = sp.diff(f, u, v) - ((2 / r) * (-(ru * rv) / r) + eps * pu * pv)
E3 = sp.diff(phi, u, v) - (-(ru * pv + rv * pu) / r)
Cu = sp.diff(r, u, 2) + sp.diff(f, u) * ru + (r / 2) * eps * pu ** 2
Cv = sp.diff(r, v, 2) + sp.diff(f, v) * rv + (r / 2) * eps * pv ** 2
res = [sp.simplify(e) for e in (E1, E2, E3, Cu, Cv)]
ok = all(x == 0 for x in res)
print(f"[{'PASS' if ok else 'FAIL'}] K1: residuals of r_uv (no sphere term), f_uv, phi_uv, C_uu, C_vv at n = 2, A and C symbolic: {res}")
# K2: on the throat, k = 2/(n A^2 - n - 1) at n = 2, and k = 2 at A = sqrt2 (H1: A = (2/pi) phi_inf, phi_inf = pi/sqrt2)
x = sp.symbols("x", positive=True)
ef = sp.exp(f).subs({u: x, v: x})
H = sp.exp(f / 2).subs({u: x, v: x}) * (ru + rv).subs({u: x, v: x}) / (sp.sqrt(2) * r.subs({u: x, v: x}))
Av = sp.Rational(3, 2)                                           # a value with 2A^2 > 3
tau_rem = sp.integrate(sp.sqrt(2) * sp.exp(-f.subs({u: x, v: x}) / 2).subs({A: Av, C: 1}), (x, x, sp.oo))
kk = sp.simplify((1 / H.subs({A: Av, C: 1})) / tau_rem)          # 1/H = (tau_s - tau)/k ... so (1/H)/(tau_s - tau) = 1/k
k_meas = sp.simplify(1 / kk)
k_pred = 2 / (2 * Av ** 2 - 2 - 1)
ok2 = sp.simplify(k_meas - k_pred) == 0
print(f"[{'PASS' if ok2 else 'FAIL'}] K2: k on the throat at A = 3/2: {k_meas} against 2/(2A^2 - 3) = {k_pred}")
kH1 = 2 / (2 * 2 - 3)
print(f"  at A = sqrt2 (H1, n = 2): k = 2/(2*2 - 3) = {kH1}")
sys.exit(0 if ok and ok2 else 1)

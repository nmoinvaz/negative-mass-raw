#!/usr/bin/env python3
"""ind224: the Schwarzschild-de Sitter spacelike gluing by the coordinator's own derivation (criteria in README.md)."""
import random
import sys

import sympy as sp

MUT = sys.argv[1].split("=", 1)[1] if len(sys.argv) > 1 and sys.argv[1].startswith("--mutate=") else None
F, u, r0, H = sp.symbols("F u r0 H", positive=True)
G = u**2 - 1
sgn = -1 if MUT == "dS-normal" else 1
Kx_m, Kth_m = (F + 1) / (2 * r0 * sp.sqrt(F)), -sp.sqrt(F) / r0
Kx_p, Kth_p = sgn * (u / r0)**2 * r0 / sp.sqrt(G), sgn * sp.sqrt(G) / r0      # H^2 r0 / sqrt(G) with H = u / r0
jx, jth = Kx_p - Kx_m, Kth_p - Kth_m
px = -2 * jth                                                                    # kappa p_x
u_iso = sp.sqrt((F + 1) * (9 * F + 1)) / (3 * F + 1)
res = []
r1 = sp.simplify((jx - jth).subs(u, u_iso))
r2 = sp.simplify(sp.solve(sp.Eq(jx, jth), u)[0] - u_iso) if sp.solve(sp.Eq(jx, jth), u) else "no solution"
ok1 = r1 == 0 and r2 == 0
print(f"[{'PASS' if ok1 else 'FAIL'}] K1: jump difference at the note's u: {r1}; solved u minus the note's: {r2}")
res.append(ok1)
rng = random.Random(224)
neg = all(float(px.subs({F: rng.uniform(1e-3, 50), u: rng.uniform(1.0001, 20), r0: 1})) < 0 for _ in range(200))
crit = sp.solve(sp.diff(u_iso**2, F), F)
umax = sp.nsimplify(sp.sqrt(sp.simplify(u_iso**2).subs(F, crit[0]))) if crit else None
ok2 = neg and crit == [sp.Rational(1, 3)] and sp.simplify(umax - 2 / sp.sqrt(3)) == 0
print(f"[{'PASS' if ok2 else 'FAIL'}] K2: p_x < 0 at 200 random points: {neg}; stationary F of u(F): {crit}; max u = {umax}")
res.append(ok2)
print(f"\n{len(res)} criteria, {sum(res)} pass; mutation {MUT}")
sys.exit(0 if all(res) else 1)

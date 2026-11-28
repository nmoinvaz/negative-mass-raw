#!/usr/bin/env python3
"""ind185: the reduction of the conical ODE in t = ln eta, its factorization, and three local classes (criteria in README.md).

    python3 ind185.py [--mutate=c33|cfac|p0]

Shares with #185 only N (det_classify.conical_N, typed below). Exit 1 when a check fails.
"""
import sys

import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
F0, F1, F2, eta = sp.symbols("F0 F1 F2 eta")
F, P, Q, T, f, c, p0 = sp.symbols("F P Q T f c p0")
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


c33 = 3 if MUT == "c33" else 2
N = (2 * F0**3 * F1**2 * F2 + 4 * F0**3 * F1 * F2**2 * eta + c33 * F0**3 * F2**3 * eta**2 + F0**2 * F1**4 * eta**2
     + 2 * F0**2 * F1**4 + 2 * F0**2 * F1**3 * F2 * eta**3 + 12 * F0**2 * F1**3 * F2 * eta
     + F0**2 * F1**2 * F2**2 * eta**4 + 6 * F0**2 * F1**2 * F2**2 * eta**2 + 4 * F0 * F1**5 * eta**3
     + 8 * F0 * F1**5 * eta + 4 * F0 * F1**4 * F2 * eta**4 + 8 * F0 * F1**4 * F2 * eta**2 - 2 * F0 * F1**3 * eta
     - 6 * F0 * F1**2 * F2 * eta**2 - 2 * F0 * F1**2 * F2 - 6 * F0 * F1 * F2**2 * eta**3
     - 4 * F0 * F1 * F2**2 * eta - 2 * F0 * F2**3 * eta**4 - 2 * F0 * F2**3 * eta**2 + F1**6 * eta**6
     + 4 * F1**6 * eta**4 + 4 * F1**6 * eta**2 - F1**4 * eta**4 - 3 * F1**4 * eta**2 - 2 * F1**4
     - 2 * F1**3 * F2 * eta**5 - 6 * F1**3 * F2 * eta**3 - 4 * F1**3 * F2 * eta - F1**2 * F2**2 * eta**6
     - 3 * F1**2 * F2**2 * eta**4 - 2 * F1**2 * F2**2 * eta**2)

# K1
M = sp.expand(sp.together(eta**4 * N.subs({F0: F, F1: P / eta, F2: (Q - P) / eta**2})))
M = sp.expand(sp.cancel(M))
poly = sp.Poly(M, eta)
degs = sorted({m[0] for m in poly.monoms()})
odd = [d for d in degs if d % 2]
A = F * (P - Q) - P**2
B = (F**2 - 1) * Q**2 + 2 * F * P**2 * Q + 2 * F * P**3 + 2 * P**4
N0 = sp.expand(M.subs(eta, 0))
check("K1", not odd and max(degs) <= 4 and sp.expand(N0 + 2 * A * B) == 0, f"eta-degrees {degs} (odd {odd}); N0 + 2AB = {sp.expand(N0 + 2 * A * B)}")

# K2
N_at0 = sp.factor(N.subs(eta, 0))
target = 2 * F1**2 * (F0**2 - 1) * (F0 * F2 + F1**2)
check("K2", sp.expand(N_at0 - target) == 0, f"N(eta = 0) = {N_at0}")

# K3: F = f + c/T, T = -t; P = dF/dt = c/T^2, Q = 2c/T^3
cc = (1 - f**2) / f if MUT == "cfac" else 2 * (1 - f**2) / f
sub = {F: f + c / T, P: c / T**2, Q: 2 * c / T**3}
Bt = sp.expand(B.subs(sub))
lead = sp.simplify(sp.limit(Bt * T**6, T, sp.oo))
sol = sp.solve(sp.Eq(lead, 0), c)
N0t = sp.expand((N0.subs(sub)).subs(c, cc))
order = sp.limit(N0t * T**8, T, sp.oo)                          # A1: N0 = O(T^-9) only at the right c
check("K3", sp.simplify(lead - (4 * (f**2 - 1) * c**2 + 2 * f * c**3)) == 0 and any(sp.simplify(s - 2 * (1 - f**2) / f) == 0 for s in sol) and sp.simplify(order) == 0,
      f"leading T^-6 coefficient of B: {sp.factor(lead)}; roots {sol}; N0 * T^8 -> {sp.simplify(order)} with c = {cc}")

# K4: F = f + p0 t (P = p0, Q = 0)
Qv = p0 if MUT == "p0" else 0
A4, B4 = sp.expand(A.subs({P: p0, Q: Qv})), sp.expand(B.subs({P: p0, Q: Qv}))
ok4 = sp.expand(A4 - (p0 * F - p0**2)) == 0 and sp.expand(B4 - (2 * p0**3 * F + 2 * p0**4)) == 0
check("K4", ok4, f"A = {A4}, B = {B4}: both grow with F = f + p0 t, so N0 = -2AB != 0 at large |t|")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

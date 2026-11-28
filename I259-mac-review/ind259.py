#!/usr/bin/env python3
"""ind259: the static mass mode of the c = -1 black universe from closed forms (criteria in README.md beside this file).

    python3 ind259.py [--mutate=no-norm|c1-one|mass-exp]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import sys

import mpmath as mp
import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


rho, L, r, x = sp.symbols("rho L r x", positive=True)
c = sp.Integer(-1)
K = -2 * c / sp.pi
A = 1 + c * (rho ** 2 + 1) + K * (rho + (rho ** 2 + 1) * sp.atan(rho))
R = sp.sqrt(1 + rho ** 2)
FL = A + 1 / L - 1

# J1: F_L in the areal radius r = sqrt(L) rho, at large r: (1/L)(1 - 2M/r + ...)
Fr = FL.subs(rho, r / sp.sqrt(L))
ser = sp.series(sp.simplify(L * Fr).subs(r, 1 / x), x, 0, 2).removeO()     # L F_L = 1 - 2M x + O(x^2), x = 1/r
c0 = sp.simplify(ser.coeff(x, 0))
c1x = sp.simplify(ser.coeff(x, 1))
M = sp.simplify(-c1x / 2)
dM = sp.simplify(sp.diff(M, L).subs(L, 1))
check("J1", sp.simplify(c0 - 1) == 0 and sp.simplify(M - 2 * L ** sp.Rational(3, 2) / (3 * sp.pi)) == 0 and sp.simplify(dM - 1 / sp.pi) == 0,
      f"L F_L = {c0} + ({c1x})/r + ...: M(L) = {M}; dM/dL at L = 1 = {dM}")

# J2: c1 = d r(S)/dL at L = 1, S at the zero rho_h(L) of F_L; kappa = A'(0)/2
kappa = sp.simplify(sp.diff(A, rho).subs(rho, 0) / 2)
drho_h = sp.simplify(-sp.diff(FL, L).subs({L: 1, rho: 0}) / sp.diff(FL, rho).subs({L: 1, rho: 0}))   # implicit function at (1, 0)
rS = sp.sqrt(L) * R
c1 = sp.simplify((sp.diff(rS, L) + sp.diff(rS, rho) * drho_h).subs({L: 1, rho: 0}))
if MUT == "c1-one":
    c1 = sp.Integer(1)
check("J2", sp.simplify(c1 - sp.Rational(1, 2)) == 0 and sp.simplify(kappa - 2 / sp.pi) == 0 and sp.simplify(kappa * c1 - dM) == 0,
      f"c1 = {c1}, kappa = {kappa}, kappa c1 - dM/dL = {sp.simplify(kappa * c1 - dM)}; d rho_h/dL at 1 = {drho_h}")

# J3: the first law along the family at finite L, 30 digits
mp.mp.dps = 30
Af = sp.lambdify(rho, A, "mpmath")


def quantities(Lv):
    Lv = mp.mpf(Lv)
    F = lambda y: Af(y) + 1 / Lv - 1  # noqa: E731
    rh = mp.findroot(F, mp.mpf(0) if Lv == 1 else mp.mpf("0.2") * (1 - 1 / Lv))
    kap = (1 if MUT == "no-norm" else mp.sqrt(Lv)) * mp.diff(F, rh) / 2
    area = 4 * mp.pi * Lv * (1 + rh ** 2)
    mass = (2 * Lv ** (mp.mpf(1) if MUT == "mass-exp" else mp.mpf(3) / 2)) / (3 * mp.pi)
    return mass, area, kap


worst = mp.mpf(0)
for Lv in ("0.7", "1", "1.3", "2"):
    dMdL = mp.diff(lambda l: quantities(l)[0], mp.mpf(Lv))
    dAdL = mp.diff(lambda l: quantities(l)[1], mp.mpf(Lv))
    kap = quantities(Lv)[2]
    rel = abs(dMdL / (kap * dAdL / (8 * mp.pi)) - 1)
    worst = max(worst, rel)
    print(f"  L = {Lv}: dM/dL {mp.nstr(dMdL, 15)}, kappa_xi dA/dL / 8pi {mp.nstr(kap * dAdL / (8 * mp.pi), 15)}, relative {mp.nstr(rel, 3)}")
check("J3", worst < mp.mpf("1e-12"), f"first law along the family at L = 0.7, 1, 1.3, 2: worst relative {mp.nstr(worst, 3)} (bar 1e-12)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Diagnostic for ind151 run 1's E8 failure (|Q0 - 1| = 2e-23 at gamma_1 = 1/2 against 1e-25).

Not a criterion. Runs ind151.py's derivation (E0-E3, unmutated) and evaluates Q at the throat three ways: the closed form
from the reduction by hand, the derived expression at x = gamma +- 1e-30 at 60 digits, and the Cauchy sum of ind151 at 30
and at 50 digits.
"""
import sys
import mpmath as mp
import sympy as sp

src = open('ind151.py').read()
src = src[:src.index('# E4 ---')]
sys.argv = ['ind151.py']
ns = {'__name__': 'diag'}
exec(compile(src, 'ind151.py[E0-E3]', 'exec'), ns)
x, g1, beta, Q0s, Q2s = ns['x'], ns['g1'], ns['beta'], ns['Q0s'], ns['Q2s']
dp, cp = sp.diff(ns['d0'], x), sp.diff(ns['c0'], x)
Qhand = (1 + x**2) * (-(2 * x / (1 + x**2) + dp) * cp + 2 / (1 + x**2) - sp.diff(cp, x))
print("Q by hand at x = gamma:", sp.simplify(Qhand.subs(x, g1)))
print("Q2 (beta^2 part) zero at 3 points:", [sp.N(Q2s.subs({x: xv, g1: sp.Rational(1, 2)}), 30) for xv in (sp.Rational(1, 3), 2, -1)])
for gv in (sp.Rational(1, 2), 1):
    print(f"gamma = {gv}: derived Q - hand Q at 3 points:",
          [float(abs(sp.N((Q0s - Qhand).subs({x: xv, g1: gv}), 60))) for xv in (sp.Rational(1, 3), 2, -1)])
    print(f"gamma = {gv}: derived Q at gamma +- 1e-30 (60 digits) minus 1:",
          [float(sp.N(Q0s.subs({g1: gv, x: gv + s * sp.Rational(1, 10**30)}), 60) - 1) for s in (1, -1)])
    f = sp.lambdify((x, g1), Q0s, modules='mpmath')
    for dps in (30, 50):
        with mp.workdps(dps):
            N, r = 64, mp.mpf(1) / 2
            z = [mp.mpf(gv) + r * mp.expjpi(mp.mpf(2 * k) / N) for k in range(N)]
            a0 = mp.fsum(f(zz, mp.mpf(gv)) for zz in z) / N
            print(f"gamma = {gv}: Cauchy n = 0 coefficient at {dps} digits: |Q0 - 1| = {mp.nstr(abs(a0 - 1), 3)}; "
                  f"largest |Q| on the circle {mp.nstr(max(abs(f(zz, mp.mpf(gv))) for zz in z), 3)}")

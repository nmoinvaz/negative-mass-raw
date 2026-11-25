#!/usr/bin/env python3
"""Diagnostic for ind159 run 1's M2 failure (N through nu^15 not zero). Not a criterion: prints the nonzero orders."""
import sys
import sympy as sp
src = open('ind159.py').read()
src = src[:src.index('# M3 ---')]
sys.argv = ['ind159.py']
ns = {'__name__': 'diag'}
exec(compile(src, 'ind159.py[M1-M2]', 'exec'), ns)
Gs, resid, simp = ns['Gs'], ns['resid'], ns['simp']
bad = sorted(((m, j), simp(c)) for (m, j), c in resid.items() if simp(c) != 0)
print("nonzero residual orders (m, j):", [k for k, _ in bad])
for k, v in bad[:3]:
    print(k, sp.factor(v))
print("series keys:", sorted(Gs))

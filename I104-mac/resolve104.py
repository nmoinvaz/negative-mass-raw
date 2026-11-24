#!/usr/bin/env python3
"""Re-solve one case of #104 (l = 29) by exact real-root isolation (sympy real_roots on rational polynomials).
chi from Lemma A in exact rationals; N and S as polynomials in rho; compare with I104-rpi5/sweep_brackets.csv."""
import sys, time
from fractions import Fraction as Fr
from math import factorial
import sympy as sp
l = int(sys.argv[1]) if len(sys.argv) > 1 else 29
L, c = l * (l + 1), l * (l + 1) - 2
def poch(x, k):
    p = 1
    for i in range(k):
        p *= x + i
    return p
cn = {1: Fr(3, 2), 2: Fr(0)}
for n in range(3, l + 3):
    cn[n] = Fr((n - 2) * ((n - 4) * L + n - 1) * poch(l - n + 3, 2 * n - 4), 2**n * factorial(n - 1)**2)
rho = sp.symbols('rho')
X = sp.Poly(sum(sp.Rational(c * cn[n].numerator, cn[n].denominator) / sp.Integer(c)**n * rho**n for n in cn), rho)  # X = c chi(rho/c)
eps = sp.Rational(1, c)
X1 = X.diff(rho)
N = X - sp.Poly(rho - 6, rho) * X1
N1 = N.diff(rho)
two = sp.Poly(2 + eps * rho, rho)
S = sp.Poly(rho, rho) * X * (N * eps + two * N1) - two * N * (X + sp.Poly(2 * rho, rho) * X1)
t0 = time.time()
rN = [z for z in sp.real_roots(N) if z > 6]
rS = sp.real_roots(S)
pos = [z for z in rS if z > 0]
rs = rN[0]
beyond = [z for z in rS if z > rs]
print(f'l = {l}, c = {c}: deg N = {N.degree()}, deg S = {S.degree()}, {time.time() - t0:.1f} s')
print(f'roots of N beyond rho = 6: {len(rN)}; c r_* = {sp.N(rs, 25)}')
print(f'positive roots of S: {len(pos)} at {[sp.N(z, 8) for z in pos]}; beyond c r_*: {len(beyond)}; c r_neg = {sp.N(beyond[0], 25) if beyond else None}')
row = next(line.split(',') for line in open(sys.argv[2]) if line.startswith(f'{l},'))
a, b, p, q = (sp.Rational(x) for x in row[2:6])
ok = len(rN) == 1 and len(beyond) == 1 and a < rs < b and p < beyond[0] < q
print(f'#104 brackets: [{row[2]}, {row[3]}], [{row[4]}, {row[5]}]: {"inside" if ok else "NOT inside"}')
sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""dev01b: the Frobenius series at W = kappa (w = 1), exponent 1/2, with g1 free (the resonance), exact in K; K -> 2/pi at the end.
Compares g2 with #248 D7 (g1 = 0: pi^2/128 + 5/12)."""
import sympy as sp
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
rho, K, g1 = sp.symbols("rho K g1")
NT = N + 6
T = sum((-1) ** n * rho ** (2 * n + 1) / sp.Integer(2 * n + 1) for n in range(NT))
R2 = 1 + rho ** 2
A = sp.expand(-rho ** 2 + K * (rho + R2 * T)); A = sum(A.coeff(rho, k) * rho ** k for k in range(NT))
a = sp.expand(sp.cancel(A / rho)); ap = sp.diff(a, rho); W = K
tr = lambda e: (lambda e: sum(e.coeff(rho, k) * rho ** k for k in range(NT)))(sp.expand(e))
C2 = tr(a * a * R2 ** 2); C1 = tr(-a * R2 ** 2 * (a - rho * ap))
C0 = tr(-(rho ** 2 * a * a - a * (a + rho * ap) * R2 - 2 * rho * a * R2 + W ** 2 * R2 ** 2))
cf = lambda P, j: P.coeff(rho, j)
s = sp.Rational(1, 2)
I = lambda sig: cf(C2, 0) * sig * (sig - 1) + cf(C1, 0) * sig + cf(C0, 0)
g = [sp.Integer(1), g1]
# order 1 consistency
n = 1; tot = g[0] * (cf(C2, 1) * s * (s - 1) + cf(C1, 1) * s + cf(C0, 1))
print("order-1 equation (must be 0 for no logarithm): ", sp.simplify(tot + g1 * I(s + 1)))
for n in range(2, N + 1):
    tot = sum(g[k] * (cf(C2, n - k) * (s + k) * (s + k - 1) + cf(C1, n - k) * (s + k) + cf(C0, n - k)) for k in range(n))
    g.append(sp.factor(sp.simplify(-tot / I(s + n))))
for n, gn in enumerate(g):
    print("g%d =" % n, gn)
print("g1 = 0   :", [sp.nsimplify(sp.simplify(x.subs(g1, 0).subs(K, 2 / sp.pi))) for x in g[:4]])
print("g1 = -1/(4K) :", [sp.nsimplify(sp.simplify(x.subs(g1, -1 / (4 * K)).subs(K, 2 / sp.pi))) for x in g[:4]])

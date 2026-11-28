#!/usr/bin/env python3
"""dev01: Frobenius series of #212's Y equation at c = -1 (A = -rho^2 + K(rho + R^2 arctan rho), K a symbol) at exponent s = 1 - w/2, W = w K.
Polynomial form: with A = rho a, C2 = a^2 R^4, C1 = -a R^4 (a - rho a'), C0 = -[rho^2 a^2 - a (a + rho a') R^2 - 2 rho a R^2 + W^2 R^4],
sum_{k+j=n} g_k [C2_j (s+k)(s+k-1) + C1_j (s+k) + C0_j] = 0.   Exact in Q(K, w)."""
import sympy as sp
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
rho, K, w = sp.symbols("rho K w")
NT = N + 6
T = sum((-1) ** n * rho ** (2 * n + 1) / sp.Integer(2 * n + 1) for n in range(NT))
R2 = 1 + rho ** 2
A = sp.expand(-rho ** 2 + K * (rho + R2 * T))
A = sum(A.coeff(rho, k) * rho ** k for k in range(NT))
a = sp.expand(sp.cancel(A / rho))
ap = sp.diff(a, rho)
W = w * K


def trunc(e, n=NT):
    e = sp.expand(e)
    return sum(e.coeff(rho, k) * rho ** k for k in range(n))


C2 = trunc(a * a * R2 ** 2)
C1 = trunc(-a * R2 ** 2 * (a - rho * ap))
C0 = trunc(-(rho ** 2 * a * a - a * (a + rho * ap) * R2 - 2 * rho * a * R2 + W ** 2 * R2 ** 2))
cf = lambda P, j: P.coeff(rho, j)
s = 1 - w / 2
g = [sp.Integer(1)]
I = lambda sig: sp.simplify(cf(C2, 0) * sig * (sig - 1) + cf(C1, 0) * sig + cf(C0, 0))
print("indicial", sp.factor(I(sp.Symbol("sigma"))))
for n in range(1, N + 1):
    tot = 0
    for k in range(n):
        j = n - k
        tot += g[k] * (cf(C2, j) * (s + k) * (s + k - 1) + cf(C1, j) * (s + k) + cf(C0, j))
    gn = sp.factor(sp.simplify(-tot / I(s + n)))
    g.append(gn)
    print("g%d(w) =" % n, gn, flush=True)
print("--- at w = 1:")
for n, gn in enumerate(g):
    lim = sp.factor(sp.limit(gn, w, 1)) if gn.has(w) else gn
    print("g%d(1) =" % n, lim, "   (K -> 2/pi:", sp.nsimplify(sp.simplify(lim.subs(K, 2 / sp.pi))), ")")

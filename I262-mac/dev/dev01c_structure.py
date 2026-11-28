#!/usr/bin/env python3
"""dev01c: structure of the series (exact in K): Y_nat / sqrt(A), Psi = Y e^{-kappa x}, F = Y e^{kappa x}/rho for the two choices g1 = -1/(4K) (nat) and 0.
Development only: reads the structure of the coefficients; no closed-form candidate is tested here."""
import sympy as sp
N = 8
rho, K = sp.symbols("rho K", positive=True)
NT = N + 6
T = sum((-1) ** n * rho ** (2 * n + 1) / sp.Integer(2 * n + 1) for n in range(NT))
R2 = 1 + rho ** 2
A = sp.expand(-rho ** 2 + K * (rho + R2 * T)); A = sum(A.coeff(rho, k) * rho ** k for k in range(NT))
a = sp.expand(sp.cancel(A / rho)); ap = sp.diff(a, rho); W = K
tr = lambda e, n=NT: (lambda e: sum(e.coeff(rho, k) * rho ** k for k in range(n)))(sp.expand(e))
C2 = tr(a * a * R2 ** 2); C1 = tr(-a * R2 ** 2 * (a - rho * ap))
C0 = tr(-(rho ** 2 * a * a - a * (a + rho * ap) * R2 - 2 * rho * a * R2 + W ** 2 * R2 ** 2))
cf = lambda P, j: P.coeff(rho, j)
s = sp.Rational(1, 2)
I = lambda sig: cf(C2, 0) * sig * (sig - 1) + cf(C1, 0) * sig + cf(C0, 0)


def frob(g1):
    g = [sp.Integer(1), g1]
    for n in range(2, N + 1):
        tot = sum(g[k] * (cf(C2, n - k) * (s + k) * (s + k - 1) + cf(C1, n - k) * (s + k) + cf(C0, n - k)) for k in range(n))
        g.append(sp.factor(sp.simplify(-tot / I(s + n))))
    return g


def ser_inv(p, n):
    """1/p as series, p(0) != 0"""
    p = sp.Poly(sp.expand(p), rho); c0 = p.coeff_monomial(1)
    q = [1 / c0]
    for m in range(1, n):
        q.append(sp.simplify(-sum(p.coeff_monomial(rho ** j) * q[m - j] for j in range(1, m + 1)) / c0))
    return sum(q[i] * rho ** i for i in range(n))


def ser_sqrt_ratio(num, p, n):
    pass


M = N + 1
a_ser = tr(a, M)                                        # A = rho * a
# 1/A = 1/(rho a): kappa x = K * int d rho / A ; e^{kappa x} = rho^{1/2} exp(K * int (1/A - 1/(2 K rho)))
inv_a = ser_inv(a_ser, M)
h = sp.expand(K * (inv_a - 1 / (2 * K)))                   # K/A - 1/(2 rho) = h / rho
h = tr(h, M)
E = sp.series(sp.exp(sp.integrate(sp.expand(h / rho), rho)), rho, 0, M).removeO()      # e^{kappa x} / rho^{1/2}
for name, g1 in (("nat g1=-1/(4K)", -1 / (4 * K)), ("g1=0", sp.Integer(0))):
    g = frob(g1)
    Yp = sum(g[k] * rho ** k for k in range(M))           # Y / rho^{1/2}
    Psi = sp.series(Yp / E, rho, 0, M).removeO()
    sqrtA = sp.series(sp.sqrt(a_ser / (2 * K)), rho, 0, M).removeO()           # sqrt(A/(2K rho))
    Phi = sp.series(Yp / sqrtA, rho, 0, M).removeO()
    print("=====", name)
    for lab, ser in (("Y/rho^{1/2}", Yp), ("Psi = Y e^{-kappa x}", Psi), ("Y/sqrt(A/(2K))", Phi)):
        print(lab)
        for k in range(M):
            print("   rho^%d:" % k, sp.factor(sp.simplify(sp.expand(ser).coeff(rho, k))))

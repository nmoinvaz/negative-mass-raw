"""dev10: first-order monodromy J = oint Phi0^{-1} B1 Phi0 d rho at (c, W) = (-1, kappa), exactly (K = 2/pi; coefficients in Q[pi, 1/pi]).
Basis: Y_a = Y_nat (g1 = -1/(4K)), Y_b = rho^{3/2}(1 + ...). B1 = d_eps B, c = -1 + eps, W fixed. entries J_ij: Y_j -> sum_i Y_i J_ij."""
import sympy as sp
import sys
NORD = int(sys.argv[1]) if len(sys.argv) > 1 else 9
rho = sp.Symbol("rho")
pi = sp.pi
K = 2 / pi
NT = NORD + 8
T = sum((-1) ** n * rho ** (2 * n + 1) / sp.Integer(2 * n + 1) for n in range(NT))
R2 = 1 + rho ** 2
tr = lambda e, n=NT: sp.expand(sum(sp.expand(e).coeff(rho, k) * rho ** k for k in range(n)))
A = tr(-rho ** 2 + K * (rho + R2 * T))
A1 = tr(R2 - K * (rho + R2 * T))                      # d_c A at c = -1: R^2 + K'(c)(rho + R^2 T), K' = -2/pi = -K
aA = sp.expand(sp.cancel(A / rho))
W = K


def ser(e, n):
    return sp.expand(sp.series(e, rho, 0, n).removeO())


# Laurent pieces
ell = ser(A1 / (rho * aA), NORD)                       # A1/A  = ell (has 1/rho)
ellp = sp.diff(ell, rho)
iR2 = ser(1 / R2, NORD + 4)
P1 = -ellp
Q1 = ser(-(1 / rho) * iR2 * ellp + 2 * iR2 * A1 / (rho ** 2 * aA ** 2) - 2 * W ** 2 * A1 / (rho ** 3 * aA ** 3), NORD)
# Frobenius coefficient lists (exact) for a(w=1, g1 = -1/(4K)) and b
g1n = -1 / (4 * K)
from sympy import Rational
def frob(s, g1, N):
    C2 = tr(aA * aA * R2 ** 2)
    C1 = tr(-aA * R2 ** 2 * (aA - rho * sp.diff(aA, rho)))
    C0 = tr(-(rho ** 2 * aA * aA - aA * (aA + rho * sp.diff(aA, rho)) * R2 - 2 * rho * aA * R2 + W ** 2 * R2 ** 2))
    cf = lambda P, j: P.coeff(rho, j)
    I = lambda sig: cf(C2, 0) * sig * (sig - 1) + cf(C1, 0) * sig + cf(C0, 0)
    g = [sp.Integer(1)]
    start = 1
    if s == Rational(1, 2):
        g.append(g1); start = 2
    for n in range(start, N + 1):
        tot = sum(g[k] * (cf(C2, n - k) * (s + k) * (s + k - 1) + cf(C1, n - k) * (s + k) + cf(C0, n - k)) for k in range(n))
        g.append(sp.simplify(-tot / I(s + n)))
    return g
ga = frob(Rational(1, 2), g1n, NORD)
gb = frob(Rational(3, 2), None, NORD)
ya = sum(ga[k] * rho ** k for k in range(NORD + 1))        # Y_a = rho^{1/2} ya
yb = sum(gb[k] * rho ** k for k in range(NORD + 1))        # Y_b = rho^{3/2} yb
# Y_j = rho^{s_j} y_j ; Y_j' = rho^{s_j - 1} (s_j y_j + rho y_j')
sa, sb = Rational(1, 2), Rational(3, 2)
def dY(s, y):
    return s * y + rho * sp.diff(y, rho)
# Wronskian W_ab = Y_a Y_b' - Y_a' Y_b = rho^{3/2 + 1/2 - 1} (ya (sb yb + rho yb') - (sa ya + rho ya') yb) = rho (...)
Wab = sp.expand(ya * dY(sb, yb) - dY(sa, ya) * yb)
print("Wronskian / rho at 0:", sp.simplify(Wab.coeff(rho, 0)), " and Abel check W = 2K rho^2/A: ", sp.simplify(ser(Wab * rho - 2 * K * rho ** 2 / aA * 1 / rho * rho ** 0, 3).coeff(rho, 0)) if False else "")
invW = ser(1 / Wab, NORD)             # 1/(rho Wab) = (1/rho) invW
def Jentry(i, j):
    """i, j in {'a','b'}: J_ij = +- oint (Y_other(i)/Wr)(Q1 Y_j + P1 Y_j') d rho, Wr = Y_a Y_b' - Y_a' Y_b = rho Wab"""
    ys, ss = {"a": (ya, sa), "b": (yb, sb)}, None
    yj, sj = (ya, sa) if j == "a" else (yb, sb)
    yo, so = (yb, sb) if i == "a" else (ya, sa)
    sign = -1 if i == "a" else +1
    # Y_o (Q1 Y_j + P1 Y_j') / Wr = rho^{so} yo ( Q1 rho^{sj} yj + P1 rho^{sj-1} dY(sj, yj) ) / (rho Wab)
    #   = rho^{so + sj - 1} yo (rho Q1 yj + P1 dY) * (1/(rho Wab)) * ... collect: rho^{so + sj} yo ( Q1 yj + P1 dY/rho ) / (rho Wab)
    inner = sp.expand(yo * (rho * Q1 * yj + P1 * dY(sj, yj)) * invW)        # times rho^{so + sj - 1 - 1}
    expo = so + sj - 2                                                       # integer
    assert expo == int(expo)
    full = sp.expand(inner * rho ** int(expo))
    res = full.coeff(rho, -1)
    return sign * 2 * sp.pi * sp.I * res, sp.simplify(res)
kap = K
kdot = sp.pi / 4 - 2 / sp.pi
for (i, j) in (("a", "a"), ("a", "b"), ("b", "a"), ("b", "b")):
    val, res = Jentry(i, j)
    print("J_%s%s = %s   (residue %s)" % (i, j, sp.simplify(val), res))
print("expected: J_aa = i pi kdot/kappa =", sp.simplify(sp.I * sp.pi * kdot / kap), "= -J_bb;  J_ba = 0;  J_ab = -i pi^2")

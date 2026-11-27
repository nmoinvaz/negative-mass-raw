"""prototype: the Y4-free, L4-free integrand of G6 (E1, E2, E3 at k = 6 and the Y4 step), in generators"""
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i220/notes/wormhole_largeD")
_a, sys.argv = sys.argv, sys.argv[:1]
import order6 as o6  # noqa: E402
sys.argv = _a
import sympy as sp  # noqa: E402

lg, S, u, C, D3, Lc, th, q = sp.symbols("ell S u C D3 Lc2 th q")
w = sp.symbols("w0:6")
R = 1 / (1 - S)
l = -2 * lg
Om = list(w)
Y = [sp.Integer(1), 2 * lg, 4 * w[0] * lg - 6 * lg**2,
     4 * w[1] * lg - 4 * lg**3 + 32 * lg**2 - 16 * w[0] * lg + 32 * u * C - 16 * D3]
L = [sp.Integer(-1), -2 * w[0] + 4 * lg, -2 * w[1] - 4 * w[0] * lg + 16 * lg**2 + 16 * u * C]
h3 = o6.hk(3, Om, l, R, Y, L)
sc = u * (1 - S)
B = -32 * (lg + q) * C + 16 * S * C + 32 * Lc + 16 * sc * lg * (lg + 2 * q) - 4 * w[1] * th - 2 * w[1] * sc
L3 = -2 * h3 + 2 * u * B
L = L + [L3]
cc = lambda m, o=Om: o6.cc(m, o, l, R)  # noqa: E731
o5z = list(Om)
o5z[5] = 0          # Omega5 is h6(1), subtracted: set to 0 in the table, and Omega5 drops from the integrand


def fact(n):
    return sp.factorial(n)


T1 = 8 * lg * sum(Y[j] * cc(5 - j) for j in range(4)) / S
T2 = 2 * sum(L[5 - j] * l**j / fact(j) for j in range(2, 6))
T3 = 2 * sum(Y[j] * cc(6 - j, o5z) for j in range(4)) / S
T4 = -4 * (lg - w[0]) * sum(L[4 - j] * l**j / fact(j) for j in range(1, 5))
T5 = 8 * w[0] * lg * (S * L[3] + sum(Y[j] * cc(4 - j) for j in range(4))) / S
g = 22 * lg**2 - 8 * w[0] * lg - 2 * w[1]
F3 = sum(L[3 - j] * l**j / fact(j) for j in range(4))
T6 = -2 * (g + 16 * u * C) * F3
I6 = T1 + T2 + T3 + T4 + T5 + T6


def red_u(e):
    p = sp.Poly(sp.expand(e), u)
    return sp.expand(sum(cf * (S / (1 - S)) ** (k // 2) * u ** (k % 2) for (k,), cf in p.terms()))


I6 = red_u(I6.subs(w[0], -4 * q))
if __name__ == "__main__":
    P = sp.Poly(I6, C, D3, Lc)
    for mon, cf in P.terms():
        cfs = sp.factor(sp.together(cf))
        print(mon, ":", str(cfs)[:1500])
        print()

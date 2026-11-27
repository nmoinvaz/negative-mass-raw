"""dev_34: the structure of the Y_4-free integrand I_5 (E3) of G_5 at Omega0 = -4 ln 2: sympy, generators ell = ln cos, S = sin^2, u = tan, C = Cl2(pi - 2 th),
D3 = Cl3(pi - 2 th) + 3 zeta(3)/4, Lc2 = int_0^th ln^2 cos, th. u^2 = S/(1 - S)."""
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i208/notes/wormhole_largeD")
_a, sys.argv = sys.argv, sys.argv[:1]
import order5 as o5
sys.argv = _a
import sympy as sp

lg, S, u, C, D3, Lc, th, q = sp.symbols("ell S u C D3 Lc2 th q")
w0, w1, w2, w3, w4 = sp.symbols("w0 w1 w2 w3 w4")
R = 1 / (1 - S)             # R = sec^2
l = -2 * lg
c2 = 1 - S
sc = u * c2
# closed forms at Omega0 = w0 (= -4 q), as in order4.reduced_pieces: L0, L1, L2, Y0 .. Y3
L = [-1, -2 * w0 + 4 * lg, -2 * w1 - 4 * w0 * lg + 16 * lg**2 + 16 * u * C]
Y = [1, 2 * lg, 4 * w0 * lg - 6 * lg**2, 4 * w1 * lg - 4 * lg**3 + 32 * lg**2 - 16 * w0 * lg + 32 * u * C - 16 * D3]
Om = [w0, w1, w2, w3, w4]
h3 = o5.hk(3, Om, l, R, Y + [0], L)
# o5.hk(3, ...) uses Y[3]/2: Y has 4 entries here (Y0 .. Y3)
B = -32 * (lg + q) * C + 16 * S * C + 32 * Lc + 16 * sc * lg * (lg + 2 * q) - 4 * w1 * th - 2 * w1 * sc
L3 = -2 * h3 + 2 * u * B
LL = L + [L3]
h4 = S * LL[3] + sum(Y[j] * o5.cc(4 - j, Om, l, R) for j in range(4))           # Y_4/2 removed
t1 = 8 * lg * h4 / S
t2 = 2 * sum(LL[3 - j] * l ** (j + 1) / sp.factorial(j + 1) for j in range(4))
o = list(Om)
o[4] = 0
t3 = 2 * sum(Y[j] * o5.cc(5 - j, o, l, R) for j in range(4)) / S
F3 = sum(LL[3 - j] * l**j / sp.factorial(j) for j in range(4))
t4 = -4 * (lg - w0) * F3
I5 = sp.expand((t1 + t2 + t3 + t4).subs(w0, -4 * q))
# u^2 -> S/(1-S): reduce powers of u
def red_u(e):
    e = sp.expand(e)
    p = sp.Poly(e, u)
    out = 0
    for (k,), cf in p.terms():
        out += cf * (S / (1 - S)) ** (k // 2) * u ** (k % 2)
    return sp.expand(sp.together(out)) if False else out
I5 = red_u(I5)
print("terms in generators C, D3, Lc2, th, u (powers):")
for gen in (C, D3, Lc, th, u):
    print(gen, sp.Poly(I5, gen).degree())
parts = {}
for f in (C, D3, Lc):
    parts[f] = sp.factor_terms(sp.together(sp.Poly(I5, f).coeff_monomial(f)))
rest = I5.subs({C: 0, D3: 0, Lc: 0})
for f, cf in parts.items():
    print(f"coefficient of {f}:", sp.simplify(cf))
print("rest (no C, D3, Lc2):", sp.simplify(rest))

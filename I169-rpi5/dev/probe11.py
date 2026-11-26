import sys, time
import sympy as sp
sys.argv = [sys.argv[0]]
sys.path.insert(0, "/home/nathan/Source/negative-mass-i169/notes/warp")
from sum_products import *
t0 = time.time()
k1, k2, z1, z2, c1 = sp.symbols("k1 k2 z1 z2 c1")
# step (i): coefficient of z1^6 with X2 = 0 (b's irrelevant)
sub = {A0: z1, A1: k1 * z1, A2: k1**2 * z1, B0: 0, B1: 0, B2: 0}
E1 = sp.expand(E_SYM.subs(sub))
P1 = sp.Poly(E1, z1)
c60 = P1.coeff_monomial(z1**6)
print("c60 factor:", sp.factor(c60))
print("support in z1 (one product):", sorted(m[0] for m in P1.monoms()))
# step (ii): R1 = c1 const
sub2 = {A0: z1, A1: k1 * z1, A2: k1**2 * z1, B0: z2, B1: k2 * z2, B2: k2**2 * z2, a0: c1, a1: 0, a2: 0}
E2 = sp.expand(E_SYM.subs(sub2))
P2 = sp.Poly(E2, z1, z2)
supp = sorted(P2.monoms())
print("support (i,j):", supp)
print("max i, max j, max i+j:", max(m[0] for m in supp), max(m[1] for m in supp), max(sum(m) for m in supp))
print("divisible by z2^2 b1^2:", sp.simplify(sp.cancel(E2 / (z2**2 * b1**2))).is_polynomial(z1, z2, b0, b1, b2))
Epp = sp.expand(sp.cancel(E2 / (z2**2 * b1**2)))
Pp = sp.Poly(Epp, z1, z2)
print("E'' support:", sorted(Pp.monoms()), "terms per coefficient:", [len(sp.Poly(c, b0, b1, b2, c1, k1, k2, v).terms()) for c in Pp.coeffs()])
print("time", time.time() - t0)
# resonant ratios q = k1/k2 from support coincidences
qs = set()
for (i, j) in supp:
    for (i2, j2) in supp:
        if i != i2:
            qs.add(sp.Rational(j2 - j, i - i2))
qs = sorted(q for q in qs if q != 1 and abs(q) >= 1)
print("resonant q (|q| >= 1, != 1):", qs, len(qs))

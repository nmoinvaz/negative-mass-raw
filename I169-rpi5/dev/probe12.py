import sys, time
import sympy as sp
sys.argv = [sys.argv[0]]
sys.path.insert(0, "/home/nathan/Source/negative-mass-i169/notes/warp")
from sum_products import *
k1, k2, z1, z2, c1, t = sp.symbols("k1 k2 z1 z2 c1 t")
sub2 = {A0: z1, A1: k1 * z1, A2: k1**2 * z1, B0: z2, B1: k2 * z2, B2: k2**2 * z2, a0: c1, a1: 0, a2: 0}
E2 = sp.expand(E_SYM.subs(sub2))
Epp = sp.expand(sp.cancel(E2 / (z2**2 * b1**2)))
P = sp.Poly(Epp, z1, z2)
coefs = {m: c for m, c in P.terms()}
case = sys.argv[1] if len(sys.argv) > 1 else "generic"
t0 = time.time()
polys = list(coefs.values())
G = sp.groebner(polys + [t * c1 * k1 * k2 * (k1 - k2) * b1 - 1], t, b0, b1, b2, c1, k1, k2, v, order="grevlex")
print("generic: unit ideal:", G.exprs == [1], len(G.exprs), f"{time.time()-t0:.1f}s", flush=True)
for q in [sp.Integer(-2), sp.Integer(-1), sp.Rational(4, 3), sp.Rational(3, 2), sp.Integer(2), sp.Integer(3), sp.Integer(4)]:
    t0 = time.time()
    classes = {}
    for (i, j), c in coefs.items():
        classes[i * q + j] = classes.get(i * q + j, 0) + c.subs(k1, q * k2)
    ps = [sp.expand(c) for c in classes.values()]
    G = sp.groebner(ps + [t * c1 * k2 * b1 - 1], t, b0, b1, b2, c1, k2, v, order="grevlex")
    print(f"q={q}: classes {len(classes)}, unit ideal: {G.exprs == [1]}, basis {len(G.exprs)}, {time.time()-t0:.1f}s", flush=True)

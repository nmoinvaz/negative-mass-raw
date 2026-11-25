import sys, time, pickle
import sympy as sp
W = sp.symbols("W0:7")
zz = sp.Symbol("zz")
d = pickle.load(open("ricnum_0_1_1.pkl", "rb"))
polys = {k: sp.sympify(v[0]) for k, v in d.items() if sp.sympify(v[0]).free_symbols}
for k, p in polys.items():
    print(k, sp.Poly(p, *W[:5]).degree_list(), "linear in W4:", sp.degree(p, W[4]) , "in W3:", sp.degree(p, W[3]))
print(sp.factor(polys[(2,2)]))
t0 = time.time()
gens = (zz,) + tuple(W[:5])
G = sp.groebner(list(polys.values()) + [zz*W[1] - 1], *gens, order="grevlex")
print("groebner", time.time()-t0, len(G.exprs))
for g in G.exprs[:12]:
    print("  ", sp.factor(g))

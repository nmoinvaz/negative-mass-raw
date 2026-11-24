import sys, time, pickle
import sympy as sp
W = sp.symbols("W0:7")
d = pickle.load(open("ricnum_0_1_1.pkl", "rb"))
N = {k: sp.sympify(v[0]) for k, v in d.items() if sp.sympify(v[0]).free_symbols}
W0, W1, W2, W3, W4 = W[:5]
B = {k: sp.expand(p.subs(W4, 0)) for k, p in N.items()}
A = {k: sp.expand(sp.diff(p, W4)) for k, p in N.items()}
print({k: sp.factor(a) for k, a in A.items()})
E1 = sp.expand(N[(0,0)] + 2*W0*N[(0,2)])
E2 = sp.expand(N[(1,1)] + 2*(W1+W2)*N[(0,2)])
E3 = N[(2,2)]
for nm, E in (("E1", E1), ("E2", E2), ("E3", E3)):
    print(nm, "has W4:", E.has(W4))
    f = sp.factor_list(E)
    print("  ", [(sp.Poly(g, *W[:4]).degree_list(), m) for g, m in f[1]], "const", f[0])
for nm, E in (("E1", E1), ("E2", E2), ("E3", E3)):
    print(nm, sp.factor(E))

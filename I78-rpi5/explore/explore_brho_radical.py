# Why brho_rank1 failed: the ideal of the 2 x 2 minors of R_3 - lam eta_3 for a shift b(rho) is not radical.
import sympy as sp, itertools
lm, hh, QQ, zz = sp.symbols('lm h Q zz', real=True)
Nb = sp.Matrix([[lm - hh, QQ, 0], [QQ, -lm - hh, 0], [0, 0, hh - lm]])
minb = [sp.expand(Nb[i, k]*Nb[j, l] - Nb[i, l]*Nb[j, k]) for (i, j) in itertools.combinations(range(3), 2)
        for (k, l) in itertools.combinations(range(3), 2)]
print("minors:", minb)
G = sp.groebner(minb + [1 - zz*hh], zz, lm, QQ, hh, order="grevlex")
print("basis:", list(G.exprs))
for name, p in [("lam - h", lm - hh), ("Q", QQ), ("(lam - h)^2", (lm - hh)**2), ("Q^2", QQ**2)]:
    print(f"{name} in ideal (h != 0): {G.contains(p)}")
W = sp.groebner([lm - hh, QQ, 1 - zz*hh], zz, lm, QQ, hh, order="grevlex")
print("each minor in <lam - h, Q>:", all(W.contains(m) for m in minb))

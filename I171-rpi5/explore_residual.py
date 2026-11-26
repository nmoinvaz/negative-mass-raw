# Exploration before the README of I171-rpi5 (not of record). Own Einstein tensor; Theorem E metric with undefined H, J.
import time, sympy as sp
t0 = time.time()
p, q, y, z = sp.symbols("p q y z", real=True)
c = sp.Symbol("c", real=True, nonzero=True)
H, J = sp.Function("H")(p), sp.Function("J")(q)
X = (p, q, y, z)
s = H * J
g = sp.zeros(4, 4); g[0, 1] = g[1, 0] = -sp.exp(2 * s); g[2, 2] = g[3, 3] = 1

def einstein(g, X):
    n = len(X); gi = g.inv().applyfunc(sp.simplify)
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[cc]) + sp.diff(g[d, cc], X[b]) - sp.diff(g[b, cc], X[d])) for d in range(n)) / 2)
             for cc in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for cc in range(n):
            Ric[b, cc] = sp.simplify(sum(sp.diff(Gam[a][b][cc], X[a]) - sp.diff(Gam[a][a][b], X[cc]) for a in range(n))
                                     + sum(Gam[a][a][d] * Gam[d][b][cc] - Gam[a][cc][d] * Gam[d][a][b] for a in range(n) for d in range(n)))
    Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    return Ric, Rs, (Ric - Rs * g / 2).applyfunc(sp.simplify), gi

Ric, Rs, G, gi = einstein(g, X)
print("Ricci", Ric.tolist()); print("R", Rs); print("G", G.tolist()); print(f"[{time.time()-t0:.1f} s]")
A1, A2, V = sp.symbols("A1 A2 V")  # alpha1^2, alpha2^2, V value
f1 = (c * H - 4 * J / c); f2 = (c * H + 4 * J / c)
def Tm(f, a2):
    d = sp.Matrix([sp.diff(f, x) for x in X]); k = (d.T * gi * d)[0]
    return a2 * (d * d.T - g * k / 2)
T = Tm(f1, A1) - Tm(f2, A2) - g * V
Res = (G - 8 * sp.pi * T).applyfunc(sp.simplify)
print("Res", Res.tolist()); print(f"[{time.time()-t0:.1f} s]")
eqs = [sp.numer(sp.together(Res[i, j])) for i in range(4) for j in range(i, 4)]
eqs = [e for e in eqs if e != 0]
print("eqs", eqs)
h1, j1, E = sp.symbols("h1 j1 E", positive=True)
sub = {sp.diff(H, p): h1, sp.diff(J, q): j1}
eqs2 = [sp.simplify(e.subs(sub).subs(sp.exp(2 * H * J), E).subs(sp.exp(-2 * H * J), 1 / E)) for e in eqs]
print("eqs2", eqs2)
print(sp.solve(eqs2, [A1, A2, V], dict=True))
print(f"[{time.time()-t0:.1f} s]")
